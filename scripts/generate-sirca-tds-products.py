#!/usr/bin/env python3
"""Generate src/data/products-sirca-tds.ts from TDS JSON for SKUs not yet in catalog."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TDS_PATH = ROOT / "src/data/sirca-tds.json"
CATALOG_PATH = ROOT / "src/data/products-sirca.ts"
OUT_PATH = ROOT / "src/data/products-sirca-tds.ts"

SRC = "прайс дилера, сентябрь 2026"

# slug -> skip (already on site under different sku)
SKIP = {"OWE500G"}  # covered by OWE500


def slugify(sku: str) -> str:
    s = sku.lower().replace("..", "").replace(".", "-")
    s = re.sub(r"[^a-z0-9-]", "", s.replace("_", "-"))
    s = re.sub(r"-+", "-", s).strip("-")
    return s


def classify(sku: str, use: str) -> tuple[str, str, list[str], int]:
    u = use.lower()
    prefix = re.match(r"^([A-Z]+)", sku.upper())
    p = prefix.group(1) if prefix else ""

    if p == "CRW" or ("интерьер" in u and "паркет" not in u):
        return "furniture", "water", ["mebel"], 1900
    if "паркет" in u or "пол" in u or "настил" in u or p in ("FWPI", "OWB"):
        tasks = ["parket", "pol"] if "спорт" not in u else ["parket", "pol"]
        return "parquet", "water", tasks, 2550
    if "мебел" in u or ("фасад" in u and "панел" in u) or p == "OWPI":
        return "furniture", "water", ["mebel"], 2350
    if "окон" in u or "двер" in u or "ставен" in u or p in ("OWP", "SIW"):
        return "windows", "water", ["okna-dveri"], 2000
    if "стул" in u or "mdf" in u or p.startswith("FW") and p not in ("FWP", "FWE", "FIW", "FWPI"):
        return "furniture", "water", ["mebel"], 2100
    if p in ("FIW", "FWE", "FWP", "FWBP"):
        return "exterior", "water", ["fasad", "okna-dveri"], 1450
    if p.startswith("OWE") or p == "WOP":
        return "exterior", "water", ["fasad", "okna-dveri"], 2100
    if p.startswith("OW"):
        return "parquet", "water", ["parket", "pol"], 2450
    return "exterior", "water", ["fasad"], 1800


def short_name(sku: str, use: str) -> str:
    u = use[:80].strip()
    if u.endswith("Способ"):
        u = u.split("Способ")[0].strip()
    return u or f"Позиция {sku} из каталога домостроения"


def features_from(sku: str, use: str, row: dict) -> list[str]:
    feats = ["Водоразбавимая"]
    u = use.lower()
    if row.get("gloss"):
        g = row["gloss"].split("Назначение")[0].strip()[:20]
        if g:
            feats.append(f"Блеск {g}")
    if "паркет" in u:
        feats.append("Паркет")
    elif "мебел" in u:
        feats.append("Мебель")
    elif "окон" in u or "двер" in u:
        feats.append("Окна и двери")
    elif "фасад" in u or "экстерьер" in u:
        feats.append("Экстерьер")
    elif "спорт" in u:
        feats.append("Спортивные полы")
    if "mdf" in u:
        feats.append("MDF")
    if row.get("wetGsm"):
        feats.append(f"~{row['wetGsm']} г/м²")
    return feats[:4]


def main() -> None:
    catalog_text = CATALOG_PATH.read_text(encoding="utf-8")
    core_part = catalog_text.split("export const sircaProducts")[0]
    existing = {m.group(1).upper() for m in re.finditer(r"sku: '([^']+)'", core_part)}
    tds_list = json.loads(TDS_PATH.read_text(encoding="utf-8"))
    tds = {row["sku"]: row for row in tds_list}

    lines = [
        "import { belowMarket, type Pack } from './pricing';",
        "import type { SircaProduct } from './products-sirca';",
        "",
        f"const SRC = '{SRC}';",
        "",
        "function pack(unit: 'л' | 'кг', liters: number, market: number): Pack & { source: string; unit: 'л' | 'кг' } {",
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

    added = 0
    for sku in sorted(tds):
        if sku.upper() in existing or sku in SKIP:
            continue
        row = tds[sku]
        use_text = row.get("use", "")
        use, chem, tasks, price = classify(sku, use_text)
        slug = slugify(sku)
        desc = row.get("description", "")[:280] or f"{sku} — водоразбавимый материал Sirca. Подбор цикла по TDS."
        desc = desc.replace("'", "\\'")
        short = short_name(sku, use_text).replace("'", "\\'")
        name = f"{sku} — водный материал Sirca"
        if "грунт" in use_text.lower():
            name = f"{sku} — водный грунт"
        elif "лак" in use_text.lower() or "финиш" in use_text.lower():
            name = f"{sku} — водный лак"
        elif "эмаль" in use_text.lower():
            name = f"{sku} — водная эмаль"
        elif "пропит" in use_text.lower():
            name = f"{sku} — водная пропитка"
        elif "гермет" in use_text.lower():
            name = f"{sku} — герметик"

        extra = ""
        if row.get("wetGsm"):
            extra += f"\n    wetGsm: {row['wetGsm']},"
        if row.get("coats"):
            extra += f"\n    coats: {row['coats']},"

        task_str = ", ".join(f"'{t}'" for t in tasks)
        feat_str = ", ".join(f"'{f}'" for f in features_from(sku, use_text, row))
        lines.append(f"""  {{
    sku: '{sku}',
    slug: '{slug}',
    brand: 'sirca',
    name: '{name}',
    short: '{short}.',
    description: '{desc}',
    tasks: [{task_str}],
    use: '{use}',
    chemistry: '{chem}',
    unit: 'л',
    packs: [pack('л', 1, {price})],
    features: [{feat_str}],{extra}
  }},""")
        added += 1

    lines.append("];\n")
    OUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {added} products to {OUT_PATH}")


if __name__ == "__main__":
    main()
