#!/usr/bin/env python3
"""
Send full-frame DMX512 (512 slots) over a serial port.

Requires:
  pip install pyserial
"""

import argparse
import fcntl
import os
import sys
import time

import serial


# Linux ioctl constants (from asm-generic/ioctls.h / termios)
TIOCSBRK = 0x5427  # set break (TX low)
TIOCCBRK = 0x5428  # clear break


def busy_sleep_us(us: int) -> None:
    """Busy-wait sleep with microsecond-ish precision."""
    target = time.perf_counter_ns() + us * 1000
    while time.perf_counter_ns() < target:
        pass


def send_break_and_mab(fd: int, break_us: int, mab_us: int) -> None:
    """Assert BREAK then MAB with approximate microsecond timing."""
    fcntl.ioctl(fd, TIOCSBRK)
    busy_sleep_us(break_us)
    fcntl.ioctl(fd, TIOCCBRK)
    busy_sleep_us(mab_us)


def build_frame(start_code: int, slots: bytes) -> bytes:
    if not (0 <= start_code <= 255):
        raise ValueError("start_code must be 0..255")
    if len(slots) != 512:
        raise ValueError("slots must be exactly 512 bytes")
    return bytes([start_code]) + slots


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Generate and send full-frame DMX512 data."
    )
    ap.add_argument("port", help="Serial port, e.g. /dev/ttyUSB0")
    ap.add_argument(
        "--fps", type=float, default=44.0, help="Frames per second (default: 44.0)"
    )
    ap.add_argument(
        "--break-us", type=int, default=120, help="BREAK duration in us (default: 120)"
    )
    ap.add_argument(
        "--mab-us", type=int, default=12, help="MAB duration in us (default: 12)"
    )
    ap.add_argument(
        "--start-code",
        type=lambda x: int(x, 0),
        default=0x00,
        help="DMX start code (default: 0x00)",
    )
    ap.add_argument(
        "--mode",
        choices=["solid", "ramp", "chase"],
        default="solid",
        help="Payload pattern (default: solid)",
    )
    ap.add_argument(
        "--value", type=int, default=0, help="For solid: 0..255 (default: 0)"
    )
    ap.add_argument(
        "--channel",
        type=int,
        default=1,
        help="For chase: 1..512 channel to move (default: 1)",
    )
    args = ap.parse_args()

    if args.fps <= 0:
        print("fps must be > 0", file=sys.stderr)
        return 2

    if not (0 <= args.value <= 255):
        print("value must be 0..255", file=sys.stderr)
        return 2

    if not (1 <= args.channel <= 512):
        print("channel must be 1..512", file=sys.stderr)
        return 2

    period_s = 1.0 / args.fps

    try:
        ser = serial.Serial(
            port=args.port,
            baudrate=250000,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_TWO,
            timeout=0,
            xonxoff=False,
            rtscts=False,
            dsrdtr=False,
            write_timeout=1,
        )
    except Exception as e:
        print(f"Failed to open {args.port}: {e}", file=sys.stderr)
        return 2

    fd = ser.fileno()

    # Pre-allocate slots buffer
    slots = bytearray(512)

    print(
        f"Sending DMX on {args.port} @ 250000 8N2, {args.fps:.3f} fps. Ctrl-C to stop."
    )

    frame_count = 0
    ramp_val = 0
    chase_pos = args.channel - 1  # 0-based
    chase_dir = 1

    try:
        next_t = time.perf_counter()
        while True:
            # Build payload
            if args.mode == "solid":
                slots[:] = bytes([args.value]) * 512

            elif args.mode == "ramp":
                # Same value on all channels, ramping 0..255
                slots[:] = bytes([ramp_val]) * 512
                ramp_val = (ramp_val + 1) & 0xFF

            elif args.mode == "chase":
                # One channel at 255, others 0, bouncing across the universe
                slots[:] = b"\x00" * 512
                slots[chase_pos] = 255
                chase_pos += chase_dir
                if chase_pos >= 512:
                    chase_pos = 510
                    chase_dir = -1
                elif chase_pos < 0:
                    chase_pos = 1
                    chase_dir = 1

            frame = build_frame(args.start_code, slots)

            # DMX framing: BREAK + MAB + frame bytes
            send_break_and_mab(fd, args.break_us, args.mab_us)
            ser.write(frame)
            ser.flush()  # ensure bytes are pushed out before timing next frame

            frame_count += 1

            # Rate control
            next_t += period_s
            now = time.perf_counter()
            sleep_s = next_t - now
            if sleep_s > 0:
                # normal sleep is fine at ~22ms periods
                time.sleep(sleep_s)
            else:
                # we're running late; skip sleeping and rebase occasionally
                if -sleep_s > 0.5:
                    next_t = now

    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        ser.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
