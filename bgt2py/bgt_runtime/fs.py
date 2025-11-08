"""
fs — Files & directories mapping.
"""
from __future__ import annotations
import glob
import shutil
import os
from pathlib import Path

def find_files(pattern: str):
    return glob.glob(pattern, recursive=True)

def make_directory(path: str, exist_ok=True):
    Path(path).mkdir(parents=True, exist_ok=exist_ok)

def copy_file(src: str, dst: str):
    shutil.copy2(src, dst)

def move_file(src: str, dst: str):
    shutil.move(src, dst)

def delete_file(path: str, missing_ok=True):
    p = Path(path)
    if p.exists():
        p.unlink()

def file_exists(path: str) -> bool:
    return Path(path).exists()
