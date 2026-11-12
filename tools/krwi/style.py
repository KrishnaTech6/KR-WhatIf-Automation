"""Visual styles for the main video (and so its Short/Reel, which reframe the main frames).

    atlas      "Cinematic Night Atlas", the original look (default). Flat illustrated scenes, sunset palette.
               For: how things work, technology, inventions, the body, everyday science.
    cinematic  Style 1. Near-black, one light source, glow, thin spaced type, countdowns, very little colour.
               For: crisis / countdown / danger / survival / huge-scale topics (and space, when Krishna asks).
    collage    Style 4. Paper cut-outs on kraft paper, halftone, tape, typewriter labels, red marker, stamps,
               red string, 12 fps stop-motion. For: India, money, society, cities, people, news-like topics.

The style comes from runs/<slug>/video/run.json {"style": "..."} (`wi.py <slug> style NAME` writes it);
KR_STYLE overrides it. Missing = atlas, so old runs render exactly as before.

What switches automatically: explainer_bg, big_text, pill/pop, stamp, glow strength, chapter cards, the frame
finish, and (collage) 12 fps stop-motion with a tiny per-drawing jitter. What never switches: KR's design, the logo
sting and the end card (brand), the music, the thumbnail look.

Topic art in a run should be drawn IN the style with the helpers below (everything here is in `krwi.lib`):
    collage:   cutout(c, draw), halftone(c, path, color), tape(c, ...), torn_strip(c, ...), type_text(c, ...),
               index_card(c, ...), marker_circle(c, ...), red_string(c, ...), pin(c, ...), jit(key, t)
    cinematic: starfield(c, t), bloom(c, ...), light_stream(c, ...), shock_ring(c, ...), countdown(c, ...)
    any style: bold_words(c, ...) (Style 2 caption look, also used by vertical captions when CAPTIONS = "bold")
"""
import json
import math
import os

import skia

from . import ctx
from .ctx import BRAND
from primitives import (col, paint, font, text, text_w, ease, ease_out, back_out, span, clamp,  # noqa: F401
                        night_sky, vignette, grain)
from primitives import finish as atlas_finish, glow as atlas_glow, pill as atlas_pill

STYLES = ("atlas", "cinematic", "collage")
INK, RED_INK, PAPER, KRAFT = "#1C1A17", "#B3261E", "#F4EFE3", "#CDB68C"


def _load():
    s = os.environ.get("KR_STYLE")
    if not s:
        p = os.path.join(ctx.VIDEO, "run.json")
        if os.path.exists(p):
            s = json.load(open(p)).get("style")
    s = (s or "atlas").strip().lower()
    if s not in STYLES:
        raise ValueError(f"unknown style {s!r} in run.json (use one of {', '.join(STYLES)})")
    return s


NAME = _load()


def rng(i, k=1.0):
    x = math.sin(i * 12.9898 + k * 78.233) * 43758.5453
    return x - math.floor(x)


def _seed(s):
    return sum((i + 1) * ord(ch) for i, ch in enumerate(str(s))) % 9973


# ---------------------------------------------------------------- fonts (Special Elite: Apache 2.0, Anton: OFL)
_TF = {}


def sfont(kind, size):
    """Style fonts: 'type' (Special Elite typewriter), 'anton' (Style 2 captions)."""
    files = {"type": "SpecialElite_400Regular.ttf", "anton": "Anton_400Regular.ttf"}
    if kind not in _TF:
        _TF[kind] = skia.Typeface.MakeFromFile(os.path.join(BRAND, "fonts", files[kind]))
    f = skia.Font(_TF[kind], size)
    f.setEdging(skia.Font.Edging.kAntiAlias)
    return f


def _covers(f, s):
    return all(g != 0 for g, ch in zip(f.textToGlyphs(s), s) if not ch.isspace())


def type_font(s, size):
    """Typewriter font, or Poppins bold if a glyph is missing (e.g. the rupee sign)."""
    f = sfont("type", size)
    return f if _covers(f, s) else font("bold", size * 0.9)


# ---------------------------------------------------------------- time: collage is stop-motion
def frame_time(t, kind=None):
    """Time the shot is drawn at. Collage holds each drawing for 1/12 s (brand moments stay smooth)."""
    if NAME == "collage" and kind not in ("logo", "end"):
        return math.floor(t * 12 + 1e-6) / 12
    return t


def jit(key, t, amt=3.0):
    """Per-element stop-motion wobble for collage art: (dx, dy, degrees), new every 1/12 s. Zero in other styles."""
    if NAME != "collage":
        return 0.0, 0.0, 0.0
    n = int(t * 12 + 1e-6) + _seed(key) * 31
    return (rng(n, 1) - 0.5) * 2 * amt, (rng(n, 2) - 0.5) * 2 * amt, (rng(n, 3) - 0.5) * 1.2


def frame_jitter(c, W, H, t, kind=None):
    """Whole-frame stop-motion boil for collage (scaled 0.4% so edges never show)."""
    if NAME != "collage" or kind in ("logo", "end"):
        return
    dx, dy, r = jit("frame", t, 1.6)
    c.translate(W / 2 + dx, H / 2 + dy); c.rotate(r * 0.25); c.scale(1.004, 1.004); c.translate(-W / 2, -H / 2)


# ---------------------------------------------------------------- backgrounds
_STARS = [(rng(i, 1), rng(i, 2), 0.5 + 2.0 * rng(i, 3), rng(i, 4) * 6.28) for i in range(320)]


def starfield(c, t, W=None, H=None, n=320, a=1.0):
    W, H = W or ctx.W, H or ctx.H
    for x, y, r, ph in _STARS[:n]:
        tw = 0.5 + 0.5 * math.sin(ph + t * 2.1)
        c.drawCircle(x * W, y * H, r * (W / 1920), paint("#FFFFFF", (0.18 + 0.6 * tw) * a))


def cinematic_bg(c, t, tint="plum", W=None, H=None):
    W, H = W or ctx.W, H or ctx.H
    c.drawRect(skia.Rect(0, 0, W, H), paint("#05060C"))
    atlas_glow(c, W * 0.22, H * 0.8, W * 0.55, "#2B1F63", 0.45)
    atlas_glow(c, W * 0.85, H * 0.15, W * 0.4, "#0E3A52", 0.35)
    if tint not in (None, "plum"):
        atlas_glow(c, W / 2, H * 0.55, W * 0.45, tint, 0.12)
    starfield(c, t, W, H)


_KRAFT = {}


def _kraft_image(W, H):
    if (W, H) not in _KRAFT:
        s = skia.Surface(W, H); k = s.getCanvas()
        k.drawRect(skia.Rect(0, 0, W, H), paint(KRAFT))
        for freq, amt, mode in ((0.004, 0.22, skia.BlendMode.kMultiply), (0.03, 0.12, skia.BlendMode.kOverlay),
                                (0.6, 0.10, skia.BlendMode.kOverlay)):
            p = skia.Paint(Shader=skia.PerlinNoiseShader.MakeFractalNoise(freq, freq, 3, 7), Alphaf=amt, BlendMode=mode)
            k.drawRect(skia.Rect(0, 0, W, H), p)
        for i in range(int(700 * W * H / 2073600)):            # paper fibres
            x, y, L = rng(i, 5) * W, rng(i, 6) * H, 8 + 50 * rng(i, 7)
            a = rng(i, 8) * 3.14
            k.drawLine(x, y, x + math.cos(a) * L, y + math.sin(a) * L, paint("#8C7651", 0.18, stroke=1.2))
        _KRAFT[(W, H)] = s.makeImageSnapshot()
    return _KRAFT[(W, H)]


def collage_bg(c, t=0.0, tint=None, W=None, H=None):
    W, H = W or ctx.W, H or ctx.H
    c.drawImage(_kraft_image(W, H), 0, 0)


def background(c, t, tint="plum"):
    """The style's plain backdrop (explainer_bg dispatches here)."""
    if NAME == "cinematic":
        cinematic_bg(c, t, tint)
    else:
        collage_bg(c, t)


# ---------------------------------------------------------------- finish
def finish(c, W, H, t=0.0, kind=None):
    if NAME == "atlas" or kind in ("logo", "end"):
        atlas_finish(c, W, H, t)
    elif NAME == "cinematic":
        vignette(c, W, H, 0.72)
        grain(c, W, H, t, 0.03)
    else:
        sh = skia.GradientShader.MakeRadial(skia.Point(W / 2, H / 2), math.hypot(W, H) / 2,
                                            [col("#3A2410", 0), col("#3A2410", 0), col("#3A2410", 0.38)], [0, 0.6, 1])
        c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Shader=sh))
        grain(c, W, H, frame_time(t), 0.05)


# ---------------------------------------------------------------- paper pieces (collage)
def cutout(c, draw, border=10, shadow=(8, 12), border_color=PAPER):
    """Draw anything as a paper cut-out: white paper border + drop shadow around what draw(k) paints on canvas k.
        cutout(c, lambda k: k.drawPath(paper_circle(960, 400, 150), paint("#F6A21E")))
    Coordinates are the same as on c. The effect is computed only inside the drawing's bounds (fast)."""
    rec = skia.PictureRecorder()
    draw(rec.beginRecording(skia.Rect(-4000, -4000, 8000, 8000), skia.RTreeFactory()()))
    pic = rec.finishRecordingAsPicture()
    r = pic.cullRect()
    b = skia.Rect(r.left() - border - 20, r.top() - border - 20, r.right() + border + 20, r.bottom() + border + 20)
    rings = [(math.cos(a) * border, math.sin(a) * border) for a in (i * math.pi / 8 for i in range(16))]
    lb = skia.Rect(b.left(), b.top(), b.right() + shadow[0] + 10, b.bottom() + shadow[1] + 10)
    # shadow: the outline in black, blurred, offset
    sp = skia.Paint(ColorFilter=skia.ColorFilters.Blend(col("#000000", 0.38), skia.BlendMode.kSrcIn),
                    ImageFilter=skia.ImageFilters.Blur(5, 5))
    c.saveLayer(lb, sp)
    for dx, dy in rings[::2]:
        c.save(); c.translate(dx + shadow[0], dy + shadow[1]); c.drawPicture(pic); c.restore()
    c.restore()
    # paper edge: the drawing stamped around a circle in the paper colour (a fast dilate)
    c.saveLayer(lb, skia.Paint(ColorFilter=skia.ColorFilters.Blend(col(border_color), skia.BlendMode.kSrcIn)))
    for dx, dy in rings:
        c.save(); c.translate(dx, dy); c.drawPicture(pic); c.restore()
    c.restore()
    c.drawPicture(pic)


def _jag(cx, cy, r, seed, n=72, amp=0.035):
    p = skia.Path()
    for i in range(n):
        a = i / n * 2 * math.pi
        rr = r * (1 + (rng(seed * 7 + i) - 0.5) * 2 * amp)
        (p.moveTo if i == 0 else p.lineTo)(cx + rr * math.cos(a), cy + rr * math.sin(a))
    p.close()
    return p


def paper_circle(cx, cy, r, seed=1, amp=0.035):
    """A hand-cut (slightly jagged) circle path, for planets, suns, coins, holes."""
    return _jag(cx, cy, r, seed, amp=amp)


def halftone(c, path, color="#000000", a=0.35, step=18, light=(-0.6, -0.6)):
    """Halftone dots inside `path`, bigger away from the light direction (print look)."""
    b = path.getBounds()
    c.save(); c.clipPath(path, doAntiAlias=True)
    pt = paint(color, a)
    diag = math.hypot(b.width(), b.height()) or 1
    lx, ly = b.centerX() + light[0] * b.width() / 2, b.centerY() + light[1] * b.height() / 2
    y, row = b.top(), 0
    while y < b.bottom() + step:
        x = b.left() + (step / 2 if row % 2 else 0)
        while x < b.right() + step:
            d = math.hypot(x - lx, y - ly) / diag
            if d > 0.15:
                c.drawCircle(x, y, min(step * 0.48, step * 0.55 * d), pt)
            x += step
        y += step; row += 1
    c.restore()


def tape(c, x, y, w=150, h=46, rot=-8):
    c.save(); c.translate(x, y); c.rotate(rot)
    c.drawRect(skia.Rect(-w / 2, -h / 2, w / 2, h / 2), paint("#EFE6C8", 0.72))
    for i in range(-int(w / 2), int(w / 2), 7):
        c.drawLine(i, -h / 2, i + 3, -h / 2 - 2, paint("#EFE6C8", 0.5, stroke=2))
    c.restore()


def _torn(x0, y0, w, h, seed, amp=6):
    p = skia.Path(); n = max(8, int(w / 28))
    for i in range(n + 1):
        (p.moveTo if i == 0 else p.lineTo)(x0 + w * i / n, y0 + (rng(seed + i, 1) - 0.5) * 2 * amp)
    for i in range(n + 1):
        p.lineTo(x0 + w - w * i / n, y0 + h + (rng(seed + i, 2) - 0.5) * 2 * amp)
    p.close()
    return p


def torn_strip(c, x, y, w, h, seed=1, color=PAPER, rot=0.0, shadow=True):
    """A torn paper strip centred on (x, y)."""
    c.save(); c.translate(x, y); c.rotate(rot)
    p = _torn(-w / 2, -h / 2, w, h, seed)
    if shadow:
        c.save(); c.translate(6, 9); c.drawPath(p, paint("#000000", 0.28)); c.restore()
    c.drawPath(p, paint(color))
    c.restore()


def type_text(c, s, x, y, size, p=1.0, color=INK, align="center"):
    """Typewriter text, revealed letter by letter as p goes 0 -> 1. y is the vertical centre."""
    if p <= 0 or not s:
        return
    f = type_font(s, size)
    n = max(1, int(round(len(s) * clamp(p))))
    w = text_w(s, f)
    x0 = x - (w / 2 if align == "center" else w if align == "right" else 0)
    c.drawString(s[:n], x0, y + size * 0.35, f, paint(color))


def index_card(c, x, y, w, h, rot=2.0, seed=3):
    c.save(); c.translate(x, y); c.rotate(rot)
    r = skia.Rect(-w / 2, -h / 2, w / 2, h / 2)
    c.save(); c.translate(7, 10); c.drawRect(r, paint("#000000", 0.28)); c.restore()
    c.drawRect(r, paint("#FDFCF7"))
    c.drawRect(skia.Rect(-w / 2, -h / 2 + h * 0.24, w / 2, -h / 2 + h * 0.24 + 3), paint("#D9534F", 0.6))
    yy = -h / 2 + h * 0.24 + h * 0.18
    while yy < h / 2 - 6:
        c.drawRect(skia.Rect(-w / 2, yy, w / 2, yy + 2), paint("#7FA8D6", 0.45)); yy += h * 0.18
    c.restore()
    tape(c, x + math.sin(math.radians(rot)) * h / 2, y - h / 2 - 2, min(170, w * 0.3), 44, rot + 3)


def _wobble_ellipse(cx, cy, rx, ry, seed, turns=1.1, n=90):
    pts = []
    for i in range(n + 1):
        a = -1.9 + i / n * turns * 2 * math.pi
        k = 1 + 0.035 * math.sin(i * 0.31 + seed)
        pts.append((cx + rx * k * math.cos(a) + (rng(seed + i) - 0.5) * 3, cy + ry * k * math.sin(a) + (rng(seed + i, 9) - 0.5) * 3))
    return pts


def _poly_part(pts, p):
    path = skia.Path(); n = max(2, int(len(pts) * clamp(p)))
    path.moveTo(*pts[0])
    for q in pts[1:n]:
        path.lineTo(*q)
    return path


def marker_circle(c, cx, cy, rx, ry, p, seed=7, color=RED_INK, width=11):
    """Red marker circle drawn on over p 0 -> 1."""
    if p <= 0:
        return
    c.drawPath(_poly_part(_wobble_ellipse(cx, cy, rx, ry, seed), p), paint(color, 0.9, stroke=width))


def marker_line(c, pts, p, color=RED_INK, width=9):
    if p > 0:
        c.drawPath(_poly_part(pts, p), paint(color, 0.9, stroke=width))


def pin(c, x, y, color="#D62828"):
    c.drawCircle(x + 3, y + 4, 13, paint("#000000", 0.3))
    c.drawCircle(x, y, 13, paint(color))
    c.drawCircle(x - 4, y - 4, 4, paint("#FFFFFF", 0.6))


def red_string(c, pts, p):
    """Investigation-board red string through pts, drawn on over p, with pins at both ends."""
    if p <= 0:
        return
    path = skia.Path(); path.moveTo(*pts[0])
    segs = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    left = sum(segs) * clamp(p)
    for i, L in enumerate(segs):
        if left >= L:
            path.lineTo(*pts[i + 1]); left -= L
        else:
            k = left / L if L else 0
            path.lineTo(pts[i][0] + (pts[i + 1][0] - pts[i][0]) * k, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * k); break
    c.drawPath(path, paint("#A4161A", stroke=5))
    pin(c, *pts[0])
    if p >= 1:
        pin(c, *pts[-1])


# ---------------------------------------------------------------- light (cinematic)
def bloom(c, x, y, r, color="#FFB347", a=1.0, core="#FFF6E0"):
    """A glowing light source: wide halo + bright core."""
    atlas_glow(c, x, y, r * 3.2, color, 0.55 * a)
    sh = skia.GradientShader.MakeRadial(skia.Point(x - r * 0.2, y - r * 0.2), r * 1.1,
                                        [col(core, a), col(color, a), col(color, 0)], [0, 0.6, 1])
    c.drawCircle(x, y, r, skia.Paint(Shader=sh, AntiAlias=True))


def light_stream(c, x0, y0, x1, y1, t, front=0.0, color="#FFD9A0", n=16, speed=0.32):
    """Photons travelling from (x0, y0) to (x1, y1). front 0..1 = how far the dark gap has moved (light 'cut off')."""
    L = math.dist((x0, y0), (x1, y1)) or 1
    for i in range(n):
        k = (i / n + t * speed) % 1
        if k < front:
            continue
        x, y = x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
        atlas_glow(c, x, y, 16, color, 0.95)


def shock_ring(c, x, y, p, rmax=1000, color="#FFE2C4"):
    if 0 < p < 1:
        c.drawCircle(x, y, 30 + rmax * ease_out(p), paint(color, (1 - p) * 0.8, stroke=2 + 6 * (1 - p)))


def countdown(c, seconds, x, y, size=96, color="#FFD39A", decimals=1):
    """mm:ss.d timer, e.g. countdown(c, 500 - (t - t0), ...)."""
    s = max(0.0, seconds)
    txt = f"{int(s // 60):02d}:{s % 60:0{3 + decimals}.{decimals}f}" if decimals else f"{int(s // 60):02d}:{int(s % 60):02d}"
    text(c, txt, x, y, font("regular", size), paint(color), spacing=size * 0.06)


# ---------------------------------------------------------------- styled library pieces
def big_text(c, s, x, y, size, p=1.0, color="cream", kind="extrabold"):
    if p <= 0:
        return
    if NAME == "cinematic":
        a = ease_out(p)
        k = "semibold" if kind in ("extrabold", "bold") else kind
        f = font(k, size * 0.9)
        sp = size * 0.07
        g = paint(color, 0.35 * a); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 14))
        text(c, s, x, y + (1 - a) * 18, f, g, spacing=sp)
        text(c, s, x, y + (1 - a) * 18, f, paint(color, a), spacing=sp)
    else:                                                    # collage: typed on a torn paper strip
        f = type_font(s, size * 0.92)
        w = text_w(s, f) + size * 0.9
        rot = (rng(_seed(s)) - 0.5) * 2.4
        dx, dy, r = jit(s, ctx_t[0])
        torn_strip(c, x + dx, y - size * 0.32 + dy, w, size * 1.45, _seed(s), PAPER, rot + r)
        ink = RED_INK if color in ("coral", "sunset", "magenta", "gold", "amber") else INK
        c.save(); c.translate(x + dx, y - size * 0.32 + dy); c.rotate(rot + r)
        type_text(c, s, 0, 0, size * 0.92, p * 1.6, ink)
        c.restore()


ctx_t = [0.0]          # current frame time, set by the compositor (collage jitter needs it inside big_text/pill)


def pill(c, x, y, s, label, color="teal", text_color="cream", size=34):
    if NAME == "cinematic":
        f = font("regular", size * s)
        sp = size * 0.12 * s
        w = text_w(label.upper(), f, sp) + 56 * s
        h = size * 1.6 * s
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2), h / 2, h / 2),
                    paint("#FFFFFF", 0.06))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2), h / 2, h / 2),
                    paint("cream", 0.55, stroke=1.6))
        text(c, label.upper(), x, y + size * 0.36 * s, f, paint("cream"), spacing=sp)
    else:                                                    # collage: a typed paper tag with tape
        f = type_font(label, size * s)
        w = text_w(label, f) + 50 * s
        h = size * 1.7 * s
        dx, dy, r = jit(label, ctx_t[0], 2)
        rot = (rng(_seed(label), 4) - 0.5) * 4 + r
        c.save(); c.translate(x + dx, y + dy); c.rotate(rot)
        r_ = skia.Rect(-w / 2, -h / 2, w / 2, h / 2)
        c.save(); c.translate(5, 7); c.drawRect(r_, paint("#000000", 0.28)); c.restore()
        c.drawRect(r_, paint("#FDFCF7"))
        c.drawRect(skia.Rect(-w / 2, -h / 2, -w / 2 + 10 * s, h / 2), paint(color, 0.9))
        c.drawString(label, -text_w(label, f) / 2 + 5 * s, size * 0.36 * s, f,
                     paint(RED_INK if color in ("coral", "sunset") else INK))
        c.restore()
        tape(c, x + dx - w / 2 + 10, y + dy - h / 2, 70 * s, 26 * s, -20)


def stamp(c, x, y, label, p, color="coral", rot=-12):
    if p <= 0:
        return
    k = 1.6 - 0.6 * back_out(p)
    a = min(1, p * 2) * 0.9
    ink = RED_INK if NAME == "collage" else color
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k)
    f = sfont("type", 76) if NAME == "collage" else font("extrabold", 70)
    w = text_w(label, f, 4) + 60
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-w / 2, -64, w / 2, 40), 10, 10), paint(ink, a, stroke=9))
    text(c, label, 0, 6, f, paint(ink, a), spacing=4)
    c.restore()


def glow(c, x, y, r, color, a=0.6):
    atlas_glow(c, x, y, r, color, a * (0.35 if NAME == "collage" else 1.0))


def chapter_card(c, W, H, value, name, p=1.0, t=0.0):
    """Style chapter card ('DAY 10' + name). Atlas uses the brand card in logo.py."""
    s = min(W, H) / 1080
    if NAME == "cinematic":
        cinematic_bg(c, t, None, W, H)
        k = ease_out(span(p, 0.05, 0.5))
        f = font("semibold", 140 * s)
        g = paint("#FFD39A", 0.4 * k); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 20))
        for pt in (g, paint("#FFE9C7", k)):
            text(c, value.upper(), W / 2, H / 2 + 20 * s + (1 - k) * 20, f, pt, spacing=14 * s)
        lw = 420 * s * ease(span(p, 0.25, 0.7))
        c.drawLine(W / 2 - lw, H / 2 + 75 * s, W / 2 + lw, H / 2 + 75 * s, paint("cream", 0.5, stroke=2))
        a = ease_out(span(p, 0.4, 0.8))
        text(c, name.upper(), W / 2, H / 2 + 150 * s, font("regular", 44 * s), paint("sand", 0.9 * a), spacing=8 * s)
    else:
        collage_bg(c, t, None, W, H)
        dx, dy, r = jit("card" + value, t)
        cw, ch = 1000 * s, 460 * s
        k = back_out(span(p, 0.0, 0.3))
        c.save(); c.translate(W / 2 + dx, H / 2 + dy); c.scale(k, k); c.translate(-W / 2, -H / 2)
        index_card(c, W / 2, H / 2, cw, ch, -2 + r)
        c.save(); c.translate(W / 2, H / 2); c.rotate(-2 + r)
        type_text(c, value.upper(), 0, -30 * s, 150 * s, span(p, 0.15, 0.55), RED_INK)
        type_text(c, name, 0, 120 * s, 54 * s, span(p, 0.5, 0.9), INK)
        c.restore(); c.restore()
    finish(c, W, H, t)


def comment_card(c, x, y, s, q, p, t):
    if NAME != "collage":
        return None
    if p <= 0:
        return True
    k = back_out(p)
    c.save(); c.translate(x, y); c.scale(k * s, k * s)
    index_card(c, 0, 0, 1100, 260, -1.5)
    c.save(); c.rotate(-1.5)
    type_text(c, "TELL ME IN THE COMMENTS:", 0, -70, 34, 1.0, RED_INK)
    type_text(c, q, 0, 30, 46, span(p, 0.2, 1.0), INK)
    c.restore(); c.restore()
    return True


def kr_cutout(c, draw):
    """KR (unchanged design) as a paper cut-out in collage; plain elsewhere. draw(k) paints on canvas k."""
    if NAME == "collage":
        cutout(c, draw, border=9)
    else:
        draw(c)


# ---------------------------------------------------------------- Style 2 bold words (captions look)
def bold_words(c, words, x, y, size, hl=(), p=1.0, max_w=None, rot=-1.4):
    """Style 2 look: Anton, white words with a thick black outline, highlighted words in yellow, pop-in scale.
    words: list of str (shown upper-case). hl: indexes to paint yellow. Returns the drawn width."""
    if p <= 0 or not words:
        return 0
    words = [w.upper() for w in words]
    while True:
        f = sfont("anton", size)
        sp = f.measureText(" ")
        total = sum(f.measureText(w) for w in words) + sp * (len(words) - 1)
        if not max_w or total <= max_w or size <= 40:
            break
        size -= 4
    k = 0.72 + 0.28 * back_out(p, 2.2)
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k)
    xx = -total / 2
    for i, w in enumerate(words):
        sh = paint("#000000", 0.35); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 4))
        c.drawString(w, xx, size * 0.36 + 10, f, sh)
        c.drawString(w, xx, size * 0.36, f, paint("#0D0D12", stroke=size * 0.13))
        c.drawString(w, xx, size * 0.36, f, paint("#FFE14D" if i in hl else "#FFFFFF"))
        xx += f.measureText(w) + sp
    c.restore()
    return total
