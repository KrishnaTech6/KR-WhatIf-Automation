"""Thumbnail for 'What If You Didn't Use Your Phone for 30 Days?' (rules: brand/thumbnail_rules.md).
One thumbnail; text = the title; hero = a glowing phone locked inside a glass jar, notifications piling up on the glass."""
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


def jar(c, cx, cy):
    # glass jar body + lid, phone inside, notification bubbles pressed against the glass
    body = skia.RRect.MakeRectXY(skia.Rect(cx - 300, cy - 330, cx + 300, cy + 380), 90, 90)
    c.drawRRect(body, paint("#BFE8FF", 0.16))
    smartphone(c, cx, cy + 40, 0.92, T0, "notifs", rot=-6, glow_a=0.9, notifs=99)
    for i, (dx, dy, r) in enumerate([(-200, -200, -8), (170, -120, 6), (-210, 120, 4), (190, 220, -5), (-60, -280, 3)]):
        c.save(); c.translate(cx + dx, cy + dy); c.rotate(r)
        bubble(c, 0, 0, 0.8, 1.0, i=i)
        c.restore()
    c.drawRRect(body, paint("#FFFFFF", 0.85, stroke=14))                  # white sticker outline
    c.drawRRect(body, paint("#9FD8FF", 0.6, stroke=5))
    hl = skia.Path(); hl.moveTo(cx - 230, cy - 230); hl.quadTo(cx - 260, cy + 50, cx - 220, cy + 280)
    c.drawPath(hl, paint("#FFFFFF", 0.55, stroke=22))                      # glass highlight
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(cx - 320, cy - 420, cx + 320, cy - 330), 26, 26), paint("#C9CCD6"))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(cx - 320, cy - 420, cx + 320, cy - 330), 26, 26), paint("#FFFFFF", stroke=10))
    for k in range(9):
        c.drawLine(cx - 290 + k * 72, cy - 410, cx - 290 + k * 72, cy - 340, paint("#9AA0B0", stroke=6))
    padlock(c, cx + 250, cy - 330, 0.9, 1.0)


def thumb(c):
    lin(c, 0, 0, W, H, ["#0E2A5C", "#2B1460", "#7A1E5A"], [0, 0.55, 1])
    cx, cy = 1400, 560
    for i in range(18):
        a = i / 18 * 2 * math.pi
        p = skia.Path(); p.moveTo(cx, cy)
        p.lineTo(cx + math.cos(a - 0.08) * 1400, cy + math.sin(a - 0.08) * 1400)
        p.lineTo(cx + math.cos(a + 0.08) * 1400, cy + math.sin(a + 0.08) * 1400); p.close()
        c.drawPath(p, paint("#FFB347", 0.16))
    glow(c, cx, cy, 700, "#FF8A3D", 0.9)
    glow(c, cx, cy, 300, "#FFE3A3", 0.55)
    jar(c, cx, cy)
    day_tile(c, 1760, 330, 1.05, 1.0, "30")
    words(c, [("WHAT IF YOU", "cream")], 60, 230, 128)
    words(c, [("DIDN'T USE", "cream")], 60, 390, 128)
    words(c, [("YOUR PHONE", "cream")], 60, 550, 128)
    words(c, [("FOR ", "cream"), ("30 DAYS?", "gold")], 60, 730, 150)
    vignette(c, W, H, 0.3)


if __name__ == "__main__":
    s, c = canvas()
    thumb(c)
    p = save(s, "THUMB.jpg")
    compare([p])
