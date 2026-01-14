# lr-dmx

DMX512 helpers that reuse the same FT231XS-based hardware but operate the port at 250000-8N2 with explicit BREAK / Mark-After-Break control. The package provides both a CLI (`lr-dmx`) and Python APIs for streaming frames or inspecting a live universe.

## Features
- Deterministic transmitter with configurable BREAK/MAB timings and FPS throttling
- Receiver that aligns to PARMRK BREAK markers for robust resynchronisation
- CLI-compatible wrappers for the legacy `tests/send-dmx.py` and `tests/receive-dmx.py` utilities
- Pure-Python helpers that can be embedded into bespoke hardware-in-the-loop harnesses

## Installation
```bash
python -m pip install lr-dmx
```

For development work inside this repository, install in editable mode together with the extra tooling:
```bash
python -m pip install -e python/lr_dmx[dev]
```

## CLI usage
### Send constant or patched scenes
```bash
lr-dmx send --port /dev/ttyUSB1 --fps 41 --value 64 --set 0=255 --set 5=0
```

Flags such as `--frames`, `--duration`, `--break-us`, and `--mab-us` allow you to bound a test run or fine-tune the waveform. Use the `LR_DMX_PORT` environment variable to set a default adapter path.

### Receive with BREAK lock
```bash
lr-dmx receive --port /dev/ttyUSB0 --show 32 --stats --stats-interval 10
```

Each frame is tagged as `OK` (BREAK-synchronised) or `BEST` (length-only) so you can judge whether the receiver is coasting between marker hiccups.

## Python API
```python
from lr_dmx import DMXTransmitter, DMXReceiver, build_constant_frame

frame = build_constant_frame(0x80)
with DMXTransmitter("/dev/ttyUSB1") as tx:
    tx.stream(frame, fps=30.0, frame_count=300)

with DMXReceiver("/dev/ttyUSB0") as rx:
    for idx, frame in enumerate(rx.frames()):
        print(idx, frame.start_code, list(frame.slots[:8]))
        if idx >= 10:
            break
```

## License
These modules follow the same license as the parent repository. See the root `LICENSE` file for details.
