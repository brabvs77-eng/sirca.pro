#!/usr/bin/env python3
"""Render authentic card imagery from the Sirca house-building catalog."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "sirca.pdf.pdf"
DEST = ROOT / "public" / "img" / "sirca"

# PDF page, crop x/y/width/height at 100 dpi (rendered page: 827 × 1170).
ASSETS = {
    "catalog": (25, "0:120:827:620"),
    "imw": (26, "0:135:827:620"),
    "water-barrier": (33, "0:135:827:620"),
    "water-white": (35, "0:130:827:620"),
    "water-lacquer": (36, "0:120:827:620"),
    "water-enamel": (37, "0:130:827:620"),
    "oil": (38, "0:120:827:620"),
    "pu": (41, "0:130:827:620"),
    "acrylic": (43, "0:130:827:620"),
    "parquet": (45, "0:130:827:620"),
}


def run(command: list[str]) -> None:
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="sirca-pages-") as folder:
        temp = Path(folder)
        for name, (page, crop) in ASSETS.items():
            prefix = temp / name
            run(
                [
                    "pdftoppm",
                    "-f",
                    str(page),
                    "-l",
                    str(page),
                    "-jpeg",
                    "-r",
                    "100",
                    str(PDF),
                    str(prefix),
                ]
            )
            source = next(temp.glob(f"{name}-*.jpg"))
            x, y, width, height = crop.split(":")
            run(
                [
                    "ffmpeg",
                    "-y",
                    "-i",
                    str(source),
                    "-vf",
                    f"crop={width}:{height}:{x}:{y},scale=720:540",
                    "-c:v",
                    "libwebp",
                    "-quality",
                    "76",
                    str(DEST / f"{name}.webp"),
                ]
            )

    print(f"created {len(ASSETS)} Sirca card images in {DEST}")


if __name__ == "__main__":
    main()
