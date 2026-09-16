#!/usr/bin/env python3
"""Scrape public dealer prices from woodperfect.ru Sirca vendor page."""

from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "src/data/sirca-dealer-prices.json"
URL = "https://woodperfect.ru/im/vendor/sirca-italiya"
UA = {"User-Agent": "Mozilla/5.0"}


def sku_tokens(title: str) -> list[str]:
    t = title.upper().replace("ТН", "TH").replace("ТH", "TH")
    found = re.findall(r"\b([A-Z]{1,4}\s*\d+[A-Z0-9]*)\b", t)
    out: list[str] = []
    for raw in found:
        sku = re.sub(r"\s+", "", raw)
        if sku not in out:
            out.append(sku)
    return out


def main() -> None:
    html = urllib.request.urlopen(urllib.request.Request(URL, headers=UA), timeout=30).read().decode(
        "utf-8", "ignore"
    )
    names = re.findall(r'value="([^"]+)" name="product_name"', html)
    prices_raw = re.findall(r'price-current">\s*<strong>([^<]+)</strong>', html)

    by_sku: dict[str, dict] = {}
    for title, price_s in zip(names, prices_raw):
        price = int(round(float(re.sub(r"[^\d.]", "", price_s.replace("\xa0", "")))))
        unit = "кг" if "(кг)" in price_s or "(1 кг)" in title.lower() else "л"
        tokens = sku_tokens(title)
        if not tokens and title.upper().startswith("PH"):
            tokens = ["PH"]
        for sku in tokens:
            rec = {
                "sku": sku,
                "price": price,
                "unit": unit,
                "title": title,
                "source": "woodperfect.ru",
            }
            prev = by_sku.get(sku)
            if not prev or price < prev["price"]:
                by_sku[sku] = rec

    # Aliases seen on dealer cards
    aliases = {
        "MW4800": "IMW4800",
        "OP1930": "OPP1930G",
        "WP2130": "OWPI2130G",
        "WP130": "OWPI130G",
    }
    for src, dst in aliases.items():
        if src in by_sku and dst not in by_sku:
            by_sku[dst] = {**by_sku[src], "sku": dst, "aliasOf": src}

    catalog = sorted(by_sku.values(), key=lambda r: r["sku"])
    OUT.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(catalog)} dealer prices → {OUT}")


if __name__ == "__main__":
    main()
