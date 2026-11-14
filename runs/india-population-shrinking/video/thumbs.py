"""Thumbnail for 'What If India's Population Started Shrinking?' (rules: brand/thumbnail_rules.md).
One thumbnail; text = the title; hero = India as a sticker cut-out full of people, a chunk of the crowd
falling off its edge, a red -20 CRORE stamp."""
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


def thumb(c):
    lin(c, 0, 0, W, H, ["#0F5E5A", "#0B3D4A", "#14213D"], [0, 0.5, 1])
    cx, cy = 1480, 560
    # big warm sun-disc behind the map (not rays): saffron rings
    for r, colr, a in [(640, "#E76F51", 0.45), (520, "#E76F51", 0.7), (400, "#D9573D", 0.85)]:
        c.drawCircle(cx, cy, r, paint(colr, a))
    glow(c, cx, cy, 300, "#FF9F6B", 0.6)
    # India as a thick white-outlined sticker
    k = 27
    c.save()
    sh = paint("#000000", 0.5); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 22))
    c.restore()
    c.save(); c.translate(12, 18)
    c.saveLayer(None, skia.Paint(ColorFilter=skia.ColorFilters.Blend(col("#000000", 0.45), skia.BlendMode.kSrcIn)))
    india_map(c, cx, cy, k)
    c.restore(); c.restore()
    india_map(c, cx, cy, k)
    # a crowd on the map, thinning towards the south-east edge where people fall off
    for i in range(70):
        x = cx + (rng(i, 2) - 0.5) * k * 12 - 20
        y = cy + (rng(i, 3) - 0.5) * k * 14 - 60
        cutout(c, lambda kk, x=x, y=y, i=i: figure(kk, x, y, 0.22, i=i, female=i % 2 == 0), border=3, shadow=(2, 3))
    for i in range(5):
        x = cx - 330 - i * 40
        y = cy + 120 + i * 85
        c.save(); c.rotate(-30 - i * 22, x, y - 40)
        cutout(c, lambda kk, x=x, y=y, i=i: figure(kk, x, y, 0.28, i=i + 3, female=i % 2 == 1), border=3, shadow=(3, 5))
        c.restore()
    sx, sy, sw, shh = cx - 420, cy - 20, 760, 200
    c.save(); c.rotate(-12, sx + sw / 2, sy + shh / 2)
    sh = paint("#000000", 0.55); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 18))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(sx + 8, sy + 22, sx + sw + 18, sy + shh + 32), 36, 36), sh)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(sx - 10, sy - 10, sx + sw + 10, sy + shh + 10), 36, 36), paint("#FFFFFF"))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(sx, sy, sx + sw, sy + shh), 28, 28), paint("#D62828"))
    outline_text(c, "−20 CRORE", sx + 45, sy + 152, 142, "gold", stroke=16)
    c.restore()
    # title, word for word, key word in gold
    words(c, [("WHAT IF ", "cream"), ("INDIA'S", "gold")], 60, 250, 132)
    words(c, [("POPULATION", "cream")], 60, 410, 132)
    words(c, [("STARTED", "cream")], 60, 570, 132)
    words(c, [("SHRINKING?", "gold")], 60, 740, 140)
    vignette(c, W, H, 0.35)


if __name__ == "__main__":
    s, c = canvas()
    thumb(c)
    p = save(s, "THUMB.jpg")
    compare([p])
