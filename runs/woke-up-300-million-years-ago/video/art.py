"""Scene art for 'What If You Woke Up 300 Million Years Ago?' (Night Atlas palette, skia).
All functions are pure functions of their inputs + t."""
import math, os, sys, json
import skia

BRAND = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "brand")
sys.path.insert(0, os.path.abspath(BRAND))
from primitives import (col, paint, font, text, text_w, clamp, ease, ease_out, back_out, span, keys,
                        night_sky, glow, vignette, grain, finish, pill)  # noqa
from kr import draw_kr  # noqa

W, H = 1920, 1080


def rng(i, k=1.0):
    """deterministic pseudo-random 0..1"""
    x = math.sin(i * 12.9898 + k * 78.233) * 43758.5453
    return x - math.floor(x)


class Cam:
    """with Cam(c, zoom, cx, cy, rot, shake, t): ... zooms about (cx, cy) of the frame."""
    def __init__(self, c, zoom=1.0, cx=W / 2, cy=H / 2, rot=0.0, shake=0.0, t=0.0):
        self.c, self.z, self.cx, self.cy, self.r, self.sh, self.t = c, zoom, cx, cy, rot, shake, t

    def __enter__(self):
        c = self.c
        c.save()
        sx = math.sin(self.t * 53) * self.sh
        sy = math.cos(self.t * 47) * self.sh
        c.translate(W / 2 + sx, H / 2 + sy)
        c.rotate(self.r)
        c.scale(self.z, self.z)
        c.translate(-self.cx, -self.cy)
        return c

    def __exit__(self, *a):
        self.c.restore()


def lin(c, x0, y0, x1, y1, cols, stops=None, rect=None):
    sh = skia.GradientShader.MakeLinear([skia.Point(x0, y0), skia.Point(x1, y1)], [col(*k) if isinstance(k, tuple) else col(k) for k in cols], stops)
    c.drawRect(rect or skia.Rect(0, 0, W, H), skia.Paint(Shader=sh))


def swamp_sky(c, t, day=0.0):
    """misty green-teal Carboniferous sky (day 0..1)."""
    lin(c, 0, 0, 0, H, [("deep",), ("purple",), ("#2E4A4A",), ("#5C7A5A",)] if False else
        ["#14122B", "#1E2A3A", "#2C4A48", "#5E7D5C"], [0, 0.35, 0.7, 1.0])
    glow(c, W * 0.7, H * 0.35, 700, "#C9E6A8", 0.18 + 0.1 * day)


def water(c, y, t, a=1.0):
    lin(c, 0, y, 0, H, ["#1C2B2A", "#0E1716"], rect=skia.Rect(0, y, W, H))
    for i in range(18):
        yy = y + 14 + i * 22
        x = (rng(i) * W + t * 20 * (1 + i % 3)) % (W + 300) - 150
        c.drawLine(x, yy, x + 120 + 80 * rng(i, 2), yy, paint("#9FC6B0", 0.10 * a, stroke=2))


def lycopsid(c, x, base, h, w, t, seed=0, dark=0.0, burn=0.0):
    """Lepidodendron-like scaly trunk with a forked crown of grassy leaves."""
    trunk = skia.Rect(x - w / 2, base - h, x + w / 2, base)
    base_col = "#5A4A32" if burn < 0.5 else "#2A1E16"
    lin(c, x - w / 2, 0, x + w / 2, 0, ["#3A2E1E", base_col, "#8A7450", "#A08658" if burn < 0.5 else "#3A2A1A", base_col], [0, 0.25, 0.6, 0.72, 1.0], rect=trunk)
    # root flare
    rf = skia.Path(); rf.moveTo(x - w / 2, base - w * 0.6); rf.quadTo(x - w * 0.6, base - 4, x - w * 1.3, base)
    rf.lineTo(x + w * 1.3, base); rf.quadTo(x + w * 0.6, base - 4, x + w / 2, base - w * 0.6); rf.close()
    c.drawPath(rf, paint(base_col))
    # diamond leaf-scar scales
    sc = paint("#3A2E1E", 0.55, stroke=2)
    step = max(10, w / 4)
    for row in range(int(h / step)):
        yy = base - row * step
        off = (row % 2) * step / 2
        xx = x - w / 2 + off
        while xx < x + w / 2:
            p = skia.Path(); p.moveTo(xx, yy); p.lineTo(xx + step / 2, yy - step / 2)
            p.lineTo(xx + step, yy); p.lineTo(xx + step / 2, yy + step / 2); p.close()
            c.save(); c.clipRect(trunk); c.drawPath(p, sc); c.restore()
            xx += step
    # crown: dichotomous branches
    top = base - h
    sway = math.sin(t * 0.8 + seed) * 6
    def br(x0, y0, ang, L, d):
        x1 = x0 + math.cos(ang) * L + sway * (3 - d) * 0.3
        y1 = y0 - math.sin(ang) * L
        c.drawLine(x0, y0, x1, y1, paint(base_col, 1, stroke=max(3, w * 0.35 / (d + 1))))
        if d < 3:
            br(x1, y1, ang + 0.45, L * 0.72, d + 1)
            br(x1, y1, ang - 0.45, L * 0.72, d + 1)
        else:
            leaf = "#6E8F4E" if burn < 0.3 else "#3A2A1A"
            if burn < 0.3:
                glow(c, x1, y1 - 10, 44, "#9FCF7A", 0.18)
            for k in range(13):
                a2 = ang + (k - 6) * 0.2
                L2 = 30 + 16 * rng(k, seed + d)
                c.drawLine(x1, y1, x1 + math.cos(a2) * L2, y1 - math.sin(a2) * L2 + 6,
                           paint(leaf if k % 3 else "#8DB466", 0.92, stroke=3))
    br(x, top + 2, math.pi / 2, w * 2.2, 0)
    if dark > 0:
        c.drawRect(skia.Rect(x - w * 6, top - w * 6, x + w * 6, base), paint("space", dark))


def tree_fern(c, x, base, h, t, seed=0, s=1.0):
    c.drawLine(x, base, x + math.sin(seed) * 10, base - h, paint("#4A3A28", 1, stroke=16 * s))
    tx, ty = x + math.sin(seed) * 10, base - h
    for k in range(9):
        a = math.pi * (0.1 + 0.8 * k / 8) + math.sin(t * 0.9 + seed + k) * 0.04
        L = (150 + 40 * rng(k, seed)) * s
        p = skia.Path(); p.moveTo(tx, ty)
        ex, ey = tx + math.cos(a) * L, ty - math.sin(a) * L * 0.55 + L * 0.35
        p.quadTo(tx + math.cos(a) * L * 0.6, ty - math.sin(a) * L * 0.7, ex, ey)
        c.drawPath(p, paint("#5F8A48", 0.95, stroke=7 * s))
        for j in range(1, 8):
            u = j / 8
            px = tx + (ex - tx) * u; py = ty + (ey - ty) * u - math.sin(u * math.pi) * L * 0.25
            c.drawLine(px, py, px + 16 * s, py + 14 * s, paint("#7FA65A", 0.8, stroke=3 * s))
            c.drawLine(px, py, px - 16 * s, py + 14 * s, paint("#7FA65A", 0.8, stroke=3 * s))


def ferns_ground(c, y, t, a=1.0, seed=0):
    for i in range(40):
        x = rng(i, seed) * W
        h = 40 + 60 * rng(i, seed + 3)
        for k in range(5):
            ang = math.pi / 2 + (k - 2) * 0.35 + math.sin(t + i) * 0.05
            c.drawLine(x, y, x + math.cos(ang) * h, y - math.sin(ang) * h, paint("#4E7A3E", 0.85 * a, stroke=5))


def mist(c, y, t, a=0.25):
    for i in range(6):
        x = (i * 420 + t * 15) % (W + 600) - 300
        glow(c, x, y, 380, "#CFE3D0", a)


def swamp_scene(c, t, cam_x=0.0, burn=0.0, night=0.0, seed=0):
    """3-layer parallax coal swamp."""
    swamp_sky(c, t)
    # far trunks
    c.save(); c.translate(-cam_x * 0.3, 0)
    for i in range(9):
        lycopsid(c, 80 + i * 240 + rng(i, 7) * 60, 760, 520 + rng(i, 8) * 160, 26, t, i, dark=0.35)
    c.restore()
    mist(c, 700, t, 0.18)
    c.save(); c.translate(-cam_x * 0.6, 0)
    for i in range(5):
        tree_fern(c, 200 + i * 430 + rng(i, 4) * 80, 860, 240 + rng(i, 5) * 80, t, i, 0.9)
    c.restore()
    water(c, 820, t)
    # reflections of the far light on the water
    for i in range(10):
        x = 120 + i * 190 + math.sin(t * 0.6 + i) * 12
        c.drawLine(x, 840 + (i % 3) * 18, x + 90, 840 + (i % 3) * 18, paint("#CFE3D0", 0.10, stroke=3))
    if night < 0.5 and burn < 0.5:
        god_rays(c, t)
    c.save(); c.translate(-cam_x, 0)
    log(c, 1250, 905, 1.0)
    for i in range(3):
        lycopsid(c, 300 + i * 700 + rng(i, 9) * 100, 900, 820, 70, t, i + 20, burn=burn)
    ferns_ground(c, 1000, t, seed=seed)
    c.restore()
    spores(c, t, 0.7 if night < 0.5 else 0.25)
    # dark foreground frond silhouettes framing the shot
    for side, x0 in ((1, -40), (-1, W + 40)):
        for k in range(4):
            ang = (math.pi * 0.28 + k * 0.12) if side > 0 else (math.pi * 0.72 - k * 0.12)
            ang += math.sin(t * 0.7 + k) * 0.02
            L = 360 - k * 40
            p = skia.Path(); p.moveTo(x0, H + 20)
            ex, ey = x0 + math.cos(ang) * L, H + 20 - math.sin(ang) * L
            p.quadTo(x0 + math.cos(ang) * L * 0.5 + side * 40, H - math.sin(ang) * L * 0.6, ex, ey)
            c.drawPath(p, paint("#0B1210", 0.95, stroke=10))
            for j in range(1, 9):
                u = j / 9
                px = x0 + (ex - x0) * u; py = H + 20 + (ey - H - 20) * u
                c.drawLine(px, py, px + side * 34, py - 10, paint("#0B1210", 0.95, stroke=6))
                c.drawLine(px, py, px - side * 10, py - 34, paint("#0B1210", 0.95, stroke=6))
    if night > 0:
        c.drawRect(skia.Rect(0, 0, W, H), paint("#05030C", 0.6 * night))


def god_rays(c, t, a=1.0):
    for i in range(5):
        x = 600 + i * 260 + math.sin(t * 0.2 + i) * 30
        p = skia.Path(); p.moveTo(x, -50); p.lineTo(x + 90, -50); p.lineTo(x - 260, H); p.lineTo(x - 420, H); p.close()
        sh = skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(0, H)], [col("#E8F5C8", 0.10 * a), col("#E8F5C8", 0.0)])
        c.drawPath(p, skia.Paint(Shader=sh, AntiAlias=True))


def spores(c, t, a=0.6):
    for i in range(45):
        x = (rng(i, 11) * W + t * (8 + 10 * rng(i))) % W
        y = (rng(i, 12) * H - t * (5 + 6 * rng(i, 3))) % H
        r = 1.5 + 2.5 * rng(i, 13)
        tw = 0.5 + 0.5 * math.sin(t * 2 + i)
        c.drawCircle(x, y, r, paint("#F4F1C8", a * 0.6 * tw))


def log(c, x, y, s):
    c.save(); c.translate(x, y); c.rotate(-4); c.scale(s, s)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-260, -34, 260, 34), 34, 34), paint("#3E3024"))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-260, -34, 260, -10), 20, 20), paint("#5A4A32", 0.8))
    for k in range(10):
        c.drawCircle(-220 + k * 48, -30, 10 + 6 * rng(k, 5), paint("#6E8F4E", 0.8))
    c.drawOval(skia.Rect(240, -34, 290, 34), paint("#7A6644"))
    c.drawOval(skia.Rect(252, -20, 278, 20), paint("#5A4A32", stroke=3))
    c.restore()


def dragonfly(c, x, y, s, t, ang=0.0, a=1.0):
    """Meganeura-like griffinfly. Body length ~ 0.55 * wingspan; wingspan = 520*s px."""
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    flap = math.sin(t * 38) * 0.18
    for side in (-1, 1):
        for k, (L, wdt, oy) in enumerate([(260, 52, -30), (240, 58, 20)]):
            c.save(); c.translate(0, oy); c.scale(side, 1); c.rotate(math.degrees(flap) * (1 if k == 0 else -1) - (8 if k == 0 else -8))
            r = skia.Rect(10, -wdt / 2, 10 + L, wdt / 2)
            sh = skia.GradientShader.MakeLinear([skia.Point(10, 0), skia.Point(10 + L, 0)], [col("#9FD8E0", 0.38 * a), col("#E6F7F4", 0.18 * a)])
            c.drawOval(r, skia.Paint(Shader=sh, AntiAlias=True))
            c.save(); wp = skia.Path(); wp.addOval(r); c.clipPath(wp, doAntiAlias=True)
            for v in range(1, 4):   # long veins
                yv = -wdt / 2 + wdt * v / 4
                c.drawLine(10, yv * 0.4, 10 + L, yv, paint("#E9F7F5", 0.45 * a, stroke=1.6))
            for v in range(1, 22):  # cross veins (net)
                xv = 10 + L * v / 22
                c.drawLine(xv, -wdt / 2, xv + 6, wdt / 2, paint("#E9F7F5", 0.22 * a, stroke=1))
            c.restore()
            c.drawOval(r, paint("#E9F7F5", 0.6 * a, stroke=2))
            c.drawRect(skia.Rect(10 + L * 0.8, -wdt * 0.42, 10 + L * 0.87, -wdt * 0.28), paint("#2A1E16", 0.8 * a))
            c.restore()
    # thorax + abdomen
    for side in (-1, 1):   # legs
        for k in range(3):
            c.drawLine(side * 10, -30 + k * 18, side * (34 + k * 6), -10 + k * 24, paint("#1E2A1C", a, stroke=3))
    th = skia.GradientShader.MakeLinear([skia.Point(-16, 0), skia.Point(16, 0)], [col("#2E4A2C", a), col("#6E9A5A", a), col("#2E4A2C", a)])
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-16, -50, 16, 40), 16, 16), skia.Paint(Shader=th, AntiAlias=True))
    for i in range(10):
        yy = 40 + i * 23
        r2 = skia.Rect(-9 + i * 0.4, yy, 9 - i * 0.4, yy + 22)
        c.drawRRect(skia.RRect.MakeRectXY(r2, 8, 8), paint("#4F7A44" if i % 2 else "#3E5E3A", a))
        c.drawRect(skia.Rect(r2.left(), yy + 15, r2.right(), yy + 21), paint("#C9A24A", 0.8 * a))
        c.drawLine(r2.left() + 3, yy + 3, r2.left() + 3, yy + 14, paint("#9FCF7A", 0.6 * a, stroke=2))
    for ex in (-13, 13):
        eg = skia.GradientShader.MakeRadial(skia.Point(ex - 4, -66), 18, [col("#5A8AA8", a), col("#1C2E44", a)])
        c.drawCircle(ex, -60, 15, skia.Paint(Shader=eg, AntiAlias=True))
        c.drawCircle(ex - 5, -66, 4, paint("cream", 0.85 * a))
    c.restore()


def millipede(c, x, y, s, t, length=14, a=1.0, flip=False):
    """Arthropleura-like segmented crawler, head at (x, y) facing right (or left if flip)."""
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    seg = 46
    for i in range(length, -1, -1):
        sx = -i * seg
        wave = math.sin(t * 6 - i * 0.6) * 3
        for k2, dxl in enumerate((-12, 12)):
            ph = math.sin(t * 9 - i * 0.9 + k2 * math.pi)
            c.drawLine(sx + dxl, 20 + wave, sx + dxl + ph * 16, 105, paint("#B08A5A", a, stroke=7))
        c.drawOval(skia.Rect(sx - 34, 92, sx + 34, 112), paint("space", 0.25 * a))
        r = skia.Rect(sx - 28, -44 + wave, sx + 28, 34 + wave)
        pl = skia.GradientShader.MakeLinear([skia.Point(0, -44 + wave), skia.Point(0, 34 + wave)],
                                           [col("#B08A5A", a), col("#7A5A3A" if i % 2 else "#64482E", a), col("#3A2A1C", a)], [0, 0.35, 1])
        c.drawRRect(skia.RRect.MakeRectXY(r, 22, 22), skia.Paint(Shader=pl, AntiAlias=True))
        c.drawLine(sx - 24, -10 + wave, sx + 24, -10 + wave, paint("#3A2A1C", 0.6 * a, stroke=2))
        for sp in (-14, 14):   # side knobs
            c.drawCircle(sx + sp, -40 + wave, 6, paint("#C9A26A", 0.9 * a))
        c.drawRRect(skia.RRect.MakeRectXY(r, 18, 18), paint("#8A6A48", 0.6 * a, stroke=3))
        c.drawLine(sx - 20, -24 + wave, sx + 20, -24 + wave, paint("#9A7A56", 0.5 * a, stroke=3))
    c.drawCircle(30, 0, 26, paint("#5A4230", a))
    c.drawLine(44, -10, 90, -40 + math.sin(t * 5) * 8, paint("#3A2C20", a, stroke=5))
    c.drawLine(44, 10, 90, 40 + math.sin(t * 5 + 1) * 8, paint("#3A2C20", a, stroke=5))
    c.restore()


def bed(c, x, y, s, blanket="#2A9D8F", a=1.0):
    """bed footprint ~ 420*s wide; (x, y) = floor centre."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-220, -110, 220, -40), 14, 14), paint("#5A3E2A", a))
    c.drawRect(skia.Rect(-220, -60, -205, 0), paint("#3E2A1C", a)); c.drawRect(skia.Rect(205, -60, 220, 0), paint("#3E2A1C", a))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-240, -200, -200, -40), 10, 10), paint("#4A3222", a))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-196, -150, -110, -110), 18, 18), paint("cream", a))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-120, -140, 215, -100), 16, 16), paint(blanket, a))
    c.restore()


def eye_open(c, p, t):
    """eyelid mask: p 0 closed -> 1 open, drawn over the frame."""
    if p >= 1:
        return
    h = (1 - ease(p)) * H / 2
    pth = skia.Path()
    pth.addRect(skia.Rect(0, 0, W, H))
    o = skia.Path(); o.addOval(skia.Rect(-200, H / 2 - (H / 2 - h) * 1.3, W + 200, H / 2 + (H / 2 - h) * 1.3))
    m = skia.Op(pth, o, skia.PathOp.kDifference_PathOp)
    c.drawPath(m, paint("#05030C"))


def gauge(c, x, y, r, val, t, label=True, alert=False):
    """oxygen dial 0..40 %, needle at val."""
    c.drawCircle(x, y, r, paint("deep", 0.92))
    c.drawCircle(x, y, r, paint("sand", 0.9, stroke=r * 0.05))
    for i in range(9):
        a = math.radians(210 - i * 30)
        c.drawLine(x + math.cos(a) * r * 0.78, y - math.sin(a) * r * 0.78, x + math.cos(a) * r * 0.9, y - math.sin(a) * r * 0.9,
                   paint("cream", 0.8, stroke=r * 0.025))
    arc = skia.Path(); arc.addArc(skia.Rect(x - r * 0.7, y - r * 0.7, x + r * 0.7, y + r * 0.7), -210 + 240 * 21 / 40, 240 * 9 / 40)
    c.drawPath(arc, paint("teal", 0.9, stroke=r * 0.08))
    arc2 = skia.Path(); arc2.addArc(skia.Rect(x - r * 0.7, y - r * 0.7, x + r * 0.7, y + r * 0.7), -210 + 240 * 30 / 40, 240 * 6 / 40)
    c.drawPath(arc2, paint("coral" if alert else "amber", 0.9, stroke=r * 0.08))
    a = math.radians(210 - 240 * clamp(val / 40, 0, 1)) + math.sin(t * 13) * 0.01
    c.drawLine(x, y, x + math.cos(a) * r * 0.82, y - math.sin(a) * r * 0.82, paint("gold" if not alert else "coral", 1, stroke=r * 0.05))
    c.drawCircle(x, y, r * 0.08, paint("gold"))
    if label:
        text(c, f"{val:.0f}%", x, y + r * 0.55, font("extrabold", r * 0.32), paint("cream"))
        text(c, "OXYGEN", x, y + r * 0.78, font("semibold", r * 0.14), paint("sand", 0.85), spacing=r * 0.02)
    if alert:
        glow(c, x, y, r * 1.6, "coral", 0.35 + 0.15 * math.sin(t * 8))


def flame(c, x, y, s, t, seed=0, a=1.0):
    for k, (cc, sc) in enumerate([("sunset", 1.0), ("amber", 0.7), ("gold", 0.42)]):
        fl = 1 + 0.12 * math.sin(t * 17 + seed * 3 + k)
        h = 120 * s * sc * fl
        w = 46 * s * sc
        p = skia.Path(); p.moveTo(x, y - h)
        p.cubicTo(x + w, y - h * 0.5, x + w, y, x, y)
        p.cubicTo(x - w, y, x - w, y - h * 0.5, x, y - h)
        c.drawPath(p, paint(cc, 0.95 * a))
    glow(c, x, y - 40 * s, 160 * s, "amber", 0.35 * a)


def fire_wall(c, front_x, y, t, a=1.0, height=1.0):
    """fire covering x < front_x along ground y."""
    for i in range(60):
        x = i * 34 - 40
        if x > front_x:
            break
        k = clamp((front_x - x) / 400)
        flame(c, x, y + 20 * rng(i), (1.4 + 1.6 * rng(i, 3)) * height * (0.5 + 0.5 * k), t, i, a)
    glow(c, min(front_x, W) * 0.5, y - 200, max(300, front_x * 0.6), "sunset", 0.35 * a)
    for i in range(50):   # embers
        ph = (t * 0.4 + rng(i, 21)) % 1.0
        ex = rng(i, 22) * min(front_x, W) + math.sin(t * 2 + i) * 30
        ey = y - 60 - ph * 600 * height
        if ex < front_x:
            c.drawCircle(ex, ey, 3 + 2 * rng(i), paint("gold", a * (1 - ph)))
    for i in range(8):    # smoke
        ph = (t * 0.12 + rng(i, 31)) % 1.0
        sx = rng(i, 32) * min(front_x, W)
        glow(c, sx, y - 300 - ph * 600, 160 + 200 * ph, "#2A2230", 0.45 * a * (1 - ph))


def bolt(c, x, y0, y1, seed, a=1.0):
    p = skia.Path(); p.moveTo(x, y0)
    n = 9
    xx = x
    for i in range(1, n + 1):
        xx += (rng(i, seed) - 0.5) * 120
        p.lineTo(xx, y0 + (y1 - y0) * i / n)
    c.drawPath(p, paint("cream", a, stroke=10))
    c.drawPath(p, paint("#BFD8FF", a * 0.6, stroke=24))
    glow(c, x, (y0 + y1) / 2, 500, "#BFD8FF", 0.5 * a)


def clouds(c, y, t, a=1.0, dark=True):
    for i in range(10):
        x = (i * 230 + t * 30) % (W + 400) - 200
        for k in range(4):
            c.drawCircle(x + k * 70, y + math.sin(i + k) * 20, 110 - k * 10, paint("#1C1A2E" if dark else "#3A3550", 0.95 * a))


def rain(c, t, a=0.5):
    for i in range(160):
        x = (rng(i) * W + t * 300) % W
        y = (rng(i, 2) * H + t * 1400) % H
        c.drawLine(x, y, x - 10, y + 34, paint("#BFD8FF", a * 0.4, stroke=2))


def coal_seam(c, x, y, w, h, t, reveal=1.0):
    layers = ["#3B2F25", "#1A1512", "#4A3C2E", "#0E0B0A", "#2E2620", "#0B0908", "#3A2E24"]
    lh = h / len(layers)
    for i, cc in enumerate(layers):
        r = skia.Rect(x, y + i * lh, x + w * reveal, y + (i + 1) * lh)
        c.drawRect(r, paint(cc))
        if cc in ("#0E0B0A", "#0B0908", "#1A1512"):
            for k in range(14):
                sx = x + rng(k, i) * w
                if sx < x + w * reveal:
                    c.drawLine(sx, y + i * lh + lh * 0.3, sx + 40 + 50 * rng(k, i + 9), y + i * lh + lh * 0.35 + 6 * rng(k),
                               paint("#5A5550", 0.8, stroke=3))


def trex(c, x, y, s, a=1.0):
    """generic theropod silhouette cut-out (not a specific franchise design)."""
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path()
    pts = [(-260, -40), (-120, -90), (-20, -130), (60, -200), (150, -210), (175, -185), (140, -170), (175, -160),
           (120, -145), (70, -140), (40, -100), (60, -60), (40, -55), (20, -80), (0, -60), (10, 0), (30, 40),
           (-10, 40), (-30, 0), (-60, -10), (-80, 40), (-110, 40), (-100, -20), (-160, -40)]
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    p.close()
    c.drawPath(p, paint("#2A1E2E", a))
    c.drawPath(p, paint("sand", 0.8 * a, stroke=6))
    c.restore()


def stamp(c, x, y, label, p, color="coral", rot=-12):
    if p <= 0:
        return
    k = 1.6 - 0.6 * back_out(p)
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k)
    f = font("extrabold", 70)
    w = text_w(label, f) + 60
    r = skia.Rect(-w / 2, -60, w / 2, 40)
    c.drawRRect(skia.RRect.MakeRectXY(r, 12, 12), paint(color, min(1, p * 2), stroke=8))
    text(c, label, 0, 4, f, paint(color, min(1, p * 2)))
    c.restore()


def big_text(c, s, x, y, size, p=1.0, color="cream", kind="extrabold"):
    if p <= 0:
        return
    a = ease_out(p)
    c.save(); c.translate(x, y + (1 - a) * 24)
    sh = paint("space", 0.55 * a); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 8))
    text(c, s, 0, 6, font(kind, size), sh)
    text(c, s, 0, 0, font(kind, size), paint(color, a))
    c.restore()


def counter_text(c, v0, v1, p, fmt, x, y, size, color="gold"):
    v = v0 + (v1 - v0) * ease(p)
    big_text(c, fmt(v), x, y, size, 1.0, color)


# ---------------------------------------------------------------- globe / paleo map
PANGAEA = [(-0.55, -0.62), (-0.2, -0.75), (0.25, -0.6), (0.45, -0.3), (0.38, 0.0), (0.2, 0.2), (0.35, 0.45),
           (0.15, 0.78), (-0.25, 0.85), (-0.55, 0.62), (-0.42, 0.32), (-0.62, 0.05), (-0.5, -0.3)]
INDIA_PALEO = [(0.02, 0.55), (0.14, 0.52), (0.16, 0.64), (0.08, 0.74), (0.0, 0.66)]


def blob(c, pts, cx, cy, r, p, stroke=None):
    path = skia.Path()
    q = [(cx + x * r, cy + y * r) for x, y in pts]
    path.moveTo((q[0][0] + q[-1][0]) / 2, (q[0][1] + q[-1][1]) / 2)
    for i in range(len(q)):
        a, b = q[i], q[(i + 1) % len(q)]
        path.quadTo(a[0], a[1], (a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    path.close()
    c.drawPath(path, p)
    if stroke:
        c.drawPath(path, stroke)
    return path


def globe(c, cx, cy, r, t, ice=1.0, india=1.0, merge=1.0, show_equator=True):
    glow(c, cx, cy, r * 1.5, "teal", 0.18)
    c.drawCircle(cx, cy, r, paint("#173A5A"))
    c.save()
    clip = skia.Path(); clip.addCircle(cx, cy, r); c.clipPath(clip, doAntiAlias=True)
    # continents drifting together: pieces offset by (1-merge)
    pieces = [[(-0.55, -0.62), (-0.2, -0.75), (0.25, -0.6), (0.45, -0.3), (0.38, 0.0), (-0.1, -0.05), (-0.5, -0.3)],
              [(-0.1, -0.05), (0.38, 0.0), (0.2, 0.2), (0.35, 0.45), (0.15, 0.78), (-0.25, 0.85), (-0.55, 0.62), (-0.42, 0.32), (-0.62, 0.05)]]
    offs = [(-0.25, -0.2), (0.15, 0.25)]
    for pc, (ox, oy) in zip(pieces, offs):
        m = 1 - ease(merge)
        blob(c, [(x + ox * m, y + oy * m) for x, y in pc], cx, cy, r, paint("#6E8F4E"))
    if ice > 0:
        ic = skia.Path(); ic.addOval(skia.Rect(cx - r * 0.75, cy + r * 0.45, cx + r * 0.75, cy + r * 1.25))
        c.drawPath(ic, paint("cream", 0.85 * ice))
    if show_equator:
        eq = paint("gold", 0.6, stroke=3); eq.setPathEffect(skia.DashPathEffect.Make([16, 12], 0))
        c.drawLine(cx - r, cy, cx + r, cy, eq)
    c.restore()
    if india > 0:
        dash = paint("gold", india, stroke=5); dash.setPathEffect(skia.DashPathEffect.Make([14, 10], t * 30))
        blob(c, INDIA_PALEO, cx, cy, r, paint("sand", 0.35 * india), dash)
    sh = skia.GradientShader.MakeRadial(skia.Point(cx - r * 0.35, cy - r * 0.35), r * 1.4, [col("cream", 0.12), col("space", 0.0), col("space", 0.55)], [0, 0.5, 1])
    c.drawCircle(cx, cy, r, skia.Paint(Shader=sh, AntiAlias=True))
    c.drawCircle(cx, cy, r, paint("teal", 0.8, stroke=3))


# ---------------------------------------------------------------- India map (complete outline, brand rule)
_INDIA = None
TINTS = ["#E9D8A6", "#E3CC94", "#EFDDB3", "#DCC48A", "#E6D3A0", "#F1E2BC"]


def india_map(c, cx, cy, k, highlight=(), hcol="#3A3A3A", ha=1.0, a=1.0, ice=0.0):
    global _INDIA
    if _INDIA is None:
        _INDIA = json.load(open(os.path.join(BRAND, "india.json")))
    P = lambda lon, lat: (cx + (lon - 82.5) * k, cy - (lat - 22) * k * 1.08)
    def path_of(rings):
        p = skia.Path()
        for r in rings:
            x, y = P(*r[0]); p.moveTo(x, y)
            for q in r[1:]:
                p.lineTo(*P(*q))
            p.close()
        return p
    out = path_of(_INDIA["outline"])
    c.drawPath(out, paint("#D8C38E", a))
    for i, st in enumerate(_INDIA["states"]):
        sp = path_of(st["rings"])
        hl = st["name"] in highlight
        c.drawPath(sp, paint(hcol if hl else TINTS[i % len(TINTS)], (ha if hl else 1.0) * a))
        c.drawPath(sp, paint("#B89F6A", 0.8 * a, stroke=1.2))
    if ice > 0:
        c.save(); c.clipPath(out, doAntiAlias=True)
        c.drawRect(skia.Rect(-4 * W, -4 * H, 4 * W, 4 * H), paint("#E8F3F6", 0.85 * ice))
        for i in range(25):
            x = cx + (rng(i) - 0.5) * k * 30; y = cy + (rng(i, 4) - 0.5) * k * 32
            c.drawLine(x, y, x + 60, y + 25, paint("#A9C9D6", 0.7 * ice, stroke=3))
        c.restore()
    c.drawPath(out, paint("cream", a, stroke=2.5))
    return P


def boulders(c, x, y, s, t):
    for i in range(7):
        bx = x + (i - 3) * 120 * s + rng(i) * 40 * s
        r = (40 + 50 * rng(i, 2)) * s
        c.drawOval(skia.Rect(bx - r * 1.2, y - r * 1.4, bx + r * 1.2, y), paint("#7A7268"))
        c.drawOval(skia.Rect(bx - r * 0.8, y - r * 1.3, bx + r * 0.3, y - r * 0.7), paint("#9A9288", 0.6))


def glacier(c, a, t, top=420):
    if a <= 0:
        return
    p = skia.Path(); p.moveTo(0, top)
    for i in range(13):
        p.lineTo(i * 160, top - 40 * rng(i, 5) + math.sin(t + i) * 4)
    p.lineTo(W, H); p.lineTo(0, H); p.close()
    c.drawPath(p, paint("#DDEFF4", 0.75 * a))
    for i in range(12):
        x = rng(i, 3) * W
        c.drawLine(x, top + 60, x + 80, top + 200, paint("#A9C9D6", 0.6 * a, stroke=4))


# ---------------------------------------------------------------- room / switch / fan
def room(c, t, warm=1.0):
    lin(c, 0, 0, 0, H, ["#2A1E3A", "#3B2A4A"])
    c.drawRect(skia.Rect(0, 800, W, H), paint("#2A1C24"))
    c.drawRect(skia.Rect(1320, 160, 1740, 560), paint("#1A2A4A"))
    c.drawRect(skia.Rect(1320, 160, 1740, 560), paint("#5A4A6A", stroke=14))
    c.drawLine(1530, 160, 1530, 560, paint("#5A4A6A", stroke=8))
    glow(c, 1530, 360, 260, "gold", 0.12 * warm)


def fan(c, x, y, s, t, speed=4.0):
    c.drawLine(x, y - 140 * s, x, y, paint("#C8BDA8", stroke=8 * s))
    c.save(); c.translate(x, y); c.rotate(math.degrees(t * speed))
    for k in range(3):
        c.save(); c.rotate(k * 120)
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(20 * s, -22 * s, 300 * s, 22 * s), 20 * s, 20 * s), paint("#D9CDB6", 0.92))
        c.restore()
    c.restore()
    c.drawCircle(x, y, 36 * s, paint("#B8AC96"))


def switch(c, x, y, s, on, t):
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 90 * s, y - 130 * s, x + 90 * s, y + 130 * s), 18 * s, 18 * s), paint("cream"))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 90 * s, y - 130 * s, x + 90 * s, y + 130 * s), 18 * s, 18 * s), paint("#B8AC96", stroke=4 * s))
    yy = y + (-40 if on > 0.5 else 40) * s
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 40 * s, yy - 50 * s, x + 40 * s, yy + 50 * s), 12 * s, 12 * s), paint("#E9E2D2"))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 40 * s, yy - 50 * s, x + 40 * s, yy + 50 * s), 12 * s, 12 * s), paint("#9A8E78", stroke=3 * s))
    if on > 0.5:
        glow(c, x, y, 260 * s, "gold", 0.3)


def paper(c, x, y, s, title, sub, color="teal", rot=0, a=1.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-210, -270, 210, 270), 10, 10), paint("cream", a))
    c.drawRect(skia.Rect(-210, -270, 210, -170), paint(color, a))
    text(c, title, 0, -205, font("extrabold", 54), paint("cream", a))
    for i in range(7):
        c.drawLine(-160, -120 + i * 40, 160 - (i % 3) * 50, -120 + i * 40, paint("#B8AC96", a, stroke=6))
    text(c, sub, 0, 220, font("bold", 40), paint(color, a))
    c.restore()


def comment_card(c, x, y, s, q, p, t):
    if p <= 0:
        return
    k = back_out(p)
    c.save(); c.translate(x, y); c.scale(k * s, k * s)
    r = skia.Rect(-520, -110, 520, 110)
    c.drawRRect(skia.RRect.MakeRectXY(r, 30, 30), paint("deep", 0.95))
    c.drawRRect(skia.RRect.MakeRectXY(r, 30, 30), paint("gold", stroke=4))
    text(c, "TELL ME IN THE COMMENTS", 0, -50, font("bold", 30), paint("gold"), spacing=3)
    text(c, q, 0, 30, font("semibold", 46), paint("cream"))
    c.restore()


def carbon_dots(c, x, y, t, n=40, rise=1.0, a=1.0, color="#9A9AA8"):
    for i in range(n):
        ph = (t * 0.25 + rng(i)) % 1.0
        xx = x + (rng(i, 3) - 0.5) * 500 + math.sin(t + i) * 20
        yy = y - ph * 700 * rise
        c.drawCircle(xx, yy, 6 + 6 * rng(i, 7), paint(color, a * (1 - ph)))


def o2_dots(c, x, y, t, n=40, rise=1.0, a=1.0):
    for i in range(n):
        ph = (t * 0.2 + rng(i)) % 1.0
        xx = x + (rng(i, 3) - 0.5) * 900 + math.sin(t + i) * 20
        yy = y - ph * 800 * rise
        c.drawCircle(xx, yy, 8, paint("#9FE3E0", a * (1 - ph)))
        text(c, "O2", xx, yy - 14, font("bold", 16), paint("#9FE3E0", a * (1 - ph) * 0.8))


def slide_bg(c, t):
    """explainer backdrop: night sky + faint swamp-forest silhouettes + floating spores (adds depth to plain slides)."""
    night_sky(c, W, H, t)
    glow(c, W / 2, H * 0.55, 900, "plum", 0.25)
    for i in range(10):
        x = 60 + i * 200 + rng(i, 41) * 60
        lycopsid(c, x, H + 10, 380 + 160 * rng(i, 42), 22, t, i + 50, dark=0.0)
    c.drawRect(skia.Rect(0, 0, W, H), paint("deep", 0.72))
    for i in range(18):
        x = rng(i, 43) * W
        h = 60 + 70 * rng(i, 44)
        for k in range(5):
            ang = math.pi / 2 + (k - 2) * 0.35
            c.drawLine(x, H, x + math.cos(ang) * h, H - math.sin(ang) * h, paint("#0B1210", 0.9, stroke=6))
    spores(c, t, 0.4)
