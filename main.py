#!/usr/bin/env python3
"""Entrypoint for the news-image-20261121 entry.

Copies the pre-rendered front page (entry.png, drawn by draw_poster.py
and committed to this repository) to the output directory as entry.png.

Standard library only, no network, fully deterministic: a byte-for-byte
copy, so repeated runs always produce identical output.
"""

import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        raise SystemExit("entry.png missing next to main.py: %s" % src)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    size = os.path.getsize(dst)
    if size == 0:
        raise SystemExit("copied entry.png is empty")
    print("wrote %s (%d bytes)" % (dst, size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
