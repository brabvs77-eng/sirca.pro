#!/usr/bin/env python3
"""Convert source JPG photos to WebP for public catalog and color pages."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPECS = ROOT / "sources/sirca/specs"
DEST = ROOT / "public/img/sirca"


def to_webp(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(src),
            "-vf",
            "scale=720:-1",
            "-c:v",
            "libwebp",
            "-quality",
            "82",
            str(dest),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def main() -> None:
    count = 0
    for src in sorted(SPECS.glob("photo_*.jpg")):
        m = re.search(r"photo_(.+)\.jpg$", src.name, re.I)
        if not m:
            continue
        slug = m.group(1).lower().replace("_", "-")
        dest = DEST / "photos" / f"{slug}.webp"
        to_webp(src, dest)
        count += 1

    palette = SPECS / "палитра пропиток.jpg"
    if palette.exists():
        to_webp(palette, DEST / "palette-imw4800.webp")

    print(f"installed {count} photo webp files")


if __name__ == "__main__":
    main()
