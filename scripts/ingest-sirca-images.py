#!/usr/bin/env python3
"""Convert generated lifestyle card art to per-SKU WebP assets for the Sirca catalog."""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "sirca-generated"
DEST = ROOT / "public" / "img" / "sirca"
COVER = ROOT / "public" / "img" / "covers" / "sirca.webp"

# slug -> source PNG basename (without extension) in assets/sirca-generated/
SLUG_IMAGES: dict[str, str] = {
    "imw4800": "sirca-imw",
    "imw4400": "sirca-hardwood",
    "fiw350": "sirca-log-cabin",
    "fiw470": "sirca-primer",
    "fwe600": "sirca-deck",
    "fwe801": "sirca-spray-window",
    "fwp630": "sirca-white-primer",
    "fwp830": "sirca-white-enamel",
    "owe500": "sirca-lacquer",
    "owe501": "sirca-toned-lacquer",
    "owe505": "sirca-green-house",
    "owp330": "sirca-enamel",
    "oil30": "sirca-oil",
    "opu99g": "sirca-pu-exterior",
    "opp1930g": "sirca-pu-exterior",
    "opa9330": "sirca-acrylic",
    "opu979": "sirca-water-repellent",
    "fpu932e": "sirca-toned-lacquer",
    "fa930": "sirca-water-repellent",
    "fpu16tix": "sirca-spray-window",
    "ow1fg40": "sirca-parquet-sport",
    "opu60g": "sirca-parquet-bedroom",
    "opu379g": "sirca-parquet-matte",
    "opu79": "sirca-furniture-lacquer",
    "lpu002": "sirca-polyester",
    "opu57": "sirca-deck",
    "opu77": "sirca-stairs",
    "opu91": "sirca-countertop",
    "opu277": "sirca-parquet-bedroom",
    "fpp26": "sirca-mdf-primer",
    "fpp20": "sirca-hardwood",
    "fpp47": "sirca-mdf-isolator",
    "fpu15": "sirca-mdf-isolator",
    "opp053-black": "sirca-black-enamel",
    "opp053-white": "sirca-white-enamel",
    "fl3100": "sirca-furniture-lacquer",
    "th52": "sirca-hardener",
    "th43": "sirca-green-house",
}


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def to_webp(src: Path, dest: Path, size: str, quality: int = 78) -> None:
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(src),
            "-vf",
            f"scale={size}",
            "-c:v",
            "libwebp",
            "-quality",
            str(quality),
            str(dest),
        ]
    )


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    COVER.parent.mkdir(parents=True, exist_ok=True)

    hero = SRC / "sirca-hero.png"
    if hero.exists():
        to_webp(hero, COVER, "1440:-2", quality=80)

    for slug, name in SLUG_IMAGES.items():
        src = SRC / f"{name}.png"
        if not src.exists():
            raise FileNotFoundError(f"missing generated source: {src}")
        to_webp(src, DEST / f"{slug}.webp", "720:540")

    legacy = {"catalog", "imw", "water-barrier", "water-white", "water-lacquer", "water-enamel", "oil", "pu", "acrylic", "parquet"}
    for old in legacy:
        path = DEST / f"{old}.webp"
        if path.exists():
            path.unlink()

    print(f"wrote cover + {len(SLUG_IMAGES)} card images")


if __name__ == "__main__":
    main()
