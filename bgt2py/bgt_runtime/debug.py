"""
debug — Debugging and analysis mapping.
"""
from __future__ import annotations
import traceback
import cProfile, pstats, io as _io

def assert_(cond: bool, msg: str="Assertion failed"):
    if not cond:
        raise AssertionError(msg)

def get_call_stack() -> str:
    return "".join(traceback.format_stack())

def generate_profile(func, *args, **kwargs):
    pr = cProfile.Profile()
    pr.enable()
    try:
        result = func(*args, **kwargs)
    finally:
        pr.disable()
        s = _io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats("cumtime")
        ps.print_stats()
    return result, s.getvalue()
