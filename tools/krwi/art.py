"""Generic drawing helpers for every video (Night Atlas look). Moved unchanged from the first runs, so old shots keep
working. `from krwi.art import *` gives: brand primitives (col, paint, font, text, ease, span, keys, glow, pill, ...),
draw_kr, the logo/chapter/end cards, W/H, and the helpers below. Topic-specific art stays in the run's video/art.py."""
import math, os, json
import skia

from . import ctx
from .ctx import W, H, BRAND
from primitives import (col, paint, font, text, text_w, clamp, ease, ease_out, back_out, span, keys,  # noqa: F401
                        night_sky, glow, vignette, grain, finish, pill)
from kr import draw_kr  # noqa: F401
from logo import draw_logo, chapter_card, end_card  # noqa: F401


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


def pop(c, x, y, label, t, t0, color="teal", size=40):
    p = span(t, t0, t0 + 0.35)
    if p <= 0:
        return
    k = back_out(p)
    c.save(); c.translate(x, y); c.scale(k, k); pill(c, 0, 0, 1.0, label, color, "cream", size); c.restore()


def xmark(c, x, y, s, p):
    if p <= 0:
        return
    a = ease_out(p)
    c.drawLine(x - 40 * s, y - 40 * s, x - 40 * s + 80 * s * a, y - 40 * s + 80 * s * a, paint("coral", stroke=12 * s))
    if p > 0.5:
        b = ease_out((p - 0.5) * 2)
        c.drawLine(x + 40 * s, y - 40 * s, x + 40 * s - 80 * s * b, y - 40 * s + 80 * s * b, paint("coral", stroke=12 * s))


def explainer_bg(c, t, tint="plum"):
    """Plain explainer backdrop: night sky, a soft glow, darkened. Default background of the shot library."""
    night_sky(c, W, H, t)
    glow(c, W / 2, H * 0.55, 900, tint, 0.3)
    c.drawRect(skia.Rect(0, 0, W, H), paint("deep", 0.55))
