"""Thumbnail for 'What If Every Indian Got Rs 1 Crore Tomorrow?' (rules: brand/thumbnail_rules.md).
One thumbnail (package 1); text = the title; hero = the phone glowing '1,00,00,000 CREDITED' with paper note bundles
spilling out (the outer ones crumbling into confetti) and a red-marker price tag '2 LAKH?'.
Run: KR_RUN=runs/every-indian-1-crore PYTHONPATH=tools python3 runs/every-indian-1-crore/video/thumbs.py"""
import math
import skia
from art import *  # noqa: F401,F403
from krwi.thumb import canvas, save, compare

T0 = 0.0
CREAM, GOLD_T = "#FFF6E0", "#FFC83D"


def outline_text(c, s, x, y, size, color=CREAM, stroke=20):
    f = font("extrabold", size)
    sh = paint("#000000", 0.55); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 12))
    c.drawString(s, x + 6, y + 10, f, sh)
    c.drawString(s, x, y, f, paint("#16081F", stroke=stroke))
    c.drawString(s, x, y, f, paint(color))


def line(c, parts, x, y, size, max_w):
    """parts = [(text, colour)] on one line from x, shrunk to fit max_w."""
    f = font("extrabold", size)
    w = sum(text_w(s, f) for s, _ in parts)
    if w > max_w:
        size *= max_w / w; f = font("extrabold", size)
    for s, colr in parts:
        outline_text(c, s, x, y, size, colr, stroke=size * 0.13)
        x += text_w(s, f)


def burst(c, cx, cy):
    for i in range(20):
        a = i / 20 * 2 * math.pi
        p = skia.Path(); p.moveTo(cx, cy)
        p.lineTo(cx + math.cos(a - 0.07) * 1500, cy + math.sin(a - 0.07) * 1500)
        p.lineTo(cx + math.cos(a + 0.07) * 1500, cy + math.sin(a + 0.07) * 1500); p.close()
        c.drawPath(p, paint("#FFD27A", 0.17))
    glow(c, cx, cy, 720, "#FF9A3D", 0.95)
    glow(c, cx, cy, 320, "#FFF0C2", 0.7)


def thumb(c):
    lin(c, 0, 0, W, H, ["#0B2A6B", "#3A1670", "#8A1F5C"], [0, 0.55, 1])     # cool -> warm
    cx, cy = 1400, 470
    burst(c, cx, cy)
    # note bundles spilling out of the phone: solid near it, crumbling into confetti at the edges
    for i, (bx, by, r, cr) in enumerate([(1130, 760, -18, 0.0), (1660, 770, 16, 0.0), (1010, 560, -30, 0.55),
                                         (1800, 560, 28, 0.6), (930, 360, -38, 0.9), (1860, 330, 34, 0.95)]):
        bundle(c, bx, by, 1.05, T0, key=f"tb{i}", rot=r, crumble=cr)
    phone_msg(c, cx, cy + 10, 1.22, T0, [("₹1,00,00,000", 64, "#1F6E43"), ("CREDITED", 54, "#1F6E43")],
              key="thumbphone", rot=-6, head="BANK")
    # a big green tick fills the lower half of the screen
    c.save(); c.rotate(-6, cx, cy + 10)
    tx, ty = cx, cy + 10 + 200
    glow(c, tx, ty, 160, "#7CFFB0", 0.35)
    c.drawCircle(tx, ty, 92, paint("#1F8A4C"))
    m = skia.Path(); m.moveTo(tx - 44, ty + 2); m.lineTo(tx - 12, ty + 36); m.lineTo(tx + 48, ty - 34)
    c.drawPath(m, paint("#FFFFFF", stroke=22))
    c.restore()
    # red-marker price tag; text placed left of the string hole
    tgx, tgy, tgs = 1690, 175, 1.1
    price_tag(c, tgx, tgy, tgs, T0, "", key="thumbtag", rot=10)
    c.save(); c.rotate(10, tgx, tgy - 120 * tgs)
    type_text(c, "₹2 LAKH?", tgx - 40 * tgs, tgy, 52 * tgs, 1.0, color=RED_INK)
    c.restore()
    # title, word for word; the key words in gold
    x, mw = 60, 900
    line(c, [("WHAT IF EVERY", CREAM)], x, 230, 140, mw)
    line(c, [("INDIAN GOT", CREAM)], x, 410, 150, mw)
    line(c, [("₹1 CRORE", GOLD_T)], x, 640, 220, mw)
    line(c, [("TOMORROW?", CREAM)], x, 820, 150, mw)
    vignette(c, W, H, 0.3)


if __name__ == "__main__":
    s, c = canvas()
    thumb(c)
    p = save(s, "THUMB.jpg")
    compare([p])
