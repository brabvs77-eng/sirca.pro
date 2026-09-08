#!/usr/bin/env python3
"""Compress repo media into public/img and public/video for the catalog."""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path("/workspace")
PUB = ROOT / "public"


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def webp(src: Path, dest: Path, width: int, quality: int = 72) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 1000:
        return
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(src),
            "-vf",
            f"scale={width}:-1",
            "-c:v",
            "libwebp",
            "-quality",
            str(quality),
            str(dest),
        ]
    )


def poster(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        return
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(src),
            "-vframes",
            "1",
            "-vf",
            "scale=720:-1",
            "-c:v",
            "libwebp",
            "-quality",
            "70",
            str(dest),
        ]
    )


def compress_mp4(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 20000:
        return
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(src),
            "-vf",
            "scale=540:-2",
            "-c:v",
            "libx264",
            "-crf",
            "32",
            "-preset",
            "veryfast",
            "-an",
            "-movflags",
            "+faststart",
            str(dest),
        ]
    )


def first_match(patterns: list[str]) -> Path | None:
    for p in ROOT.iterdir():
        name = p.name
        for pat in patterns:
            if name == pat:
                return p
    return None


PACKS = {
    "110": ["110.png"],
    "120": ["120.png"],
    "140": ["140.png"],
    "170": ["170.png"],
    "227": ["227_075.png", "227_0375.png"],
    "245": ["245_075.png"],
    "255": ["255_075.png"],
    "266": ["266_075.png"],
    "271": ["271_075.png"],
    "277": ["277_075.png"],
    "280": ["280_075.png"],
    "285": ["285_075.png"],
    "290": ["290_твердый воск.jpg", "1_290.png"],
    "425": ["425_075.png"],
    "460": ["460_075.png"],
    "461": ["461_075.png"],
    "475": ["475_075.png"],
    "476": ["476_075.png"],
    "860": ["860_075.png"],
    "870": ["870_075.png"],
    "875": ["875_075.png"],
}

LIFE = {
    "280": ["280_масло для фасада.jpg"],
    "245": ["245_твердое масло.jpg"],
    "277": ["277_для террас.jpg", "277_масло для террас.jpg"],
    "425": ["425_лазурь.jpg"],
    "460": ["460_461_краска.jpg"],
    "285": ["285_металлик.jpg"],
    "227": ["227_для столешниц.jpg"],
    "255": ["255_масло с тв_воском.jpg"],
    "266": ["266_масло для пола.jpg"],
}

COLORS_INT = [
    ("01", "01 Арктический лед.png"),
    ("02", "02 Китайский фарфор.png"),
    ("03", "03 Бельгийские сливки.png"),
    ("04", "04 Вьетнамский лотос.png"),
    ("05", "05 Турецкая халва.png"),
    ("06", "06 Итальянский латте.png"),
    ("07", "07 Эфиопский кофе.png"),
    ("08", "08 Швейцарский шоколад.png"),
    ("09", "09 Французское крем-брюле.png"),
    ("10", "10 Тибетское плато.png"),
    ("11", "11 Австрийские Альпы.png"),
    ("12", "12 Шотландский вереск.png"),
    ("13", "13 Туманный Альбион.png"),
    ("14", "14 Сибирская тайга.png"),
    ("15", "15 Калифорнийский залив.png"),
    ("16", "16 Маркканская глина.png"),
    ("17", "17 Индийский чай.png"),
    ("18", "18 Мексиканский кактус.png"),
    ("19", "19 Новозеландский мох.png"),
    ("20", "20 Ливанский кедр.png"),
]

COLORS_COSMO = [
    ("01", "1_Космический рассвет.jpg"),
    ("10", "10_Серебро сатурна.jpg"),
    ("11", "11_Астероидный серый.jpg"),
    ("12", "12_Марсианский закат.jpg"),
    ("13", "13_Звездный свет.jpg"),
    ("14", "14_Эхо вселенной.jpg"),
    ("15", "15_Открытый космос.jpg"),
    ("16", "16_Млечный путь.jpg"),
]


def main() -> None:
    for sku, names in PACKS.items():
        src = first_match(names)
        if src:
            webp(src, PUB / "img/products" / f"{sku}.webp", 720)

    extra_packs = [
        ("227", "0375", "227_0375.png"),
        ("245", "0375", "245_0375.png"),
        ("245", "2-5", "245_2,5.png"),
        ("245", "10", "245_10.png"),
        ("255", "0375", "255_0375.png"),
        ("255", "2-5", "255_2,5.png"),
        ("266", "0375", "266_0375.png"),
        ("266", "2-5", "266_2,5.png"),
        ("271", "2-5", "271_2,5.png"),
        ("277", "0375", "277_0375.png"),
        ("277", "2-5", "277_2,5.png"),
        ("277", "10", "277_10.png"),
        ("280", "0375", "280_0375.png"),
        ("280", "2-5", "280_2,5.png"),
        ("280", "10", "280_10.png"),
        ("285", "0375", "285_0375.png"),
        ("285", "2-5", "285_2,5.png"),
        ("285", "10", "285_10.png"),
        ("425", "0375", "425_0375.png"),
        ("425", "2-5", "425_2,5.png"),
        ("425", "10", "425_10.png"),
        ("460", "0375", "460_0375.png"),
        ("460", "2-5", "460_2,5.png"),
        ("460", "10", "460_10.png"),
        ("461", "0375", "461_0375.png"),
        ("461", "2-5", "461_2,5.png"),
        ("475", "0375", "475_0375.png"),
        ("475", "2-5", "475_2,5.png"),
        ("475", "10", "475_10.png"),
        ("476", "0375", "476_0375.png"),
        ("476", "2-5", "476_2,5.png"),
        ("476", "10", "476_10.png"),
        ("860", "2-5", "860_2,5.png"),
        ("870", "2-5", "870_2,5.png"),
        ("870", "10", "870_10.png"),
        ("875", "2-5", "875_2,5.png"),
        ("875", "10", "875_10.png"),
    ]
    for sku, pack, name in extra_packs:
        src = first_match([name])
        if src:
            webp(src, PUB / "img/packs" / f"{sku}_{pack}.webp", 560, 70)

    for sku, names in LIFE.items():
        src = first_match(names)
        if src:
            webp(src, PUB / "img/life" / f"{sku}.webp", 1200, 74)

    for num, name in COLORS_INT:
        src = first_match([name])
        if src:
            webp(src, PUB / "img/colors" / f"vc-{num}.webp", 640, 72)

    for num, name in COLORS_COSMO:
        src = first_match([name])
        if src:
            webp(src, PUB / "img/colors" / f"pk-{num}.webp", 640, 72)

    logo = first_match(["Лого Gnature зеленый.png", "Gnature (1).png"])
    if logo:
        webp(logo, PUB / "img/logo-gn.webp", 320, 80)

    for w, names in {
        "50": ["Кисть_спираль_50.png", "Кисть_1_0_спиралевид_50мм.jpg"],
        "70": ["GN_Кисть_70.png", "Кисть_спираль_70.png"],
        "100": ["GN_Кисть_100.png", "Кисть_спираль_100.png"],
    }.items():
        src = first_match(names)
        if src:
            webp(src, PUB / "img/tools" / f"kist-{w}.webp", 640, 72)

    videos = []
    for p in ROOT.iterdir():
        if p.suffix.lower() == ".mp4":
            videos.append(p)

    key = {"110", "120", "140", "170", "227", "245", "255", "266", "271", "277", "280", "285", "425", "460", "461", "860", "870", "875"}
    for p in videos:
        stem = p.stem
        if stem in key:
            poster(p, PUB / "img/posters" / f"{stem}.webp")
            compress_mp4(p, PUB / "video" / f"{stem}.mp4")

    brand = {
        "gnature": ["О GNATURE .mp4", "О GNATURE.mp4"],
        "fasad": ["Фасад.mp4", "Фасад 1.mp4"],
        "terrassa": ["Терраса.mp4", "Терраса 1.mp4"],
    }
    for slug, names in brand.items():
        src = first_match(names)
        if not src:
            for p in videos:
                if any(n.replace(".mp4", "") in p.name for n in names):
                    src = p
                    break
        if src:
            poster(src, PUB / "img/posters" / f"{slug}.webp")
            compress_mp4(src, PUB / "video" / f"{slug}.mp4")

    print("done")
    for folder in ["img/products", "img/colors", "img/posters", "video", "img/tools"]:
        paths = list((PUB / folder).glob("*")) if (PUB / folder).exists() else []
        print(folder, len(paths))


if __name__ == "__main__":
    main()
