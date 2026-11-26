#!/usr/bin/env python3
"""Draw the front page for Thursday, 26 November 2026.

One-page newspaper: masthead + date, one lead story (Cairo tanker
fire) and five story cards, plus a footer strip. Every pictogram is
drawn from basic shapes with Pillow, positioned as fractions of its
box so the same pictogram fits a tall card, a wide card or the lead
panel. No photos, no downloaded art.
Run: python3 draw.py  -> writes entry.png (1024x1024) next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 227)
INK = (20, 20, 20)
RED = (178, 32, 44)
BLUE = (31, 78, 121)
ORANGE = (214, 96, 20)
GOLD = (212, 160, 32)
DARK = (43, 43, 43)
GREY = (110, 110, 104)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


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


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None, align="left"):
    if leading is None:
        leading = int(fnt.size * 1.22)
    for line in lines:
        if align == "center":
            w = draw.textlength(line, font=fnt)
            draw.text((x - w / 2, y), line, font=fnt, fill=fill)
        else:
            draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---- pictograms: each draws inside the box (x, y, w, h),
#      using fractions of w/h so any box size works ----

def pic_tanker(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 32, 30))
    road_y = y + h * 0.88
    d.rectangle([x, road_y, x + w, road_y + 6], fill=(90, 86, 80))
    for i in range(5):
        dx = x + w * (0.05 + i * 0.19)
        d.rectangle([dx, road_y + 1, dx + w * 0.07, road_y + 5],
                    fill=(240, 220, 120))
    # smoke puffs
    for (fx, fy, fr) in [(0.12, 0.12, 0.07), (0.20, 0.08, 0.09),
                         (0.78, 0.10, 0.08), (0.87, 0.16, 0.06)]:
        r = fr * w
        d.ellipse([x + fx * w - r, y + fy * h - r,
                   x + fx * w + r, y + fy * h + r], fill=(120, 116, 110))
    # flames above the tank
    base = y + h * 0.66
    for (fx, fw, fh, col) in [(0.24, 0.15, 0.30, ORANGE),
                              (0.40, 0.14, 0.40, (232, 130, 30)),
                              (0.54, 0.12, 0.26, ORANGE),
                              (0.38, 0.10, 0.20, (245, 196, 60))]:
        d.polygon([(x + fx * w, base),
                   (x + (fx + fw / 2) * w, base - fh * h),
                   (x + (fx + fw) * w, base)], fill=col)
    # tanker: cylinder + cab + wheels
    ty = y + h * 0.66
    th = h * 0.20
    d.rounded_rectangle([x + w * 0.08, ty, x + w * 0.72, ty + th],
                        radius=int(th / 2), fill=(200, 200, 196),
                        outline=(120, 120, 116), width=3)
    d.rectangle([x + w * 0.72, ty + th * 0.1, x + w * 0.90, ty + th],
                fill=RED)
    d.rectangle([x + w * 0.76, ty + th * 0.2, x + w * 0.86, ty + th * 0.55],
                fill=(180, 220, 235))
    for wx in (0.20, 0.62, 0.81):
        cx = x + wx * w
        r = h * 0.075
        d.ellipse([cx - r, ty + th - r * 0.4, cx + r, ty + th + r * 1.6],
                  fill=(20, 20, 20))
        d.ellipse([cx - r * 0.4, ty + th + r * 0.3,
                   cx + r * 0.4, ty + th + r * 1.1], fill=(150, 150, 146))


def pic_tariffs(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 236, 244))
    base = y + h * 0.86
    for (bx, bh, col) in [(0.08, 0.30, BLUE), (0.36, 0.46, RED),
                          (0.64, 0.62, (38, 120, 70))]:
        d.rectangle([x + bx * w, base - bh * h,
                     x + (bx + 0.20) * w, base], fill=col)
    d.line([(x + w * 0.05, base), (x + w * 0.95, base)], fill=INK, width=3)
    pct = SANS_B(int(min(w, h) * 0.34))
    d.text((x + w * 0.68, y + h * 0.04), "%", font=pct, fill=RED)


def pic_space(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 28, 52))
    for (fx, fy) in [(0.08, 0.12), (0.22, 0.26), (0.70, 0.10),
                     (0.86, 0.30), (0.48, 0.08), (0.92, 0.55)]:
        sx, sy = x + fx * w, y + fy * h
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    # ringed planet, top right
    px, py = x + w * 0.76, y + h * 0.24
    r = min(w, h) * 0.13
    d.ellipse([px - r, py - r, px + r, py + r], fill=GOLD)
    d.arc([px - r * 1.7, py - r * 0.45, px + r * 1.7, py + r * 0.45],
          start=200, end=340, fill=(240, 220, 160), width=4)
    # rocket, left of centre
    rx = x + w * 0.30
    rw = w * 0.16
    d.polygon([(rx, y + h * 0.18), (rx + rw / 2, y + h * 0.34),
               (rx + rw, y + h * 0.18)], fill=RED)
    d.rectangle([rx, y + h * 0.34, rx + rw, y + h * 0.68],
                fill=(240, 240, 238))
    d.ellipse([rx + rw * 0.28, y + h * 0.42, rx + rw * 0.72, y + h * 0.56],
              fill=BLUE)
    d.polygon([(rx, y + h * 0.62), (rx - rw * 0.5, y + h * 0.80),
               (rx, y + h * 0.76)], fill=RED)
    d.polygon([(rx + rw, y + h * 0.62), (rx + rw * 1.5, y + h * 0.80),
               (rx + rw, y + h * 0.76)], fill=RED)
    d.polygon([(rx + rw * 0.2, y + h * 0.68),
               (rx + rw / 2, y + h * 0.92),
               (rx + rw * 0.8, y + h * 0.68)], fill=(245, 160, 40))


def pic_embassy(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 208))
    bx, by = x + w * 0.18, y + h * 0.42
    bw, bh = w * 0.64, h * 0.42
    d.rectangle([bx, by, bx + bw, by + bh], fill=(120, 116, 110))
    d.polygon([(bx - w * 0.04, by), (bx + bw / 2, by - h * 0.18),
               (bx + bw + w * 0.04, by)], fill=(90, 86, 80))
    for i in range(3):
        cx0 = bx + bw * (0.10 + i * 0.30)
        d.rectangle([cx0, by + bh * 0.24, cx0 + bw * 0.09, by + bh],
                    fill=(246, 241, 227))
    d.rectangle([bx - w * 0.03, by + bh, bx + bw + w * 0.03, by + bh + h * 0.06],
                fill=(90, 86, 80))
    # flag pole + flag
    d.line([(bx + bw / 2, by - h * 0.18), (bx + bw / 2, by - h * 0.36)],
           fill=INK, width=4)
    d.polygon([(bx + bw / 2, by - h * 0.36),
               (bx + bw / 2 + w * 0.15, by - h * 0.31),
               (bx + bw / 2, by - h * 0.26)], fill=RED)
    # red X: closed
    d.line([(x + w * 0.06, y + h * 0.06), (x + w * 0.94, y + h * 0.94)],
           fill=RED, width=10)
    d.line([(x + w * 0.94, y + h * 0.06), (x + w * 0.06, y + h * 0.94)],
           fill=RED, width=10)


def pic_store(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 238, 222))
    bx, by = x + w * 0.16, y + h * 0.40
    bw, bh = w * 0.68, h * 0.46
    d.rectangle([bx, by, bx + bw, by + bh], fill=(246, 241, 227),
                outline=INK, width=3)
    # striped awning
    for i in range(6):
        col = RED if i % 2 == 0 else (246, 241, 227)
        sx0 = bx + bw * i / 6
        sx1 = bx + bw * (i + 1) / 6
        d.polygon([(sx0, by), (sx1, by), (sx1 - w * 0.03, by - h * 0.14),
                   (sx0 - w * 0.03, by - h * 0.14)], fill=col)
    d.rectangle([bx + bw * 0.10, by + bh * 0.32, bx + bw * 0.42, by + bh],
                fill=BLUE)
    d.rectangle([bx + bw * 0.54, by + bh * 0.32, bx + bw * 0.88, by + bh * 0.68],
                fill=(180, 220, 235))
    # green rescue check, bottom right
    cx, cy = x + w * 0.80, y + h * 0.80
    r = min(w, h) * 0.17
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(38, 120, 70))
    d.line([(cx - r * 0.55, cy), (cx - r * 0.12, cy + r * 0.42),
            (cx + r * 0.6, cy - r * 0.42)], fill=(255, 255, 255), width=7)


def pic_chess(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 232, 210))
    s = min(w, h) * 0.17
    ox, oy = x + w * 0.10, y + h * 0.10
    for r in range(4):
        for c in range(4):
            if (r + c) % 2 == 0:
                d.rectangle([ox + c * s, oy + r * s,
                             ox + (c + 1) * s, oy + (r + 1) * s],
                            fill=(60, 52, 44))
    # king piece standing right of the board
    kx = x + w * 0.76
    ky = y + h * 0.88
    kw = min(w, h) * 0.16
    d.polygon([(kx - kw, ky), (kx + kw, ky), (kx + kw * 0.7, ky - h * 0.30),
               (kx - kw * 0.7, ky - h * 0.30)], fill=(246, 241, 227),
              outline=INK, width=3)
    d.ellipse([kx - kw * 0.75, ky - h * 0.52, kx + kw * 0.75, ky - h * 0.30],
              fill=(246, 241, 227), outline=INK, width=3)
    d.line([(kx, ky - h * 0.72), (kx, ky - h * 0.52)], fill=INK, width=5)
    d.line([(kx - kw * 0.45, ky - h * 0.62), (kx + kw * 0.45, ky - h * 0.62)],
           fill=INK, width=5)


CARDS = [
    ("TRADE", "US UNVEILS NEW TARIFFS",
     "China +20%; EU, Brazil and others hit.",
     pic_tariffs),
    ("SPACE", "PAKISTAN ASTRONAUT REACHES TIANGONG",
     "Zeeshan Ali docks on Shenzhou-24.",
     pic_space),
    ("DIPLOMACY", "N. KOREA EXPELS SWISS ENVOY",
     "Pyongyang office ordered shut in a sanctions row.",
     pic_embassy),
    ("COLOMBIA", "20 HOSTAGES FREED IN CARTAGENA",
     "Forces storm a supermarket after a 17-hour siege.",
     pic_store),
    ("CHESS", "GUKESH, SINDAROV DRAW AGAIN",
     "Game 2 ends in 20 moves; title match level 1-1 in Geneva.",
     pic_chess),
]


def draw_card(d, x, y, w, h, kicker, headline, deck, pic, horizontal=False):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    if horizontal:
        pw = 150
        pic(d, x + 2, y + 2, pw - 4, h - 4)
        tx = x + pw + 14
        tw = w - pw - 28
        yy = y + 16
        d.text((tx, yy), kicker, font=SANS_B(17), fill=RED)
        yy += 28
        yy = text_block(d, tx, yy,
                        wrap(d, headline, SERIF_B(24), tw),
                        SERIF_B(24), leading=29)
        text_block(d, tx, yy + 6,
                   wrap(d, deck, SANS(17), tw), SANS(17), leading=21)
    else:
        ph = 100
        pic(d, x + 2, y + 2, w - 4, ph)
        yy = y + ph + 10
        d.text((x + 14, yy), kicker, font=SANS_B(16), fill=RED)
        yy += 26
        yy = text_block(d, x + 14, yy,
                        wrap(d, headline, SERIF_B(22), w - 28),
                        SERIF_B(22), leading=26)
        text_block(d, x + 14, yy + 4,
                   wrap(d, deck, SANS(16), w - 28), SANS(16), leading=20)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 24  # margin

    # ---- masthead ----
    text_block(d, W // 2, 14, ["THE WORLD TODAY"], SERIF_B(62),
               align="center", leading=70)
    rule(d, m, 92, W - m, 3)
    text_block(d, W // 2, 102, ["THURSDAY, 26 NOVEMBER 2026"],
               SANS_B(30), fill=RED, align="center", leading=36)
    text_block(d, W // 2, 140,
               ["THE DAY'S NEWS IN ONE PAGE  •  SIX STORIES, FIVE CONTINENTS"],
               SANS(15), fill=GREY, align="center", leading=20)
    rule(d, m, 166, W - m, 3)

    # ---- lead story ----
    ly = 182
    pic_tanker(d, m, ly, 446, 272)
    tx = m + 466
    tw = W - m - tx
    d.text((tx, ly + 2), "EGYPT  •  LEAD STORY", font=SANS_B(19), fill=RED)
    y = text_block(d, tx, ly + 34,
                   ["FIRE ON CAIRO", "RING ROAD KILLS", "AT LEAST 31"],
                   SERIF_B(42), leading=50)
    y = text_block(d, tx, y + 10,
                   wrap(d, "A fuel tanker overturned and exploded, "
                        "charring dozens of cars and motorcycles.",
                        SANS(20), tw), SANS(20), leading=26)
    text_block(d, tx, y + 8,
               ["Death toll updated to 31, health ministry says — AP"],
               SANS(15), fill=GREY, leading=20)
    rule(d, m, 468, W - m, 2)

    # ---- card rows: 3 on top, 2 wide below ----
    cw, gap = 320, 8
    cy = 482
    ch = 240
    for i in range(3):
        kicker, headline, deck, pic = CARDS[i]
        draw_card(d, m + i * (cw + gap), cy, cw, ch,
                  kicker, headline, deck, pic)
    cy2 = cy + ch + 12
    w2 = (W - 2 * m - gap) // 2
    for j in range(2):
        kicker, headline, deck, pic = CARDS[3 + j]
        draw_card(d, m + j * (w2 + gap), cy2, w2, 170,
                  kicker, headline, deck, pic, horizontal=True)

    # ---- footer ----
    fy = cy2 + 170 + 14
    rule(d, m, fy, W - m, 2)
    foot = ("ALSO TODAY:  Second US judge blocks Trump's birthright order  •  "
            "Saudi defences down a Houthi missile  •  Duran Duran guitarist "
            "Andy Taylor dies at 65")
    text_block(d, m, fy + 10,
               wrap(d, foot, SANS_B(15), W - 2 * m), SANS_B(15), leading=20)
    text_block(d, W // 2, H - 26,
               ["Sources: AP, Reuters, Xinhua / CMSA, KCNA, Chess.com"],
               SANS(13), fill=GREY, align="center", leading=16)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
