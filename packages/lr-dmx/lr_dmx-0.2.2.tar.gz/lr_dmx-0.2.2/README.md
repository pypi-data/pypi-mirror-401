# lr-dmx

Lightweight DMX512 helper tailored for FTDI-based hardware-in-the-loop setups with explicit BREAK / Mark-After-Break control. The package provides both a CLI (`lr-dmx`) and Python APIs for streaming frames or inspecting a live universe.

## Features
- Deterministic transmitter with configurable BREAK/MAB timings and FPS throttling
- Receiver that aligns to PARMRK BREAK markers for robust resynchronisation
- Pure-Python helpers that can be embedded into bespoke hardware-in-the-loop test harnesses
- CLI wrappers utilities for quick experiments, scripting, and test automation

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
Released under the MIT License. Copyright (c) 2026 LumenRadio AB.

```
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
