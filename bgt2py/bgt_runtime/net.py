"""
net — Internet-related and basic sockets.

High-fidelity:
- url_get(url) / url_post(url, data) using requests if available, else urllib fallback
- download_file(url, dst)
- Simple TCP client helpers (connect/send/recv/close)
"""
from __future__ import annotations
import socket
from pathlib import Path

try:
    import requests
except Exception:
    requests = None
import urllib.request
import urllib.parse

def url_get(url: str, timeout=15):
    if requests:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        return r.text
    with urllib.request.urlopen(url, timeout=timeout) as f:
        return f.read().decode("utf-8", errors="replace")

def url_post(url: str, data: dict | bytes, timeout=15):
    if requests:
        r = requests.post(url, data=data, timeout=timeout)
        r.raise_for_status()
        return r.text
    if isinstance(data, dict):
        data = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as f:
        return f.read().decode("utf-8", errors="replace")

def download_file(url: str, dst: str, timeout=30):
    if requests:
        with requests.get(url, stream=True, timeout=timeout) as r:
            r.raise_for_status()
            p = Path(dst); p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "wb") as out:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        out.write(chunk)
            return str(p)
    urllib.request.urlretrieve(url, dst)
    return dst

class TCPClient:
    def __init__(self):
        self.sock = None
    def connect(self, host: str, port: int, timeout=10):
        self.sock = socket.create_connection((host, port), timeout=timeout)
    def send(self, data: bytes):
        self.sock.sendall(data)
    def recv(self, bufsize=4096):
        return self.sock.recv(bufsize)
    def close(self):
        try: self.sock.close()
        except Exception: pass
