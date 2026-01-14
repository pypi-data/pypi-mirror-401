"""Command line interface for lr-dmx send/receive helpers."""

from __future__ import annotations

import argparse
import os
import sys
import time
from typing import Callable, Dict, List

from .constants import (
    DEFAULT_BREAK_US,
    DEFAULT_FPS,
    DEFAULT_MAB_US,
    DEFAULT_START_CODE,
    DMX_SLOT_COUNT,
)
from .receiver import DMXReceiver
from .transmitter import DMXTransmitter, FrameTiming, build_frame


def _env_default(name: str, fallback: str) -> str:
    return os.environ.get(name, fallback)


def _parse_overrides(pairs: List[str]) -> Dict[int, int]:
    overrides: Dict[int, int] = {}
    for raw in pairs:
        if "=" not in raw:
            raise ValueError(f"Invalid override '{raw}', expected CH=VALUE")
        lhs, rhs = raw.split("=", 1)
        channel = int(lhs, 0)
        value = int(rhs, 0)
        if not 0 <= channel < DMX_SLOT_COUNT:
            raise ValueError("Channel must be between 0 and 511")
        if not 0 <= value <= 0xFF:
            raise ValueError("Channel value must be between 0 and 255")
        overrides[channel] = value
    return overrides


def _apply_overrides(default: int, overrides: Dict[int, int]) -> List[int]:
    slots = [default] * DMX_SLOT_COUNT
    for channel, value in overrides.items():
        slots[channel] = value
    return slots


def _build_frame_source(args: argparse.Namespace) -> Callable[[], bytes]:
    if args.mode == "solid":
        overrides = _parse_overrides(args.set or [])
        slots = _apply_overrides(args.value, overrides)
        frame = build_frame(start_code=args.start_code, slots=slots)

        def _solid() -> bytes:
            return frame

        return _solid

    if args.mode == "ramp":
        slots = bytearray(DMX_SLOT_COUNT)
        ramp_val = args.value & 0xFF

        def _ramp() -> bytes:
            nonlocal ramp_val
            slots[:] = bytes([ramp_val]) * DMX_SLOT_COUNT
            ramp_val = (ramp_val + 1) & 0xFF
            return build_frame(start_code=args.start_code, slots=slots)

        return _ramp

    if args.mode == "chase":
        slots = bytearray(DMX_SLOT_COUNT)
        chase_pos = args.channel - 1
        chase_dir = 1

        def _chase() -> bytes:
            nonlocal chase_pos, chase_dir
            slots[:] = b"\x00" * DMX_SLOT_COUNT
            slots[chase_pos] = 0xFF
            chase_pos += chase_dir
            if chase_pos >= DMX_SLOT_COUNT:
                chase_pos = DMX_SLOT_COUNT - 2
                chase_dir = -1
            elif chase_pos < 0:
                chase_pos = 1
                chase_dir = 1
            return build_frame(start_code=args.start_code, slots=slots)

        return _chase

    raise ValueError(f"Unsupported mode: {args.mode}")


def _cmd_send(args: argparse.Namespace) -> int:
    if not 0 <= args.value <= 0xFF:
        print("ERROR: --value must be between 0 and 255", file=sys.stderr)
        return 2
    if args.mode != "solid" and args.set:
        print(
            "ERROR: --set overrides are only supported in solid mode", file=sys.stderr
        )
        return 2
    if args.mode == "chase" and not (1 <= args.channel <= DMX_SLOT_COUNT):
        print("ERROR: --channel must be between 1 and 512", file=sys.stderr)
        return 2

    try:
        frame_source = _build_frame_source(args)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    timing = FrameTiming(break_us=args.break_us, mab_us=args.mab_us)
    try:
        with DMXTransmitter(args.port, timing=timing) as tx:
            tx.stream(
                frame_source=frame_source,
                fps=args.fps,
                frame_count=args.frames,
                duration=args.duration,
            )
    except KeyboardInterrupt:
        return 130
    return 0


def _format_slots(slots: bytes, show: int) -> str:
    preview = list(slots[: max(0, min(show, len(slots)))])
    return ", ".join(str(v) for v in preview)


def _cmd_receive(args: argparse.Namespace) -> int:
    try:
        with DMXReceiver(args.port, timeout=args.timeout) as rx:
            seen = 0
            last_stats = time.monotonic()
            for frame in rx.frames():
                seen += 1
                tag = "OK" if frame.locked else "BEST"
                if args.raw:
                    raw = frame.start_code.to_bytes(1, "big") + frame.slots
                    print(raw.hex())
                else:
                    shown = _format_slots(frame.slots, args.show)
                    print(f"[{tag}] start=0x{frame.start_code:02X} ch0..={shown}")
                if args.limit and seen >= args.limit:
                    break
                if (
                    args.stats
                    and args.stats_interval
                    and (time.monotonic() - last_stats) >= args.stats_interval
                ):
                    stats = rx.stats
                    print(
                        f"[stats] ok={stats.ok_frames} best={stats.best_effort_frames}"
                        f" breaks={stats.breaks_seen} resyncs={stats.resyncs}"
                    )
                    last_stats = time.monotonic()
    except KeyboardInterrupt:
        return 130
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lr-dmx",
        description="DMX512 helper CLI for the UART↔RS-485 dev board",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    send = sub.add_parser("send", help="Stream DMX frames at a fixed FPS")
    send.add_argument(
        "--port",
        default=_env_default("LR_DMX_PORT", "/dev/ttyUSB0"),
        help="Serial port to transmit on",
    )
    send.add_argument(
        "--fps", type=float, default=DEFAULT_FPS, help="Frames per second"
    )
    send.add_argument(
        "--value",
        type=int,
        default=0,
        help="Default slot value (0-255). Also used as the starting value for ramp mode",
    )
    send.add_argument(
        "--mode",
        choices=["solid", "ramp", "chase"],
        default="solid",
        help="Payload pattern (matches reference send-dmx.py)",
    )
    send.add_argument(
        "--set",
        action="append",
        metavar="CH=VALUE",
        help="Override specific slots using CH=VALUE syntax",
    )
    send.add_argument(
        "--channel",
        type=int,
        default=1,
        help="Chase mode: 1-512 channel that starts at full",
    )
    send.add_argument(
        "--start-code",
        type=int,
        default=DEFAULT_START_CODE,
        help="DMX start code byte",
    )
    send.add_argument(
        "--frames",
        type=int,
        help="Stop after streaming this many frames (default: run forever)",
    )
    send.add_argument(
        "--duration",
        type=float,
        help="Stop after this many seconds (default: run forever)",
    )
    send.add_argument(
        "--break-us",
        type=int,
        default=DEFAULT_BREAK_US,
        help="Length of BREAK in microseconds",
    )
    send.add_argument(
        "--mab-us",
        type=int,
        default=DEFAULT_MAB_US,
        help="Length of Mark After Break in microseconds",
    )

    recv = sub.add_parser("receive", help="Listen for DMX frames with BREAK lock")
    recv.add_argument(
        "--port",
        default=_env_default("LR_DMX_PORT", "/dev/ttyUSB0"),
        help="Serial port to listen on",
    )
    recv.add_argument(
        "--show",
        type=int,
        default=16,
        help="How many slots to print from each frame",
    )
    recv.add_argument(
        "--raw",
        action="store_true",
        help="Dump raw frames as bytes",
    )
    recv.add_argument(
        "--stats",
        action="store_true",
        help="Print periodic receiver statistics",
    )
    recv.add_argument(
        "--stats-interval",
        type=float,
        default=5.0,
        help="Seconds between stats prints (0 disables)",
    )
    recv.add_argument(
        "--limit",
        type=int,
        help="Stop after this many frames (default: run until Ctrl-C)",
    )
    recv.add_argument(
        "--timeout",
        type=float,
        default=0.2,
        help="Serial read timeout in seconds",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "send":
        return _cmd_send(args)
    if args.command == "receive":
        if args.stats_interval <= 0:
            args.stats_interval = None
        return _cmd_receive(args)

    parser.error("Unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
