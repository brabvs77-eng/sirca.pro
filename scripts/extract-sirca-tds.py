#!/usr/bin/env python3
"""Extract metadata and markdown from Sirca TDS .doc files in sources/sirca/specs/."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import olefile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from normalize_sirca_sku import normalize_sku_from_stem, slugify
SPECS = ROOT / "sources/sirca/specs"
DOCS = ROOT / "docs/sirca"
OUT_JSON = ROOT / "src/data/sirca-tds.json"


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


def parse_tds(text: str, sku: str, source_file: str) -> dict:
    info: dict = {"sku": sku, "file": source_file}

    m = re.search(r"Назначение:\s*([^\.]{15,160})", text, re.I)
    if m:
        info["use"] = re.sub(r"\s+", " ", m.group(1)).strip()

    m = re.search(r"Химический тип:\s*([^\.]{10,80})", text, re.I)
    if m:
        info["chem"] = m.group(1).strip()

    m = re.search(r"Степень блеска[^:]*:\s*([^\n]{3,30})", text, re.I)
    if m:
        info["gloss"] = m.group(1).strip()

    m = re.search(r"Сухой остаток[^:]*:\s*([0-9,\.]+)\s*[±+]", text, re.I)
    if m:
        info["solids"] = m.group(1).replace(",", ".")

    m = re.search(r"Вес мокрого слоя,\s*г/м2?:\s*([0-9,\.\s\-–]+)", text, re.I)
    if m:
        raw = m.group(1).replace(",", ".")
        nums = [float(x) for x in re.findall(r"[0-9]+(?:\.[0-9]+)?", raw)]
        if nums:
            info["wetGsm"] = round(sum(nums) / len(nums))

    m = re.search(r"Количество слоёв:\s*([0-9,\.\s\-]+)", text, re.I)
    if m:
        nums = [int(x) for x in re.findall(r"\d+", m.group(1))]
        if nums:
            info["coats"] = max(nums)

    m = re.search(r"Описание:\s*(.{80,600}?)(?:\s+Перед|\s+Не |\s+Очистка|\s+Хранить|$)", text, re.I)
    if m:
        info["description"] = m.group(1).strip()

    if len(text) < 100:
        info["parseError"] = "empty or unreadable"

    return info


def to_markdown(info: dict) -> str:
    sku = info["sku"]
    src = info.get("file", f"{sku}.doc")
    lines = [
        f"# {sku} — техническая спецификация Sirca",
        "",
        f"> Источник: `sources/sirca/specs/{src}`",
        "",
    ]
    if info.get("chem"):
        lines += [f"**Химический тип:** {info['chem']}", ""]
    if info.get("use"):
        lines += [f"**Назначение:** {info['use']}", ""]
    if info.get("gloss"):
        lines += [f"**Блеск:** {info['gloss']}", ""]
    if info.get("solids"):
        lines += [f"**Сухой остаток:** {info['solids']}%", ""]
    if info.get("wetGsm"):
        lines += [f"**Вес мокрого слоя:** ~{info['wetGsm']} г/м²", ""]
    if info.get("coats"):
        lines += [f"**Слоёв:** {info['coats']}", ""]
    if info.get("description"):
        lines += ["## Описание", "", info["description"], ""]
    return "\n".join(lines)


def main() -> int:
    DOCS.mkdir(parents=True, exist_ok=True)
    by_sku: dict[str, dict] = {}

    for path in sorted(SPECS.glob("*.doc")):
        sku = normalize_sku_from_stem(path.stem)
        text = extract_text(path)
        info = parse_tds(text, sku, path.name)
        prev = by_sku.get(sku)
        if not prev or len(text) > prev.get("_textLen", 0):
            info["_textLen"] = len(text)
            by_sku[sku] = info

    catalog = []
    for sku in sorted(by_sku):
        info = by_sku[sku]
        info.pop("_textLen", None)
        catalog.append(info)
        (DOCS / f"{slugify(sku)}.md").write_text(to_markdown(info), encoding="utf-8")

    OUT_JSON.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Parsed {len(catalog)} unique TDS → {DOCS} and {OUT_JSON}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
