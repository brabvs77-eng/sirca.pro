#!/usr/bin/env python3
"""Generate src/data/products-sirca-tds.ts from TDS JSON for SKUs not in core catalog."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from normalize_sirca_sku import slugify
from sirca_price_resolver import PriceResolver
TDS_PATH = ROOT / "src/data/sirca-tds.json"
CATALOG_PATH = ROOT / "src/data/products-sirca.ts"
OUT_PATH = ROOT / "src/data/products-sirca-tds.ts"

SRC = "прайс дилера, сентябрь 2026"
SKIP = {"OWE500G"}  # alias of OWE500 on site


def classify(sku: str, use: str, chem: str) -> tuple[str, str, list[str], int, str]:
    u = (use or "").lower()
    c = (chem or "").lower()
    p = re.match(r"^([A-Z0-9]+)", sku.upper())
    prefix = p.group(1) if p else sku.upper()

    if re.match(r"^(ADTS|ADTW)", sku.upper()):
        return "furniture", "pu", ["mebel"], 0, "кг"
    if re.match(r"^(TH|CT|F912|F915|F921|CTE|DPN)", sku.upper()) or "отвердител" in u:
        return "furniture", "pu", ["mebel"], 0, "кг"
    if re.match(r"^(FDE|FDL|FBU|GDV)", sku.upper()) or "растворител" in u or "разбавител" in u:
        return "furniture", "pu", ["mebel"], 890, "л"
    if sku.upper().startswith("ES") or "эпоксид" in c:
        return "furniture", "pu", ["mebel", "okna-dveri"], 2400, "кг"
    if sku.upper().startswith("UV"):
        return "furniture", "pu", ["mebel"], 2800, "кг"
    if re.match(r"^(CR|ADTS)", sku.upper()) or "конвертер" in u or "колеровочн" in u:
        return "furniture", "water", ["mebel"], 1900, "л"
    if re.match(r"^(OPU|OPP|FPP|FPU|FL|LPU)", sku.upper()) and "экстерьер" not in u:
        if "паркет" in u or "пол" in u:
            return "parquet", "pu", ["parket", "pol"], 2550, "л"
        return "furniture", "pu", ["mebel"], 2200, "кг"
    if re.match(r"^(OPA|FA|FPU93)", sku.upper()) or "акрил" in c:
        return "windows", "acrylic", ["okna-dveri"], 2100, "кг"
    if "паркет" in u or "пол" in u or "настил" in u or prefix.startswith("FWPI") or prefix == "OWB":
        return "parquet", "water", ["parket", "pol"], 2550, "л"
    if "мебел" in u or prefix.startswith("OWPI") or prefix.startswith("SO"):
        return "furniture", "water", ["mebel"], 2350, "л"
    if "окон" in u or "двер" in u or prefix.startswith("OWP") or prefix.startswith("SIW"):
        return "windows", "water", ["okna-dveri"], 2000, "л"
    if prefix.startswith("IMW") or prefix.startswith("IWJ") or "пропит" in u:
        return "exterior", "water", ["fasad", "okna-dveri"], 1500, "л"
    if prefix.startswith("IWC") or "лазур" in u or "воск" in u:
        return "oils", "water", ["terrassa", "fasad"], 1650, "л"
    if prefix.startswith("FIW") or prefix.startswith("FWBP") or "грунт" in u:
        return "exterior", "water", ["fasad", "okna-dveri"], 1400, "л"
    if prefix.startswith("FWE") or "эмаль" in u:
        return "exterior", "water", ["fasad"], 1850, "л"
    if prefix.startswith("FWP") or prefix.startswith("OWE") or prefix.startswith("WOP"):
        return "exterior", "water", ["fasad", "okna-dveri"], 2100, "л"
    if prefix.startswith("OW"):
        return "parquet", "water", ["parket", "pol"], 2450, "л"
    if prefix.startswith("F4") or prefix.startswith("F3") or prefix.startswith("FO"):
        return "furniture", "pu", ["mebel"], 2100, "кг"
    return "exterior", "water", ["fasad"], 1800, "л"


def product_name(sku: str, use: str) -> str:
    u = (use or "").lower()
    if "отвердител" in u:
        return f"{sku} — отвердитель"
    if "растворител" in u or "разбавител" in u:
        return f"{sku} — растворитель"
    if "грунт" in u:
        return f"{sku} — грунт"
    if "лак" in u or "финиш" in u:
        return f"{sku} — лак"
    if "эмаль" in u:
        return f"{sku} — эмаль"
    if "пропит" in u:
        return f"{sku} — пропитка"
    if sku.upper().startswith("ES"):
        return f"{sku} — эпоксидная система"
    if sku.upper().startswith("UV"):
        return f"{sku} — УФ-лак"
    return f"{sku} — Sirca"


def short_name(use: str) -> str:
    u = (use or "")[:90].strip()
    if "Способ" in u:
        u = u.split("Способ")[0].strip()
    return u or "Позиция из каталога Sirca"


def features_from(sku: str, use: str, row: dict) -> list[str]:
    feats: list[str] = []
    u = (use or "").lower()
    if row.get("parseError"):
        feats.append("TDS уточняется")
    else:
        feats.append("TDS Sirca")
    if row.get("gloss"):
        g = row["gloss"].split("Назначение")[0].strip()[:18]
        if g:
            feats.append(f"Блеск {g}")
    if "паркет" in u:
        feats.append("Паркет")
    elif "мебел" in u:
        feats.append("Мебель")
    elif "окон" in u or "двер" in u:
        feats.append("Окна и двери")
    elif "экстерьер" in u or "фасад" in u:
        feats.append("Экстерьер")
    if row.get("wetGsm"):
        feats.append(f"~{row['wetGsm']} г/м²")
    return feats[:4]


def esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace("'", "\\'")


def main() -> None:
    core_part = CATALOG_PATH.read_text(encoding="utf-8").split("export const sircaProducts")[0]
    existing = {m.group(1).upper() for m in re.finditer(r"sku: '([^']+)'", core_part)}
    tds_list = json.loads(TDS_PATH.read_text(encoding="utf-8"))

    lines = [
        "import { belowMarket, type Pack } from './pricing';",
        "import type { SircaProduct } from './products-sirca';",
        "",
        f"const SRC = '{SRC}';",
        "",
        "function pack(unit: 'л' | 'кг', liters: number, market: number): (Pack & { source: string; unit: 'л' | 'кг' }) {",
        "  return {",
        "    volume: `1 ${unit}`,",
        "    liters,",
        "    marketPrice: market,",
        "    price: belowMarket(market),",
        "    source: SRC,",
        "    unit,",
        "  };",
        "}",
        "",
        "/** Auto-generated from TDS — scripts/generate-sirca-tds-products.py */",
        "export const sircaTdsProducts: SircaProduct[] = [",
    ]

    resolver = PriceResolver()
    added = 0
    priced = 0
    for row in sorted(tds_list, key=lambda r: r["sku"]):
        sku = row["sku"]
        if sku.upper() in existing or sku.upper() in SKIP:
            continue
        use_text = row.get("use", "")
        chem = row.get("chem", "")
        use, chemistry, tasks, fallback_price, unit = classify(sku, use_text, chem)
        price, unit, price_on_request = resolver.resolve(sku, unit)
        if price_on_request and fallback_price > 0:
            price = fallback_price
            price_on_request = False
        if price > 0:
            priced += 1
        slug = slugify(sku)
        desc = row.get("description", "")[:280] or f"{sku} — материал Sirca. Подбор цикла по TDS."
        short = short_name(use_text)
        name = product_name(sku, use_text)

        extra = ""
        if row.get("wetGsm"):
            extra += f"\n    wetGsm: {row['wetGsm']},"
        if row.get("coats"):
            extra += f"\n    coats: {row['coats']},"
        if price_on_request:
            extra += "\n    priceOnRequest: true,"

        task_str = ", ".join(f"'{t}'" for t in tasks)
        feat_str = ", ".join(f"'{esc(f)}'" for f in features_from(sku, use_text, row))
        pack_line = (
            "packs: [],"
            if price_on_request
            else f"packs: [pack('{unit}', 1, {price})],"
        )

        lines.append(f"""  {{
    sku: '{esc(sku)}',
    slug: '{slug}',
    brand: 'sirca',
    name: '{esc(name)}',
    short: '{esc(short)}.',
    description: '{esc(desc)}',
    tasks: [{task_str}],
    use: '{use}',
    chemistry: '{chemistry}',
    unit: '{unit}',
    {pack_line}
    features: [{feat_str}],{extra}
  }},""")
        added += 1

    lines.append("];\n")
    OUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {added} products ({priced} with dealer/core price) to {OUT_PATH}")


if __name__ == "__main__":
    main()
