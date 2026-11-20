"""Thumbnail for 'What If You Woke Up at 5 AM for 30 Days?' (rules: brand/thumbnail_rules.md).
One thumbnail; text = the title; hero = a big twin-bell alarm clock at exactly 5:00, ringing, with a night sky
turning into sunrise behind it and a '30 DAYS' calendar page (the same pieces the video's first shots use)."""
import math
import skia
from art import *  # noqa: F401,F403
from krwi.thumb import canvas, save, compare


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


def thumb(c):
    # night (cool) at the top -> sunrise (warm) at the bottom right
    lin(c, 0, 0, W * 0.4, H, ["#0B1E52", "#3A1A6E", "#C2412E", "#FF9A3C"], [0, 0.45, 0.8, 1])
    for k in range(70):
        x, y = rng(k, 1) * W, rng(k, 2) * H * 0.45
        c.drawCircle(x, y, 1.5 + 2.5 * rng(k, 3), paint("cream", 0.5 + 0.4 * rng(k, 4)))
    cx, cy = 1430, 500
    for i in range(18):
        a = i / 18 * 2 * math.pi
        p = skia.Path(); p.moveTo(cx, cy)
        p.lineTo(cx + math.cos(a - 0.08) * 1400, cy + math.sin(a - 0.08) * 1400)
        p.lineTo(cx + math.cos(a + 0.08) * 1400, cy + math.sin(a + 0.08) * 1400); p.close()
        c.drawPath(p, paint("#FFB347", 0.15))
    glow(c, cx, cy, 720, "#FF8A3D", 0.85)
    glow(c, cx, cy, 320, "#FFE3A3", 0.6)
    # white sticker outline behind the clock
    c.drawCircle(cx, cy, 2.55 * 122 + 26, paint("#FFFFFF"))
    alarm_clock(c, cx, cy, 2.55, 0.37, ring=1.0, digital=False)
    # 30 DAYS calendar page
    c.save(); c.translate(1830, 160); c.rotate(10)
    c.drawRRect(rr(-120, -110, 120, 130, 18), paint("#FFFFFF"))
    c.drawRRect(rr(-108, -98, 108, 118, 14), paint("cream"))
    c.drawRRect(rr(-108, -98, 108, -36, 14), paint("coral")); c.drawRect(skia.Rect(-108, -52, 108, -36), paint("coral"))
    label(c, "30", 0, 66, 110, "ink", "extrabold")
    label(c, "DAYS", 0, 108, 34, "ink", "extrabold")
    c.restore()
    words(c, [("WHAT IF YOU", "cream")], 60, 250, 120)
    words(c, [("WOKE UP AT", "cream")], 60, 400, 120)
    words(c, [("5 AM", "gold")], 60, 620, 230)
    words(c, [("FOR 30 DAYS?", "cream")], 60, 790, 120)
    vignette(c, W, H, 0.25)


if __name__ == "__main__":
    s, c = canvas()
    thumb(c)
    p = save(s, "THUMB.jpg")
    compare([p])
