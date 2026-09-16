#!/usr/bin/env python3
"""Create visually distinct, family-relevant WebP card images for Sirca catalog."""

from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIFESTYLE_DIR = ROOT / "assets" / "sirca-generated"
PACKSHOT_DIR = ROOT / "assets" / "sirca-packshots"
SAMPLE_DIR = ROOT / "assets" / "sirca-samples"
DEST_DIR = ROOT / "public" / "img" / "sirca"
CATALOG = ROOT / "src/data/products-sirca.ts"
TDS_CATALOG = ROOT / "src/data/products-sirca-tds.ts"

# Family regex → lifestyle PNG stems (multiple per family for visual variety)
FAMILY_POOLS: list[tuple[str, list[str]]] = [
    (
        r"^es",
        [
            "sirca-es-effect",
            "sirca-es-cement",
            "sirca-es-copper",
            "sirca-polyester",
            "sirca-metal-primer",
            "sirca-converter-colors",
            "sirca-countertop",
        ],
    ),
    (
        r"^uv",
        [
            "sirca-uv-line",
            "sirca-uv-curing",
            "sirca-uv-roller",
            "sirca-furniture-lacquer",
            "sirca-pu-furniture",
            "sirca-toned-lacquer",
            "sirca-white-enamel",
            "sirca-mdf-primer",
            "sirca-polyester",
        ],
    ),
    (r"^wetro", ["sirca-wetro-deck", "sirca-deck", "sirca-iwc-deck", "sirca-hardwood", "sirca-oil"]),
    (r"^lpp", ["sirca-lpp-enamel", "sirca-white-enamel", "sirca-furniture-lacquer", "sirca-mdf-primer"]),
    (r"^pcv|^puv", ["sirca-pcv-floor", "sirca-parquet-sport", "sirca-fwpi-floor", "sirca-parquet-bedroom"]),
    (
        r"^f3|^f4|^fo|^fop|^ffo|^f33|^f42|^f52|^f88|^f10",
        ["sirca-metal-primer", "sirca-primer", "sirca-white-primer", "sirca-acrylic", "sirca-additives"],
    ),
    (
        r"^adts|^adtw|^ct|^cte|^dpn|^fde|^fdl|^fbu|^gdv|^f912|^f915|^f921|^otvep|^pm$",
        ["sirca-additives", "sirca-hardener", "sirca-th43"],
    ),
    (r"^cr(?!w)", ["sirca-converter-colors", "sirca-imw", "sirca-deck", "sirca-iwc-deck"]),
    (r"^opu99|^opp19|^fpu16", ["sirca-pu-exterior-alt", "sirca-pu-exterior", "sirca-green-house"]),
    (r"^opu60|^opu379", ["sirca-parquet-bedroom", "sirca-parquet-matte", "sirca-fwpi-floor"]),
    (r"^opu", ["sirca-pu-furniture", "sirca-opu277", "sirca-opu57", "sirca-opu79", "sirca-furniture-lacquer"]),
    (r"^opp053", ["sirca-white-enamel", "sirca-black-enamel", "sirca-enamel"]),
    (r"^opp", ["sirca-opp1930g", "sirca-pu-exterior", "sirca-white-enamel"]),
    (r"^fpp", ["sirca-fpp-mdf", "sirca-fpp20", "sirca-mdf-primer", "sirca-mdf-isolator"]),
    (r"^fpu93|^opu979|^opa|^fa", ["sirca-acrylic-exterior", "sirca-acrylic", "sirca-opu979", "sirca-spray-window"]),
    (r"^fpu15", ["sirca-fpu15", "sirca-fpu16tix", "sirca-primer"]),
    (r"^fl|^lpu", ["sirca-polyester", "sirca-furniture-lacquer", "sirca-countertop"]),
    (r"^th", ["sirca-hardener", "sirca-th43", "sirca-additives"]),
    (r"^imw|^iwj", ["sirca-imw", "sirca-log-cabin", "sirca-deck", "sirca-owe-window", "sirca-green-house"]),
    (r"^iwc", ["sirca-iwc-deck", "sirca-deck", "sirca-oil", "sirca-hardwood"]),
    (r"^fiw|^fwbp", ["sirca-primer", "sirca-log-cabin", "sirca-white-primer", "sirca-fwe801"]),
    (r"^fwe", ["sirca-deck", "sirca-fwe801", "sirca-log-cabin", "sirca-owe-window"]),
    (r"^fwp", ["sirca-white-primer", "sirca-fwp830", "sirca-enamel"]),
    (r"^fwpi|^idrofloor|^sportfloor", ["sirca-fwpi-floor", "sirca-parquet-sport", "sirca-parquet-bedroom"]),
    (r"^owe", ["sirca-owe-window", "sirca-owe501", "sirca-spray-window", "sirca-enamel"]),
    (r"^owp|^wop", ["sirca-enamel", "sirca-green-house", "sirca-fwp830"]),
    (r"^owpi|^so|^crw", ["sirca-furniture-water", "sirca-furniture-lacquer", "sirca-mdf-primer"]),
    (r"^owb", ["sirca-parquet-bedroom", "sirca-parquet-matte", "sirca-fwpi-floor"]),
    (r"^ow", ["sirca-parquet-matte", "sirca-parquet-bedroom", "sirca-hardwood"]),
    (r"^siw", ["sirca-enamel", "sirca-spray-window", "sirca-owe-window"]),
    (r"^oil", ["sirca-oil", "sirca-iwc-deck", "sirca-deck"]),
    (r"^fw", ["sirca-furniture-lacquer", "sirca-furniture-water", "sirca-toned-lacquer"]),
]

ES_SAMPLE_MAP = {
    "s05": "photo_ES1013s05.jpg",
    "s07": "photo_ES1013s07.jpg",
    "s08": "photo_ES1013s08.jpg",
    "s09": "photo_ES1013s09.jpg",
    "s304": "photo_ES1013s304.jpg",
}


def slugs_from_catalog() -> list[str]:
    text = CATALOG.read_text(encoding="utf-8") + TDS_CATALOG.read_text(encoding="utf-8")
    return sorted(set(re.findall(r"slug: '([^']+)'", text)))


def digest(slug: str, salt: str = "") -> int:
    return int(hashlib.md5(f"{slug}:{salt}".encode()).hexdigest(), 16)


def lifestyle_paths(stems: list[str]) -> list[Path]:
    out: list[Path] = []
    for stem in stems:
        path = LIFESTYLE_DIR / f"{stem}.png"
        if path.exists():
            out.append(path)
    return out


def family_stems(slug: str) -> list[str]:
    key = slug.lower().replace("_", "-")
    for pattern, stems in FAMILY_POOLS:
        if re.match(pattern, key):
            return stems
    return ["sirca-imw", "sirca-deck", "sirca-primer", "sirca-log-cabin"]


def build_pool(slug: str) -> list[Path]:
    pool: list[Path] = []
    seen: set[str] = set()

    def add(path: Path | None) -> None:
        if path and path.exists() and path.name not in seen:
            seen.add(path.name)
            pool.append(path)

    sku = slug.upper().replace("-", "")
    for code, filename in ES_SAMPLE_MAP.items():
        if code.upper() in sku:
            add(SAMPLE_DIR / filename)

    for path in lifestyle_paths(family_stems(slug)):
        add(path)

    # One packshot per SKU — lifestyle images carry most of the visual variety
    packshots = sorted(PACKSHOT_DIR.glob("*.jpg"))
    if packshots:
        add(packshots[digest(slug, "pack") % len(packshots)])

    # Extra lifestyle stems from other families (slug-hash pick) for more scene variety
    all_stems = sorted({stem for _, stems in FAMILY_POOLS for stem in stems})
    start = digest(slug, "extra") % max(1, len(all_stems))
    for i in range(min(4, len(all_stems))):
        for path in lifestyle_paths([all_stems[(start + i) % len(all_stems)]]):
            add(path)

    samples = sorted(SAMPLE_DIR.glob("*.jpg"))
    if samples and re.match(r"^es", slug, re.I):
        start = digest(slug, "es") % len(samples)
        for i in range(len(samples)):
            add(samples[(start + i) % len(samples)])

    if not pool:
        add(LIFESTYLE_DIR / "sirca-imw.png")
    return pool


def resolve_source(slug: str) -> Path:
    pool = build_pool(slug)
    return pool[digest(slug) % len(pool)]


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def derive(src: Path, dest: Path, slug: str, salt: str = "") -> None:
    d = digest(slug, salt)
    w, h = 720, 540

    flip = "hflip," if d % 2 == 0 else ""
    angle = ((d >> 4) % 11) - 5  # -5..+5 degrees
    zoom = 1.08 + ((d >> 8) % 45) / 100  # 1.08..1.52
    hue = ((d >> 12) % 81) - 40
    sat = 0.75 + ((d >> 18) % 41) / 100
    bright = ((d >> 22) % 31) - 15
    contrast = 0.92 + ((d >> 26) % 17) / 100

    if src.suffix.lower() in {".jpg", ".jpeg"}:
        cx = (d >> 2) % 120
        cy = (d >> 10) % 80
        vf = (
            f"scale=iw*{zoom}:ih*{zoom},"
            f"crop=640:480:{cx}:{cy},"
            f"{flip}"
            f"rotate={angle}*PI/180:fillcolor=black@0:ow={w}:oh={h},"
            f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},"
            f"eq=brightness={bright / 100}:contrast={contrast}:saturation={sat},"
            f"hue=h={hue}:s={sat}"
        )
    else:
        cx = (d >> 2) % 200
        cy = (d >> 10) % 120
        cw = 480 + (d % 140)
        ch = 360 + ((d >> 6) % 100)
        vf = (
            f"crop={cw}:{ch}:{cx}:{cy},"
            f"scale=iw*{zoom}:ih*{zoom},"
            f"{flip}"
            f"rotate={angle}*PI/180:fillcolor=black@0:ow={w}:oh={h},"
            f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},"
            f"eq=brightness={bright / 100}:contrast={contrast}:saturation={sat},"
            f"hue=h={hue}:s={sat}"
        )

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
            "84",
            str(dest),
        ]
    )


def main() -> None:
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    slugs = slugs_from_catalog()

    for slug in slugs:
        derive(resolve_source(slug), DEST_DIR / f"{slug}.webp", slug)

    hashes: dict[str, list[str]] = {}
    for webp in DEST_DIR.glob("*.webp"):
        h = hashlib.md5(webp.read_bytes()).hexdigest()
        hashes.setdefault(h, []).append(webp.name)

    dupes = {h: names for h, names in hashes.items() if len(names) > 1}
    if dupes:
        for names in dupes.values():
            for name in names:
                slug = name.removesuffix(".webp")
                derive(resolve_source(slug), DEST_DIR / name, slug, salt="retry")
        hashes = {}
        for webp in DEST_DIR.glob("*.webp"):
            hh = hashlib.md5(webp.read_bytes()).hexdigest()
            hashes.setdefault(hh, []).append(webp.name)
        dupes = {hh: n for hh, n in hashes.items() if len(n) > 1}
        if dupes:
            sample = next(iter(dupes.values()))
            raise SystemExit(f"duplicate card images remain, e.g. {sample[:5]}")

    # Report source spread
    from collections import Counter

    src_count = Counter(resolve_source(s).name for s in slugs)
    top = src_count.most_common(3)
    print(f"derived {len(slugs)} cards, max shared source: {top[0][1]}× {top[0][0]}")


if __name__ == "__main__":
    main()
