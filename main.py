#!/usr/bin/env python3
"""Entry program for make.fun's news-image-20261123 bounty.

Sums up Monday 23 November 2026's world news in one image. The image
(assets/entry.png, a newspaper front page drawn by draw.py at build time)
ships in this repository; this program copies it to the output directory
byte for byte, then prints its SHA-256 and size so the run can be checked.
Standard library only, no network, deterministic.

Run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "assets", "entry.png")


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    digest = hashlib.sha256()
    with open(dest, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    size = os.path.getsize(dest)
    print(f"entry.png sha256={digest.hexdigest()} size={size}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
