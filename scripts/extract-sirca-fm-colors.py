#!/usr/bin/env python3
"""Extract Ferro Micacei color formulas from Cartella colori FM.XLSX."""

from __future__ import annotations

import json
import re
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[1]
XLSX = ROOT / "sources/sirca/specs/Cartella colori FM.XLSX"
OUT = ROOT / "src/data/sirca-fm-colors.ts"

SYSTEMS = [
    ("grossa", 1, 2, "F4FMGG / F6FMGG — крупная фракция"),
    ("fine", 6, 7, "F404FM / F406FM — мелкая фракция"),
    ("acr", 11, 12, "F7FMGG — акрил 1k"),
]


def parse_sheet() -> list[dict]:
    wb = openpyxl.load_workbook(XLSX, read_only=True, data_only=True)
    rows = list(wb["Foglio1"].iter_rows(values_only=True))
    colors: dict[str, dict] = {}

    for row in rows:
        for key, name_col, code_col, label in SYSTEMS:
            if name_col >= len(row):
                continue
            name = row[name_col]
            if not name or not isinstance(name, str):
                continue
            name = name.strip()
            if not name or name.lower().startswith("formule") or "grana" in name.lower():
                continue

            base_code = str(row[code_col]).strip() if code_col < len(row) and row[code_col] else ""
            pct = row[code_col + 1] if code_col + 1 < len(row) else None
            tint_code = ""
            tint_pct = None
            if code_col + 2 < len(row) and isinstance(row[code_col + 2], str) and re.match(r"^F", str(row[code_col + 2])):
                tint_code = str(row[code_col + 2]).strip()
                tint_pct = row[code_col + 3] if code_col + 3 < len(row) else None

            entry = colors.setdefault(name, {"name": name, "systems": {}})
            parts = [f"{base_code} {pct}%"] if base_code and pct is not None else []
            if tint_code and tint_pct is not None:
                parts.append(f"{tint_code} {tint_pct}%")
            formula = " + ".join(parts) if parts else base_code
            entry["systems"][key] = {"label": label, "formula": formula}

    return [colors[k] for k in sorted(colors)]


def to_ts(colors: list[dict]) -> str:
    payload = json.dumps(colors, ensure_ascii=False, indent=2)
    return f"""/** Ferro Micacei — из sources/sirca/specs/Cartella colori FM.XLSX */

export type FmColorSystem = {{
  label: string;
  formula: string;
}};

export type FmColor = {{
  name: string;
  systems: Record<'grossa' | 'fine' | 'acr', FmColorSystem>;
}};

export const sircaFmColors: FmColor[] = {payload} as FmColor[];
"""


def main() -> None:
    colors = parse_sheet()
    OUT.write_text(to_ts(colors), encoding="utf-8")
    print(f"Wrote {len(colors)} FM colors → {OUT}")


if __name__ == "__main__":
    main()
