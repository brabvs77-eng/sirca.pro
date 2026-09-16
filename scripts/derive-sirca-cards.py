#!/usr/bin/env python3
"""Create unique, family-relevant WebP card images for Sirca catalog."""

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

# slug/sku regex → lifestyle PNG stem (without .png)
LIFESTYLE_RULES: list[tuple[str, str]] = [
    (r"^es", "sirca-es-effect"),
    (r"^uv", "sirca-uv-line"),
    (r"^wetro", "sirca-wetro-deck"),
    (r"^lpp", "sirca-lpp-enamel"),
    (r"^pcv|^puv", "sirca-pcv-floor"),
    (r"^f3|^f4|^fo|^fop|^ffo|^fma|^f33|^f33|^f42|^f52|^f88|^f10", "sirca-metal-primer"),
    (r"^adts|^adtw|^ct|^cte|^dpn|^fde|^fdl|^fbu|^gdv|^f912|^f915|^f921|^otvep|^pm$", "sirca-additives"),
    (r"^cr(?!w)", "sirca-converter-colors"),
    (r"^opu99|^opp19|^fpu16", "sirca-pu-exterior-alt"),
    (r"^opu60|^opu379", "sirca-parquet-bedroom"),
    (r"^opu", "sirca-pu-furniture"),
    (r"^opp053", "sirca-white-enamel"),
    (r"^opp", "sirca-opp1930g"),
    (r"^fpp", "sirca-fpp-mdf"),
    (r"^fpu93|^opu979|^opa|^fa", "sirca-acrylic-exterior"),
    (r"^fpu15", "sirca-fpu15"),
    (r"^fl|^lpu", "sirca-polyester"),
    (r"^th", "sirca-hardener"),
    (r"^imw|^iwj", "sirca-imw"),
    (r"^iwc", "sirca-iwc-deck"),
    (r"^fiw|^fwbp", "sirca-primer"),
    (r"^fwe", "sirca-deck"),
    (r"^fwp", "sirca-white-primer"),
    (r"^fwpi|^idrofloor|^sportfloor", "sirca-fwpi-floor"),
    (r"^owe", "sirca-owe-window"),
    (r"^owp|^wop", "sirca-enamel"),
    (r"^owpi|^so|^crw", "sirca-furniture-water"),
    (r"^owb", "sirca-parquet-bedroom"),
    (r"^ow", "sirca-parquet-matte"),
    (r"^siw", "sirca-enamel"),
    (r"^oil", "sirca-oil"),
    (r"^fw", "sirca-furniture-lacquer"),
]

# Families that should use real Sirca packshot photos when possible
PACKSHOT_FAMILIES = re.compile(
    r"^(adts|adtw|ct|cte|dpn|fde|fdl|fbu|gdv|f912|f915|f921|hx|ima|ir|ma|onc|otvep|pm|upx|vopu|fuw|fiw|fwb)",
    re.I,
)

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


def digest(slug: str) -> int:
    return int(hashlib.md5(slug.encode()).hexdigest(), 16)


def lifestyle_stem(slug: str) -> str:
    key = slug.lower().replace("_", "-")
    for pattern, stem in LIFESTYLE_RULES:
        if re.match(pattern, key):
            return stem
    return "sirca-imw"


def pick_from_pool(pool: list[Path], slug: str) -> Path:
    return pool[digest(slug) % len(pool)]


def resolve_source(slug: str) -> Path:
    sku = slug.upper().replace("-", "")

    # ES material swatches when code matches uploaded samples
    for code, filename in ES_SAMPLE_MAP.items():
        if code.upper() in sku or code.upper() in slug.upper():
            path = SAMPLE_DIR / filename
            if path.exists():
                return path

    packshots = sorted(PACKSHOT_DIR.glob("*.jpg"))
    if packshots and PACKSHOT_FAMILIES.match(slug):
        return pick_from_pool(packshots, slug)

    # ES line: mix swatches and effect lifestyle
    if sku.startswith("ES"):
        samples = sorted(SAMPLE_DIR.glob("*.jpg"))
        if samples and digest(slug) % 3 == 0:
            return pick_from_pool(samples, slug)

    # Water-based lines: packshot on half of cards for product relevance
    if packshots and re.match(r"^(ow|owpi|owp|crw|fwpi)", slug, re.I) and digest(slug) % 2 == 0:
        return pick_from_pool(packshots, slug)

    stem = lifestyle_stem(slug)
    path = LIFESTYLE_DIR / f"{stem}.png"
    if path.exists():
        return path

    fallback = LIFESTYLE_DIR / "sirca-imw.png"
    return fallback


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def derive(src: Path, dest: Path, slug: str) -> None:
    d = digest(slug)
    w, h = 720, 540

    if src.suffix.lower() in {".jpg", ".jpeg"}:
        # Packshots and ES swatches: center crop + subtle grade
        x = (d % 40) - 20
        y = ((d >> 6) % 30) - 15
        bright = (d % 11) - 5
        sat = 1 + ((d >> 10) % 9) / 100
        vf = (
            f"scale={w}:{h}:force_original_aspect_ratio=increase,"
            f"crop={w}:{h},"
            f"eq=brightness={bright / 100}:saturation={sat},"
            f"hue=h={x}:s={sat}"
        )
    else:
        # Lifestyle PNG: sliding crop + grade for per-slug uniqueness
        cx = d % 100
        cy = (d >> 8) % 60
        hue = ((d >> 16) % 17) - 8
        sat = 1 + ((d >> 20) % 13) / 100
        bright = ((d >> 24) % 9) - 4
        vf = (
            f"crop=620:465:{cx}:{cy},"
            f"scale={w}:{h},"
            f"eq=brightness={bright / 100}:saturation={sat},"
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
            "82",
            str(dest),
        ]
    )


def main() -> None:
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    slugs = slugs_from_catalog()
    used_sources: dict[str, int] = {}

    for slug in slugs:
        src = resolve_source(slug)
        used_sources[src.name] = used_sources.get(src.name, 0) + 1
        derive(src, DEST_DIR / f"{slug}.webp", slug)

    hashes: dict[str, list[str]] = {}
    for webp in DEST_DIR.glob("*.webp"):
        h = hashlib.md5(webp.read_bytes()).hexdigest()
        hashes.setdefault(h, []).append(webp.name)

    dupes = {h: names for h, names in hashes.items() if len(names) > 1}
    if dupes:
        # Retry duplicates with stronger per-slug grade offset
        for h, names in dupes.items():
            for slug in names:
                slug_key = slug.removesuffix(".webp")
                src = resolve_source(slug_key)
                d = digest(slug_key + ":retry")
                extra = f",hue=h={(d % 41) - 20}:s={1 + (d % 7) / 50}"
                run(
                    [
                        "ffmpeg",
                        "-y",
                        "-i",
                        str(src),
                        "-vf",
                        f"scale=720:540:force_original_aspect_ratio=increase,crop=720:540,eq=brightness={(d % 9 - 4) / 80}{extra}",
                        "-c:v",
                        "libwebp",
                        "-quality",
                        "82",
                        str(DEST_DIR / slug),
                    ]
                )
        hashes = {}
        for webp in DEST_DIR.glob("*.webp"):
            hh = hashlib.md5(webp.read_bytes()).hexdigest()
            hashes.setdefault(hh, []).append(webp.name)
        dupes = {hh: n for hh, n in hashes.items() if len(n) > 1}
        if dupes:
            sample = next(iter(dupes.values()))
            raise SystemExit(f"duplicate card images remain, e.g. {sample[:5]}")

    pack_used = sum(1 for n in used_sources if n.endswith(".jpg"))
    print(f"derived {len(slugs)} card images ({pack_used} packshot/sample sources used)")


if __name__ == "__main__":
    main()
