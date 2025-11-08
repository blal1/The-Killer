"""
strings — Extended string ops commonly used in BGT code.
"""
from __future__ import annotations

def starts_with(s: str, prefix: str) -> bool:
    return s.startswith(prefix)

def ends_with(s: str, suffix: str) -> bool:
    return s.endswith(suffix)

def replace_all(s: str, old: str, new: str) -> str:
    return s.replace(old, new)

def to_upper(s: str) -> str:
    return s.upper()

def to_lower(s: str) -> str:
    return s.lower()
