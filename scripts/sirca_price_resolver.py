#!/usr/bin/env python3
"""Resolve Sirca SKU prices from dealer list + core catalog tiers."""

from __future__ import annotations

import json
import re
import statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEALER_PATH = ROOT / "src/data/sirca-dealer-prices.json"
CORE_PATH = ROOT / "src/data/products-sirca.ts"

SUFFIXES = (
    "G30",
    "G20",
    "G10",
    "G5",
    "G35",
    "G25",
    "G",
    "TIXG",
    "TIX",
    "NC",
    "S15",
    "S16",
    "S12",
    "S08",
    "S04",
    "S01G30",
    "S01G5",
    "S01G",
    "S01",
    "CT",
    "RU",
    "BLACK",
    "WHITE",
)

FAMILY_OVERRIDES: dict[str, int] = {
    "ES": 2690,  # ES101 on woodperfect
    "UV": 2650,
    "ADTS": 0,
    "ADTW": 0,
    "CTE": 2150,
    "DPN": 1200,
    "FDE": 890,
    "FDL": 950,
    "FBU": 890,
    "GDV": 1100,
    "CT": 1400,
    "F912": 1970,
    "F915": 1970,
    "F921": 1970,
}


def norm(sku: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", sku.upper())


def variants(sku: str) -> list[str]:
    s = norm(sku)
    out = [s]
    for suf in SUFFIXES:
        if s.endswith(suf) and len(s) > len(suf) + 2:
            out.append(s[: -len(suf)])
    m = re.match(r"^([A-Z]+)(\d+)(.*)$", s)
    if m:
        p, n, rest = m.groups()
        out.extend(
            [
                f"{p}{n}{rest}",
                f"{p}{int(n):03d}{rest}",
                f"{p}{int(n):02d}{rest}",
                f"{p}{int(n):04d}{rest}",
            ]
        )
    dedup: list[str] = []
    for v in out:
        if v and v not in dedup:
            dedup.append(v)
    return dedup


def load_core_prices() -> dict[str, dict]:
    text = CORE_PATH.read_text(encoding="utf-8").split("export const sircaProducts")[0]
    out: dict[str, dict] = {}
    blocks = re.split(r"\n  \{", text)
    for block in blocks:
        sku_m = re.search(r"sku: '([^']+)'", block)
        unit_m = re.search(r"unit: '([^']+)'", block)
        pack_m = re.search(r"packs: \[pack\('[^']+', 1, (\d+)\)\]", block)
        if sku_m and pack_m:
            out[norm(sku_m.group(1))] = {
                "sku": sku_m.group(1),
                "price": int(pack_m.group(1)),
                "unit": unit_m.group(1) if unit_m else "л",
                "source": "core",
            }
    return out


def load_dealer_prices() -> dict[str, dict]:
    if not DEALER_PATH.exists():
        return {}
    out: dict[str, dict] = {}
    for row in json.loads(DEALER_PATH.read_text(encoding="utf-8")):
        out[norm(row["sku"])] = row
    return out


def family_medians(core: dict[str, dict]) -> dict[str, int]:
    buckets: dict[str, list[int]] = defaultdict(list)
    for row in core.values():
        m = re.match(r"^([A-Z]+)", norm(row["sku"]))
        if m:
            buckets[m.group(1)].append(row["price"])
    return {k: int(statistics.median(v)) for k, v in buckets.items() if v}


class PriceResolver:
    def __init__(self) -> None:
        self.core = load_core_prices()
        self.dealer = load_dealer_prices()
        self.families = family_medians(self.core)

    def lookup(self, sku: str) -> dict | None:
        for key in variants(sku):
            if key in self.dealer:
                return self.dealer[key]
            if key in self.core:
                return self.core[key]
        return None

    def resolve(self, sku: str, unit_hint: str = "л") -> tuple[int, str, bool]:
        hit = self.lookup(sku)
        if hit and hit.get("price", 0) > 0:
            return hit["price"], hit.get("unit", unit_hint), False

        s = norm(sku)
        prefix_m = re.match(r"^([A-Z]+)", s)
        prefix = prefix_m.group(1) if prefix_m else s[:3]

        for key in sorted(FAMILY_OVERRIDES, key=len, reverse=True):
            if s.startswith(key):
                price = FAMILY_OVERRIDES[key]
                if price == 0:
                    return 0, unit_hint, True
                return price, unit_hint, False

        if prefix in self.families:
            return self.families[prefix], unit_hint, False

        return 0, unit_hint, True
