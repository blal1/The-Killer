# bgt_runtime (high-fidelity partial)

This package maps a subset of BGT Foundation Layer APIs to realistic Python equivalents,
with graceful fallbacks when libraries are not installed. You can install these optional dependencies:

- Audio: `pydub`, `sounddevice` (and `ffmpeg` available in PATH for pydub)
- Network: `requests` (fallbacks to urllib)

## Modules
- `audio`: playback and sound settings (open device, master volume, list devices, play_sound)
- `fs`: files and directories helpers (find_files, copy/move/delete, file_exists)
- `net`: `url_get`, `url_post`, `download_file`, and a simple `TCPClient`
- `mathutils`: math functions and RNG state helpers
- `debug`: assertions, call stack, and profiling
- `system`: sleep, ticks, alert, input_box
- `strings`: extra string helpers

## Coverage
See the generated coverage files:
- JSON: /mnt/data/bgt_runtime/bgt_api_coverage.json
- CSV : /mnt/data/bgt_runtime/bgt_api_coverage.csv

## Converter
A lightweight converter that injects `from bgt_runtime import *` is provided:
- /mnt/data/bgt_runtime/bgt2py_runtime_injector.py

For the most advanced converter you drafted earlier, just import from this runtime (`bgt_runtime`)
instead of the minimal shim.

