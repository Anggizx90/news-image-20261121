#!/usr/bin/env python3
"""Copy the finished front page to the grading output directory.

Standard library only: the grading sandbox installs nothing, so this
program just copies entry.png (the front page draw_poster.py renders)
to $MAKEFUN_OUTPUT_DIR/entry.png, defaulting to /output/entry.png.
The copy is byte-for-byte, so repeated runs write identical bytes.
"""
import os
import shutil
import sys


def output_path():
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(folder, "entry.png")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    if not os.path.isfile(source):
        print("entry.png is missing; run draw_poster.py first", file=sys.stderr)
        return 1
    target = output_path()
    os.makedirs(os.path.dirname(target) or ".", exist_ok=True)
    shutil.copyfile(source, target)
    print("wrote " + target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
