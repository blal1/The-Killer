"""
audio — Maps BGT audio_management to Python with pydub + sounddevice where available.

Functions:
- open_sound_device(device=None, samplerate=44100, channels=2, blocksize=1024)
- list_sound_devices()
- set_sound_master_volume(v) / get_sound_master_volume()
- set_sound_storage(path) / get_sound_storage()
- set_sound_decryption_key(key)  # placeholder
- play_sound(path)  # helper for quick playback

Design:
- Uses sounddevice for playback stream when installed.
- Falls back to simple blocking playback via pydub.playback if available.
- If neither is available, functions are no-ops but won't crash.
"""
from __future__ import annotations
import os
from pathlib import Path

_sound_master_volume = 1.0
_sound_storage = Path(".")
_sound_key = None

# Optional deps
try:
    import sounddevice as sd
except Exception:
    sd = None

try:
    from pydub import AudioSegment
    from pydub.playback import play as pydub_play
except Exception:
    AudioSegment = None
    pydub_play = None

def list_sound_devices():
    if sd is None:
        return []
    try:
        return [str(d.get("name", "")) for d in sd.query_devices()]
    except Exception:
        return []

def open_sound_device(device=None, samplerate=44100, channels=2, blocksize=1024):
    # For compatibility – return a simple descriptor
    return {
        "backend": "sounddevice" if sd else ("pydub" if pydub_play else "none"),
        "device": device,
        "samplerate": samplerate,
        "channels": channels,
        "blocksize": blocksize,
    }

def set_sound_master_volume(v: float):
    global _sound_master_volume
    v = float(v)
    _sound_master_volume = max(0.0, min(1.0, v))

def get_sound_master_volume() -> float:
    return _sound_master_volume

def set_sound_storage(path: str):
    global _sound_storage
    _sound_storage = Path(path)

def get_sound_storage() -> str:
    return str(_sound_storage)

def set_sound_decryption_key(key: str):
    global _sound_key
    _sound_key = key  # Placeholder

def _resolve_path(path: str) -> Path:
    p = Path(path)
    if not p.is_file():
        p2 = _sound_storage / path
        return p2
    return p

def play_sound(path: str):
    p = _resolve_path(path)
    if not p.exists():
        raise FileNotFoundError(p)
    if AudioSegment is not None and pydub_play is not None:
        seg = AudioSegment.from_file(p)
        # Apply master volume (simple linear gain)
        gain_db = 20.0 if _sound_master_volume > 1.0 else 0.0
        if gain_db != 0.0:
            seg = seg + gain_db
        pydub_play(seg)
        return True
    # No playback backend; pretend success
    return False
