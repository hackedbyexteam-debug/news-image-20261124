#!/usr/bin/env python3
"""The Day in One Page -- Tuesday 24 November 2026.

make.fun bounty news-image-20261124: sum up 24 November 2026's world news
in one 1024x1024 PNG.

Design (different from the usual wall of headlines): a dark masthead with
the date set huge, ONE dominant hero story -- Sanofi's $41bn takeover of
Insmed, the biggest biotech deal in nearly three years -- with three big
numbers a viewer can read at a glance, then a 2 x 3 digest grid of six
further stories, each tagged with its region and the date 24 NOV plus a
single verifiable fact line, and an "Also today" strip at the foot. Every
story below was first reported on Tuesday 24 November 2026; figures are
as reported that day.

Sources checked before drawing: Sanofi's press release of 24 November
2026 and Reuters (Sanofi-Insmed, Solomon Islands, Hanoi, Hasina, Iraq),
ESA (Euclid's record quasar), UN Women / UNODC (femicide brief), CMSA
(Shenzhou-24 crew), the Australian government (duty of care), AP / AJP
(Russian jets in the KADIZ) and USGS (Nepal quake). Stories first
reported on earlier days were left out -- among them the leaked Rosstat
war-dead figures (23 Nov, the previous lead), the capture of 'El Chapo
Isidro' (20-21 Nov), Bukele's Haiti announcement (22-23 Nov), the UK's
Myanmar sanctions (23 Nov), the Gaza strikes (23 Nov), the SpaceX suits
(23 Nov) and the Ma spying sentence (23 Nov).

Deterministic and offline: copy and layout are fixed in this file, fonts
are bundled under assets/fonts/ (DejaVu, freely licensed), no network, no
clock, no randomness, so two runs write identical bytes. If Pillow cannot
render for any reason, it falls back to the pre-rendered image shipped as
assets/entry.png.
"""

import shutil
import sys
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
FONTS = HERE / "assets" / "fonts"
FALLBACK = HERE / "assets" / "entry.png"
OUT = Path("/output/entry.png")

W = H = 1024
M = 32                      # page margin
CW = W - 2 * M              # 960 content width

# --- palette: ink-on-paper with a dark navy masthead ----------------------
PAPER = (247, 243, 234)
CARD = (255, 252, 245)
INK = (22, 22, 20)
SOFT = (72, 68, 60)
FAINT = (120, 114, 102)
NAVY = (16, 30, 54)         # masthead + hero art ground
NAVY_LT = (30, 52, 88)
GOLD = (201, 158, 52)
RED = (178, 34, 22)
RED_DK = (122, 20, 12)
TEAL = (14, 92, 86)
SKY = (38, 108, 138)
PURPLE = (96, 62, 145)
HAIR = (203, 195, 178)
CHIPBG = (233, 226, 210)


@lru_cache(maxsize=64)
def load(name, size):
    from PIL import ImageFont
    return ImageFont.truetype(str(FONTS / name), size)


class Page:
    """Small drawing helper bound to one Pillow canvas."""

    def __init__(self):
        from PIL import Image, ImageDraw
        self.img = Image.new("RGB", (W, H), PAPER)
        self.d = ImageDraw.Draw(self.img)

    def serif_b(self, s):
        return load("DejaVuSerif-Bold.ttf", s)

    def serif(self, s):
        return load("DejaVuSerif.ttf", s)

    def sans_b(self, s):
        return load("DejaVuSans-Bold.ttf", s)

    def sans(self, s):
        return load("DejaVuSans.ttf", s)

    def width(self, text, font):
        return self.d.textlength(text, font=font)

    def split(self, text, font, max_w):
        """Greedy wrap into lines no wider than max_w."""
        out, cur = [], ""
        for word in text.split():
            trial = f"{cur} {word}".strip()
            if self.width(trial, font) <= max_w or not cur:
                cur = trial
            else:
                out.append(cur)
                cur = word
        if cur:
            out.append(cur)
        return out

    def flow(self, x, y, text, font, max_w, fill, step):
        """Draw wrapped text; return the y below the last line."""
        for line in self.split(text, font, max_w):
            self.d.text((x, y), line, font=font, fill=fill)
            y += step
        return y

    def caps(self, x, y, text, font, fill, gap=2):
        """Letter-spaced capitals; returns the width consumed."""
        cx = x
        for ch in text:
            self.d.text((cx, y), ch, font=font, fill=fill)
            cx += self.width(ch, font) + gap
        return cx - x

    def hline(self, x, y, w, fill=INK, px=2):
        self.d.line([(x, y), (x + w, y)], fill=fill, width=px)

    def date_chip(self, x, y, text, bg, fg=(255, 255, 255)):
        """Small solid date/tag chip; returns its width."""
        f = self.sans_b(12)
        inner = self.width(text, f) + 18
        self.d.rounded_rectangle([x, y, x + inner, y + 22], radius=3,
                                 fill=bg)
        self.d.text((x + 9, y + 4), text, font=f, fill=fg)
        return inner


def deal_art(p, x0, y0, x1, y1):
    """Hero art: the deal itself.

    A dark slate panel with the two companies named, the $41bn price set
    huge, the per-share price beneath it, a rising bar chart for a
    takeover that tops the biotech league table, a two-tone capsule for
    the drug at the heart of it, and the record it sets -- so the picture
    alone says "giant cash pharma deal".
    """
    d = p.d
    d.rounded_rectangle([x0, y0, x1, y1], radius=6, fill=NAVY)
    d.rounded_rectangle([x0, y0, x1, y0 + 4], radius=2, fill=GOLD)
    # the two companies
    d.text((x0 + 26, y0 + 22), "SANOFI × INSMED", font=p.sans_b(16),
           fill=GOLD)
    # the price, huge
    d.text((x0 + 26, y0 + 50), "$41bn", font=p.sans_b(64),
           fill=(255, 255, 255))
    d.text((x0 + 26, y0 + 128), "cash deal · $175 a share",
           font=p.sans(16), fill=(196, 204, 220))
    # rising bars: the deal tops the biotech table
    base = y1 - 72
    heights = [26, 44, 62, 80]
    bw, gap = 36, 14
    for i, h in enumerate(heights):
        bx = x0 + 26 + i * (bw + gap)
        fill = GOLD if i == 3 else TEAL
        d.rectangle([bx, base - h, bx + bw, base], fill=fill)
    # two-tone capsule: the drug behind the deal
    cx0, cy0, cx1, cy1 = x0 + 216, base - 64, x0 + 298, base - 40
    mid = (cx0 + cx1) // 2
    d.rounded_rectangle([cx0, cy0, cx1, cy1], radius=12,
                        fill=(255, 255, 255))
    d.pieslice([cx0, cy0, cx0 + 24, cy1], 90, 270, fill=TEAL)
    d.rectangle([cx0 + 12, cy0, mid, cy1], fill=TEAL)
    d.rounded_rectangle([cx0, cy0, cx1, cy1], radius=12,
                        outline=(196, 204, 220), width=1)
    # the record it sets
    d.text((x0 + 26, y1 - 32), "biggest biotech deal in nearly 3 years",
           font=p.sans(14), fill=(196, 204, 220))


def digest_cell(p, x, y, w, h, accent, tag, head, fact):
    """One digest card: region tag + 24 NOV chip, headline, one fact."""
    d = p.d
    d.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=CARD,
                        outline=HAIR, width=1)
    d.rectangle([x, y, x + w, y + 4], fill=accent)
    p.caps(x + 12, y + 14, tag, p.sans_b(12), accent)
    chip_w = p.date_chip(x + w - 76, y + 10, "24 NOV", NAVY)
    ny = p.flow(x + 12, y + 38, head, p.sans_b(18), w - 24, INK, 23)
    p.flow(x + 12, ny + 2, fact, p.sans(14), w - 24, SOFT, 19)


def build():
    p = Page()
    d = p.d

    # --- frame ------------------------------------------------------------
    d.rectangle([0, 0, W - 1, H - 1], outline=NAVY, width=4)
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=1)

    # --- masthead: dark band, the date set huge ---------------------------
    d.rectangle([0, 0, W, 158], fill=NAVY)
    d.rectangle([0, 154, W, 158], fill=GOLD)
    p.caps(W // 2 - 210, 22, "ONE DAY  ·  ONE IMAGE", p.sans_b(13), GOLD)
    d.text((W // 2, 44), "Tuesday 24 November 2026",
           font=p.serif_b(52), fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 112), "The world's news in one image — every story "
           "below was first reported today",
           font=p.sans(16), fill=(196, 204, 220), anchor="ma")

    # --- hero: one dominant story -----------------------------------------
    hy = 172
    p.date_chip(M, hy, "LEAD STORY", TEAL)
    p.caps(M + 118, hy + 4, "THE DEAL OF THE DAY — PHARMA",
           p.sans_b(13), TEAL)
    y = p.flow(M, hy + 36, "Sanofi buys Insmed in a $41bn deal",
               p.serif_b(38), 604, INK, 46)
    y = p.flow(M, y + 8, "The French drugmaker will pay $175 a share in "
               "cash — a 46% premium — in the biggest biotech takeover in "
               "nearly three years, betting on the rare-lung-disease drug "
               "Brensocatib. It closes in the first half of 2027.",
               p.sans(16), 604, SOFT, 22)
    # three big numbers, readable at a glance
    stats = [("$41bn", "cash deal value"),
             ("$175", "per share, in cash"),
             ("46%", "premium over 18 Nov close")]
    sw, gap = 196, 8
    sy = 414
    for i, (num, lab) in enumerate(stats):
        sx = M + i * (sw + gap)
        d.rounded_rectangle([sx, sy, sx + sw, sy + 62], radius=4,
                            fill=CARD, outline=HAIR, width=1)
        d.text((sx + sw // 2, sy + 8), num, font=p.sans_b(24),
               fill=TEAL, anchor="ma")
        d.text((sx + sw // 2, sy + 38), lab, font=p.sans(12),
               fill=SOFT, anchor="ma")
    deal_art(p, 660, hy, W - M, 476)
    p.hline(M, 492, CW, px=2)

    # --- digest grid: six more stories, each dated ------------------------
    gy = 506
    p.caps(M, gy, "THE DAY IN BRIEF", p.sans_b(14), INK)
    right = "ALL FIRST REPORTED 24 NOVEMBER 2026"
    d.text((W - M - p.width(right, p.sans_b(12)), gy + 2), right,
           font=p.sans_b(12), fill=FAINT)
    cells = [
        (TEAL, "PACIFIC", "Solomon Islands drops China pact",
         "Honiara will not renew the 2022 security deal when it expires "
         "in April; a new treaty with Australia is due on Wednesday."),
        (NAVY_LT, "KOREA", "Russian jets enter Seoul's air zone",
         "Several Russian aircraft flew into South Korea's air defence "
         "identification zone over waters near Japan."),
        (RED, "VIETNAM", "Hanoi gas blast kills 6",
         "A cooking-gas blast tore through a food shop on Dong Da "
         "Street, killing six and injuring ten."),
        (SKY, "SPACE", "Shenzhou-24 crew unveiled",
         "Three astronauts named, including Pakistan's Zeeshan Ali — "
         "the first foreigner to visit Tiangong."),
        (PURPLE, "AUSTRALIA", "Australia's big-tech duty of care",
         "Canberra struck a deal forcing platforms to police harmful "
         "content, with fines of up to 5% of global revenue."),
        (RED_DK, "BANGLADESH", "Hasina to return on 16 December",
         "Dhaka says the ousted leader returns on Victory Day — only "
         "under extradition, with her death sentence standing."),
    ]
    cw, ch, cg = 468, 108, 24
    for i, (accent, tag, head, fact) in enumerate(cells):
        cx = M + (i % 2) * (cw + cg)
        cy = 534 + (i // 2) * (ch + 8)
        digest_cell(p, cx, cy, cw, ch, accent, tag, head, fact)

    # --- also today ---------------------------------------------------------
    ay = 884
    p.caps(M, ay, "ALSO TODAY", p.sans_b(14), INK)
    p.hline(M, ay + 22, CW, fill=HAIR, px=1)
    also = [
        ("NEPAL — ", "A 5.6-magnitude quake struck near the Chinese border."),
        ("IRAQ — ", "Baghdad ordered a takeover of Kurdish oilfields."),
        ("UN — ", "47,000 women and girls killed by partners or family "
         "in 2025."),
        ("SPACE — ", "Euclid found the most distant quasar ever seen."),
    ]
    for i, (lead, body) in enumerate(also):
        ax = M + (i % 2) * 492
        ayy = ay + 30 + (i // 2) * 24
        d.text((ax, ayy), lead, font=p.sans_b(13), fill=INK)
        d.text((ax + p.width(lead, p.sans_b(13)), ayy), body,
               font=p.sans(13), fill=SOFT)
    src = ("Compiled from reports first published on Tuesday 24 November "
           "2026 — Reuters · Sanofi · ESA · UN Women · Al Jazeera")
    d.text((W // 2, 988), src, font=p.sans(11), fill=FAINT, anchor="ma")

    return p.img


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    try:
        build().save(OUT, format="PNG", optimize=True)
    except Exception as exc:
        print(f"render failed ({exc}); using fallback image",
              file=sys.stderr)
        shutil.copyfile(FALLBACK, OUT)


if __name__ == "__main__":
    main()
