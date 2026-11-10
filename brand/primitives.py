"""Shared drawing helpers for KR's What If Explained ("Cinematic Night Atlas" look). skia-python.

Every function is a pure function of its inputs (and time t), so frames render in any order.
"""
import math
import os

import skia

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- palette (approved channel look)
PALETTE = {
    "space": "#0A0716", "deep": "#170E33", "purple": "#2A1450", "plum": "#4E1C5E",
    "magenta": "#8A2A5C", "sunset": "#D9573D", "teal": "#2A9D8F", "sand": "#E9D8A6",
    "cream": "#F4F1E8", "coral": "#E76F51", "amber": "#F2B44C", "gold": "#FFD27A",
    # KR only
    "skin": "#C98B5E", "skin_shade": "#A96F47", "hair": "#1B1030", "ink": "#1A1230",
    "hoodie": "#2A9D8F", "hoodie_shade": "#207A6F", "white": "#FFFFFF",
}


def col(name_or_hex, a=1.0):
    h = PALETTE.get(name_or_hex, name_or_hex).lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return skia.Color(r, g, b, int(round(255 * max(0.0, min(1.0, a)))))


def paint(color, a=1.0, stroke=None, cap=skia.Paint.kRound_Cap, aa=True):
    p = skia.Paint(AntiAlias=aa, Color=col(color, a))
    if stroke is not None:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(stroke)
        p.setStrokeCap(cap)
        p.setStrokeJoin(skia.Paint.kRound_Join)
    return p


# ---------------------------------------------------------------- fonts
_FONTS = {}
FONT_FILES = {
    "regular": "Poppins_400Regular.ttf", "semibold": "Poppins_600SemiBold.ttf",
    "bold": "Poppins_700Bold.ttf", "extrabold": "Poppins_800ExtraBold.ttf",
    "serif_italic": "DMSerifDisplay_400Regular_Italic.ttf",
}


def font(kind, size):
    if kind not in _FONTS:
        _FONTS[kind] = skia.Typeface.MakeFromFile(os.path.join(HERE, "fonts", FONT_FILES[kind]))
    f = skia.Font(_FONTS[kind], size)
    f.setEdging(skia.Font.Edging.kAntiAlias)
    return f


def text_w(s, f, spacing=0.0):
    return f.measureText(s) + spacing * max(0, len(s) - 1)


def text(c, s, x, y, f, p, align="center", spacing=0.0):
    """Draw text with baseline y. align: left | center | right. spacing = extra px between letters."""
    w = text_w(s, f, spacing)
    x0 = x - (w / 2 if align == "center" else w if align == "right" else 0)
    if spacing == 0:
        c.drawString(s, x0, y, f, p)
        return
    for ch in s:
        c.drawString(ch, x0, y, f, p)
        x0 += f.measureText(ch) + spacing


# ---------------------------------------------------------------- timing
def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def ease(v):
    """ease-in-out (cubic) on 0..1"""
    v = clamp(v)
    return 4 * v ** 3 if v < 0.5 else 1 - (-2 * v + 2) ** 3 / 2


def ease_out(v):
    return 1 - (1 - clamp(v)) ** 3


def back_out(v, k=1.7):
    """overshoot then settle (anticipation/follow-through for pops)"""
    v = clamp(v) - 1
    return 1 + (k + 1) * v ** 3 + k * v ** 2


def span(t, t0, t1):
    return clamp((t - t0) / (t1 - t0)) if t1 > t0 else float(t >= t1)


def keys(t, kf, fn=ease):
    """kf = [(time, value), ...] sorted by time; eased between keys."""
    if t <= kf[0][0]:
        return kf[0][1]
    for (t0, v0), (t1, v1) in zip(kf, kf[1:]):
        if t <= t1:
            return v0 + (v1 - v0) * fn(span(t, t0, t1))
    return kf[-1][1]


# ---------------------------------------------------------------- backgrounds and finish
def night_sky(c, W, H, t=0.0, horizon=None):
    """space → purple → magenta → sunset gradient with a few twinkling stars."""
    horizon = horizon or H
    shader = skia.GradientShader.MakeLinear(
        [skia.Point(0, 0), skia.Point(0, horizon)],
        [col("space"), col("deep"), col("purple"), col("plum"), col("magenta")],
        [0.0, 0.35, 0.65, 0.88, 1.0])
    c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Shader=shader))
    for i in range(70):
        sx = (i * 977.0) % W
        sy = (i * 431.0) % (horizon * 0.7)
        tw = 0.45 + 0.55 * (0.5 + 0.5 * math.sin(t * 1.7 + i * 1.3))
        c.drawCircle(sx, sy, 1.1 + (i % 3) * 0.5, paint("cream", 0.55 * tw))


def glow(c, x, y, r, color, a=0.6):
    shader = skia.GradientShader.MakeRadial(skia.Point(x, y), r, [col(color, a), col(color, 0)])
    c.drawCircle(x, y, r, skia.Paint(Shader=shader, AntiAlias=True))


def vignette(c, W, H, a=0.55):
    shader = skia.GradientShader.MakeRadial(skia.Point(W / 2, H / 2), math.hypot(W, H) / 2,
                                            [col("space", 0), col("space", 0), col("space", a)], [0.0, 0.55, 1.0])
    c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Shader=shader))


def grain(c, W, H, t=0.0, amount=0.045):
    """3–6% film grain: fixed noise tile shifted per frame (deterministic)."""
    shader = skia.PerlinNoiseShader.MakeFractalNoise(0.9, 0.9, 2, int(t * 30) % 97)
    p = skia.Paint(Shader=shader, Alphaf=amount, BlendMode=skia.BlendMode.kOverlay)
    c.drawRect(skia.Rect(0, 0, W, H), p)


def finish(c, W, H, t=0.0):
    vignette(c, W, H)
    grain(c, W, H, t)


def pill(c, x, y, s, label, color="teal", text_color="cream", size=34):
    f = font("semibold", size * s)
    w = text_w(label, f) + 44 * s
    h = size * 1.7 * s
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2), h / 2, h / 2),
                paint(color, 0.92))
    text(c, label, x, y + size * 0.36 * s, f, paint(text_color))


def surface(W, H):
    return skia.Surface(W, H)


def save_png(surf, path):
    surf.makeImageSnapshot().save(path, skia.kPNG)
