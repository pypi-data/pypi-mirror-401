"""DMX512 receiver that reuses the reference PARMRK-based design."""

from __future__ import annotations

import threading
import termios
import time
from dataclasses import dataclass
from typing import Generator, Optional

import serial

from .constants import (
    DEFAULT_TIMEOUT,
    DMX_BAUDRATE,
    DMX_FRAME_LENGTH,
    READ_CHUNK_SIZE,
)


BREAK_SEQ = b"\xff\x00\x00"


@dataclass
class DMXFrame:
    start_code: int
    slots: bytes
    locked: bool  # True when a BREAK preceded the frame


@dataclass
class DMXReceiverStats:
    ok_frames: int = 0
    best_effort_frames: int = 0
    breaks_seen: int = 0
    resyncs: int = 0


def _enable_parmrk_break(fd: int):
    """Enable PARMRK/INPCK while keeping BREAKs in-band (reference logic)."""

    attrs = termios.tcgetattr(fd)
    iflag, oflag, cflag, lflag, ispeed, ospeed, cc = attrs

    iflag |= termios.PARMRK | termios.INPCK
    if hasattr(termios, "IGNBRK"):
        iflag &= ~termios.IGNBRK
    if hasattr(termios, "BRKINT"):
        iflag &= ~termios.BRKINT

    termios.tcsetattr(
        fd, termios.TCSANOW, [iflag, oflag, cflag, lflag, ispeed, ospeed, cc]
    )
    return attrs


def _restore_termios(fd: int, attrs) -> None:
    if attrs is not None:
        termios.tcsetattr(fd, termios.TCSANOW, attrs)


def _decode_parmrk_segment(seg: bytes) -> bytearray:
    """Decode a RAW segment where BREAK markers were already split out."""

    out = bytearray()
    i = 0
    n = len(seg)
    while i < n:
        b = seg[i]
        if b != 0xFF:
            out.append(b)
            i += 1
            continue

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
            if i + 2 >= n:
                out.append(0xFF)
                i += 1
                continue
            out.append(seg[i + 2])
            i += 3
            continue

        out.append(0xFF)
        i += 1

    return out


def _extract_trailing_marker(raw: bytes, carry: bytearray) -> bytes:
    if raw.endswith(b"\xff\x00"):
        carry.extend(b"\xff\x00")
        return raw[:-2]
    if raw.endswith(b"\xff"):
        carry.extend(b"\xff")
        return raw[:-1]
    return raw


class DMXReceiver:
    """Produces DMX frames using the proven reference implementation."""

    def __init__(
        self,
        port: str,
        *,
        timeout: float = DEFAULT_TIMEOUT,
        chunk_size: int = READ_CHUNK_SIZE,
    ) -> None:
        self._port = port
        self._timeout = timeout
        self._chunk_size = chunk_size
        self._serial: Optional[serial.Serial] = None
        self._termios_attrs = None
        self._stats = DMXReceiverStats()

    def __enter__(self) -> "DMXReceiver":
        self.open()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def open(self) -> None:
        if self._serial and self._serial.is_open:
            return

        self._serial = serial.Serial(
            self._port,
            baudrate=DMX_BAUDRATE,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_TWO,
            timeout=self._timeout,
            xonxoff=False,
            rtscts=False,
            dsrdtr=False,
            exclusive=True,
        )
        self._termios_attrs = _enable_parmrk_break(self._serial.fileno())

    def close(self) -> None:
        if not self._serial:
            return

        try:
            if self._termios_attrs is not None:
                _restore_termios(self._serial.fileno(), self._termios_attrs)
        finally:
            self._termios_attrs = None
            self._serial.close()
            self._serial = None

    @property
    def stats(self) -> DMXReceiverStats:
        return self._stats

    def frames(
        self,
        *,
        stop_event: Optional[threading.Event] = None,
        deadline: Optional[float] = None,
    ) -> Generator[DMXFrame, None, None]:
        if not self._serial:
            self.open()
        assert self._serial is not None

        frame_buf = bytearray()
        carry = bytearray()
        frame_locked = False

        while True:
            if stop_event and stop_event.is_set():
                raise KeyboardInterrupt
            if deadline is not None and time.monotonic() >= deadline:
                raise TimeoutError("Receiver deadline exceeded")

            try:
                chunk = self._serial.read(self._chunk_size)
            except serial.SerialException as exc:
                if "returned no data" in str(exc).lower():
                    self._recover_from_empty_read()
                    frame_buf.clear()
                    carry.clear()
                    frame_locked = False
                    continue
                raise RuntimeError(
                    f"Serial read failed on {self._port}: {exc}"
                ) from exc

            if not chunk:
                continue

            raw = bytes(carry) + chunk
            carry.clear()
            raw = _extract_trailing_marker(raw, carry)

            parts = raw.split(BREAK_SEQ)

            if parts:
                pre = parts[0]
                if pre:
                    decoded = _decode_parmrk_segment(pre)
                    if decoded:
                        frame_buf.extend(decoded)
                        frames_out = self._collect_frames(
                            frame_buf, frame_locked, drop_remainder=False
                        )
                        if frames_out:
                            frame_locked = False
                            for frame in frames_out:
                                yield frame

                for seg in parts[1:]:
                    self._stats.breaks_seen += 1
                    if 0 < len(frame_buf) < DMX_FRAME_LENGTH:
                        self._stats.resyncs += 1
                    frame_buf.clear()
                    frame_locked = True

                    if seg:
                        decoded_break_seg = _decode_parmrk_segment(seg)
                        if decoded_break_seg:
                            frame_buf.extend(decoded_break_seg)

                    if len(frame_buf) >= DMX_FRAME_LENGTH:
                        frames_out = self._collect_frames(
                            frame_buf, frame_locked, drop_remainder=True
                        )
                        if frames_out:
                            frame_locked = False
                            for frame in frames_out:
                                yield frame

            if len(frame_buf) > DMX_FRAME_LENGTH * 4:
                frame_buf.clear()
                frame_locked = False

    def _collect_frames(
        self,
        buffer: bytearray,
        locked: bool,
        *,
        drop_remainder: bool,
    ) -> list[DMXFrame]:
        frames: list[DMXFrame] = []
        while len(buffer) >= DMX_FRAME_LENGTH:
            payload = bytes(buffer[:DMX_FRAME_LENGTH])
            if drop_remainder:
                buffer.clear()
            else:
                del buffer[:DMX_FRAME_LENGTH]

            frame = DMXFrame(start_code=payload[0], slots=payload[1:], locked=locked)
            if frame.locked:
                self._stats.ok_frames += 1
            else:
                self._stats.best_effort_frames += 1

            frames.append(frame)

            locked = False
            if drop_remainder:
                break

        return frames

    def _recover_from_empty_read(self) -> None:
        pause = self._timeout if self._timeout > 0 else 0.05
        self.close()
        time.sleep(min(pause, 0.5))
        self.open()
