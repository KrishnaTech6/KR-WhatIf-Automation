"""Thumbnail for 'What If You Ate Only Maggi for 30 Days?' (rules: brand/thumbnail_rules.md).
One thumbnail; text = the title word for word; hero = our big glossy noodle bowl with a red warning glow, a salt heap
3x over the daily-limit line, and a torn DAY 30 page (the same pieces as the hook's first shot). No KR, no real logo."""
import math
import os
import skia
from art import *  # noqa: F401,F403
from krwi.thumb import canvas, save, compare

T0 = 0.6


def outline_text(c, s, x, y, size, color="cream", stroke=20, kind="extrabold"):
    f = font(kind, size)
    sh = paint("#000000", 0.6); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 14))
    c.drawString(s, x + 8, y + 12, f, sh)
    c.drawString(s, x, y, f, paint("#120A24", stroke=stroke))
    c.drawString(s, x, y, f, paint(color))


def words(c, parts, x, y, size):
    f = font("extrabold", size)
    for s, colr in parts:
        outline_text(c, s, x, y, size, colr)
        x += text_w(s, f)


def background(c):
    # bold saturated gradient: hot magenta/orange (warm, left) to electric blue (cool, right)
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(W, H)],
                [col("#FF6A2A"), col("#C2185B"), col("#3A1C8A"), col("#1E6FD9")], [0, 0.38, 0.7, 1]))
    c.drawRect(skia.Rect(0, 0, W, H), p)
    # light burst behind the hero
    cx, cy = 600, 700
    for k in range(24):
        a0 = k * 15
        ray = skia.Path(); ray.moveTo(cx, cy)
        ray.lineTo(cx + 2000 * math.cos(math.radians(a0)), cy + 2000 * math.sin(math.radians(a0)))
        ray.lineTo(cx + 2000 * math.cos(math.radians(a0 + 6)), cy + 2000 * math.sin(math.radians(a0 + 6)))
        ray.close()
        c.drawPath(ray, paint("#FFE9A0", 0.10))
    rg = skia.Paint(AntiAlias=True)
    rg.setShader(skia.GradientShader.MakeRadial(skia.Point(cx, cy), 620, [col("#FFF4C0", 0.95), col("#FFB347", 0.5), col("#FF6A2A", 0.0)], [0, 0.35, 1]))
    c.drawRect(skia.Rect(0, 0, W, H), rg)


def sticker_bowl(c, x, y, s):
    """White sticker outline around the bowl silhouette, then the hero bowl itself."""
    c.save(); c.translate(x, y); c.scale(s, s)
    sil = skia.Path()
    sil.addOval(skia.Rect(-300, -82, 300, 82))
    b = skia.Path(); b.moveTo(-300, 0); b.cubicTo(-292, 170, -150, 245, 0, 245); b.cubicTo(150, 245, 292, 170, 300, 0); b.close()
    sil.addPath(b)
    c.drawPath(sil, paint("white", stroke=70))
    c.restore()
    bowl(c, x, y, s, T0, warn=1.0, steam_a=1.0)
    c.save(); c.translate(x, y); c.scale(s, s)
    rimp = skia.Path(); rimp.addArc(skia.Rect(-300, -82, 300, 82), 0, 180)
    c.drawPath(rimp, paint("#FF3A2A", 0.9, stroke=10))
    c.restore()


PHOTO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ref", "krishna_packet_photo.jpg")


def photo_sticker(c, cx, cy, w, rot):
    """The photo, cropped tight on the packet + noodle block, graded warmer/contrastier, as a tilted sticker:
    thick white border, rounded corners, drop shadow, rim glow, a torn DAY 30 tag taped to its corner."""
    img = skia.Image.open(PHOTO)
    src = skia.Rect(0, 10, 678, 452)
    h = w * src.height() / src.width()
    c.save(); c.translate(cx, cy); c.rotate(rot)
    glow(c, 0, 0, w * 0.8, "#FFD23A", 0.35)
    sh = paint("#000000", 0.55); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 22))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-w / 2 - 6, -h / 2 + 10, w / 2 + 26, h / 2 + 40), 40, 40), sh)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-w / 2 - 22, -h / 2 - 22, w / 2 + 22, h / 2 + 22), 44, 44), paint("white"))
    k = 1.18; off = -0.06
    m = [k * 1.06, 0, 0, 0, off + 0.04,
         0, k, 0, 0, off + 0.01,
         0, 0, k * 0.9, 0, off - 0.03,
         0, 0, 0, 1, 0]
    pp = skia.Paint(AntiAlias=True); pp.setColorFilter(skia.ColorFilters.Matrix(m))
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect(-w / 2, -h / 2, w / 2, h / 2), 30, 30), True)
    c.drawImageRect(img, src, skia.Rect(-w / 2, -h / 2, w / 2, h / 2), skia.SamplingOptions(skia.CubicResampler.Mitchell()), pp)
    c.restore()
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-w / 2 - 22, -h / 2 - 22, w / 2 + 22, h / 2 + 22), 44, 44), paint("#FFD9A0", 0.9, stroke=6))
    # torn DAY 30 tag + tape on the top-right corner
    calendar_page(c, w / 2 - 40, -h / 2 + 10, 0.42, "DAY", "30", rot=14)
    c.save(); c.translate(w / 2 - 40, -h / 2 - 60); c.rotate(-30)
    c.drawRect(skia.Rect(-70, -18, 70, 18), paint("#F4F1E8", 0.75))
    c.restore()
    c.restore()


def thumb(c):
    background(c)
    # Krishna's own packet photo as a tilted sticker, right side (thumbnail only, never the video)
    photo_sticker(c, 1500, 430, 690, -8)
    # salt heap, 3x over the daily-limit line, red glow
    base, lim = 1040, 125
    salt_heap(c, 1160, base, 3 * lim, 380, T0, red=1.0)
    c.drawLine(930, base - lim, 1400, base - lim, paint("white", stroke=10))
    c.drawLine(930, base - lim, 1400, base - lim, dashed("#120A24", 1.0, 6, 26, 18))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(1250, base - lim + 16, 1530, base - lim + 76), 26, 26), paint("#120A24", 0.9))
    text(c, "DAILY LIMIT", 1390, base - lim + 60, font("extrabold", 38), paint("white"))
    outline_text(c, "3×", 1290, base - 3 * lim + 40, 150, "#FF4A3A", stroke=22)
    # hero bowl, big, with sticker outline
    glow(c, 560, 860, 640, "#FF1A1A", 0.6)
    sticker_bowl(c, 560, 720, 1.32)
    # the title, word for word, 3 lines
    words(c, [("WHAT IF YOU ATE", "white")], 50, 150, 128)
    words(c, [("ONLY MAGGI", "#FFD23A")], 50, 300, 150)
    words(c, [("FOR ", "white"), ("30 DAYS", "#FFD23A"), ("?", "white")], 50, 440, 128)


if __name__ == "__main__":
    s, c = canvas()
    thumb(c)
    p = save(s, "THUMB.jpg")
    compare([p])
