"""Thumbnail for 'What If You Stopped Paying Your EMI?' (rules: brand/thumbnail_rules.md).
One thumbnail; text = the title; hero = a padlocked house with a red AUCTION stamp, the phone says EMI BOUNCED."""
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
    f = font("extrabold", size)
    for s, colr in parts:
        outline_text(c, s, x, y, size, colr)
        x += text_w(s, f)


def big_stamp(c, x, y, label, size, rot):
    c.save(); c.translate(x, y); c.rotate(rot)
    f = font("extrabold", size)
    w = text_w(label, f) + 60
    h = size * 1.25
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-w / 2, -h / 2, w / 2, h / 2), 14, 14), paint("#FFFFFF", 0.92))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-w / 2, -h / 2, w / 2, h / 2), 14, 14), paint("#D62828", stroke=14))
    c.drawString(label, -text_w(label, f) / 2, size * 0.36, f, paint("#D62828"))
    c.restore()


def thumb(c):
    lin(c, 0, 0, W, H, ["#0E2A5C", "#2B1460", "#7A1E5A"], [0, 0.55, 1])
    cx, cy = 1380, 520
    for i in range(18):
        a = i / 18 * 2 * math.pi
        p = skia.Path(); p.moveTo(cx, cy)
        p.lineTo(cx + math.cos(a - 0.08) * 1400, cy + math.sin(a - 0.08) * 1400)
        p.lineTo(cx + math.cos(a + 0.08) * 1400, cy + math.sin(a + 0.08) * 1400); p.close()
        c.drawPath(p, paint("#FFB347", 0.16))
    glow(c, cx, cy, 700, "#FF8A3D", 0.95)
    glow(c, cx, cy, 300, "#FFE3A3", 0.6)
    house(c, 1460, 940, 1.9, T0, key="th_house")
    padlock(c, 1460, 840, 2.4, T0, key="th_lock")
    big_stamp(c, 1460, 600, "AUCTION", 104, -8)
    smartphone(c, 1080, 860, 0.62, T0, [("EMI\nBOUNCED", "#C0392B")], 1.0, title="BANK ALERT", key="th_phone", rot=-12)
    words(c, [("WHAT IF YOU", "cream")], 60, 220, 128)
    words(c, [("STOPPED", "cream")], 60, 390, 150)
    words(c, [("PAYING YOUR", "cream")], 60, 550, 128)
    words(c, [("EMI?", "gold")], 60, 760, 200)
    vignette(c, W, H, 0.35)


if __name__ == "__main__":
    s, c = canvas()
    thumb(c)
    p = save(s, "THUMB.jpg")
    compare([p])
