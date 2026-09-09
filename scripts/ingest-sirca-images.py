#!/usr/bin/env python3
"""Convert generated lifestyle card art to per-SKU WebP assets for the Sirca catalog."""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "sirca-generated"
DEST = ROOT / "public" / "img" / "sirca"
COVER = ROOT / "public" / "img" / "covers" / "sirca.webp"

# One unique source PNG per SKU (basename without extension in assets/sirca-generated/).
SLUG_IMAGES: dict[str, str] = {
    "imw4800": "sirca-imw",
    "imw4400": "sirca-hardwood",
    "fiw350": "sirca-log-cabin",
    "fiw470": "sirca-primer",
    "fwe600": "sirca-deck",
    "fwe801": "sirca-fwe801",
    "fwp630": "sirca-white-primer",
    "fwp830": "sirca-fwp830",
    "owe500": "sirca-lacquer",
    "owe501": "sirca-owe501",
    "owe505": "sirca-green-house",
    "owp330": "sirca-enamel",
    "oil30": "sirca-oil",
    "opu99g": "sirca-pu-exterior",
    "opp1930g": "sirca-opp1930g",
    "opa9330": "sirca-acrylic",
    "opu979": "sirca-opu979",
    "fpu932e": "sirca-toned-lacquer",
    "fa930": "sirca-water-repellent",
    "fpu16tix": "sirca-fpu16tix",
    "ow1fg40": "sirca-parquet-sport",
    "opu60g": "sirca-parquet-bedroom",
    "opu379g": "sirca-parquet-matte",
    "opu79": "sirca-opu79",
    "lpu002": "sirca-polyester",
    "opu57": "sirca-opu57",
    "opu77": "sirca-stairs",
    "opu91": "sirca-countertop",
    "opu277": "sirca-opu277",
    "fpp26": "sirca-mdf-primer",
    "fpp20": "sirca-fpp20",
    "fpp47": "sirca-mdf-isolator",
    "fpu15": "sirca-fpu15",
    "opp053-black": "sirca-black-enamel",
    "opp053-white": "sirca-white-enamel",
    "fl3100": "sirca-furniture-lacquer",
    "th52": "sirca-hardener",
    "th43": "sirca-th43",
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


def file_hash(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def main() -> None:
    if len(SLUG_IMAGES) != len(set(SLUG_IMAGES)):
        dupes = [v for v in set(SLUG_IMAGES.values()) if list(SLUG_IMAGES.values()).count(v) > 1]
        raise SystemExit(f"duplicate source mapping: {dupes}")

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

    hashes: dict[str, list[str]] = {}
    for webp in DEST.glob("*.webp"):
        h = file_hash(webp)
        hashes.setdefault(h, []).append(webp.name)
    dupes = {h: names for h, names in hashes.items() if len(names) > 1}
    if dupes:
        raise SystemExit(f"duplicate output images: {dupes}")

    legacy = {"catalog", "imw", "water-barrier", "water-white", "water-lacquer", "water-enamel", "oil", "pu", "acrylic", "parquet"}
    for old in legacy:
        path = DEST / f"{old}.webp"
        if path.exists():
            path.unlink()

    print(f"wrote cover + {len(SLUG_IMAGES)} unique card images")


if __name__ == "__main__":
    main()
