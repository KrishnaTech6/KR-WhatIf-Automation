"""Thumbnail for 'What If UPI Stopped Working for One Week?' (rules: brand/thumbnail_rules.md).
One thumbnail; text = the title; hero = a phone with PAYMENT FAILED and a cracking QR code."""
import math
import skia
from art import *  # noqa: F401,F403
from krwi.thumb import canvas, save, compare

T0 = 0.0


def outline_text(c, s, x, y, size, color="cream", stroke=18, kind="extrabold"):
    f = font(kind, size)
    sh = paint("#000000", 0.55); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 12))
    c.drawString(s, x + 6, y + 10, f, sh)
    c.drawString(s, x, y, f, paint("#120A24", stroke=stroke))
    c.drawString(s, x, y, f, paint(color))


def words(c, parts, x, y, size):
    """parts = [(text, color), ...] drawn on one line from x."""
    f = font("extrabold", size)
    for s, colr in parts:
        outline_text(c, s, x, y, size, colr)
        x += text_w(s, f)


def cracked_phone(c, x, y, s):
    phone(c, x, y, s, T0, key="thumbphone", screen="failed", p=1.0, rot=-8)
    # cracks over the screen
    c.save(); c.rotate(-8, x, y)
    c.clipRect(skia.Rect(x - 150 * s, y - 300 * s, x + 150 * s, y + 300 * s))
    crack = paint("#FFFFFF", 0.85, stroke=5)
    for k in range(7):
        a = k / 7 * 2 * math.pi + 0.3
        p = skia.Path(); px, py = x + 60 * s, y + 140 * s
        p.moveTo(px, py)
        for j in range(4):
            px += math.cos(a + (rng(k * 9 + j) - 0.5)) * 55 * s
            py += math.sin(a + (rng(k * 7 + j) - 0.5)) * 55 * s
            p.lineTo(px, py)
        c.drawPath(p, crack)
    c.restore()


def thumb(c):
    lin(c, 0, 0, W, H, ["#0E2A5C", "#2B1460", "#7A1E5A"], [0, 0.55, 1])
    # light burst behind the hero (warm on cool)
    cx, cy = 1360, 470
    for i in range(18):
        a = i / 18 * 2 * math.pi
        p = skia.Path(); p.moveTo(cx, cy)
        p.lineTo(cx + math.cos(a - 0.08) * 1400, cy + math.sin(a - 0.08) * 1400)
        p.lineTo(cx + math.cos(a + 0.08) * 1400, cy + math.sin(a + 0.08) * 1400); p.close()
        c.drawPath(p, paint("#FFB347", 0.16))
    glow(c, cx, cy, 700, "#FF8A3D", 0.95)
    glow(c, cx, cy, 300, "#FFE3A3", 0.6)
    cracked_phone(c, cx, cy + 20, 1.32)
    chai(c, 1080, 860, 1.0, T0, key="thumbchai", steam=True)
    # title, word for word, key words in gold
    words(c, [("WHAT IF ", "cream"), ("UPI", "gold")], 70, 250, 150)
    words(c, [("STOPPED", "cream")], 70, 420, 150)
    words(c, [("WORKING FOR", "cream")], 70, 585, 128)
    words(c, [("ONE WEEK?", "gold")], 70, 760, 150)
    vignette(c, W, H, 0.35)


if __name__ == "__main__":
    s, c = canvas()
    thumb(c)
    p = save(s, "THUMB.jpg")
    compare([p])
