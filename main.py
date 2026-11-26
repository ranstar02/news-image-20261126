#!/usr/bin/env python3
"""Entry point: copy the pre-rendered front page to the output dir.

The image (entry.png, 1024x1024) is drawn by draw.py at build time
and committed in this repo. This program only copies those exact
bytes to $MAKEFUN_OUTPUT_DIR/entry.png, so both runs are identical.
Standard library only; no network.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    sys.exit(main())
