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


# ================================================================ v2 concepts (Krishna: v1 'very poor')
def title_block(c, x=90, lines=None, max_w=None):
    lines = lines or (("WHAT IF YOU WALKED", 92, "cream"), ("10,000 STEPS", 150, "gold"), ("EVERY DAY", 104, "cream"), ("FOR A YEAR?", 104, "cream"))
    y = 150
    for txt, size, colr in lines:
        y += size * 0.95
        f = font("extrabold", size)
        st = paint("#12081F", stroke=24); st.setStrokeJoin(skia.Paint.kRound_Join)
        text(c, txt, x, y, f, st, align="left")
        text(c, txt, x, y, f, paint(colr), align="left")
        y += size * 0.22


def limb(k, x0, y0, x1, y1, w, colr):
    p = paint(colr, stroke=w); p.setStrokeCap(skia.Paint.kRound_Cap)
    k.drawLine(x0, y0, x1, y1, p)


def walker_big(k, x, y, s, body="#1A1030", rim="#FFD27A"):
    """Big faceless walker in side view mid-stride (feet at y), hoodie + cap, strong warm rim light on the front."""
    k.save(); k.translate(x, y); k.scale(s, s)
    for colr, w_add, dx in ((rim, 18, 6), (body, 0, 0)):
        k.save(); k.translate(dx, -dx * 0.3)
        # back leg, back arm
        limb(k, -10, -430, -120, -230, 92 + w_add, colr); limb(k, -120, -230, -190, -30, 80 + w_add, colr)
        limb(k, -20, -780, -150, -600, 70 + w_add, colr); limb(k, -150, -600, -200, -470, 62 + w_add, colr)
        # torso (hoodie)
        tp = skia.Path(); tp.moveTo(-90, -820); tp.cubicTo(-130, -650, -110, -500, -70, -400); tp.lineTo(80, -400)
        tp.cubicTo(110, -520, 120, -680, 70, -830); tp.close()
        k.drawPath(tp, paint(colr, stroke=w_add) if w_add else paint(colr))
        if w_add:
            k.drawPath(tp, paint(colr))
        # front leg, front arm
        limb(k, 20, -430, 120, -240, 92 + w_add, colr); limb(k, 120, -240, 220, -50, 80 + w_add, colr)
        limb(k, 40, -770, 150, -620, 70 + w_add, colr); limb(k, 150, -620, 250, -560, 62 + w_add, colr)
        # head + cap
        k.drawCircle(10, -910, 92 + w_add / 2, paint(colr))
        cap = skia.Path(); cap.moveTo(-90, -940); cap.quadTo(0, -1030, 90, -945); cap.lineTo(190, -935); cap.lineTo(90, -915); cap.close()
        k.drawPath(cap, paint(colr))
        k.restore()
    # shoes in colour
    sneaker(k, -175, -8, 0.62, rot=-6, colr="#E94F37")
    sneaker(k, 255, -20, 0.62, rot=14, colr="#E94F37")
    k.restore()


def bg_road(c):
    """Sunrise road vanishing to the horizon, footprints glowing all the way back."""
    c.drawRect(skia.Rect(0, 0, W, H), vgrad(0, H, ["#2A1460", "#B8306A", "#FF8A3D", "#FFD27A"], [0, 0.35, 0.58, 0.66]))
    hx, hy = 1420, 640
    glow(c, hx, hy, 700, "#FFE9A8", 0.85); glow(c, hx, hy, 260, "#FFFFFF", 0.8)
    for kk in range(16):
        a0 = 180 + kk * 11.5
        p = skia.Path(); p.moveTo(hx, hy)
        p.lineTo(hx + 1700 * math.cos(math.radians(a0)), hy + 1700 * math.sin(math.radians(a0)))
        p.lineTo(hx + 1700 * math.cos(math.radians(a0 + 5)), hy + 1700 * math.sin(math.radians(a0 + 5)))
        p.close(); c.drawPath(p, paint("#FFF3C4", 0.10))
    c.drawRect(skia.Rect(0, hy, W, H), vgrad(hy, H, ["#3A1C4A", "#1A0E2E"]))
    road = skia.Path(); road.moveTo(hx - 30, hy); road.lineTo(hx + 30, hy); road.lineTo(W + 400, H); road.lineTo(700, H); road.close()
    c.drawPath(road, vgrad(hy, H, ["#5A3A6A", "#2A1A40"]))
    for kk in range(14):   # footprints shrinking toward the horizon
        u = (kk / 13) ** 1.7
        x_ = hx + (1300 - hx) * (1 - u) * 0 + (1350 + (1 - u) * 300 - hx) * (1 - u) + hx * 0
        x_ = hx + ((1500 + 120 * (kk % 2)) - hx) * (1 - u)
        y_ = hy + (H + 60 - hy) * (1 - u)
        shoe_print(c, x_, y_, 0.25 + 1.1 * (1 - u), rot=-70, a=0.85)
        glow(c, x_, y_, 30 + 60 * (1 - u), "gold", 0.35)


def concept_walker():
    s, c = canvas()
    bg_road(c)
    from_ = 1460
    sticker(c, lambda k: walker_big(k, 1330, 980, 0.8), pad=12)
    pill(c, 1500, 110, 1.0, "3,650,000 STEPS", "#3BB273", "cream", 60)
    title_block(c)
    return save(s, "THUMB_B.jpg")


def bg_split(c):
    c.drawRect(skia.Rect(0, 0, W, H), hgrad(0, W, ["#0E2A6A", "#1E6BFF", "#FF7A2F", "#FFB347"], [0, 0.45, 0.55, 1]))
    for x_, colr in ((560, "#9AD0FF"), (1460, "#FFE9A8")):
        glow(c, x_, 600, 520, colr, 0.75)
    vignette(c, W, H, 0.3)


def concept_twist():
    """Left: the scale that didn't move (cold). Right: the brain that grew (warm). Title across the top."""
    s, c = canvas()
    bg_split(c)
    sticker(c, lambda k: bath_scale(k, 560, 720, 1.25, needle=0.0, readout="-2.5 kg", read_col="#9AD0FF"), pad=12)
    sticker(c, lambda k: head_side(k, 1440, 760, 1.25, grow=1.0, glow_a=1.0), pad=12)
    for txt, x_, colr in (("SCALE: BARELY MOVED", 560, "cream"), ("BRAIN: GREW", 1440, "gold")):
        f = font("extrabold", 64)
        st = paint("#12081F", stroke=18); st.setStrokeJoin(skia.Paint.kRound_Join)
        text(c, txt, x_, 1040, f, st); text(c, txt, x_, 1040, f, paint(colr))
    lines = (("WHAT IF YOU WALKED 10,000 STEPS", 84, "cream"), ("EVERY DAY FOR A YEAR?", 84, "gold"))
    y = 130
    for txt, size, colr in lines:
        f = font("extrabold", size)
        st = paint("#12081F", stroke=22); st.setStrokeJoin(skia.Paint.kRound_Join)
        text(c, txt, W / 2, y, f, st); text(c, txt, W / 2, y, f, paint(colr))
        y += 100
    return save(s, "THUMB_C.jpg")


if __name__ == "__main__":
    b = concept_walker(); cc = concept_twist()
    compare([b, cc], "compare_v2.jpg")
