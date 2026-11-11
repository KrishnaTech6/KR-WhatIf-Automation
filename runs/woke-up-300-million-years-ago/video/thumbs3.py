"""Thumbnails v3: thumbnail-style backgrounds (bold gradient, light burst, sticker outline). No KR; text = title."""
import os, math, skia
from art import *  # noqa
from art import W, H
import thumbs2 as T2
OUT = T2.OUT
T0 = 1.3


def radial_bg(c, cx, cy, inner, outer, r=1300):
    sh = skia.GradientShader.MakeRadial(skia.Point(cx, cy), r, [col(inner), col(outer)], [0.0, 1.0])
    c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Shader=sh))


def burst(c, cx, cy, color, n=24, a=0.18, L=1800):
    for i in range(n):
        ang = 2 * math.pi * i / n
        p = skia.Path(); p.moveTo(cx, cy)
        p.lineTo(cx + math.cos(ang - 0.06) * L, cy + math.sin(ang - 0.06) * L)
        p.lineTo(cx + math.cos(ang + 0.06) * L, cy + math.sin(ang + 0.06) * L); p.close()
        c.drawPath(p, paint(color, a))


def sticker(c, draw, outline="white", r=9, glow_col=None):
    """draw() paints the hero on a transparent layer; we add a solid outline + optional glow behind it."""
    S = skia.Surface(W, H); cc = S.getCanvas(); cc.clear(skia.Color(0, 0, 0, 0)); draw(cc)
    img = S.makeImageSnapshot()
    if glow_col:
        p = skia.Paint(); p.setImageFilter(skia.ImageFilters.Blur(40, 40, skia.TileMode.kDecal, skia.ImageFilters.ColorFilter(
            skia.ColorFilters.Blend(col(glow_col), skia.BlendMode.kSrcIn), None)))
        p.setAlphaf(0.9); c.drawImage(img, 0, 0, skia.SamplingOptions(), p)
    p = skia.Paint(); p.setImageFilter(skia.ImageFilters.Dilate(r, r, skia.ImageFilters.ColorFilter(
        skia.ColorFilters.Blend(col(outline), skia.BlendMode.kSrcIn), None)))
    c.drawImage(img, 0, 0, skia.SamplingOptions(), p)
    c.drawImage(img, 0, 0)


def tree_silhouettes(c, color, a=1.0, side_only=True):
    for i, (x, h, w) in enumerate([(-30, 980, 120), (150, 820, 80), (1810, 1000, 130), (1650, 760, 70)]):
        p = paint(color, a)
        c.drawRect(skia.Rect(x - w / 2, H - h, x + w / 2, H), p)
        cx, top = x, H - h
        for k in range(9):
            ang = math.pi / 2 + (k - 4) * 0.28
            c.drawLine(cx, top, cx + math.cos(ang) * 230, top - math.sin(ang) * 170, paint(color, a, stroke=16))


def thumb_a(c):
    """Giant dragonfly, bright burst, cool teal bg vs warm gold subject glow."""
    radial_bg(c, 1450, 430, "#2FB7A5", "#06202A", 1250)
    burst(c, 1450, 430, "#E9FFF6", 26, 0.10)
    glow(c, 1450, 430, 520, "#FFF3C4", 0.55)
    tree_silhouettes(c, "#04161C", 0.9)
    sticker(c, lambda cc: dragonfly(cc, 1450, 360, 1.6, 0.37, ang=-6), "white", 3, "gold")
    sticker(c, lambda cc: T2.person(cc, 1170, 1060, 330, "stand", "#04161C"), "white", 5)
    T2.title_block(c)
    vignette(c, W, H, 0.45)


def thumb_b(c):
    """Movie-poster scale: tiny person, towering black trees, orange sunset burst."""
    radial_bg(c, 1450, 520, "#FFB347", "#5A0F2E", 1300)
    burst(c, 1450, 520, "#FFE8B0", 22, 0.12)
    glow(c, 1450, 560, 360, "#FFF1C8", 0.8)
    for i, (x, h, w) in enumerate([(1030, 700, 60), (1240, 560, 40), (1720, 720, 70), (1890, 600, 50), (1560, 470, 28)]):
        lycopsid(c, x, H + 5, h, w, T0, i + 30)
        c.drawRect(skia.Rect(x - w * 1.4, 0, x + w * 1.4, H), paint("#1A0710", 0.0))
    c.drawRect(skia.Rect(860, 0, W, H), paint("#1A0710", 0.0))
    # turn the trees into silhouettes by overpainting them dark (keep the bright sky)
    S = skia.Surface(W, H); cc = S.getCanvas(); cc.clear(skia.Color(0, 0, 0, 0))
    for i, (x, h, w) in enumerate([(1030, 700, 60), (1240, 560, 40), (1720, 720, 70), (1890, 600, 50), (1560, 470, 28)]):
        lycopsid(cc, x, H + 5, h, w, T0, i + 30)
    p = skia.Paint(); p.setColorFilter(skia.ColorFilters.Blend(col("#1A0710"), skia.BlendMode.kSrcIn))
    c.drawImage(S.makeImageSnapshot(), 0, 0, skia.SamplingOptions(), p)
    c.drawRect(skia.Rect(0, 990, W, H), paint("#1A0710"))
    sticker(c, lambda cc: dragonfly(cc, 1450, 300, 1.1, 0.4, ang=8), "white", 3, "gold")
    sticker(c, lambda cc: T2.person(cc, 1450, 995, 170, "stand", "#1A0710"), "#FFE8B0", 4)
    T2.title_block(c)
    vignette(c, W, H, 0.4)


def thumb_c(c):
    """Glowing bulb with the forest inside, purple bg + yellow burst."""
    radial_bg(c, 1520, 450, "#6A2C9A", "#12061F", 1250)
    burst(c, 1520, 450, "#FFE27A", 28, 0.13)
    glow(c, 1520, 450, 650, "#FFD27A", 0.55)
    c.drawLine(1520, 0, 1520, 120, paint("#12061F", stroke=12))
    import thumbs as T1
    sticker(c, lambda cc: T1.bulb_forest(cc, 1520, 450, 330), "white", 7)
    T2.title_block(c)
    vignette(c, W, H, 0.45)


if __name__ == "__main__":
    import thumbs as T1
    ps = [T2.render(thumb_a, "THUMB_A.jpg"), T2.render(thumb_b, "THUMB_B.jpg"), T2.render(thumb_c, "THUMB_C.jpg")]
    T1.sheet(ps)
    for p in ps: print(p, os.path.getsize(p))


def thumb_one(c):
    """Single thumbnail: sunset poster + giant dragonfly hero + tiny person for scale."""
    radial_bg(c, 1430, 470, "#FFB347", "#5A0F2E", 1300)
    burst(c, 1430, 470, "#FFE8B0", 24, 0.12)
    glow(c, 1430, 470, 420, "#FFF1C8", 0.75)
    S = skia.Surface(W, H); cc = S.getCanvas(); cc.clear(skia.Color(0, 0, 0, 0))
    for i, (x, h, w) in enumerate([(1000, 760, 60), (1190, 600, 40), (1780, 780, 70), (1640, 520, 32), (1900, 640, 50)]):
        lycopsid(cc, x, H + 5, h, w, T0, i + 30)
    p = skia.Paint(); p.setColorFilter(skia.ColorFilters.Blend(col("#1A0710"), skia.BlendMode.kSrcIn))
    c.drawImage(S.makeImageSnapshot(), 0, 0, skia.SamplingOptions(), p)
    c.drawRect(skia.Rect(0, 1000, W, H), paint("#1A0710"))
    sticker(c, lambda cc: dragonfly(cc, 1430, 360, 1.6, 0.37, ang=-6), "white", 3, "gold")
    sticker(c, lambda cc: T2.person(cc, 1250, 1005, 200, "stand", "#1A0710"), "#FFE8B0", 4)
    T2.title_block(c)
    vignette(c, W, H, 0.4)


def bed_wakeup(c, x, base, s, color="#1A0710", rim="#FFE8B0"):
    """Silhouette: a bed, and a faceless person sitting up in it with one arm raised (just woke up)."""
    c.save(); c.translate(x, base); c.scale(s, s)
    p = skia.Path()
    p.addRect(skia.Rect(-260, -70, 260, -30))                     # mattress
    p.addRect(skia.Rect(-280, -190, -250, 0)); p.addRect(skia.Rect(250, -110, 275, 0))   # head/foot boards
    p.addRect(skia.Rect(-250, -30, -235, 0)); p.addRect(skia.Rect(235, -30, 250, 0))
    blanket = skia.Path(); blanket.moveTo(-120, -70); blanket.cubicTo(-60, -120, 120, -110, 250, -80); blanket.lineTo(250, -60); blanket.lineTo(-120, -60); blanket.close()
    p = skia.Op(p, blanket, skia.PathOp.kUnion_PathOp)
    torso = skia.Path(); torso.moveTo(-170, -70); torso.lineTo(-150, -190); torso.lineTo(-110, -195); torso.lineTo(-95, -70); torso.close()
    p = skia.Op(p, torso, skia.PathOp.kUnion_PathOp)
    head = skia.Path(); head.addCircle(-128, -222, 26); p = skia.Op(p, head, skia.PathOp.kUnion_PathOp)
    arm = skia.Path(); arm.moveTo(-112, -185); arm.lineTo(-40, -270); arm.lineTo(-28, -260); arm.lineTo(-98, -170); arm.close()
    p = skia.Op(p, arm, skia.PathOp.kUnion_PathOp)
    pillow = skia.Path(); pillow.addRRect(skia.RRect.MakeRectXY(skia.Rect(-245, -100, -170, -70), 14, 14)); p = skia.Op(p, pillow, skia.PathOp.kUnion_PathOp)
    c.drawPath(p, paint(color))
    c.drawPath(p, paint(rim, 0.55, stroke=3))
    c.restore()


def thumb_wakeup(c):
    """You just woke up in bed 300 million years ago: giant dragonfly over the bed, forest silhouettes, sunset burst."""
    radial_bg(c, 1400, 430, "#FFB347", "#5A0F2E", 1300)
    burst(c, 1400, 430, "#FFE8B0", 24, 0.12)
    glow(c, 1400, 430, 420, "#FFF1C8", 0.75)
    S = skia.Surface(W, H); cc = S.getCanvas(); cc.clear(skia.Color(0, 0, 0, 0))
    for i, (x, h, w) in enumerate([(980, 760, 60), (1170, 560, 36), (1820, 780, 70), (1660, 520, 30), (1930, 640, 50)]):
        lycopsid(cc, x, H + 5, h, w, T0, i + 30)
    for i in range(6):
        tree_fern(cc, 900 + i * 210, 1010, 140 + 40 * (i % 2), T0, i, 0.8)
    p = skia.Paint(); p.setColorFilter(skia.ColorFilters.Blend(col("#1A0710"), skia.BlendMode.kSrcIn))
    c.drawImage(S.makeImageSnapshot(), 0, 0, skia.SamplingOptions(), p)
    c.drawRect(skia.Rect(0, 1000, W, H), paint("#1A0710"))
    bed_wakeup(c, 1330, 1005, 1.15)
    sticker(c, lambda cc: dragonfly(cc, 1420, 330, 1.45, 0.37, ang=-8), "white", 3, "gold")
    T2.title_block(c)
    vignette(c, W, H, 0.4)
