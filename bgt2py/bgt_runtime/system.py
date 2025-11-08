"""
system — Sleep/time and simple UI replacements.
"""
from __future__ import annotations
import time
from pathlib import Path

def sleep(ms: int):
    time.sleep(ms / 1000.0)

def get_tick_count():
    # milliseconds since epoch
    return int(time.time() * 1000)

def alert(title: str, message: str):
    print(f"[{title}] {message}")

def input_box(title: str, message: str, default: str=""):
    try:
        return input(f"{title} - {message} [{default}]: ") or default
    except EOFError:
        return default
