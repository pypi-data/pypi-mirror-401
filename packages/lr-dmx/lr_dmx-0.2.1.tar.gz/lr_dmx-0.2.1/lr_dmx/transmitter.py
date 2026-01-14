"""DMX512 frame builders and transmitter logic aligned with the reference design."""

from __future__ import annotations

import fcntl
import termios
import time
from dataclasses import dataclass
from typing import Callable, Optional, Sequence

import serial

from .constants import (
    DEFAULT_BREAK_US,
    DEFAULT_FPS,
    DEFAULT_MAB_US,
    DEFAULT_START_CODE,
    DMX_BAUDRATE,
    DMX_FRAME_LENGTH,
    DMX_SLOT_COUNT,
)

TIOCSBRK = getattr(termios, "TIOCSBRK", 0x5427)
TIOCCBRK = getattr(termios, "TIOCCBRK", 0x5428)


@dataclass(frozen=True)
class FrameTiming:
    """User-configurable DMX timings for BREAK and Mark-After-Break."""

    break_us: int = DEFAULT_BREAK_US
    mab_us: int = DEFAULT_MAB_US

    def __post_init__(self) -> None:
        if self.break_us < 0 or self.mab_us < 0:
            raise ValueError("BREAK/MAB timings must be non-negative")


def build_frame(
    *,
    start_code: int = DEFAULT_START_CODE,
    slots: Optional[Sequence[int]] = None,
    fill_value: int = 0,
) -> bytes:
    """Construct a DMX frame payload (start code + 512 slots).

    Slots shorter than 512 bytes are padded with ``fill_value``. Values outside 0-255
    raise ``ValueError``.
    """

    if not 0 <= start_code <= 0xFF:
        raise ValueError("Start code must fit in one byte")

    if slots is None:
        slot_values = [fill_value] * DMX_SLOT_COUNT
    else:
        slot_values = list(slots)
        if len(slot_values) > DMX_SLOT_COUNT:
            raise ValueError("DMX payload exceeds 512 slots")
        if len(slot_values) < DMX_SLOT_COUNT:
            slot_values.extend([fill_value] * (DMX_SLOT_COUNT - len(slot_values)))

    for idx, value in enumerate(slot_values):
        if not 0 <= int(value) <= 0xFF:
            raise ValueError(f"Slot {idx} has invalid value {value}")
        slot_values[idx] = int(value)

    return bytes([start_code] + slot_values)


def build_constant_frame(value: int, *, start_code: int = DEFAULT_START_CODE) -> bytes:
    """Helper that fills the entire universe with the same value."""

    return build_frame(start_code=start_code, slots=None, fill_value=value)


def busy_sleep_us(us: int) -> None:
    """Busy-wait for sub-millisecond accuracy."""
    if us <= 0:
        return
    target = time.perf_counter_ns() + us * 1000
    while time.perf_counter_ns() < target:
        pass


def send_break_and_mab(fd: int, break_us: int, mab_us: int) -> None:
    """Assert BREAK then MAB with approximate microsecond timing."""
    fcntl.ioctl(fd, TIOCSBRK)
    busy_sleep_us(break_us)
    fcntl.ioctl(fd, TIOCCBRK)
    busy_sleep_us(mab_us)


class DMXTransmitter:
    """Streams DMX frames over a USB↔RS-485 adapter."""

    def __init__(
        self,
        port: str,
        *,
        timing: FrameTiming | None = None,
    ) -> None:
        self._port = port
        self._timing = timing or FrameTiming()
        self._serial: Optional[serial.Serial] = None

    def __enter__(self) -> "DMXTransmitter":
        self.open()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def open(self) -> None:
        if self._serial and self._serial.is_open:
            return
        self._serial = serial.Serial(
            port=self._port,
            baudrate=DMX_BAUDRATE,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_TWO,
            timeout=0,
            xonxoff=False,
            rtscts=False,
            dsrdtr=False,
            write_timeout=1,
        )
        # Drain any stale input to avoid echoing old data as the receiver starts.
        self._serial.reset_input_buffer()

    def close(self) -> None:
        if self._serial:
            self._serial.close()
            self._serial = None

    def send_frame(self, frame: bytes) -> None:
        if len(frame) == 0 or len(frame) > DMX_FRAME_LENGTH:
            raise ValueError("DMX frame must be between 1 and 513 bytes")
        if not self._serial:
            raise RuntimeError("Serial port is not open")
        fd = self._serial.fileno()
        send_break_and_mab(fd, self._timing.break_us, self._timing.mab_us)
        self._serial.write(frame)
        self._serial.flush()

    def stream(
        self,
        frame: Optional[bytes] = None,
        *,
        frame_source: Optional[Callable[[], bytes]] = None,
        fps: Optional[float] = DEFAULT_FPS,
        frame_count: Optional[int] = None,
        duration: Optional[float] = None,
        should_stop: Optional[Callable[[], bool]] = None,
    ) -> int:
        """Stream frames at a fixed cadence.

        Provide either a constant ``frame`` or a ``frame_source`` callback that builds a
        fresh payload each iteration (used for ramp/chase patterns)."""

        if frame_source is None and frame is None:
            raise ValueError("Either frame or frame_source must be provided")
        if frame_source is not None and frame is not None:
            raise ValueError("Provide only frame or frame_source, not both")

        def _next_frame() -> bytes:
            return frame if frame is not None else frame_source()  # type: ignore[arg-type]

        self.open()
        sent = 0
        start = time.perf_counter()
        next_tick = start
        period = 0.0
        if fps is not None and fps > 0:
            period = 1.0 / fps
        while True:
            if should_stop and should_stop():
                break
            payload = _next_frame()
            self.send_frame(payload)
            sent += 1
            if frame_count is not None and sent >= frame_count:
                break
            if duration is not None and (time.perf_counter() - start) >= duration:
                break
            if period > 0:
                next_tick += period
                sleep_for = next_tick - time.perf_counter()
                if sleep_for > 0:
                    time.sleep(sleep_for)
        return sent

    @property
    def port(self) -> str:
        return self._port

    @property
    def timing(self) -> FrameTiming:
        return self._timing
