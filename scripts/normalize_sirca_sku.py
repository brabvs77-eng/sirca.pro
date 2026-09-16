#!/usr/bin/env python3
"""SKU normalization helpers for Sirca TDS filenames."""

from __future__ import annotations

import re

CYR_TO_LAT = str.maketrans(
    {
        "А": "A",
        "В": "V",
        "С": "C",
        "Е": "E",
        "Н": "H",
        "К": "K",
        "М": "M",
        "О": "O",
        "Р": "P",
        "Т": "T",
        "Х": "X",
        "а": "a",
        "в": "v",
        "с": "c",
        "е": "e",
        "н": "h",
        "к": "k",
        "м": "m",
        "о": "o",
        "р": "p",
        "т": "t",
        "х": "x",
    }
)


def normalize_sku_from_stem(stem: str) -> str:
    s = stem.strip()
    if "(" in s:
        s = s.split("(")[0].strip()
    s = re.sub(r"_RU(?:\(\d+\))?$", "", s, flags=re.I)
    s = re.sub(r"\s+.*$", "", s)
    return s.translate(CYR_TO_LAT).upper()


def slugify(sku: str) -> str:
    s = sku.translate(CYR_TO_LAT).lower()
    s = s.replace("..", "-").replace(".", "-")
    s = re.sub(r"[^a-z0-9-]", "", s.replace("_", "-"))
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "unknown"
