"""Channel logo, logo sting, chapter card and end card. LOCKED: reuse as-is in every video.

draw_logo(c, cx, cy, s=1.0, p=1.0, t=0.0)   p = sting progress 0..1 (1 = finished logo)
  0.00–0.35 gold ring draws itself · 0.20–0.45 dashed outer ring · 0.25–0.50 "KR's"
  0.35–0.60 "What If" pops in · 0.50–0.75 "EXPLAINED" wipes in · 0.60+ glow pulse
  The sting runs ~2.5 s after the hook (p = time / 2.5). Only the background behind it may change.
chapter_card(c, W, H, value, name, p=1.0, t=0.0)   ~1.5 s full-screen card, e.g. ("+2 HOURS", "The city goes dark")
end_card(c, W, H, p=1.0, t=0.0)                    logo + "See you in the next What If"
"""
import math

import skia

from primitives import (back_out, col, ease, ease_out, font, glow, night_sky, paint, span, text, text_w,
                        finish)

R = 190.0


def _ring(c, cx, cy, r, prog, color, width, a=1.0):
    if prog <= 0:
        return
    path = skia.Path()
    path.addArc(skia.Rect(cx - r, cy - r, cx + r, cy + r), -90, 359.9 * min(prog, 1.0))
    c.drawPath(path, paint(color, a, stroke=width))


def draw_logo(c, cx, cy, s=1.0, p=1.0, t=0.0):
    r = R * s
    ring = ease(span(p, 0.0, 0.35))
    pulse = 0.5 + 0.5 * math.sin(t * 2.4) if p >= 1 else ease(span(p, 0.6, 0.85))
    glow(c, cx, cy, r * 1.9, "magenta", 0.22 + 0.10 * pulse * ring)
    glow(c, cx, cy, r * 1.25, "amber", 0.10 + 0.08 * pulse * ring)
    # dashed outer ring (the channel's "missing" circle motif), slowly turning
    da = ease(span(p, 0.2, 0.45))
    if da > 0:
        dash = paint("teal", 0.8 * da, stroke=3 * s)
        dash.setPathEffect(skia.DashPathEffect.Make([14 * s, 12 * s], 0))
        c.save(); c.rotate(t * 6.0, cx, cy)
        c.drawCircle(cx, cy, r * 1.14, dash)
        c.restore()
    # gold ring drawing itself, with a bright head while it draws
    _ring(c, cx, cy, r, ring, "amber", 9 * s)
    _ring(c, cx, cy, r, ring, "gold", 3 * s, 0.9)
    if 0 < ring < 1:
        ang = math.radians(-90 + 360 * ring)
        glow(c, cx + r * math.cos(ang), cy + r * math.sin(ang), 34 * s, "gold", 0.9)
    # KR's
    a = ease_out(span(p, 0.25, 0.50))
    if a > 0:
        text(c, "KR's", cx, cy - 62 * s + (1 - a) * 18 * s, font("semibold", 40 * s), paint("sand", a), spacing=5 * s)
    # What If
    w = span(p, 0.35, 0.60)
    if w > 0:
        k = back_out(w)
        c.save(); c.translate(cx, cy + 28 * s); c.scale(k, k)
        text(c, "What If", -6 * s, 0, font("serif_italic", 88 * s), paint("cream", min(1, w * 2)))
        c.restore()
    # EXPLAINED wipe
    e = ease(span(p, 0.50, 0.75))
    if e > 0:
        f = font("bold", 28 * s)
        sp = 10 * s
        tw = text_w("EXPLAINED", f, sp)
        c.save()
        c.clipRect(skia.Rect(cx - tw / 2 - 4, cy + 60 * s, cx - tw / 2 + tw * e + 4, cy + 110 * s))
        text(c, "EXPLAINED", cx, cy + 86 * s, f, paint("teal"), spacing=sp)
        c.restore()


def chapter_card(c, W, H, value, name, p=1.0, t=0.0):
    night_sky(c, W, H, t)
    s = min(W, H) / 1080
    cx, cy = W / 2, H / 2 - 30 * s
    glow(c, cx, cy, 420 * s, "plum", 0.45)
    ring = ease(span(p, 0.0, 0.5))
    dash = paint("teal", 0.75, stroke=3 * s)
    dash.setPathEffect(skia.DashPathEffect.Make([14 * s, 12 * s], 0))
    c.save(); c.rotate(t * 8.0, cx, cy)
    path = skia.Path(); path.addArc(skia.Rect(cx - 420 * s, cy - 420 * s, cx + 420 * s, cy + 420 * s), -90, 359.9 * ring)
    c.drawPath(path, dash)
    c.restore()
    k = back_out(span(p, 0.1, 0.55))
    if k > 0:
        c.save(); c.translate(cx, cy + 60 * s); c.scale(k, k)
        text(c, value, 0, 0, font("extrabold", 150 * s), paint("gold"))
        c.restore()
    a = ease_out(span(p, 0.4, 0.8))
    if a > 0:
        text(c, name, cx, cy + 170 * s + (1 - a) * 20 * s, font("semibold", 52 * s), paint("cream", a))
    finish(c, W, H, t)


def end_card(c, W, H, p=1.0, t=0.0):
    night_sky(c, W, H, t)
    s = min(W, H) / 1080
    draw_logo(c, W / 2, H / 2 - 70 * s, s, min(1.0, p * 1.4), t)
    a = ease_out(span(p, 0.6, 1.0))
    if a > 0:
        text(c, "See you in the next What If", W / 2, H / 2 + 250 * s, font("serif_italic", 64 * s), paint("cream", a))
    finish(c, W, H, t)
