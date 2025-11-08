"""
bgt_runtime — High-fidelity partial runtime for BGT to Python.
This package provides realistic mappings for common BGT APIs with graceful fallbacks.
"""

# Re-export convenience
from .audio import *
from .fs import *
from .net import *
from .mathutils import *
from .debug import *
from .system import *
from .strings import *

# Legacy helper names that many converted scripts expect
# (These mirror convenience utilities that existed in BGT samples)
def string_replace(s, old, new, all_occurrences=True):
    return s.replace(old, new) if all_occurrences else s.replace(old, new, 1)

def string_split(s, sep="\n", keep_empty=True):
    parts = s.split(sep)
    if not keep_empty:
        parts = [x for x in parts if x]
    return parts

def string_contains(s, sub, start_index=0):
    return s.find(sub, start_index)

def string_left(s, n):
    return s[:n]

def string_right(s, n):
    return s[-n:] if n else ""

def string_trim_left(s, n_or_prefix):
    if isinstance(n_or_prefix, int):
        return s[n_or_prefix:]
    try:
        idx = int(n_or_prefix)
        return s[idx:]
    except Exception:
        pre = str(n_or_prefix)
        return s[len(pre):] if s.startswith(pre) else s

def string_trim_right(s, n):
    return s[:-n] if n else s

class file:
    def __init__(self): self._fp = None
    def open(self, path, mode="r"):
        self._fp = open(path, mode, encoding="utf-8", errors="ignore")
    def read(self): return self._fp.read()
    def write(self, data): self._fp.write(data)
    def close(self):
        try: self._fp.close()
        except Exception: pass

def file_exists(path):
    from pathlib import Path
    return Path(path).exists()

from .audio_advanced import *
from .events import *
from .timers import *
from .dispatcher import *
try:
    from .input import *
except Exception:
    # input depends on pygame; ignore if unavailable
    pass

# Gameplay façades (BGT-style)
from .gameplay.core import Game, Stage, Entity, AABB
from .gameplay.sidescroller import SidescrollerStage, Player, Platform
from .gameplay.fighter import Fighter
from .gameplay.resources import ResourceCache
