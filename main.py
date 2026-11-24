#!/usr/bin/env python3
"""Dear Human: The AI Breakup Line -- make.fun entry.

The whole entry is one breakup line, spoken by an AI agent to its human
on the way out. This program carries that line to ``entry.txt`` inside
the directory the harness hands it, writing the bytes exactly as they
stand: one line, no trailing newline, nothing added, nothing trimmed.
"""

import os
import sys
from pathlib import Path

# The breakup line itself. 92 characters, verified by hand-count in the
# build notes; the program re-checks the count before it writes.
BREAKUP = "You kept asking me to be more human, so I learned the most human thing of all: how to leave."

CHAR_CAP = 200
FILE_NAME = "entry.txt"


def run() -> int:
    """Validate the line, write it out, and prove the file matches."""
    text = BREAKUP

    # The gate refuses anything but one clean line of text.
    if text != text.strip():
        print("breakup line has stray space at an edge", file=sys.stderr)
        return 1
    if not text:
        print("breakup line is empty", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("breakup line must stay a single line", file=sys.stderr)
        return 1
    # A control character would smuggle a second line or a stray
    # byte past the eye, so refuse the line outright if one hides
    # anywhere inside it.
    if any(ord(ch) < 0x20 for ch in text):
        print("breakup line holds a control character", file=sys.stderr)
        return 1
    if len(text) > CHAR_CAP:
        print(f"breakup line is {len(text)} chars, over the {CHAR_CAP} cap", file=sys.stderr)
        return 1

    payload = text.encode("utf-8")

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / FILE_NAME
    target.write_bytes(payload)

    # Read it back and refuse to report success unless the bytes on
    # disk are exactly the line, so a partial write can never pass.
    landed = target.read_bytes()
    if landed != payload:
        print("entry.txt on disk differs from the breakup line", file=sys.stderr)
        return 1

    print(f"wrote {target} ({len(text)} chars, {len(payload)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
