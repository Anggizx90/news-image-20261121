#!/usr/bin/env python3
"""Draw THE WORLD TODAY, a one-page newspaper front page summing up the
world news of Saturday 21 November 2026.

Build-time script (run locally by the author). It renders a dense 1024x1024
PNG with Pillow and writes it to entry.png next to this file, or to the path
given as the first argument. The entrypoint main.py only copies that PNG,
so nothing here runs inside the grader.

Deterministic: no clock, no randomness, no network. Same input bytes in,
same PNG bytes out.
"""

import hashlib
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024
MARGIN = 28

PAPER = (246, 241, 227)      # warm newsprint
INK = (17, 17, 17)           # near-black
RED = (168, 30, 38)          # headline red
GREY = (84, 80, 70)          # secondary text
RULE = (201, 194, 174)       # hairline rules
BOX = (255, 253, 244)        # story-box fill
BOX_EDGE = (196, 189, 166)   # story-box border
BLACK_BAND = (14, 14, 14)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

PROBLEMS = []


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fitted(draw, text, path, size, max_w, max_lines, shrink_to=9):
    """Pick the largest font size (down to shrink_to) whose wrap fits."""
    size_now = size
    while size_now > shrink_to:
        fnt = font(path, size_now)
        if len(wrap(draw, text, fnt, max_w)) <= max_lines:
            return fnt, wrap(draw, text, fnt, max_w)
        size_now -= 1
    fnt = font(path, shrink_to)
    lines = wrap(draw, text, fnt, max_w)
    if len(lines) > max_lines:
        PROBLEMS.append("overflow: %r needs %d lines at min size" % (text, len(lines)))
        lines = lines[:max_lines]
    return fnt, lines


def text_block(draw, x, y, w, lines, fnt, fill=INK, leading=None):
    """Draw lines left-aligned; return the y just below the block."""
    lh = leading if leading is not None else int(fnt.size * 1.18)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def starburst(draw, cx, cy, r_out, r_in, points=8, fill=RED):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        ang = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def draw_masthead(draw):
    band_top, band_h = 22, 78
    draw.rectangle([0, band_top, W, band_top + band_h], fill=BLACK_BAND)
    title = "THE WORLD TODAY"
    fnt = font(SERIF_BOLD, 56)
    tw = draw.textlength(title, font=fnt)
    draw.text(((W - tw) / 2, band_top + 10), title, font=fnt, fill=(250, 247, 238))
    # date strip under the band
    y = band_top + band_h + 12
    date_fnt = font(SANS_BOLD, 21)
    draw.text((MARGIN, y), "SATURDAY, 21 NOVEMBER 2026", font=date_fnt, fill=RED)
    side = "THE DAY'S NEWS IN ONE PAGE"
    side_fnt = font(SANS_BOLD, 13)
    sw = draw.textlength(side, font=side_fnt)
    draw.text((W - MARGIN - sw, y + 5), side, font=side_fnt, fill=GREY)
    rule(draw, MARGIN, y + 32, W - MARGIN, width=3)
    return y + 40


def draw_lead(draw, y):
    """Lead story: the AI market rout, with a falling chart on the right."""
    x0, x1 = MARGIN, W - MARGIN
    chart_w = 300
    text_w = (x1 - x0) - chart_w - 24
    head = "AI ROUT SENDS MARKETS INTO FREE FALL"
    fnt, lines = fitted(draw, head, SERIF_BOLD, 40, text_w, 2)
    yy = text_block(draw, x0, y, text_w, lines, fnt, fill=INK, leading=46)
    deck = ("Wall Street's AI sell-off deepens into a rout: the S&P 500 and "
            "the Dow enter correction as Nvidia tumbles 14% \u2014 and Asia "
            "follows, with Tokyo down 5.1%.")
    deck_fnt = font(SANS, 15)
    deck_lines = wrap(draw, deck, deck_fnt, text_w)
    if len(deck_lines) > 3:
        PROBLEMS.append("lead deck overflow: %d lines" % len(deck_lines))
        deck_lines = deck_lines[:3]
    yy = text_block(draw, x0, yy + 4, text_w, deck_lines, deck_fnt,
                    fill=GREY, leading=19)
    # falling chart, right side
    cx0 = x1 - chart_w
    cy0, cy1 = y + 6, y + 118
    draw.rectangle([cx0, cy0, x1, cy1], outline=RULE, width=1, fill=BOX)
    pts = [(cx0 + 8, cy0 + 26), (cx0 + 60, cy0 + 40), (cx0 + 110, cy0 + 36),
           (cx0 + 160, cy0 + 58), (cx0 + 205, cy0 + 70), (cx0 + 250, cy0 + 86),
           (cx0 + 292, cy1 - 12)]
    draw.line(pts, fill=RED, width=4, joint="curve")
    for px, py in pts[1:-1]:
        draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
    draw.ellipse([pts[-1][0] - 5, pts[-1][1] - 5, pts[-1][0] + 5, pts[-1][1] + 5],
                 fill=RED)
    lab = font(SANS_BOLD, 12)
    draw.text((cx0 + 10, cy1 - 22), "NASDAQ THIS WEEK", font=lab, fill=GREY)
    draw.text((cx0 + 232, cy1 - 22), "\u22125.3%", font=font(SANS_BOLD, 15), fill=RED)
    return max(yy, cy1) + 10


def draw_ticker(draw, y):
    """One-line market scoreboard."""
    cells = [("S&P 500", "\u22123.7%"), ("NASDAQ", "\u22125.3%"),
             ("NIKKEI", "\u22125.1%"), ("KOSPI", "\u22125.2%"),
             ("GOLD", "\u22124.0%"), ("VIX", "37")]
    x0, x1 = MARGIN, W - MARGIN
    cw = (x1 - x0) / len(cells)
    draw.rectangle([x0, y, x1, y + 44], fill=BLACK_BAND)
    for i, (label, val) in enumerate(cells):
        cx = x0 + i * cw
        lf = font(SANS_BOLD, 10)
        vf = font(SANS_BOLD, 19)
        lw = draw.textlength(label, font=lf)
        vw = draw.textlength(val, font=vf)
        draw.text((cx + (cw - lw) / 2, y + 4), label, font=lf,
                  fill=(190, 186, 172))
        draw.text((cx + (cw - vw) / 2, y + 19), val, font=vf, fill=(255, 255, 255))
        if i:
            draw.line([(cx, y + 6), (cx, y + 38)], fill=(70, 70, 70), width=1)
    return y + 44 + 12


def feature_box(draw, x, y, w, h, kicker, headline, deck, motif):
    draw.rectangle([x, y, x + w, y + h], fill=BOX, outline=BOX_EDGE, width=1)
    pad = 12
    ix = x + pad
    iy = y + 10
    kf = font(SANS_BOLD, 11)
    draw.text((ix, iy), kicker, font=kf, fill=RED)
    iy += 18
    rule(draw, ix, iy, x + w - pad, width=1, fill=RULE)
    iy += 8
    if motif == "strikes":
        # three short red ticks, tucked into the kicker row (right side)
        bx, by = x + w - 66, y + 12
        for j, off in enumerate((0, 7, 14)):
            draw.line([(bx + off, by + 10), (bx + off + 12, by + 2)], fill=RED, width=3)
    elif motif == "riyadh":
        # one small burst, tucked into the kicker row (right side)
        starburst(draw, x + w - 24, y + 18, 10, 4)
    hf, hlines = fitted(draw, headline, SANS_BOLD, 23, w - 2 * pad, 2)
    iy = text_block(draw, ix, iy, w - 2 * pad, hlines, hf, fill=INK, leading=27)
    df = font(SANS, 13)
    dlines = wrap(draw, deck, df, w - 2 * pad)
    if len(dlines) > 3:
        PROBLEMS.append("feature deck overflow: %r" % deck[:40])
        dlines = dlines[:3]
    text_block(draw, ix, iy + 4, w - 2 * pad, dlines, df, fill=GREY, leading=17)


def draw_features(draw, y):
    gap = 16
    w = (W - 2 * MARGIN - gap) // 2
    h = 156
    feature_box(draw, MARGIN, y, w, h, "WAR IN EUROPE",
                "Russia's biggest strikes hit Kyiv \u2014 and Poland",
                "More than 400 drones and 110 missiles rain down overnight; "
                "eight killed in Kyiv and three bridges hit. A Russian "
                "missile lands in Poland \u2014 Warsaw calls it a deliberate "
                "provocation.", "strikes")
    feature_box(draw, MARGIN + w + gap, y, w, h, "MIDDLE EAST",
                "Third night of fire over Riyadh",
                "Saudi defences intercept three Houthi missiles aimed at the "
                "capital early on Saturday, days after a strike damaged the "
                "PIF Tower, Riyadh's tallest.", "riyadh")
    return y + h + 12


GRID = [
    ("UK\u2013EU RESET", "Britain and EU seal biggest post-Brexit deal",
     "100,000 youth-mobility places a year, plus food and carbon pacts, agreed in Brussels."),
    ("GEN Z", "Young Europe takes to the streets",
     "Tens of thousands march in 25 countries: \u201cMoney for schools, not war.\u201d"),
    ("CLIMATE", "COP31 runs past its deadline",
     "Talks in Antalya deadlocked as a draft deal drops any fossil-fuel phase-out."),
    ("DENMARK", "Denmark says Russia plotted to kill a rapper",
     "Kyivstoner was the target, police say; Moscow\u2019s defence attach\u00e9 expelled."),
    ("ESTONIA", "Estonia to shut its Russia border",
     "Road crossings close from 1 December for at least six months over sabotage fears."),
    ("CYBER", "FBI crime database hacked",
     "Breach of the national NCIC system is probed \u2014 the second FBI intrusion in months."),
    ("NVIDIA", "Nvidia slides as SEC opens probe",
     "Shares fall 14% as regulators examine the chip giant\u2019s accounting."),
    ("TRUMP", "Trump threatens tax on data centres abroad",
     "\u201cTremendous tax\u201d for US firms that build AI centres overseas, he says."),
    ("GTA VI", "GTA VI banks $3.79bn in a day",
     "Rockstar\u2019s launch is the biggest in entertainment history: 32.5m copies."),
    ("PERU", "6.9 quake shakes Peru",
     "Tremor felt in Lima; no damage or casualties reported."),
    ("HEALTH", "Cancer pill hailed a breakthrough",
     "Daraxonrasib halted tumour growth in 90% of 61 pancreatic cancer patients."),
    ("JUSTICE", "Guilty: man who started Palisades fire",
     "Jury convicts Rinderknecht over the blaze that killed 12 in Los Angeles."),
]


def draw_grid(draw, y):
    cols, rows = 3, 4
    gap = 10
    bw = (W - 2 * MARGIN - gap * (cols - 1)) // cols
    bh = 109
    for idx, (kicker, headline, deck) in enumerate(GRID):
        r, c = divmod(idx, cols)
        x = MARGIN + c * (bw + gap)
        yy = y + r * (bh + gap)
        draw.rectangle([x, yy, x + bw, yy + bh], fill=BOX, outline=BOX_EDGE, width=1)
        pad = 10
        ix = x + pad
        iy = yy + 8
        kf = font(SANS_BOLD, 10)
        draw.text((ix, iy), kicker, font=kf, fill=RED)
        iy += 16
        hf, hlines = fitted(draw, headline, SANS_BOLD, 16, bw - 2 * pad, 2)
        iy = text_block(draw, ix, iy, bw - 2 * pad, hlines, hf, fill=INK, leading=19)
        df = font(SANS, 11)
        dlines = wrap(draw, deck, df, bw - 2 * pad)
        if len(dlines) > 2:
            PROBLEMS.append("grid deck overflow: %r" % deck[:40])
            dlines = dlines[:2]
        text_block(draw, ix, iy + 2, bw - 2 * pad, dlines, df, fill=GREY, leading=14)
    return y + rows * bh + (rows - 1) * gap


def draw_footer(draw, y):
    rule(draw, MARGIN, y, W - MARGIN, width=2)
    note = ("All stories as reported on Saturday 21 November 2026  \u00b7  "
            "Reuters \u00b7 AP \u00b7 CNN \u00b7 WSJ \u00b7 The Guardian")
    fnt = font(SANS, 11)
    tw = draw.textlength(note, font=fnt)
    draw.text(((W - tw) / 2, y + 8), note, font=fnt, fill=GREY)


def build(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    y = draw_masthead(draw)
    y = draw_lead(draw, y)
    y = draw_ticker(draw, y)
    y = draw_features(draw, y)
    y = draw_grid(draw, y)
    draw_footer(draw, y + 8)
    if PROBLEMS:
        for p in PROBLEMS:
            print("LAYOUT PROBLEM:", p, file=sys.stderr)
        raise SystemExit("layout overflow: %d problem(s)" % len(PROBLEMS))
    img.save(out_path, format="PNG")
    data = open(out_path, "rb").read()
    print("wrote %s  %d bytes  md5 %s" % (out_path, len(data),
          hashlib.md5(data).hexdigest()))


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "entry.png")
    build(target)
