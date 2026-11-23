#!/usr/bin/env python3
"""Draw the news-image-20261123 front page (1024x1024, Pillow).

A newspaper front page summing up Monday 23 November 2026: Ukraine sinks
the Russian corvette Merkury off Libya, NATO warns of a Russian
nuclear-armed satellite, Mexico captures 'El Chapo Isidro', COP31's
aftermath, the AI market sell-off, and the day's other big stories.

Run:  python3 draw.py   (writes assets/entry.png)
Deterministic: fixed layout, fixed text, no randomness, no network.
Only Pillow is needed, and only at build time.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "entry.png")

W, H = 1024, 1024
MARGIN = 36
COL_W = W - 2 * MARGIN  # 952

INK = (18, 18, 18)
RED = (178, 34, 34)
BLUE = (24, 68, 120)
SEA = (38, 92, 140)
SKY = (214, 228, 238)
PAPER = (255, 255, 255)
GREY = (110, 110, 110)
LIGHT = (238, 238, 238)

FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def font(name, size):
    """Best-effort font lookup; falls back to PIL's built-in font."""
    want = {
        "serif-bold": "DejaVuSerif-Bold.ttf",
        "serif": "DejaVuSerif.ttf",
        "sans-bold": "DejaVuSans-Bold.ttf",
        "sans": "DejaVuSans.ttf",
        "serif-italic": "DejaVuSerif-Italic.ttf",
    }.get(name)
    if want:
        for path in FONT_PATHS:
            if os.path.basename(path) == want and os.path.exists(path):
                return ImageFont.truetype(path, size)
        # italic not installed: fall back to the regular serif face
        if name == "serif-italic":
            return font("serif", size)
    return ImageFont.load_default()


def text_width(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if text_width(draw, trial, fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centered(draw, y, text, fnt, fill=INK):
    w = text_width(draw, text, fnt)
    draw.text(((W - w) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size + 4


def rule(draw, y, weight=2, x0=MARGIN, x1=W - MARGIN):
    draw.line([(x0, y), (x1, y)], fill=INK, width=weight)
    return y + weight + 4


def story(draw, x, y, width, kicker, headline, body, kicker_color=RED):
    """One column story: kicker, headline, body. Returns y below it."""
    kf = font("sans-bold", 14)
    hf = font("serif-bold", 21)
    bf = font("serif", 15)
    draw.text((x, y), kicker, font=kf, fill=kicker_color)
    y += 20
    for line in wrap(draw, headline, hf, width):
        draw.text((x, y), line, font=hf, fill=INK)
        y += 26
    y += 2
    for line in wrap(draw, body, bf, width):
        draw.text((x, y), line, font=bf, fill=INK)
        y += 20
    return y + 8


def draw_sea_scene(draw, x0, y0, x1, y1):
    """Stylised illustration: the corvette Merkury capsized at Benghazi."""
    # sky and sea
    draw.rectangle([x0, y0, x1, y0 + 46], fill=SKY)
    draw.rectangle([x0, y0 + 46, x1, y1], fill=SEA)
    draw.line([(x0, y0 + 46), (x1, y0 + 46)], fill=INK, width=2)
    # sun
    cx, cy = x0 + 70, y0 + 26
    draw.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(240, 200, 90))
    # distant shoreline
    draw.polygon(
        [(x0, y0 + 46), (x0 + 180, y0 + 30), (x0 + 360, y0 + 46)],
        fill=(150, 160, 150),
    )
    # waves
    for wx in range(x0 + 20, x1 - 40, 90):
        wy = y0 + 46 + 58 + ((wx * 7) % 40)
        draw.arc([wx, wy, wx + 60, wy + 18], 180, 360, fill=(255, 255, 255), width=2)
    # capsized hull: tilted grey slab, bow up out of the water
    hull = [
        (x0 + 330, y0 + 118),
        (x0 + 620, y0 + 96),
        (x0 + 660, y0 + 128),
        (x0 + 360, y0 + 152),
    ]
    draw.polygon(hull, fill=(90, 95, 100), outline=INK)
    draw.line([(x0 + 360, y0 + 152), (x0 + 660, y0 + 128)], fill=INK, width=2)
    # mast / funnel leaning over
    draw.line([(x0 + 470, y0 + 108), (x0 + 430, y0 + 62)], fill=INK, width=5)
    draw.line([(x0 + 560, y0 + 100), (x0 + 540, y0 + 70)], fill=INK, width=4)
    # explosion burst above the hull
    ex, ey = x0 + 520, y0 + 74
    for r, col in [(46, (220, 90, 20)), (34, (245, 160, 40)), (22, (250, 220, 90))]:
        spikes = []
        for i in range(12):
            ang = i * 30
            import math
            rad = math.radians(ang)
            spikes.append((ex + r * math.cos(rad), ey + r * math.sin(rad)))
        draw.polygon(spikes, fill=col)
    # smoke
    for sx, sy, sr in [(x0 + 470, y0 + 40, 16), (x0 + 500, y0 + 28, 20), (x0 + 540, y0 + 38, 14)]:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(90, 90, 90))
    # sea drones: small dark hulls with a mast
    for dx in (x0 + 200, x0 + 280, x0 + 360):
        dy = y0 + 150
        draw.polygon([(dx, dy), (dx + 46, dy), (dx + 38, dy + 10), (dx + 8, dy + 10)], fill=(30, 30, 30))
        draw.line([(dx + 22, dy), (dx + 22, dy - 12)], fill=(30, 30, 30), width=2)
    # label
    lf = font("sans-bold", 15)
    draw.text((x0 + 12, y1 - 26), "BENGHAZI, LIBYA", font=lf, fill=(255, 255, 255))
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    y = 22
    # masthead
    mf = font("serif-bold", 62)
    centered(d, y, "THE WORLD TODAY", mf)
    y += 78
    y = rule(d, y, 3)
    df = font("sans-bold", 16)
    centered(d, y, "MONDAY, 23 NOVEMBER 2026  ·  THE WORLD IN ONE PAGE", df)
    y += 24
    y = rule(d, y, 1)

    # lead headline
    y += 6
    hf = font("serif-bold", 46)
    for line in ("UKRAINE SINKS", "RUSSIAN WARSHIP", "OFF LIBYA"):
        centered(d, y, line, hf)
        y += 54
    y += 2
    # deck
    deck = font("serif-italic", 20)
    for line in wrap(
        d,
        "Seven sea drones sink the corvette Merkury at Benghazi — Kyiv's "
        "longest-range strike yet, 2,400 km from the front.",
        deck,
        COL_W - 60,
    ):
        centered(d, y, line, deck)
        y += 26
    y += 6

    # illustration
    draw_sea_scene(d, MARGIN, y, W - MARGIN, y + 160)
    y += 160 + 6
    cf = font("sans", 13)
    centered(
        d, y,
        "The corvette Merkury burns at Benghazi after Ukrainian sea drones struck.  Illustration.",
        cf, fill=GREY,
    )
    y += 22
    y = rule(d, y, 1)

    # two columns of stories
    col_w = (COL_W - 28) // 2
    left_x, right_x = MARGIN, MARGIN + col_w + 28
    y0 = y + 4
    ly = y0
    ly = story(
        d, left_x, ly, col_w,
        "SPACE · NATO",
        "Russia 'ready to launch nuclear-armed satellite'",
        "Western intelligence says the Sputnik-S satellite, built years ago "
        "and held near Moscow, could fly as early as December.",
    )
    ly = story(
        d, left_x, ly, col_w,
        "MEXICO",
        "'El Chapo Isidro' captured; 11 killed in Sinaloa",
        "FBI most-wanted cartel boss Fausto Isidro Meza Flores is seized in "
        "Guasave. Seven gunmen and four soldiers die in the raid.",
    )
    ly = story(
        d, left_x, ly, col_w,
        "CLIMATE",
        "COP31 ends with no deal; backlash grows",
        "The Antalya summit collapses as the EU and about 130 nations reject "
        "a text with no mention of fossil fuels.",
    )
    ry = y0
    ry = story(
        d, right_x, ry, col_w,
        "MARKETS",
        "AI sell-off spreads: S&P −3.7%, Nikkei −5.06%",
        "Fears that AI shares are overpriced drive world markets down. Gold "
        "rises 2.72% as investors seek safety.",
    )
    ry = story(
        d, right_x, ry, col_w,
        "UKRAINE",
        "Russian strikes kill 11 near Kyiv",
        "A drone wrecks a five-storey block in Dymer; 14 are missing across "
        "the region.",
    )
    ry = story(
        d, right_x, ry, col_w,
        "INDONESIA · AMERICA",
        "34 missing after factory fire; House flips to Democrats",
        "More remains are found after the Cikande candy-factory fire. In the "
        "US, Democrats win 258 House seats, most since 1992.",
    )
    y = max(ly, ry) + 2
    y = rule(d, y, 1)

    # market strip
    y += 2
    msf = font("sans-bold", 15)
    centered(
        d, y,
        "MARKETS  S&P 500 6,910  ▼3.70%   ·   NIKKEI  ▼5.06%   ·   GOLD  ▲2.72%   ·   BRENT $89.96  ▲0.01%",
        msf,
    )
    y += 24
    y = rule(d, y, 1)

    # sport footer
    y += 2
    sf = font("serif-bold", 17)
    centered(
        d, y,
        "SPORT  ·  Márquez wins eighth MotoGP title  ·  Alcaraz takes the ATP Finals",
        sf,
    )
    y += 26
    ff = font("sans", 12)
    centered(
        d, y,
        "Sources: Reuters · Al Jazeera · CNN · WSJ · SCMP · Süddeutsche Zeitung — reporting of 23 November 2026",
        ff, fill=GREY,
    )

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, "PNG")
    print(f"wrote {OUT} ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
