#!/usr/bin/env python3
"""Copy packshot and sample photos into assets/ for card derivation."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKSHOT_DIR = ROOT / "assets" / "sirca-packshots"
SAMPLE_DIR = ROOT / "assets" / "sirca-samples"


def main() -> None:
    PACKSHOT_DIR.mkdir(parents=True, exist_ok=True)
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)

    for src in (ROOT / "sources/sirca/images").glob("*.jpg"):
        shutil.copy2(src, PACKSHOT_DIR / src.name)

    for src in (ROOT / "sources/sirca/specs").glob("photo_ES1013*.jpg"):
        shutil.copy2(src, SAMPLE_DIR / src.name)

    print(f"packshots: {len(list(PACKSHOT_DIR.glob('*.jpg')))}")
    print(f"samples: {len(list(SAMPLE_DIR.glob('*.jpg')))}")


if __name__ == "__main__":
    main()
