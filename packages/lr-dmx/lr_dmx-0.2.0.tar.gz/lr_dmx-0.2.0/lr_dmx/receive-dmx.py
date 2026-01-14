#!/usr/bin/env python3
"""
DMX512 receiver (Ubuntu 24.04) using termios PARMRK to detect DMX BREAK.

- Port: 250000 baud, 8N2
- Enable PARMRK so BREAK is encoded as: FF 00 00 in the input stream
- A literal data byte 0xFF is encoded as: FF FF
- Frame boundary: BREAK (FF 00 00)
- After each BREAK, collect:
    start code (1 byte) + up to 512 slot bytes
  and print once we have 513 bytes.

Self-healing:
- BREAK before 513 bytes -> drop partial, restart at this BREAK
- Extra bytes between BREAKs (unexpected) -> keep first 513, drop remainder until next BREAK

Important correctness:
- We clear BRKINT (do NOT set it), otherwise BREAK may be handled by the line discipline.
- We restore original termios settings on exit and on reopen.

Requires: pip install pyserial
"""

import argparse
import sys
import time
import serial
import termios
from contextlib import contextmanager
from serial.serialutil import SerialException

FRAME_LEN = 513
BREAK_SEQ = b"\xff\x00\x00"


def set_parmrk_break_mode(fd: int):
    """
    Configure input so BREAK is delivered as PARMRK sequence FF 00 00.

    Returns the old termios attrs so caller can restore them.
    """
    old = termios.tcgetattr(fd)
    iflag, oflag, cflag, lflag, ispeed, ospeed, cc = old

    iflag |= termios.PARMRK | termios.INPCK

    if hasattr(termios, "IGNBRK"):
        iflag &= ~termios.IGNBRK
    if hasattr(termios, "BRKINT"):
        iflag &= ~termios.BRKINT  # critical: do NOT let BREAK become "interrupty"

    termios.tcsetattr(
        fd, termios.TCSANOW, [iflag, oflag, cflag, lflag, ispeed, ospeed, cc]
    )
    return old


def restore_termios(fd: int, old_attrs) -> None:
    termios.tcsetattr(fd, termios.TCSANOW, old_attrs)


@contextmanager
def open_dmx_serial(path: str, timeout: float = 0.2):
    """
    Context-managed serial port open with safe termios configure/restore.
    Ensures:
      - termios is restored before closing the FD
      - serial port is closed even on exceptions
    """
    with serial.Serial(
        path,
        baudrate=250000,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_TWO,
        timeout=timeout,
        xonxoff=False,
        rtscts=False,
        dsrdtr=False,
        exclusive=True,
    ) as ser:
        old_attrs = None
        try:
            old_attrs = set_parmrk_break_mode(ser.fileno())
            yield ser
        finally:
            # Restore termios BEFORE the fd is closed by Serial.__exit__()
            if old_attrs is not None:
                try:
                    restore_termios(ser.fileno(), old_attrs)
                except Exception:
                    # Best-effort restore; don't mask the original exception
                    pass


def decode_parmrk_segment(seg: bytes) -> bytearray:
    """
    Decode a byte string that has PARMRK enabled, *with no BREAK sequences inside*.
    Handles:
      - FF FF -> literal FF
      - FF 00 x (x != 00) -> parity/framing marked byte 'x' (we keep x)
    """
    out = bytearray()
    i = 0
    n = len(seg)
    while i < n:
        b = seg[i]
        if b != 0xFF:
            out.append(b)
            i += 1
            continue

        # b == 0xFF: need at least one more byte
        if i + 1 >= n:
            out.append(0xFF)
            i += 1
            continue

        b1 = seg[i + 1]
        if b1 == 0xFF:
            out.append(0xFF)
            i += 2
            continue

        if b1 == 0x00:
            # parity/framing mark: FF 00 x  (BREAKs are split out before calling)
            if i + 2 >= n:
                out.append(0xFF)
                i += 1
                continue
            out.append(seg[i + 2])
            i += 3
            continue

        # unexpected; treat first FF as data
        out.append(0xFF)
        i += 1

    return out


def run_receiver(ser: serial.Serial, args) -> None:
    carry = bytearray()  # holds possible split marker tail (FF or FF 00)
    frame = bytearray()
    in_frame = False

    breaks = 0
    frames = 0
    partial_drops = 0
    bytes_in_frames_sum = 0
    last_stats_t = time.monotonic()

    while True:
        chunk = ser.read(4096)
        if not chunk:
            continue

        raw = bytes(carry) + chunk
        carry.clear()

        # Keep potential split markers so we don't mis-parse them
        if raw.endswith(b"\xff\x00"):
            carry.extend(b"\xff\x00")
            raw = raw[:-2]
        elif raw.endswith(b"\xff"):
            carry.extend(b"\xff")
            raw = raw[:-1]

        # Split on BREAK markers in the raw stream
        parts = raw.split(BREAK_SEQ)

        # Process the first part (no preceding BREAK in this chunk)
        if parts and parts[0] and in_frame:
            frame.extend(decode_parmrk_segment(parts[0]))

        # Each subsequent part starts after a BREAK
        for seg in parts[1:]:
            breaks += 1

            # BREAK is authoritative: start a new frame
            if in_frame and 0 < len(frame) < FRAME_LEN:
                partial_drops += 1
            frame.clear()
            in_frame = True

            if seg:
                frame.extend(decode_parmrk_segment(seg))

            # Emit exactly one frame if we have enough
            if len(frame) >= FRAME_LEN:
                out = bytes(frame[:FRAME_LEN])
                frame.clear()
                in_frame = False

                frames += 1
                bytes_in_frames_sum += FRAME_LEN

                if args.raw:
                    print(out.hex(), flush=True)
                else:
                    start_code = out[0]
                    slots = out[1:]
                    shown = list(slots[: max(0, min(args.show, 512))])
                    if args.show != 0:
                        print(f"start=0x{start_code:02X} ch1..={shown}", flush=True)

        # Stats
        if args.stats:
            now = time.monotonic()
            if now - last_stats_t >= args.stats_interval:
                dt = now - last_stats_t
                brk_rate = breaks / dt if dt > 0 else 0.0
                frm_rate = frames / dt if dt > 0 else 0.0
                avg_len = (bytes_in_frames_sum / frames) if frames else 0.0
                print(
                    f"[stats] breaks={breaks} ({brk_rate:.1f}/s) frames={frames} ({frm_rate:.1f}/s) "
                    f"partial_drops={partial_drops} avg_frame_len={avg_len:.1f}",
                    file=sys.stderr,
                    flush=True,
                )
                breaks = frames = partial_drops = bytes_in_frames_sum = 0
                last_stats_t = now


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Receive DMX512 using BREAK markers (PARMRK)."
    )
    ap.add_argument("port")
    ap.add_argument(
        "--show", type=int, default=16, help="How many channels to print (default: 16)"
    )
    ap.add_argument(
        "--raw", action="store_true", help="Print raw 513-byte frames as hex"
    )
    ap.add_argument(
        "--stats", action="store_true", help="Print periodic stats to stderr"
    )
    ap.add_argument("--stats-interval", type=float, default=2.0)
    ap.add_argument(
        "--reopen-delay",
        type=float,
        default=1.0,
        help="Seconds before retrying open (default: 1.0)",
    )
    ap.add_argument(
        "--timeout",
        type=float,
        default=0.2,
        help="Serial read timeout seconds (default: 0.2)",
    )
    args = ap.parse_args()

    print(f"Opening {args.port} @ 250000 8N2. Syncing on BREAK (FF 00 00).", flush=True)

    while True:
        try:
            with open_dmx_serial(args.port, timeout=args.timeout) as ser:
                run_receiver(ser, args)
        except KeyboardInterrupt:
            return 0
        except SerialException as e:
            print(f"[serial] {e}", file=sys.stderr, flush=True)
            time.sleep(args.reopen_delay)
        except OSError as e:
            # Covers unplug/replug and some tty layer errors
            print(f"[os] {e}", file=sys.stderr, flush=True)
            time.sleep(args.reopen_delay)


if __name__ == "__main__":
    raise SystemExit(main())
