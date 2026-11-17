"""Thumbnail: one hero sneaker mid-stride (white sticker outline) bursting out of a step ring at 10,000, warm vs cool
gradient, the title word for word with 10,000 in gold. Bottom-right kept clear. Run: KR_RUN=... python3 video/thumbs.py"""
import math
import skia
from krwi.lib import *  # noqa: F401,F403
from krwi.thumb import canvas, save, compare
from art import *  # noqa: F401,F403


def sticker(c, draw, pad=14, w=1920, h=1080):
    """Draw `draw(k)` with a thick white sticker outline around everything it paints."""
    s = skia.Surface(w * 2, h * 2)
    k = s.getCanvas(); k.scale(2, 2)
    draw(k)
    img = s.makeImageSnapshot()
    out = skia.Paint(ImageFilter=skia.ImageFilters.ColorFilter(
        skia.ColorFilters.Blend(skia.Color(255, 255, 255), skia.BlendMode.kSrcIn), skia.ImageFilters.Dilate(pad * 2, pad * 2)))
    sh = skia.Paint(ImageFilter=skia.ImageFilters.DropShadowOnly(0, 24, 30, 30, skia.Color4f(0.05, 0.02, 0.1, 0.6)))
    r = skia.Rect(0, 0, w, h)
    c.drawImageRect(img, r, skia.SamplingOptions(), sh)
    c.drawImageRect(img, r, skia.SamplingOptions(), out)
    c.drawImageRect(img, r, skia.SamplingOptions())


def bg(c):
    c.drawRect(skia.Rect(0, 0, W, H), hgrad(0, W, ["#FF7A2F", "#E5306A", "#5B2BC8", "#1E6BFF"], [0, 0.38, 0.72, 1]))
    cx, cy = 1450, 480
    for k in range(18):   # light burst rays
        a0 = k * 20 + 5
        p = skia.Path(); p.moveTo(cx, cy)
        p.lineTo(cx + 1600 * math.cos(math.radians(a0)), cy + 1600 * math.sin(math.radians(a0)))
        p.lineTo(cx + 1600 * math.cos(math.radians(a0 + 8)), cy + 1600 * math.sin(math.radians(a0 + 8)))
        p.close()
        c.drawPath(p, paint("#FFF3C4", 0.10))
    glow(c, cx, cy, 620, "#FFE9A8", 0.9)
    glow(c, cx, cy, 300, "#FFFFFF", 0.7)
    vignette(c, W, H, 0.35)


def hero(k):
    cx, cy = 1450, 480
    k.drawCircle(cx, cy, 330, paint("#14203E", 0.92))
    ring = skia.Path(); ring.addArc(skia.Rect(cx - 300, cy - 300, cx + 300, cy + 300), -90, 359.9)
    k.drawPath(ring, paint("#3BB273", stroke=46))
    sneaker(k, 1480, 640, 1.9, rot=-12)


def main():
    s, c = canvas()
    bg(c)
    for j in range(5):
        shoe_print(c, 1000 + j * 90, 1010 - j * 60, 1.0, rot=-35, a=0.35 + 0.1 * j)
    sticker(c, hero)
    pill(c, 1450, 110, 1.0, "10,000 / DAY", "#3BB273", "cream", 64)
    # title, word for word, left side, 3 lines
    for txt, y, size, colr in (("WHAT IF YOU WALKED", 250, 92, "cream"), ("10,000 STEPS", 420, 150, "gold"),
                               ("EVERY DAY", 560, 104, "cream"), ("FOR A YEAR?", 690, 104, "cream")):
        f = font("extrabold", size)
        st = paint("#1A0C2E", stroke=22); st.setStrokeJoin(skia.Paint.kRound_Join)
        text(c, txt, 90, y, f, st, align="left")
        text(c, txt, 90, y, f, paint(colr), align="left")
    path = save(s, "THUMB.jpg")
    compare([path])


if __name__ == "__main__":
    main()
