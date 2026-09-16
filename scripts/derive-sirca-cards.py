#!/usr/bin/env python3
"""Create unique per-slug WebP card images from generated PNG sources."""

from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "assets" / "sirca-generated"
DEST_DIR = ROOT / "public" / "img" / "sirca"
CATALOG = ROOT / "src/data/products-sirca.ts"
TDS_CATALOG = ROOT / "src/data/products-sirca-tds.ts"

# Base PNG stem per product family prefix
FAMILY_SOURCE: dict[str, str] = {
    "IMW": "sirca-imw",
    "IWJ": "sirca-imw",
    "IWC": "sirca-iwc-deck",
    "FIW": "sirca-primer",
    "FWE": "sirca-deck",
    "FWP": "sirca-white-primer",
    "FWPI": "sirca-fwpi-floor",
    "FW": "sirca-furniture-lacquer",
    "FWBP": "sirca-log-cabin",
    "OWE": "sirca-owe-window",
    "OWP": "sirca-enamel",
    "WOP": "sirca-green-house",
    "OWPI": "sirca-furniture-water",
    "OWB": "sirca-parquet-bedroom",
    "OW": "sirca-parquet-matte",
    "CRW": "sirca-furniture-water",
    "IDROFLOOR": "sirca-parquet-sport",
    "SPORTFLOOR": "sirca-parquet-sport",
    "SIW": "sirca-enamel",
    "SO": "sirca-furniture-water",
    "OIL": "sirca-oil",
    "OPU": "sirca-pu-exterior",
    "OPP": "sirca-opp1930g",
    "OPA": "sirca-acrylic",
    "FPU": "sirca-fpu16tix",
    "FA": "sirca-water-repellent",
    "FPP": "sirca-mdf-primer",
    "FL": "sirca-furniture-lacquer",
    "LPU": "sirca-polyester",
    "TH": "sirca-hardener",
    "CT": "sirca-hardener",
    "F912": "sirca-hardener",
    "F915": "sirca-hardener",
    "F921": "sirca-hardener",
    "ADTS": "sirca-hardener",
    "ADTW": "sirca-hardener",
    "CTE": "sirca-hardener",
    "DPN": "sirca-hardener",
    "FDE": "sirca-hardener",
    "FDL": "sirca-hardener",
    "FBU": "sirca-hardener",
    "GDV": "sirca-hardener",
    "ES": "sirca-polyester",
    "UV": "sirca-furniture-lacquer",
    "CR": "sirca-furniture-water",
}


def slugs_from_catalog() -> list[str]:
    text = CATALOG.read_text(encoding="utf-8") + TDS_CATALOG.read_text(encoding="utf-8")
    return sorted(set(re.findall(r"slug: '([^']+)'", text)))


def source_for_slug(slug: str) -> str:
    sku = slug.upper().replace("-", "")
    # specific rules before broad prefixes
    rules: list[tuple[str, str]] = [
        (r"^OPU99|^OPP193|^FPU16", "sirca-pu-exterior-alt"),
        (r"^OPU60|^OPU379", "sirca-parquet-bedroom"),
        (r"^OPU\d|^OPU277", "sirca-pu-furniture"),
        (r"^OPP053", "sirca-white-enamel"),
        (r"^FPP", "sirca-fpp-mdf"),
        (r"^FPU93|^OPU979", "sirca-acrylic-exterior"),
        (r"^OPA|^FA930", "sirca-acrylic-exterior"),
        (r"^FPU15", "sirca-fpu15"),
        (r"^FL|^LPU", "sirca-polyester"),
        (r"^TH", "sirca-hardener"),
    ]
    for pattern, stem in rules:
        if re.match(pattern, sku):
            return stem
    for key in sorted(FAMILY_SOURCE, key=len, reverse=True):
        if sku.startswith(key.replace("-", "")) or slug.upper().startswith(key):
            return FAMILY_SOURCE[key]
    return "sirca-imw"


def digest(slug: str) -> int:
    return int(hashlib.md5(slug.encode()).hexdigest(), 16)


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def derive(src: Path, dest: Path, slug: str) -> None:
    d = digest(slug)
    # unique crop window from 720x540 source
    x = (d % 120)
    y = ((d >> 8) % 80)
    hue = ((d >> 16) % 21) - 10
    sat = 1 + ((d >> 20) % 11) / 100
    vf = f"crop=600:450:{x}:{y},scale=720:540,hue=h={hue}:s={sat}"
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(src),
            "-vf",
            vf,
            "-c:v",
            "libwebp",
            "-quality",
            "78",
            str(dest),
        ]
    )


def main() -> None:
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    slugs = slugs_from_catalog()
    missing_src: set[str] = set()
    for slug in slugs:
        stem = source_for_slug(slug)
        src = SRC_DIR / f"{stem}.png"
        if not src.exists():
            missing_src.add(stem)
            src = SRC_DIR / "sirca-imw.png"
        derive(src, DEST_DIR / f"{slug}.webp", slug)

    hashes: dict[str, list[str]] = {}
    for webp in DEST_DIR.glob("*.webp"):
        h = hashlib.md5(webp.read_bytes()).hexdigest()
        hashes.setdefault(h, []).append(webp.name)
    dupes = {h: n for h, n in hashes.items() if len(n) > 1}
    if dupes:
        sample = next(iter(dupes.values()))
        raise SystemExit(f"duplicate card images remain, e.g. {sample[:5]}")

    if missing_src:
        print("warn: missing sources, used fallback:", ", ".join(sorted(missing_src)))
    print(f"derived {len(slugs)} unique card images")


if __name__ == "__main__":
    main()
