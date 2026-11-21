#!/usr/bin/env python3
"""Draw the front page of THE WORLD TODAY for Saturday 21 November 2026.

A code-drawn newspaper page (1024x1024 PNG) summing up the day's world
news. Every story below was reported on 21 November 2026 (events of
20-21 November, first reported on the 21st in the outlets named in
README.md). No network, no clock, no randomness: the output is
byte-identical on every run.

Run:  python3 draw_poster.py        (writes entry.png next to this file)
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 252, 247)
INK = (18, 18, 18)
RULE = (18, 18, 18)
RED = (178, 34, 34)
BLUE = (24, 64, 120)
GREY = (92, 92, 92)
LIGHT_GREY = (210, 208, 200)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, max_w, leading, fill=INK, max_lines=None):
    """Draw wrapped text; returns the y just below the last line."""
    lines = wrap(draw, text, fnt, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hline(draw, x0, x1, y, width=1, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_chart(draw, x, y, w, h):
    """A small falling-line chart for the lead market story."""
    draw.rectangle([x, y, x + w, y + h], outline=RULE, width=2)
    for i in range(1, 4):
        gy = y + h * i // 4
        draw.line([(x + 4, gy), (x + w - 4, gy)], fill=LIGHT_GREY, width=1)
    # descending line: index levels across the week, Friday's plunge last
    pts = [(0.04, 0.18), (0.22, 0.24), (0.38, 0.30), (0.55, 0.38),
           (0.70, 0.44), (0.84, 0.60), (0.96, 0.86)]
    xy = [(x + w * fx, y + h * fy) for fx, fy in pts]
    draw.line(xy, fill=RED, width=4, joint="curve")
    for px, py in xy:
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED)
    draw.text((x + 8, y + 6), "S&P 500  -3.7%  FRIDAY",
              font=font(SANS_B, 15), fill=RED)


# ---------------------------------------------------------------- stories
LEAD_KICKER = "MARKETS  \u00b7  NEW YORK"
LEAD_HEAD = "AI ROUT DRAGS WALL STREET INTO CORRECTION"
LEAD_BODY = (
    "US stocks plunged on Friday as the AI sell-off spread: the S&P 500 "
    "fell 3.7% and the Dow entered a correction, and the Nasdaq dropped "
    "5.3%, wiping out all its 2026 gains. Tokyo's Nikkei fell 5.1%; "
    "gold slid 4.6%."
)

STORIES = [
    ("UKRAINE", RED,
     "Russia's biggest strikes of the year",
     "400+ drones and 110 missiles hit Ukraine overnight; eight killed "
     "in Kyiv; bridges and rail stations burn."),
    ("POLAND", RED,
     "Russian missiles land in Poland",
     "Two missiles and a suspected drone come down; Tusk calls it a "
     "deliberate provocation."),
    ("THE HAGUE", RED,
     "Court: Myanmar guilty of genocide",
     "The International Court of Justice finds Myanmar responsible for "
     "genocide against the Rohingya."),
    ("BRITAIN  \u00b7  EUROPEAN UNION", BLUE,
     "UK and EU sign biggest post-Brexit deals",
     "Three pacts on food trade, carbon and youth mobility; 100,000 "
     "young Britons gain EU access."),
    ("SAUDI ARABIA", RED,
     "Houthis fire on Riyadh again",
     "The coalition intercepts three missiles aimed at the capital, the "
     "third night in a row."),
    ("DENMARK", RED,
     "Denmark foils 'hit' on Ukrainian rapper",
     "Police arrest two men and expel a Russian diplomat over a plot to "
     "kill rapper Kyivstoner."),
    ("CLIMATE", BLUE,
     "COP31 runs past its deadline",
     "Talks in Antalya stall over fossil fuels as nearly 200 nations "
     "fail to agree; the summit is extended."),
    ("BRAZIL", BLUE,
     "Bolsonaro back in hospital",
     "The jailed ex-president, 71, is treated for a near-complete "
     "intestinal obstruction."),
    ("UNITED STATES", RED,
     "FBI crime database hacked",
     "Hackers breach the National Crime Information Center; the second "
     "FBI intrusion in recent months."),
    ("TECHNOLOGY", BLUE,
     "Trump warns tech firms over data centres",
     "The president threatens \u201ctremendous penalties\u201d for US firms "
     "building data centres abroad."),
    ("TECHNOLOGY", BLUE,
     "Nvidia slides as SEC opens probe",
     "The regulator examines Nvidia's accounting after Jensen Huang "
     "resigns; Trump urges his return."),
    ("ESTONIA", RED,
     "Estonia to shut border with Russia",
     "Crossings close from 1 December after a GRU-linked arson bid on "
     "drone maker Threod Systems."),
]

ALSO = [
    "Cancer pill clears tumours in 1 in 12",
    "GTA VI sets $3.8bn first-day record",
    "6.9 quake shakes Peru's Andes",
    "Gen Z protests in 25 countries",
    "Palisades fire arsonist convicted",
    "Three Salvadoran soldiers die in Haiti",
]


def draw_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 28                      # side margin
    right = W - mx

    # ---------------------------------------------------------- masthead
    # y 0..140
    title_f = font(SERIF_B, 66)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=title_f)
    d.text(((W - tw) / 2, 4), title, font=title_f, fill=INK)
    hline(d, mx, right, 82, width=3)
    date_f = font(SANS_B, 22)
    date = "SATURDAY, 21 NOVEMBER 2026"
    dw = d.textlength(date, font=date_f)
    d.text(((W - dw) / 2, 90), date, font=date_f, fill=RED)
    sub_f = font(SANS, 15)
    sub = "One day's world news  \u2014  every story below happened or was first reported today"
    sw = d.textlength(sub, font=sub_f)
    d.text(((W - sw) / 2, 118), sub, font=sub_f, fill=GREY)
    hline(d, mx, right, 140, width=2)

    # ---------------------------------------------------------- lead story
    # y 150..386
    y = 150
    kick_f = font(SANS_B, 15)
    d.text((mx, y), LEAD_KICKER, font=kick_f, fill=RED)
    y += 22
    head_f = font(SERIF_B, 34)
    y = text_block(d, mx, y, LEAD_HEAD, head_f, 640, 40)
    y += 4
    body_f = font(SANS, 18)
    y = text_block(d, mx, y, LEAD_BODY, body_f, 640, 23)
    # chart on the right of the lead
    draw_chart(d, 700, 150, 268, 152)
    tick_f = font(SANS_B, 14)
    tick = ("S&P 500 \u22123.7%   \u00b7   Dow in correction\n"
            "Nasdaq \u22125.3%   \u00b7   Nikkei \u22125.1%\n"
            "Anthropic \u221210%   \u00b7   Gold \u22124.6%")
    ty = 310
    for line in tick.split("\n"):
        d.text((700, ty), line, font=tick_f, fill=INK)
        ty += 19
    hline(d, mx, right, 372, width=2)

    # ---------------------------------------------------------- story grid
    # y 384..933 : 3 cols x 4 rows
    cols, rows = 3, 4
    gx0, gy0 = mx, 384
    gw = (right - mx - (cols - 1) * 18) // cols
    gh = 130
    gx_step = gw + 18
    gy_step = gh + 8
    kick2_f = font(SANS_B, 14)
    shead_f = font(SERIF_B, 21)
    sbody_f = font(SANS, 17)
    for i, (kicker, colour, head, body) in enumerate(STORIES):
        cx = gx0 + (i % cols) * gx_step
        cy = gy0 + (i // cols) * gy_step
        d.text((cx, cy), kicker, font=kick2_f, fill=colour)
        cy += 20
        cy = text_block(d, cx, cy, head, shead_f, gw, 25, max_lines=2)
        cy += 2
        text_block(d, cx, cy, body, sbody_f, gw, 21, max_lines=3)

    # ---------------------------------------------------------- also strip
    # y 940..1014
    strip_y = 940
    hline(d, mx, right, strip_y, width=2)
    also_f = font(SANS_B, 15)
    also_b = font(SANS, 15)
    label = "ALSO TODAY  \u00b7  "
    d.text((mx, strip_y + 9), label, font=also_f, fill=RED)
    lx = mx + d.textlength(label, font=also_f)
    items = "   \u00b7   ".join(ALSO)
    text_block(d, lx, strip_y + 9, items, also_b, right - lx, 20,
               max_lines=2)
    hline(d, mx, right, 1012, width=2)
    foot_f = font(SANS, 12)
    foot = "Sources: Reuters, CNN, BBC, AFP, AP, FT, Guardian, Al Jazeera  \u00b7  All stories reported 21 November 2026"
    fw = d.textlength(foot, font=foot_f)
    d.text(((W - fw) / 2, 994), foot, font=foot_f, fill=GREY)
    return img


def main():
    img = draw_page()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG")
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
