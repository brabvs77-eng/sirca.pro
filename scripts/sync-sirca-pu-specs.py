#!/usr/bin/env python3
"""Sync src/data/sirca-pu-specs.ts from TDS JSON and legacy .doc files."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import olefile

ROOT = Path(__file__).resolve().parents[1]
TDS_PATH = ROOT / "src/data/sirca-tds.json"
CORE_PATH = ROOT / "src/data/products-sirca.ts"
OUT_PATH = ROOT / "src/data/sirca-pu-specs.ts"
SIRCA_DIR = ROOT / "sources/sirca"
SPECS_DIR = ROOT / "sources/sirca/specs"

# Core PU SKUs without entry in sirca-tds.json → preferred .doc source
DOC_SOURCES: dict[str, list[str]] = {
    "OPU60G": ["OPU60G.doc"],
    "OPU379G": ["OPU379G.doc"],
    "OPU79": ["OPU79G.doc"],
    "OPU57": ["OPU57G.doc"],
    "OPU77": ["OPU77G.doc"],
    "OPU91": ["OPU91G.doc"],
    "OPU277": ["OPU277G.doc"],
    "LPU002": ["LPU002.doc"],
    "FPP26": ["FPP026.doc", "FPP026tix.doc"],
    "FPP20": ["FPP201.doc"],
    "FPP47": ["FPP201.doc"],
    "FPU15": ["FPU15s01.doc", "FPU158.doc"],
    "FL3100": ["FL3100s12.doc"],
    "OPP053-BLACK": ["OPP053G.doc", "OPP053tixG.doc"],
    "OPP053-WHITE": ["OPP053G.doc"],
}


def extract_text(path: Path) -> str:
    ole = olefile.OleFileIO(path)
    data = ole.openstream("WordDocument").read()
    ole.close()
    out: list[str] = []
    for i in range(0, len(data) - 1, 2):
        ch = data[i] | (data[i + 1] << 8)
        if 0x20 <= ch < 0x7f or 0x400 <= ch <= 0x4FF:
            out.append(chr(ch))
        elif out and out[-1] != " ":
            out.append(" ")
    return re.sub(r"\s+", " ", "".join(out)).strip()


def parse_consumption(text: str) -> dict[str, int]:
    info: dict[str, int] = {}
    m = re.search(r"Вес мокрого слоя,\s*г/м2?:\s*([0-9,\.\s\-–]+)", text, re.I)
    if m:
        nums = [float(x) for x in re.findall(r"[0-9]+(?:\.[0-9]+)?", m.group(1).replace(",", "."))]
        if nums:
            info["wetGsm"] = round(sum(nums) / len(nums))
    m = re.search(r"Количество слоёв:\s*([0-9,\.\s\-]+)", text, re.I)
    if m:
        nums = [int(x) for x in re.findall(r"\d+", m.group(1))]
        if nums:
            info["coats"] = max(nums)
    return info


def find_doc(name: str) -> Path | None:
    for base in (SPECS_DIR, SIRCA_DIR):
        path = base / name
        if path.exists():
            return path
    return None


def parse_doc(sku: str) -> dict[str, int] | None:
    for name in DOC_SOURCES.get(sku, []):
        path = find_doc(name)
        if not path:
            continue
        data = parse_consumption(extract_text(path))
        if data.get("wetGsm") and data.get("coats"):
            return data
    return None


def core_pu_skus() -> list[str]:
    text = CORE_PATH.read_text(encoding="utf-8").split("export const sircaProducts")[0]
    skus: list[str] = []
    for block in re.split(r"\n  \{", text):
        if "chemistry: 'pu'" not in block and "chemistry: 'acrylic'" not in block:
            continue
        m = re.search(r"sku: '([^']+)'", block)
        if m:
            skus.append(m.group(1))
    return skus


def main() -> None:
    tds_by_sku = {row["sku"]: row for row in json.loads(TDS_PATH.read_text(encoding="utf-8"))}
    specs: dict[str, dict[str, int]] = {}

    for sku in core_pu_skus():
        tds = tds_by_sku.get(sku)
        if tds and tds.get("wetGsm") and tds.get("coats"):
            continue  # enrichFromTds reads sirca-tds.json directly
        doc = parse_doc(sku)
        if doc:
            specs[sku] = doc
            continue
        if tds and tds.get("wetGsm") and tds.get("coats"):
            specs[sku] = {"wetGsm": tds["wetGsm"], "coats": tds["coats"]}

    lines = [
        "/** Расход и слои ПУ/акрилового блока — из TDS .doc (sources/sirca/). */",
        "",
        "export type PuSpecHint = { wetGsm: number; coats: number };",
        "",
        "export const sircaPuSpecs: Record<string, PuSpecHint> = {",
    ]
    for sku in sorted(specs):
        row = specs[sku]
        key = f"'{sku}'" if re.search(r"[^A-Z0-9]", sku) else sku
        lines.append(f"  {key}: {{ wetGsm: {row['wetGsm']}, coats: {row['coats']} }},")
    lines.append("};\n")

    OUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {len(specs)} PU spec hints → {OUT_PATH}")


if __name__ == "__main__":
    main()
