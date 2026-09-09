#!/usr/bin/env python3
"""Per-SKU Sirca card images: PDF crops from the house-building catalog + synthetic fallbacks."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "sirca.pdf.pdf"
DEST = ROOT / "public" / "img" / "sirca"

# PDF page (1-based), crop x:y:width:height at 100 dpi (page ≈ 827 × 1170).
PDF_CROPS: dict[str, tuple[int, str]] = {
    "imw4800": (26, "0:0:550:520"),
    "imw4400": (26, "0:520:550:500"),
    "fiw350": (33, "0:0:827:580"),
    "fiw470": (33, "0:580:420:420"),
    "fwe600": (35, "275:370:275:300"),
    "fwe801": (37, "0:400:380:400"),
    "fwp630": (35, "0:370:280:300"),
    "fwp830": (37, "380:0:447:400"),
    "owe500": (36, "30:180:360:400"),
    "owe501": (36, "430:180:360:400"),
    "owe505": (49, "0:0:520:550"),
    "owp330": (37, "380:400:447:400"),
    "oil30": (38, "0:0:827:650"),
    "opu99g": (41, "0:0:720:750"),
    "opp1930g": (42, "0:0:480:380"),
    "fpu16tix": (42, "0:380:480:350"),
    "opa9330": (43, "0:0:420:1170"),
    "opu979": (44, "0:0:520:420"),
    "fpu932e": (44, "0:420:520:420"),
    "fa930": (35, "560:370:267:300"),
    "ow1fg40": (45, "0:120:400:380"),
    "opu60g": (46, "0:0:550:450"),
    "opu379g": (45, "400:120:400:350"),
    "opu79": (39, "0:0:827:500"),
    "lpu002": (47, "0:0:827:550"),
    "opu57": (40, "100:150:627:500"),
    "opu77": (31, "100:150:627:500"),
    "opu91": (32, "100:150:627:500"),
    "opu277": (45, "0:500:350:350"),
    "fpp26": (45, "350:500:370:350"),
    "fpp20": (29, "450:350:377:450"),
    "fpp47": (30, "0:0:827:500"),
    "fpu15": (46, "0:450:550:400"),
    "opp053-black": (32, "550:650:250:200"),
    "opp053-white": (32, "50:200:250:200"),
    "fl3100": (47, "0:550:827:400"),
}

# Synthetic cards for products absent from the exterior catalog (hardeners, etc.).
GENERATED: dict[str, dict[str, str]] = {
    "th52": {
        "bg": "#1e3a5f",
        "accent": "#4a90c4",
        "label": "TH52",
        "subtitle": "Отвердитель 0,5 л",
    },
    "th43": {
        "bg": "#2d4a3e",
        "accent": "#6b9e78",
        "label": "TH43",
        "subtitle": "Отвердитель ПУ",
    },
}


def run(command: list[str], quiet: bool = True) -> None:
    subprocess.run(
        command,
        check=True,
        stdout=subprocess.DEVNULL if quiet else None,
        stderr=subprocess.DEVNULL if quiet else None,
    )


def extract_pdf(slug: str, page: int, crop: str, dest: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="sirca-page-") as folder:
        temp = Path(folder)
        prefix = temp / slug
        run(
            [
                "pdftoppm",
                "-f",
                str(page),
                "-l",
                str(page),
                "-jpeg",
                "-r",
                "100",
                str(PDF),
                str(prefix),
            ]
        )
        source = next(temp.glob(f"{slug}-*.jpg"))
        x, y, width, height = crop.split(":")
        run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(source),
                "-vf",
                f"crop={width}:{height}:{x}:{y},scale=720:540",
                "-c:v",
                "libwebp",
                "-quality",
                "76",
                str(dest),
            ]
        )


def generate_card(slug: str, cfg: dict[str, str], dest: Path) -> None:
    bg = cfg["bg"].lstrip("#")
    accent = cfg["accent"].lstrip("#")
    label = cfg["label"]
    subtitle = cfg["subtitle"].replace("\\", "\\\\").replace(":", "\\:").replace(",", "\\,")
    vf = (
        f"drawbox=x=40:y=40:w=640:h=460:color=0x{accent}@0.35:t=fill,"
        f"drawbox=x=40:y=40:w=640:h=460:color=white@0.15:t=3,"
        f"drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
        f"text=Sirca:fontsize=28:fontcolor=white@0.7:x=60:y=70,"
        f"drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
        f"text={label}:fontsize=52:fontcolor=white:x=60:y=200,"
        f"drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:"
        f"text={subtitle}:fontsize=24:fontcolor=white@0.85:x=60:y=270,"
        f"drawbox=x=60:y=340:w=200:h=8:color=0x{accent}:t=fill"
    )
    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"color=c=0x{bg}:s=720x540,{vf}",
            "-frames:v",
            "1",
            "-c:v",
            "libwebp",
            "-quality",
            "80",
            str(dest),
        ]
    )


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)

    # Remove legacy group images.
    for legacy in DEST.glob("*.webp"):
        if legacy.stem not in PDF_CROPS and legacy.stem not in GENERATED:
            legacy.unlink()

    for slug, (page, crop) in PDF_CROPS.items():
        extract_pdf(slug, page, crop, DEST / f"{slug}.webp")

    for slug, cfg in GENERATED.items():
        generate_card(slug, cfg, DEST / f"{slug}.webp")

    created = sorted(p.stem for p in DEST.glob("*.webp"))
    print(f"created {len(created)} unique Sirca card images in {DEST}")
    if len(created) != len(set(created)):
        raise SystemExit("duplicate image filenames detected")


if __name__ == "__main__":
    main()
