"""KR, the channel's cartoon host. LOCKED: reuse as-is in every video, never redraw.

draw_kr(c, x, y, s=1.0, expr="curious", t=0.0, look=(0, 0), flip=False)
  (x, y) = bottom centre of the bust; at s=1 KR is ~350 px tall.
  expr: curious | shocked | thinking | happy | worried | pointing | neutral
  t: global time in seconds (drives blink, breathing, tremble); look: pupils, each -1..1
  flip: mirror (KR faces/points left)

New poses or expressions are built from the parts below and added to EXPRESSIONS.
"""
import math

import skia

from primitives import col, paint, font, text

EXPRESSIONS = ["neutral", "curious", "shocked", "thinking", "happy", "worried", "pointing"]

# per expression: head tilt (deg), eye scale, pupil scale, brows (left, right) as (y_inner, y_outer),
# mouth kind, arms kind, default look
POSE = {
    "neutral":  dict(tilt=0,  eye=1.00, pupil=1.0, brows=((-242, -238), (-242, -238)), mouth="smile", arms="down", look=(0, 0)),
    "curious":  dict(tilt=7,  eye=1.05, pupil=1.0, brows=((-250, -250), (-238, -236)), mouth="smirk", arms="down", look=(0.6, -0.2)),
    "shocked":  dict(tilt=0,  eye=1.28, pupil=0.6, brows=((-256, -252), (-256, -252)), mouth="o",     arms="cheeks", look=(0, 0)),
    "thinking": dict(tilt=-6, eye=1.00, pupil=1.0, brows=((-248, -244), (-238, -236)), mouth="flat",  arms="chin", look=(-0.7, -0.8)),
    "happy":    dict(tilt=4,  eye=1.00, pupil=1.0, brows=((-248, -242), (-248, -242)), mouth="grin",  arms="open", look=(0, 0)),
    "worried":  dict(tilt=-4, eye=1.08, pupil=0.85, brows=((-248, -236), (-248, -236)), mouth="wave", arms="hands", look=(0, 0.3)),
    "pointing": dict(tilt=3,  eye=1.00, pupil=1.0, brows=((-246, -240), (-244, -240)), mouth="smile", arms="point", look=(1, 0)),
}

HEAD_C = (0.0, -215.0)
HEAD_R = 72.0


def _blinking(t, expr):
    return expr not in ("happy", "shocked") and (t % 3.7) < 0.12


def _arm(c, pts, w=34):
    p = paint("hoodie", stroke=w)
    path = skia.Path()
    path.moveTo(*pts[0])
    if len(pts) == 3:
        path.quadTo(*pts[1], *pts[2])
    else:
        path.lineTo(*pts[1])
    c.drawPath(path, paint("ink", 0.9, stroke=w + 7))
    c.drawPath(path, p)


def _hand(c, x, y, r=17, finger=None):
    if finger:
        fx, fy = finger
        c.drawLine(x, y, fx, fy, paint("ink", 0.9, stroke=13))
        c.drawLine(x, y, fx, fy, paint("skin", stroke=9))
    c.drawCircle(x, y, r + 3, paint("ink", 0.9))
    c.drawCircle(x, y, r, paint("skin"))


def _arms_behind(c, kind):
    if kind in ("down", "open"):
        spread = 26 if kind == "open" else 0
        for sx in (-1, 1):
            _arm(c, [(sx * 92, -112), (sx * (118 + spread), -60), (sx * (112 + spread), -18)])
            _hand(c, sx * (112 + spread), -16)


def _arms_front(c, kind, t):
    if kind == "point":
        _arm(c, [(-92, -112), (-118, -60), (-112, -18)]); _hand(c, -112, -16)
        _arm(c, [(92, -112), (150, -128), (196, -150)])
        _hand(c, 200, -152, finger=(236, -168))
    elif kind == "chin":
        _arm(c, [(-92, -112), (-118, -60), (-112, -18)]); _hand(c, -112, -16)
        _arm(c, [(92, -112), (122, -40), (40, -150)])
        _hand(c, 34, -160)
    elif kind == "cheeks":
        for sx in (-1, 1):
            _arm(c, [(sx * 92, -112), (sx * 130, -120), (sx * 84, -186)])
            _hand(c, sx * 80, -190)
    elif kind == "hands":
        for sx in (-1, 1):
            _arm(c, [(sx * 92, -112), (sx * 96, -60), (sx * 22, -74)])
        _hand(c, -16, -76); _hand(c, 16, -76)


def _body(c):
    body = skia.RRect.MakeRectXY(skia.Rect(-108, -152, 108, 40), 72, 72)
    c.drawRRect(body, paint("ink", 0.9))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-104, -148, 104, 40), 68, 68), paint("hoodie"))
    # shade on the left side, hood collar, drawstrings, KR badge
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect(-104, -148, 104, 40), 68, 68))
    c.drawCircle(-150, -40, 90, paint("hoodie_shade", 0.7)); c.restore()
    collar = skia.Path(); collar.addArc(skia.Rect(-58, -182, 58, -112), 20, 140)
    c.drawPath(collar, paint("hoodie_shade", stroke=16))
    for sx in (-1, 1):
        c.drawLine(sx * 14, -130, sx * 16, -92, paint("sand", stroke=4))
    c.drawCircle(46, -84, 21, paint("sand"))
    text(c, "KR", 46, -76.5, font("extrabold", 19), paint("ink"))


def _head(c, pose, expr, t, look):
    hx, hy = HEAD_C
    c.drawRect(skia.Rect(-20, -168, 20, -138), paint("skin_shade"))          # neck
    for sx in (-1, 1):                                                         # ears
        c.drawCircle(hx + sx * 70, hy + 4, 17, paint("ink", 0.9))
        c.drawCircle(hx + sx * 70, hy + 4, 14, paint("skin_shade"))
    c.drawCircle(hx, hy, HEAD_R + 3.5, paint("ink", 0.9))
    c.drawCircle(hx, hy, HEAD_R, paint("skin"))
    # hair: a cap clipped to the head + a front quiff
    c.save()
    hp = skia.Path(); hp.addCircle(hx, hy, HEAD_R + 3.5); c.clipPath(hp, doAntiAlias=True)
    c.drawCircle(hx + 6, hy - 104, 74, paint("hair"))
    c.restore()
    q = skia.Path(); q.moveTo(-30, -280); q.quadTo(4, -326, 52, -300); q.quadTo(24, -290, 12, -276); q.close()
    c.drawPath(q, paint("hair"))
    # rim light (teal, right side)
    rim = skia.Path(); rim.addArc(skia.Rect(hx - HEAD_R, hy - HEAD_R, hx + HEAD_R, hy + HEAD_R), -50, 95)
    c.drawPath(rim, paint("teal", 0.55, stroke=4))
    # cheeks
    if expr in ("happy", "pointing", "curious"):
        for sx in (-1, 1):
            c.drawCircle(hx + sx * 44, hy + 20, 11, paint("magenta", 0.22))
    # eyes
    lx, ly = look
    for sx in (-1, 1):
        ex, ey = hx + sx * 26, hy + 2
        if expr == "happy":
            arc = skia.Path(); arc.moveTo(ex - 12, ey + 4); arc.quadTo(ex, ey - 12, ex + 12, ey + 4)
            c.drawPath(arc, paint("ink", stroke=5.5))
            continue
        if _blinking(t, expr):
            c.drawLine(ex - 13, ey + 2, ex + 13, ey + 2, paint("ink", stroke=5))
            continue
        rx, ry = 15 * pose["eye"], 17 * pose["eye"]
        c.drawOval(skia.Rect(ex - rx, ey - ry, ex + rx, ey + ry), paint("white"))
        c.drawOval(skia.Rect(ex - rx, ey - ry, ex + rx, ey + ry), paint("ink", stroke=3))
        pr = 8 * pose["pupil"]
        px, py = ex + lx * (rx - pr - 2), ey + ly * (ry - pr - 2)
        c.drawCircle(px, py, pr, paint("ink"))
        c.drawCircle(px + pr * 0.35, py - pr * 0.4, max(1.6, pr * 0.32), paint("white"))
    # brows
    for sx, (yi, yo) in zip((-1, 1), pose["brows"]):
        c.drawLine(hx + sx * 12, yi + 6, hx + sx * 40, yo + 6, paint("ink", stroke=6))
    # mouth
    my, m = hy + 34, pose["mouth"]
    if m == "smile":
        p = skia.Path(); p.moveTo(-16, my); p.quadTo(0, my + 12, 16, my); c.drawPath(p, paint("ink", stroke=5))
    elif m == "smirk":
        p = skia.Path(); p.moveTo(-12, my + 2); p.quadTo(4, my + 9, 18, my - 4); c.drawPath(p, paint("ink", stroke=5))
    elif m == "flat":
        p = skia.Path(); p.moveTo(-12, my + 3); p.lineTo(10, my + 1); c.drawPath(p, paint("ink", stroke=5))
    elif m == "o":
        c.drawOval(skia.Rect(-12, my - 8, 12, my + 20), paint("ink"))
        c.drawOval(skia.Rect(-7, my + 7, 7, my + 17), paint("sunset", 0.9))
    elif m == "grin":
        p = skia.Path(); p.moveTo(-24, my - 4); p.quadTo(0, my + 30, 24, my - 4); p.close()
        c.drawPath(p, paint("ink"))
        c.save(); c.clipPath(p, doAntiAlias=True)
        c.drawCircle(0, my + 22, 12, paint("sunset", 0.9)); c.restore()
    elif m == "wave":
        p = skia.Path(); p.moveTo(-18, my + 4)
        p.cubicTo(-10, my - 4, -4, my + 10, 2, my + 3); p.cubicTo(8, my - 4, 12, my + 8, 18, my + 3)
        c.drawPath(p, paint("ink", stroke=4.5))
    if expr == "worried":   # sweat drop
        d = skia.Path(); d.moveTo(hx + 62, hy - 40); d.quadTo(hx + 74, hy - 20, hx + 66, hy - 14)
        d.quadTo(hx + 56, hy - 20, hx + 62, hy - 40); c.drawPath(d, paint("cream", 0.85))


def draw_kr(c, x, y, s=1.0, expr="curious", t=0.0, look=None, flip=False):
    pose = POSE.get(expr, POSE["neutral"])
    look = pose["look"] if look is None else look
    breathe = math.sin(t * 2.2) * 3.0
    tremble = math.sin(t * 41.0) * 1.6 if expr == "shocked" else 0.0
    c.save()
    c.translate(x + tremble * s, y)
    c.scale(-s if flip else s, s)
    c.translate(0, breathe * 0.4)
    # soft ground glow so KR sits in any scene
    c.drawOval(skia.Rect(-120, 18, 120, 44), paint("space", 0.35))
    _arms_behind(c, pose["arms"])
    _body(c)
    c.save()
    c.translate(0, breathe * 0.6)
    c.rotate(pose["tilt"], 0, -150)
    _head(c, pose, expr, t, look)
    c.restore()
    _arms_front(c, pose["arms"], t)
    c.restore()
