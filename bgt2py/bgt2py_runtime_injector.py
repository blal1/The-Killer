#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bgt2py_runtime_injector.py — Wrapper around the earlier converter that auto-injects:
    from bgt_runtime import *
and emits warnings if calls touch unsupported categories.

Usage:
  python bgt2py_runtime_injector.py "src/**/*.bgt" -o out -r
"""
from __future__ import annotations
import argparse, re, json
from pathlib import Path

INJECT = "from bgt_runtime import *\n"

def convert_basic(text: str) -> str:
    # Minimal structural conversion (reuse simple rules)
    # This is intentionally lightweight; for best conversion, use your advanced converter
    text = text.replace("\r\n", "\n")
    # comments
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    out = []
    indent = 0
    for line in text.splitlines():
        # line comment
        pos = line.find("//")
        if pos >= 0:
            line = line[:pos] + "# " + line[pos+2:]
        # tokens
        line = re.sub(r"\belse\s+if\b","elif", line)
        line = re.sub(r"\btrue\b","True", line)
        line = re.sub(r"\bfalse\b","False", line)
        line = re.sub(r"\bnull\b","None", line)
        # braces
        closes = line.count("}")
        opens = line.count("{")
        if closes:
            indent = max(0, indent - closes)
            line = line.replace("}", "")
        if opens:
            line = line.replace("{", ":")
        # strip trailing ;
        line = re.sub(r";\s*$", "", line)
        if line.strip():
            out.append(("    " * indent) + line.strip())
        else:
            out.append("")
        if opens:
            indent += opens
    return "\n".join(out) + "\n"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("-o","--outdir", type=Path, default=Path("."))
    ap.add_argument("-r","--relative", action="store_true")
    args = ap.parse_args()

    # Load coverage (if present) to know what's in the doc
    cov_path = Path(__file__).resolve().parent.parent / "bgt_api_coverage.json"
    coverage = {}
    if cov_path.exists():
        try:
            coverage = json.loads(cov_path.read_text(encoding="utf-8"))
        except Exception:
            coverage = {}

    seen_calls = set()

    matched = []
    for pattern in args.inputs:
        if any(c in pattern for c in "*?["):
            matched += list(Path().glob(pattern))
        else:
            matched += [Path(pattern)]
    matched = [p for p in matched if p.is_file()]

    for src in matched:
        txt = src.read_text(encoding="utf-8", errors="ignore")
        py = convert_basic(txt)
        # Inject runtime import at top
        py = INJECT + py

        # Heuristic: warn if text references functions known in doc but not in our current runtime modules
        categories = coverage.get("categories", {})
        missing = []
        for cat, funcs in categories.items():
            for fn in funcs:
                # If function name appears anywhere (rough heuristic), record it
                if re.search(r"\b" + re.escape(fn) + r"\b", txt):
                    # we don't check actual implementation presence here; just list for report
                    missing.append(f"{cat}.{fn}")
        if missing:
            header = "# WARN: The following BGT functions were referenced and may need explicit mapping:"
            listing = "\n".join("#   - " + m for m in sorted(set(missing)))
            py = header + "\n" + listing + "\n\n" + py

        # Save
        if args.relative:
            out_path = args.outdir / src.with_suffix(".py")
        else:
            out_path = args.outdir / src.with_suffix(".py").name
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(py, encoding="utf-8")
        print(f"[OK] {src} -> {out_path}")

if __name__ == "__main__":
    main()
