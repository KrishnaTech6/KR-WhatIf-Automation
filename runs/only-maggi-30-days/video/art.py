"""Topic art for 'What If You Ate Only Maggi for 30 Days?' (atlas style: flat illustrated night scenes, warm lamp
rim light vs cool moonlight, sunset glows, dashed 'missing' outlines). Every drawing is a pure function of its inputs
and t. The packet is our own drawing (yellow pouch, red oval, our font), never the real logo artwork."""
import math
import skia
from krwi.lib import *  # noqa: F401,F403
from krwi.art import *  # noqa: F401,F403

YEL, YEL_D, YEL_L = "#F6C21C", "#C98F0A", "#FFE57A"
RED, RED_D = "#D8262E", "#8E1620"
NOOD, NOOD_D, NOOD_L = "#F2C14E", "#A86A12", "#FFF0B0"
WOOD, WOOD_D, WOOD_L = "#7A4A2E", "#4E2E1C", "#A06A44"
NIGHT = "#241843"
COOL = "#7FB2FF"
SKIN = "#C98B5E"


def rr(x0, y0, x1, y1, r):
    return skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), r, r)


def dashed(color, a=1.0, stroke=6, on=18, off=12):
    p = paint(color, a, stroke=stroke)
    p.setPathEffect(skia.DashPathEffect.Make([on, off], 0))
    return p


def label(c, s, x, y, size, color="cream", kind="bold", a=1.0, align="center"):
    if a > 0:
        text(c, s, x, y, font(kind, size), paint(color, a), align)


def hgrad(x0, x1, cols, stops=None):
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(x0, 0), skia.Point(x1, 0)], [col(k) for k in cols], stops))
    return p


def vgrad(y0, y1, cols, stops=None):
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(0, y0), skia.Point(0, y1)], [col(k) for k in cols], stops))
    return p


def ellipse(c, x, y, rx, ry, p):
    c.drawOval(skia.Rect(x - rx, y - ry, x + rx, y + ry), p)


def dim(c, a):
    if a > 0:
        c.drawRect(skia.Rect(0, 0, W, H), paint("space", a))


# ---------------------------------------------------------------- backgrounds
def room_bg(c, t, lamp=1.0, moon=1.0, warn=0.0):
    """Hostel room at night: warm desk-lamp glow on the left, cool moonlit window on the right."""
    c.drawRect(skia.Rect(0, 0, W, H), vgrad(0, H, ["#1C1238", "#24164A", "#1A1034"]))
    c.drawRect(skia.Rect(0, H * 0.78, W, H), paint("#120A24"))
    c.drawLine(0, H * 0.78, W, H * 0.78, paint("#2E1E52", stroke=4))
    # window with moonlight
    c.drawRRect(rr(1460, 110, 1820, 470, 10), paint("#101C3E"))
    glow(c, 1700, 200, 220, COOL, 0.22 * moon)
    c.drawCircle(1720, 190, 34, paint("#DCE8FF", 0.85 * moon))
    for k in range(18):
        c.drawCircle(1470 + rng(k, 9) * 340, 120 + rng(k, 10) * 330, 1.5 + rng(k, 11) * 2, paint("cream", 0.5))
    c.drawRRect(rr(1460, 110, 1820, 470, 10), paint("#3A2A5E", stroke=14))
    c.drawLine(1640, 110, 1640, 470, paint("#3A2A5E", stroke=10))
    glow(c, 1600, 700, 600, COOL, 0.10 * moon)
    # poster
    c.drawRRect(rr(120, 140, 360, 460, 6), paint("#3A1F55"))
    c.drawCircle(240, 270, 70, paint("magenta", 0.5)); c.drawRect(skia.Rect(150, 380, 330, 400), paint("sand", 0.3))
    glow(c, 260, 520, 760, "amber", 0.20 * lamp)
    if warn > 0:
        glow(c, W / 2, H * 0.6, 900, "coral", 0.25 * warn)
    vignette(c, W, H, 0.5)


def table_top(c, y=820, a=1.0):
    c.drawRect(skia.Rect(0, y, W, H), vgrad(y, H, [WOOD, WOOD_D]))
    c.drawLine(0, y, W, y, paint(WOOD_L, a, stroke=6))
    for k in range(6):
        yy = y + 40 + k * 45
        c.drawLine(0, yy, W, yy + 10 * math.sin(k), paint(WOOD_D, 0.45, stroke=3))


# ---------------------------------------------------------------- noodles + bowl (the hero)
def noodle_tangle(c, rx, ry, seed=0, n=46, tint=None, t=0.0):
    """Wavy instant noodles packed into an ellipse (rx, ry) centred at the origin (already clipped by caller)."""
    base = tint or NOOD
    for pass_, (colr, w) in enumerate([(NOOD_D, 13), (base, 9), (NOOD_L, 2.6)]):
        for j in range(n):
            x0 = (rng(j, 1 + seed) - 0.5) * rx * 1.7
            y0 = (rng(j, 2 + seed) - 0.5) * ry * 1.7
            th = rng(j, 3 + seed) * math.pi
            L = rx * (0.55 + 0.45 * rng(j, 4 + seed))
            ph = rng(j, 5 + seed) * 6.28
            p = skia.Path()
            first = True
            u = -L / 2
            while u <= L / 2:
                px, py = u, 9 * math.sin(u * 0.16 + ph) + (0 if pass_ < 2 else -2.5)
                X = x0 + px * math.cos(th) - py * math.sin(th)
                Y = y0 + (px * math.sin(th) + py * math.cos(th)) * (ry / rx) * 1.25
                if first:
                    p.moveTo(X, Y); first = False
                else:
                    p.lineTo(X, Y)
                u += 7
            c.drawPath(p, paint(colr, 0.85 if pass_ == 2 else 1.0, stroke=w))


def steam(c, x, y, t, h=320, n=4, a=1.0, spread=180, colr="cream"):
    for i in range(n):
        ph = (t * 0.35 + i / n) % 1.0
        al = math.sin(math.pi * ph) * 0.45 * a
        if al <= 0.01:
            continue
        p = skia.Path()
        bx = x + (i - (n - 1) / 2) * spread / max(1, n - 1)
        for k in range(30):
            v = k / 29
            yy = y - ph * h * 0.6 - v * h * 0.6
            xx = bx + 26 * math.sin(v * 7 + t * 1.6 + i) * (0.4 + v)
            if k == 0:
                p.moveTo(xx, yy)
            else:
                p.lineTo(xx, yy)
        c.drawPath(p, paint(colr, al, stroke=10))


def bowl(c, x, y, s, t, steam_a=1.0, warn=0.0, veg=0.0, empty=False, dimmed=0.0, peas=None, egg=None, lemon_p=None, seed=0):
    """Hero bowl, rim centre at (x, y). warn: red warning glow. veg 0..1 blooms into a veg masala bowl.
    peas/egg/lemon_p: 0..1 drop-in progress of each topping (override veg for that topping)."""
    c.save(); c.translate(x, y); c.scale(s, s)
    if warn > 0:
        glow(c, 0, 60, 520, "coral", 0.45 * warn)
        glow(c, 0, 60, 300, RED, 0.35 * warn)
    glow(c, -260, 40, 300, "amber", 0.30)
    glow(c, 280, 40, 260, COOL, 0.22)
    # shadow
    sh = paint("space", 0.55); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 18))
    ellipse(c, 10, 255, 260, 34, sh)
    body = skia.Path()
    body.moveTo(-300, 0); body.cubicTo(-292, 170, -150, 245, 0, 245); body.cubicTo(150, 245, 292, 170, 300, 0); body.close()
    c.drawPath(body, hgrad(-300, 300, ["#F08A4A", "#B0303A", "#6E1A34", "#3E1438", "#5E7CD0"], [0, 0.18, 0.5, 0.8, 1]))
    # glossy band + highlight
    hl = skia.Path(); hl.moveTo(-250, 60); hl.cubicTo(-200, 160, -120, 200, -60, 210)
    c.drawPath(hl, paint("#FFD9B0", 0.45, stroke=10))
    c.drawPath(body, paint("#2A0C1E", 0.6, stroke=3))
    ellipse(c, 0, 248, 110, 18, paint("#3A1028"))
    # opening
    ellipse(c, 0, 0, 300, 82, paint("#F7E6C4"))
    ellipse(c, 0, 6, 284, 72, paint("#7A3410" if not empty else "#3A1A20"))
    if not empty:
        c.save()
        clip = skia.Path(); clip.addOval(skia.Rect(-280, -64, 280, 76))
        c.clipPath(clip, doAntiAlias=True)
        ellipse(c, 0, 8, 280, 70, paint("#C26A1C"))
        tint = None
        if veg > 0:
            tint = "#F2A23A" if veg > 0.3 else None
        noodle_tangle(c, 270, 66, seed=seed, tint=tint, t=t)
        pv = veg if peas is None else peas
        ev = veg if egg is None else egg
        lv = veg if lemon_p is None else lemon_p
        if veg > 0:
            for k in range(30):  # carrots, coriander, tomato bloom with veg
                a_ = span(veg, k / 45, k / 45 + 0.3)
                if a_ > 0:
                    px, py = (rng(k, 31) - 0.5) * 470, (rng(k, 32) - 0.5) * 100
                    kind = k % 3
                    if kind == 0:
                        c.drawRRect(rr(px - 18, py - 13, px + 18, py + 13, 5), paint("#F07A2A", a_))
                    elif kind == 1:
                        lf = skia.Path(); lf.moveTo(px - 22, py); lf.quadTo(px, py - 24, px + 22, py); lf.quadTo(px, py + 18, px - 22, py)
                        c.drawPath(lf, paint("#3FA34D", a_))
                    else:
                        ellipse(c, px, py, 22, 15, paint("#D8342E", a_)); ellipse(c, px, py, 12, 7, paint("#F27A5A", a_))
        if pv > 0:
            for k in range(16):
                a_ = span(pv, k / 24, k / 24 + 0.3)
                if a_ > 0:
                    px, py = (rng(k, 41) - 0.5) * 460, (rng(k, 42) - 0.5) * 95
                    dy = -120 * (1 - ease_out(a_))
                    c.drawCircle(px, py + dy, 13, paint("#5DBB46", a_))
                    c.drawCircle(px - 4, py + dy - 4, 4, paint("#C8F2A0", a_))
        if ev > 0:
            e = ease_out(ev)
            for side in (-1, 1):
                ex, ey = 110 * side, -6 - 160 * (1 - e)
                ellipse(c, ex, ey, 62, 40, paint("cream", min(1, ev * 2)))
                ellipse(c, ex + 4, ey + 2, 28, 20, paint("#F5B21E", min(1, ev * 2)))
        c.restore()
        if lv > 0:
            e = ease_out(lv)
            lx, ly = 230, -60 - 120 * (1 - e)
            lemon(c, lx, ly, 0.8, a=min(1, lv * 2), wedge=True)
    ellipse(c, 0, 0, 300, 82, paint("#FFE9C8", 0.9, stroke=6))
    rim = skia.Path(); rim.addArc(skia.Rect(-300, -82, 300, 82), 150, 60)
    c.drawPath(rim, paint("amber", 0.9, stroke=8))
    rim2 = skia.Path(); rim2.addArc(skia.Rect(-300, -82, 300, 82), -40, 70)
    c.drawPath(rim2, paint(COOL, 0.7, stroke=7))
    if not empty and steam_a > 0:
        steam(c, 0, -40, t, h=340, n=4, a=steam_a, spread=260)
    c.restore()


def lemon(c, x, y, s, a=1.0, wedge=False, glow_a=0.0, outline=False):
    c.save(); c.translate(x, y); c.scale(s, s)
    if glow_a > 0:
        glow(c, 0, 0, 160, "gold", glow_a)
    if outline:
        ellipse(c, 0, 0, 70, 52, dashed("gold", a, 5, 14, 9))
        c.restore(); return
    if wedge:
        p = skia.Path(); p.moveTo(-60, 0); p.arcTo(skia.Rect(-60, -60, 60, 60), 180, -180, False); p.close()
        c.drawPath(p, paint("#F4E04D", a))
        p2 = skia.Path(); p2.moveTo(-50, 0); p2.arcTo(skia.Rect(-50, -50, 50, 50), 180, -180, False); p2.close()
        c.drawPath(p2, paint("#FFF6A8", a))
        for k in range(5):
            ang = math.radians(180 - 18 - k * 36)
            c.drawLine(0, 0, 46 * math.cos(ang), -46 * math.sin(ang), paint("#F4E04D", a, stroke=3))
    else:
        ellipse(c, 0, 0, 70, 52, paint("#F4D83A", a))
        c.drawCircle(68, -4, 10, paint("#E0C02A", a))
        ellipse(c, -20, -18, 26, 12, paint("#FFF6B0", 0.7 * a))
        ellipse(c, 0, 0, 70, 52, paint("#B89A10", 0.6 * a, stroke=3))
        lf = skia.Path(); lf.moveTo(-60, -20); lf.quadTo(-90, -60, -50, -70); lf.quadTo(-50, -40, -60, -20)
        c.drawPath(lf, paint("#3FA34D", a))
    c.restore()


# ---------------------------------------------------------------- the packet (our own drawing)
def packet(c, x, y, s, t=0.0, rot=0.0, a=1.0, torn=0.0, dimmed=0.0, glow_a=0.0, num=None):
    """Yellow instant-noodle pouch centred at (x, y), 360x480 at s=1. torn 0..1 rips the top strip off."""
    if a <= 0:
        return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    if glow_a > 0:
        glow(c, 0, 0, 360, "gold", 0.35 * glow_a * a)
    sh = paint("space", 0.45 * a); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 16))
    c.drawRRect(rr(-170, -220, 190, 250, 20), sh)
    body = skia.Path()
    body.moveTo(-180, -205)
    body.cubicTo(-196, -60, -196, 60, -180, 205)
    body.lineTo(180, 205)
    body.cubicTo(196, 60, 196, -60, 180, -205)
    body.close()
    p = hgrad(-190, 190, [YEL_D, YEL, YEL_L, YEL, YEL_D], [0, 0.22, 0.5, 0.78, 1]); p.setAlphaf(a)
    c.drawPath(body, p)
    # crimp bands (zigzag edges)
    def band(y0, y1, edge_y, k_off=0.0):
        b = skia.Path(); b.moveTo(-180, y0)
        n = 18
        for i in range(n + 1):
            xx = -180 + 360 * i / n
            b.lineTo(xx, edge_y + (8 if i % 2 else -8))
        b.lineTo(180, y0); b.close()
        bp = paint("#E9B210", a); c.drawPath(b, bp)
        for i in range(1, 24):
            xx = -180 + 360 * i / 24
            c.drawLine(xx, min(y0, edge_y) + 6, xx, max(y0, edge_y) - 6, paint(YEL_D, 0.5 * a, stroke=3))
    band(205, 205, 244)
    if torn < 1:
        c.save()
        if torn > 0:
            e = ease_out(torn)
            c.translate(60 * e, -90 * e); c.rotate(-14 * e)
        if torn < 0.7:
            c.saveLayerAlpha(None, int(255 * a * (1 - torn / 0.7)))
            band(-205, -205, -244)
            c.restore()
        c.restore()
    if torn > 0:
        c.drawLine(-180, -205, 180, -205, paint(YEL_D, a, stroke=4))
        if torn < 0.6:   # noodle bits flying out
            for k in range(6):
                v = torn / 0.6
                c.drawCircle(-80 + k * 32, -215 - 160 * v * (0.5 + rng(k, 3)), 7, paint(NOOD, a * (1 - v)))
    # red oval label with our wordmark
    c.save(); c.translate(0, -88)
    ellipse(c, 0, 0, 150, 82, paint("#FFE14D", a))
    ellipse(c, 0, 0, 140, 73, paint(RED, a))
    ellipse(c, 0, 0, 140, 73, paint(RED_D, a, stroke=4))
    ellipse(c, -40, -36, 70, 16, paint("#FF7A7A", 0.35 * a))
    text(c, "MAGGI", 0, 22, font("extrabold", 62), paint("#FFE14D", a))
    c.restore()
    # window with a little bowl of noodles
    c.drawRRect(rr(-130, 30, 130, 180, 24), paint("#E7A10E", a))
    c.save(); c.clipRRect(rr(-130, 30, 130, 180, 24))
    ellipse(c, 0, 118, 108, 30, paint(RED_D, a))
    c.translate(0, 112); c.scale(0.36, 0.36)
    cl = skia.Path(); cl.addOval(skia.Rect(-280, -64, 280, 76)); c.clipPath(cl, doAntiAlias=True)
    ellipse(c, 0, 8, 280, 70, paint("#C26A1C", a))
    noodle_tangle(c, 270, 66, seed=3, n=22)
    c.restore()
    label(c, "MASALA", 0, 160 + 34, 26, RED_D, "extrabold", a)
    # rim light: warm left, cool right
    c.drawLine(-182, -190, -192, 190, paint("amber", 0.55 * a, stroke=5))
    c.drawLine(182, -190, 192, 190, paint(COOL, 0.45 * a, stroke=5))
    if num is not None:
        pill(c, 0, 300, 1.0, num, "coral", "cream", 40)
    c.restore()
    if dimmed > 0:
        c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
        c.drawPath(body, paint("space", dimmed * a)); c.restore()


def calendar_page(c, x, y, s, top, big, rot=0.0, a=1.0, tear=0.0, red=True):
    """Torn calendar page (top line small, big number/word)."""
    if a <= 0:
        return
    c.save(); c.translate(x, y); c.rotate(rot + tear * 25); c.translate(tear * 240, -tear * 160); c.scale(s, s)
    sh = paint("space", 0.4 * a); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 12))
    c.drawRect(skia.Rect(-150, -170, 160, 190), sh)
    pg = skia.Path(); pg.moveTo(-150, -180); pg.lineTo(150, -180)
    for i in range(13):
        pg.lineTo(150 - i * 25, 180 + (10 if i % 2 else -6))
    pg.lineTo(-150, 180); pg.close()
    c.drawPath(pg, paint("cream", a))
    c.drawRect(skia.Rect(-150, -180, 150, -100), paint("coral" if red else "teal", a))
    for k in range(5):
        c.drawCircle(-100 + k * 50, -180, 10, paint("#2A2040", a))
    label(c, top, 0, -125, 40, "cream", "extrabold", a)
    f = 150 if len(big) <= 2 else 110 if len(big) <= 3 else 80
    label(c, big, 0, 80, f, "ink", "extrabold", a)
    c.restore()


def shelf(c, x, y, w, t, n=7, shows=None, lemon_a=1.0, lemon_glow=0.0, ps=0.42):
    """Wooden hostel shelf (plank top at y, centred at x) with n packets standing like trophies; shows[i] = 0..1 pop."""
    c.drawRect(skia.Rect(x - w / 2, y, x + w / 2, y + 34), paint(WOOD_L))
    c.drawRect(skia.Rect(x - w / 2, y + 34, x + w / 2, y + 50), paint(WOOD_D))
    c.drawLine(x - w / 2, y, x + w / 2, y, paint("amber", 0.6, stroke=4))
    for bx in (x - w / 2 + 70, x + w / 2 - 70):
        c.drawRect(skia.Rect(bx - 10, y + 50, bx + 10, y + 120), paint(WOOD_D))
    gap = (w - 260) / max(1, n - 1) if n > 1 else 0
    for i in range(n):
        p = 1.0 if shows is None else shows[i]
        if p <= 0:
            continue
        k = back_out(p)
        px = x - w / 2 + 110 + i * gap
        c.save(); c.translate(px, y); c.scale(k, k); c.translate(-px, -y)
        packet(c, px, y - 250 * ps, ps, t, rot=0.0)
        c.restore()
    if lemon_a > 0:
        lemon(c, x + w / 2 - 50, y - 36, 0.55, lemon_a, glow_a=lemon_glow)


# ---------------------------------------------------------------- people (faceless silhouettes)
def figure(c, x, y, s, a=1.0, arm_l=200, arm_r=-20, lean=0.0, belly=0.0, rim="amber", fill=NIGHT, head_tilt=0.0, seated=False):
    """Faceless silhouette, feet at (x, y), ~560 px tall at s=1. Arm angles in degrees (0 = right, 90 = down)."""
    if a <= 0:
        return
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(lean)
    glow(c, 0, -380, 330, rim, 0.22 * a)
    fp = paint(fill, a)
    rimp = paint(rim, 0.75 * a, stroke=5)
    if not seated:
        c.drawLine(-28, -220, -34, 0, paint(fill, a, stroke=44))
        c.drawLine(28, -220, 34, 0, paint(fill, a, stroke=44))
    else:
        c.drawLine(-28, -200, 80, -200, paint(fill, a, stroke=44)); c.drawLine(80, -200, 90, -40, paint(fill, a, stroke=44))
    bw = 78 + 60 * belly
    torso = skia.Path(); torso.moveTo(-70, -430); torso.cubicTo(-80 - 40 * belly, -330, -bw, -260, -66, -200)
    torso.lineTo(66, -200); torso.cubicTo(bw, -260, 80 + 40 * belly, -330, 70, -430); torso.close()
    c.drawPath(torso, fp)
    for ang, sx in ((arm_l, -62), (arm_r, 62)):
        r = math.radians(ang)
        ex, ey = sx + 200 * math.cos(r), -410 + 200 * math.sin(r)
        c.drawLine(sx, -410, ex, ey, paint(fill, a, stroke=36))
    c.save(); c.translate(0, -430); c.rotate(head_tilt)
    c.drawLine(0, 0, 0, -30, paint(fill, a, stroke=40))
    c.drawCircle(0, -82, 60, fp)
    arc = skia.Path(); arc.addArc(skia.Rect(-60, -142, 60, -22), 120, 110)
    c.drawCircle(0, -82, 60, paint(COOL, 0.25 * a, stroke=3))
    c.drawPath(arc, rimp)
    arc2 = skia.Path(); arc2.addArc(skia.Rect(-60, -142, 60, -22), -60, 80)
    c.drawPath(arc2, paint(COOL, 0.55 * a, stroke=4))
    c.restore()
    c.drawPath(torso, paint(rim, 0.6 * a, stroke=6))
    c.restore()


def bubble(c, x, y, w, h, s_txt, size=48, color="cream", tcolor="ink", a=1.0, tail=-1, kind="extrabold"):
    """Speech bubble centred at (x, y), tail toward bottom-left (tail=-1) or bottom-right (1)."""
    if a <= 0:
        return
    k = back_out(min(1, a))
    c.save(); c.translate(x, y); c.scale(k, k)
    tl = skia.Path(); tl.moveTo(tail * w * 0.15, h / 2 - 4); tl.lineTo(tail * w * 0.38, h / 2 + 50); tl.lineTo(tail * w * 0.30, h / 2 - 4); tl.close()
    c.drawPath(tl, paint(color, a))
    c.drawRRect(rr(-w / 2, -h / 2, w / 2, h / 2, h * 0.4), paint(color, a))
    label(c, s_txt, 0, size * 0.35, size, tcolor, kind, a)
    c.restore()


def phone(c, x, y, s, t, screen="call", a=1.0, rot=0.0, name="MUMMY", pct=5, ring=1.0, rec=0.0):
    """Phone, centre (x, y). screen: call | battery | rec."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    if ring > 0 and screen == "call":
        jx = math.sin(t * 60) * 5 * ring
        c.translate(jx, 0)
        for k in range(3):
            ph = (t * 1.4 + k / 3) % 1
            c.drawRRect(rr(-170 - ph * 90, -330 - ph * 90, 170 + ph * 90, 330 + ph * 90, 50 + ph * 40), paint("teal", (1 - ph) * 0.5 * ring, stroke=6))
    glow(c, 0, 0, 380, "teal", 0.3 * a)
    c.drawRRect(rr(-160, -320, 160, 320, 42), paint("#0B0B12", a))
    c.drawRRect(rr(-160, -320, 160, 320, 42), paint("#4B4B60", a, stroke=6))
    c.drawRRect(rr(-145, -300, 145, 300, 30), paint("#14203E", a))
    if screen == "call":
        label(c, "incoming call", 0, -200, 28, "sand", "bold", a)
        c.drawCircle(0, -80, 70, paint("magenta", a))
        label(c, "M", 0, -56, 70, "cream", "extrabold", a)
        label(c, name, 0, 60, 56, "cream", "extrabold", a)
        c.drawCircle(-80, 210, 44, paint("coral", a)); c.drawCircle(80, 210, 44, paint("#3BB273", a))
        c.drawLine(-100, 210, -60, 210, paint("cream", a, stroke=10)); c.drawLine(64, 200, 96, 220, paint("cream", a, stroke=10))
    elif screen == "battery":
        c.drawRRect(rr(-90, -120, 90, 160, 20), paint("cream", a, stroke=10))
        c.drawRRect(rr(-35, -150, 35, -120, 8), paint("cream", a))
        blink = 0.5 + 0.5 * math.sin(t * 8)
        fh = 260 * pct / 100
        c.drawRRect(rr(-72, 142 - max(fh, 10), 72, 142, 8), paint("coral", a * (0.5 + 0.5 * blink)))
        label(c, f"{pct}%", 0, 250, 64, "coral", "extrabold", a)
    elif screen == "rec":
        c.save(); c.clipRRect(rr(-145, -300, 145, 300, 30))
        c.restore()
        c.drawCircle(-100, -260, 12, paint("coral", a * (0.5 + 0.5 * math.sin(t * 6))))
        label(c, "REC", -40, -250, 30, "coral", "extrabold", a)
    c.restore()


# ---------------------------------------------------------------- body + salt
def meter(c, x, y, w, h, p, colr, title, value=None, a=1.0, empty_label=None):
    """Vertical tube meter, centre-bottom (x, y). p = fill 0..1."""
    c.drawRRect(rr(x - w / 2, y - h, x + w / 2, y, w / 2), paint("#1A1236", 0.9 * a))
    fh = (h - 16) * clamp(p)
    if fh > 2:
        c.drawRRect(rr(x - w / 2 + 8, y - 8 - fh, x + w / 2 - 8, y - 8, w / 2 - 8), paint(colr, a))
        glow(c, x, y - 8 - fh, w * 1.2, colr, 0.35 * a)
    c.drawRRect(rr(x - w / 2, y - h, x + w / 2, y, w / 2), paint("cream", 0.85 * a, stroke=6))
    for k in range(1, 5):
        yy = y - h * k / 5
        c.drawLine(x + w / 2 - 22, yy, x + w / 2 - 6, yy, paint("cream", 0.6 * a, stroke=4))
    label(c, title, x, y - h - 30, 44, "cream", "extrabold", a)
    if value:
        label(c, value, x, y + 70, 56, colr, "extrabold", a)


def salt_jar(c, x, y, s, fill, a=1.0, over=0.0, t=0.0):
    """Glass jar 'DAILY SALT LIMIT', bottom-centre (x, y). fill 0..1, over > 0 = salt heaped above and spilling."""
    c.save(); c.translate(x, y); c.scale(s, s)
    glow(c, 0, -260, 360, COOL, 0.15)
    jar = rr(-170, -520, 170, 0, 40)
    c.drawRRect(jar, paint("#2A3A6A", 0.35 * a))
    c.save(); c.clipRRect(jar)
    fh = 500 * clamp(fill)
    c.drawRect(skia.Rect(-170, -fh, 170, 0), paint("#F4F1E8", 0.95 * a))
    for k in range(int(80 * clamp(fill))):
        c.drawCircle(-160 + rng(k, 5) * 320, -rng(k, 6) * fh, 3, paint("#C9C3B8", a))
    c.restore()
    c.drawRRect(jar, paint("#BFD4FF", 0.85 * a, stroke=7))
    c.drawRRect(rr(-130, -570, 130, -520, 10), paint("#8A93B8", a))
    c.drawLine(-140, -480, 140, -480, dashed("coral", a, 5, 16, 10))
    hl = skia.Path(); hl.moveTo(-140, -440); hl.lineTo(-140, -80)
    c.drawPath(hl, paint("white", 0.35 * a, stroke=10))
    if over > 0:
        e = ease_out(min(1, over))
        glow(c, 0, -600, 420, "coral", 0.25 * e * a)
        hp = skia.Path(); hp.moveTo(-190, -560); hp.quadTo(-120, -560 - 220 * e, 0, -560 - 240 * e)
        hp.quadTo(120, -560 - 220 * e, 190, -560); hp.close()
        c.drawPath(hp, paint("#F4F1E8", 0.95 * a))
        for side in (-1, 1):   # spilling down the sides into heaps
            sp = skia.Path(); sp.moveTo(side * 160, -560); sp.quadTo(side * 196, -470, side * 194, -40)
            c.drawPath(sp, paint("#F4F1E8", 0.9 * a, stroke=14 * e + 3))
            hp2 = skia.Path(); hp2.moveTo(side * 140, 0); hp2.quadTo(side * (240 + 40 * e), -160 * e, side * (360 + 60 * e), 0); hp2.close()
            c.drawPath(hp2, paint("#F4F1E8", 0.95 * a))
        for k in range(int(40 * e)):
            c.drawCircle((rng(k, 7) - 0.5) * 300, -560 - rng(k, 8) * 200 * e, 3, paint("#C9C3B8", a))
    c.restore()


def water_bottle(c, x, y, s, fill, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    b = skia.Path(); b.moveTo(-60, -320); b.lineTo(-60, -350); b.lineTo(60, -350); b.lineTo(60, -320)
    b.cubicTo(110, -280, 110, -250, 110, -200); b.lineTo(110, 0); b.lineTo(-110, 0); b.lineTo(-110, -200)
    b.cubicTo(-110, -250, -110, -280, -60, -320); b.close()
    c.drawPath(b, paint("#2A3A6A", 0.35 * a))
    c.save(); c.clipPath(b, doAntiAlias=True)
    fh = 330 * clamp(fill)
    c.drawRect(skia.Rect(-120, -fh, 120, 0), paint("#4FA3E0", 0.8 * a))
    c.restore()
    c.drawPath(b, paint("#BFD4FF", 0.9 * a, stroke=6))
    c.drawRRect(rr(-66, -390, 66, -350, 8), paint("#3A7CC0", a))
    c.restore()


def head_outline(c, x, y, s, puff=0.0, a=1.0, t=0.0):
    """Faceless head + shoulders outline (cream line) whose cheeks puff up with salt water."""
    c.save(); c.translate(x, y); c.scale(s, s)
    sw = 1 + 0.22 * puff
    sh = skia.Path(); sh.moveTo(-260, 380); sh.cubicTo(-240, 240, -120, 210, -70, 200); sh.lineTo(70, 200)
    sh.cubicTo(120, 210, 240, 240, 260, 380)
    c.drawPath(sh, paint("cream", a, stroke=8))
    c.drawLine(-60, 120, -70, 200, paint("cream", a, stroke=8)); c.drawLine(60, 120, 70, 200, paint("cream", a, stroke=8))
    hp = skia.Path()
    hp.moveTo(0, -200)
    hp.cubicTo(120, -200, 150, -100, 140 * sw, 0)
    hp.cubicTo(140 * sw, 100 + 30 * puff, 70, 160, 0, 165)
    hp.cubicTo(-70, 160, -140 * sw, 100 + 30 * puff, -140 * sw, 0)
    hp.cubicTo(-150, -100, -120, -200, 0, -200)
    if puff > 0:
        c.drawPath(hp, paint("#4FA3E0", 0.25 * puff * a))
    c.drawPath(hp, paint("cream", a, stroke=8))
    c.drawPath(hp, paint("amber", 0.4 * a, stroke=3))
    if puff > 0.3:
        for side in (-1, 1):
            ar = skia.Path(); ar.addArc(skia.Rect(side * 150 * sw - 60, -10, side * 150 * sw + 60, 110), -60 if side > 0 else 120, 120)
            c.drawPath(ar, paint("#7FC4FF", (puff - 0.3) * a, stroke=6))
    c.restore()


def finger_ring(c, x, y, s, t, swell=0.0, tug=0.0, a=1.0):
    """Close-up of a finger with a gold ring stuck below a swollen knuckle; a hand tugs it."""
    c.save(); c.translate(x, y); c.scale(s, s)
    fw = 70 * (1 + 0.25 * swell)
    c.drawRRect(rr(-420, -fw, 380, fw, fw), paint(SKIN, a))
    c.drawRRect(rr(300, -fw * 0.75, 400, fw * 0.75, 30), paint("#E8B6A0", a))
    c.drawRRect(rr(-420, -fw, 380, fw, fw), paint("#8A5634", a, stroke=5))
    c.drawLine(-200, -fw * 0.6, -200, fw * 0.6, paint("#8A5634", 0.5 * a, stroke=4))
    c.drawLine(100, -fw * 0.6, 100, fw * 0.6, paint("#8A5634", 0.5 * a, stroke=4))
    rx = 20 + 30 * tug * (0.5 + 0.5 * math.sin(t * 20))
    glow(c, rx, 0, 140, "gold", 0.4 * a)
    c.drawRRect(rr(rx - 34, -fw - 12, rx + 34, fw + 12, 20), paint("#D9A520", a))
    c.drawRRect(rr(rx - 34, -fw - 12, rx + 34, fw + 12, 20), paint("gold", a, stroke=6))
    c.drawCircle(rx, -fw - 26, 22, paint("#BFE8FF", a))
    c.restore()


def body_outline(c, x, y, s, water=0.0, t=0.0, a=1.0, vitc=None):
    """Full-body outline (feet at y), filled with rising blue water."""
    c.save(); c.translate(x, y); c.scale(s, s)
    b = skia.Path()
    b.addCircle(0, -720, 70)
    b.addRRect(rr(-120, -640, 120, -300, 60))
    b.addRRect(rr(-110, -330, -20, 0, 40)); b.addRRect(rr(20, -330, 110, 0, 40))
    b.addRRect(rr(-190, -620, -130, -330, 30)); b.addRRect(rr(130, -620, 190, -330, 30))
    c.drawPath(b, paint("#1A1236", 0.8 * a))
    if water > 0:
        c.save(); c.clipPath(b, doAntiAlias=True)
        top = -800 * clamp(water)
        wp = skia.Path(); wp.moveTo(-220, 10); wp.lineTo(-220, top)
        for k in range(23):
            xx = -220 + k * 20
            wp.lineTo(xx, top + 10 * math.sin(xx * 0.05 + t * 4))
        wp.lineTo(220, 10); wp.close()
        c.drawPath(wp, paint("#4FA3E0", 0.8 * a))
        c.restore()
    c.drawPath(b, paint("cream", 0.9 * a, stroke=6))
    c.restore()


def heart(c, x, y, s, t, rate=1.2, a=1.0, colr="coral"):
    k = 1 + 0.08 * max(0, math.sin(t * math.pi * 2 * rate)) ** 6
    c.save(); c.translate(x, y); c.scale(s * k, s * k)
    glow(c, 0, 0, 260, colr, 0.4 * a)
    p = skia.Path(); p.moveTo(0, 150); p.cubicTo(-260, -20, -150, -220, 0, -100); p.cubicTo(150, -220, 260, -20, 0, 150)
    c.drawPath(p, paint(colr, a)); c.drawPath(p, paint("#FFB4A0", 0.6 * a, stroke=5))
    c.restore()


def gauge(c, x, y, r, p, a=1.0, title="BLOOD PRESSURE"):
    arc = skia.Path(); arc.addArc(skia.Rect(x - r, y - r, x + r, y + r), 180, 180)
    c.drawPath(arc, paint("#2A1E4A", a, stroke=34))
    a1 = skia.Path(); a1.addArc(skia.Rect(x - r, y - r, x + r, y + r), 180, 180 * clamp(p))
    c.drawPath(a1, paint("coral" if p > 0.6 else "amber", a, stroke=34))
    ang = math.radians(180 + 180 * clamp(p))
    c.drawLine(x, y, x + (r - 40) * math.cos(ang), y + (r - 40) * math.sin(ang), paint("cream", a, stroke=10))
    c.drawCircle(x, y, 18, paint("cream", a))
    label(c, title, x, y + 70, 36, "sand", "bold", a)


# ---------------------------------------------------------------- gut
def gut_city(c, cx, cy, s, t, fade=0.0, plates=1.0, a=1.0):
    """The gut as a glowing night city of tiny bacteria (capsule towers + round domes) with empty plates in front.
    fade 0..1 = share of the bacteria types fading out (grey, transparent)."""
    c.save(); c.translate(cx, cy); c.scale(s, s)
    glow(c, 0, 40, 700, "magenta", 0.35 * a)
    lens = skia.Path(); lens.addOval(skia.Rect(-640, -360, 640, 360))
    c.drawPath(lens, paint("#2A0E2E", a))
    c.save(); c.clipPath(lens, doAntiAlias=True)
    # tissue folds (gut wall)
    for k in range(7):
        p = skia.Path(); yy = -320 + k * 90
        p.moveTo(-660, yy)
        for i in range(30):
            xx = -660 + i * 46
            p.lineTo(xx, yy + 22 * math.sin(xx * 0.012 + k))
        c.drawPath(p, paint("#5A1E46", 0.6 * a, stroke=26))
    cols = ["teal", "amber", "#7FC4FF", "magenta", "#9BE07A", "sand"]
    n = 64
    for i in range(n):
        gone = rng(i, 77) < fade * 1.0 and (i % 5 != 0 or fade > 0.35) and rng(i, 77) < 0.4 * min(1, fade / 0.4)
        aa = (0.22 if gone else 1.0) * a
        colr = "#6A6070" if gone else cols[i % 6]
        bx = -560 + (i % 16) * 74 + rng(i, 2) * 20
        row = i // 16
        by = 260 - row * 55 - rng(i, 3) * 20
        hgt = 80 + 200 * rng(i, 4) * (1 - row * 0.15)
        bob = 6 * math.sin(t * 2 + i)
        if i % 3:
            c.drawRRect(rr(bx - 24, by - hgt + bob, bx + 24, by + bob, 24), paint(colr, 0.9 * aa))
            for w_ in range(int(hgt // 40)):
                c.drawCircle(bx, by - 30 - w_ * 36 + bob, 6, paint("cream", 0.7 * aa))
        else:
            c.drawCircle(bx, by - 30 + bob, 34, paint(colr, 0.9 * aa))
            c.drawCircle(bx - 10, by - 42 + bob, 8, paint("cream", 0.6 * aa))
        if not gone:
            glow(c, bx, by - hgt / 2, 70, colr, 0.12 * aa)
    if plates > 0:
        for k in range(5):
            px = -440 + k * 220
            ellipse(c, px, 300, 80, 24, paint("cream", 0.9 * plates * a))
            ellipse(c, px, 300, 52, 14, paint("#D6CFC0", 0.9 * plates * a))
    c.restore()
    c.drawPath(lens, paint("gold", 0.7 * a, stroke=8))
    c.restore()


def loc_card(c, x, y, s, city, line2, line3=None, a=1.0, pin_p=1.0, colr="teal"):
    """A place card with a dropping pin: city name big, then year/detail lines. Never a map of India."""
    if a <= 0:
        return
    c.save(); c.translate(x, y); c.scale(s, s)
    glow(c, 0, 0, 520, colr, 0.25 * a)
    c.drawRRect(rr(-380, -230, 380, 250, 30), paint("#1C1238", 0.95 * a))
    c.drawRRect(rr(-380, -230, 380, 250, 30), paint(colr, a, stroke=6))
    # globe lines
    c.save(); c.clipRRect(rr(-380, -230, 380, 250, 30))
    for k in range(5):
        ellipse(c, 260, -90, 40 + k * 40, 200, paint(colr, 0.12 * a, stroke=3))
    c.restore()
    e = ease_out(pin_p)
    py = -120 - 160 * (1 - e)
    pp = skia.Path(); pp.moveTo(-250, py + 70); pp.cubicTo(-310, py, -300, py - 70, -250, py - 70); pp.cubicTo(-200, py - 70, -190, py, -250, py + 70)
    c.drawPath(pp, paint("coral", a * e)); c.drawCircle(-250, py - 20, 18, paint("cream", a * e))
    label(c, city, 40, -60, 88, "cream", "extrabold", a)
    label(c, line2, 40, 60, 54, "gold", "extrabold", a)
    if line3:
        label(c, line3, 0, 170, 40, "sand", "bold", a)
    c.restore()


# ---------------------------------------------------------------- day 20
def bunk(c, x, y, s, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    for xx in (-300, 300):
        c.drawLine(xx, -620, xx, 0, paint("#3A2A5E", a, stroke=22))
    for yy in (-560, -210):
        c.drawRect(skia.Rect(-300, yy, 300, yy + 60), paint("#2E2250", a))
        c.drawRRect(rr(-290, yy - 40, 290, yy + 10, 18), paint("#5A4A8A", a))
    c.drawLine(-300, -420, 300, -420, paint("#3A2A5E", a, stroke=10))
    c.restore()


def biryani_box(c, x, y, s, t, open_p=1.0, a=1.0, smell=0.0):
    """A clay biryani handi; open_p lifts the lid; steam + smell lines curl to the left."""
    c.save(); c.translate(x, y); c.scale(s, s)
    glow(c, 0, -80, 380, "amber", 0.4 * a * (0.3 + 0.7 * open_p))
    pot = skia.Path(); pot.moveTo(-200, -80); pot.cubicTo(-260, 20, -200, 150, 0, 150); pot.cubicTo(200, 150, 260, 20, 200, -80); pot.close()
    c.drawPath(pot, hgrad(-240, 240, ["#E08A50", "#A0482A", "#5E2418", "#7A90D0"], [0, 0.3, 0.75, 1]))
    c.drawRRect(rr(-215, -100, 215, -70, 14), paint("#7A3620", a))
    ellipse(c, 0, -100, 200, 40, paint("#F6E7C8", a))
    for k in range(60):
        gx, gy = (rng(k, 1) - 0.5) * 360, -100 + (rng(k, 2) - 0.5) * 60
        c.drawRRect(rr(gx - 8, gy - 3, gx + 8, gy + 3, 3), paint("#F29A2E" if k % 3 == 0 else "#FFF6DD", a))
    ellipse(c, 60, -110, 60, 30, paint("#8A3A1A", a))
    if open_p > 0:
        e = ease_out(open_p)
        c.save(); c.translate(-230 * e, -60 - 110 * e); c.rotate(-24 * e)
        ellipse(c, 0, 0, 210, 44, paint("#9A4A2A", a)); c.drawCircle(0, -40, 22, paint("#7A3620", a))
        c.restore()
        steam(c, 0, -140, t, h=300, n=4, a=open_p, spread=240)
    if smell > 0:
        for k in range(3):
            p = skia.Path()
            for i in range(40):
                v = i / 39
                xx = -60 - v * 900 * smell
                yy = -220 - k * 70 + 30 * math.sin(v * 10 + t * 3 + k)
                p.moveTo(xx, yy) if i == 0 else p.lineTo(xx, yy)
            c.drawPath(p, paint("gold", 0.7 * a, stroke=8))
    c.restore()


def book(c, x, y, s, t, hl_line=2, reps=0, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    for side in (-1, 1):
        pg = skia.Path(); pg.moveTo(0, -260); pg.quadTo(side * 200, -300, side * 420, -270); pg.lineTo(side * 420, 270); pg.quadTo(side * 200, 240, 0, 280); pg.close()
        c.drawPath(pg, paint("cream", a))
        for i in range(9):
            yy = -200 + i * 52
            x0, x1 = (30, 380) if side > 0 else (-380, -30)
            if side < 0 and i == hl_line:
                c.drawRect(skia.Rect(x0 - 8, yy - 18, x1 + 8, yy + 14), paint("#FFE57A", (0.5 + 0.4 * math.sin(t * 6)) * a))
            c.drawLine(x0, yy, x1 - (i % 3) * 40, yy, paint("#9A8FA8", a, stroke=8))
    c.drawLine(0, -260, 0, 280, paint("#B8AC96", a, stroke=6))
    c.restore()


def icon_disc(c, x, y, r, kind, a=1.0, colr="coral"):
    """Belly / sugar / BP icons in a disc."""
    if a <= 0:
        return
    k = back_out(min(1, a))
    c.save(); c.translate(x, y); c.scale(k, k)
    glow(c, 0, 0, r * 1.6, colr, 0.3)
    c.drawCircle(0, 0, r, paint("#1C1238")); c.drawCircle(0, 0, r, paint(colr, stroke=8))
    if kind == "belly":
        p = skia.Path(); p.moveTo(-50, -110); p.cubicTo(-70, -20, 110, -10, 70, 70); p.lineTo(-50, 110)
        c.drawPath(p, paint("cream", stroke=10))
        c.drawCircle(30, 20, 60, paint("coral", 0.5))
    elif kind == "sugar":
        c.drawRRect(rr(-80, -20, 20, 80, 10), paint("cream"))
        d = skia.Path(); d.moveTo(50, -110); d.cubicTo(110, -20, 110, 40, 50, 40); d.cubicTo(-10, 40, -10, -20, 50, -110)
        c.drawPath(d, paint("coral"))
    elif kind == "bp":
        gauge(c, 0, 40, 90, 0.85, 1.0, "")
    c.restore()


# ---------------------------------------------------------------- day 30
def note(c, x, y, s, rot=0.0, a=1.0):
    """A ₹500 note (stone grey), our flat drawing."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawRRect(rr(-180, -80, 180, 80, 8), paint("#B9B3A6", a))
    c.drawRRect(rr(-170, -70, 170, 70, 6), paint("#8E877A", a, stroke=3))
    c.drawCircle(-90, 0, 46, paint("#A39C8F", a))
    label(c, "₹500", 90, 22, 48, "#4A4438", "extrabold", a)
    c.restore()


def stairs(c, x, y, s, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path(); p.moveTo(-600, 0)
    for k in range(7):
        p.lineTo(-600 + k * 170, -k * 90); p.lineTo(-600 + (k + 1) * 170, -k * 90)
    p.lineTo(600, 200); p.lineTo(-600, 200); p.close()
    c.drawPath(p, paint("#2A1E4A", a))
    for k in range(7):
        c.drawLine(-600 + k * 170, -k * 90, -600 + (k + 1) * 170, -k * 90, paint("amber", 0.5 * a, stroke=5))
    c.restore()


def toothbrush(c, x, y, s, t, drop=0.0, a=1.0):
    c.save(); c.translate(x, y); c.rotate(-20); c.scale(s, s)
    c.drawRRect(rr(-420, -30, 200, 30, 30), paint("teal", a))
    c.drawRRect(rr(200, -36, 360, 20, 12), paint("cream", a))
    for k in range(12):
        c.drawLine(210 + k * 13, -36, 210 + k * 13, -110, paint("#DDEBFF", a, stroke=7))
    c.drawRect(skia.Rect(205, -110, 360, -85), paint("coral", 0.85 * a))
    c.restore()
    if drop > 0:
        dy = y + 40 + 300 * ease(drop)
        d = skia.Path(); d.moveTo(x + 230, dy - 60); d.cubicTo(x + 270, dy, x + 270, dy + 30, x + 230, dy + 30); d.cubicTo(x + 190, dy + 30, x + 190, dy, x + 230, dy - 60)
        c.drawPath(d, paint("#D8262E", a))


def arm_bruise(c, x, y, s, p, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRRect(rr(-700, -120, 700, 120, 120), paint(SKIN, a))
    c.drawRRect(rr(-700, -120, 700, 120, 120), paint("#8A5634", a, stroke=5))
    e = ease_out(p)
    for k, (r_, colr) in enumerate([(150, "#5A3A8A"), (100, "#4A2A6A"), (60, "#3A6A5A")]):
        ellipse(c, 40 + k * 10, 0, r_ * e, r_ * 0.6 * e, paint(colr, 0.7 * a))
    c.restore()


def finger_cut(c, x, y, s, t, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRRect(rr(-600, -110, 500, 110, 110), paint(SKIN, a))
    c.drawRRect(rr(380, -80, 500, 80, 40), paint("#E8B6A0", a))
    c.drawRRect(rr(-600, -110, 500, 110, 110), paint("#8A5634", a, stroke=5))
    pulse = 0.6 + 0.4 * math.sin(t * 5)
    glow(c, 0, 0, 200, "coral", 0.4 * pulse * a)
    c.drawLine(-140, -20, 140, 20, paint("#D8262E", a, stroke=14))
    c.restore()


# ---------------------------------------------------------------- the twist
def ship_scene(c, t, a=1.0, lantern=1.0):
    """An old sailing ship at night on a dark sea; the stern lantern sits where the desk lamp was."""
    if a <= 0:
        return
    c.saveLayerAlpha(None, int(255 * a))
    c.drawRect(skia.Rect(0, 0, W, H), vgrad(0, H, ["#0A0716", "#170E33", "#2A1450", "#4E1C5E"], [0, 0.4, 0.75, 1]))
    c.drawCircle(1560, 200, 70, paint("#DCE8FF"))
    glow(c, 1560, 200, 300, COOL, 0.3)
    for k in range(40):
        c.drawCircle(rng(k, 1) * W, rng(k, 2) * 500, 1.5 + rng(k, 3) * 2, paint("cream", 0.6))
    bob = 10 * math.sin(t * 1.2)
    rot = 1.5 * math.sin(t * 0.9)
    c.save(); c.translate(W / 2, 760 + bob); c.rotate(rot)
    hull = skia.Path(); hull.moveTo(-620, -60); hull.lineTo(560, -60); hull.lineTo(700, -140); hull.lineTo(560, 120); hull.lineTo(-520, 120); hull.lineTo(-660, -150); hull.close()
    c.drawPath(hull, paint("#24142E"))
    c.drawPath(hull, paint("amber", 0.4, stroke=4))
    for mx, mh in ((-300, 560), (60, 640), (380, 500)):
        c.drawLine(mx, -60, mx, -60 - mh, paint("#3A2440", stroke=14))
        for k in range(2):
            sy = -60 - mh + 60 + k * mh * 0.42
            sail = skia.Path(); sail.moveTo(mx - 150, sy); sail.lineTo(mx + 150, sy); sail.quadTo(mx + 170, sy + mh * 0.2, mx + 140, sy + mh * 0.36); sail.lineTo(mx - 140, sy + mh * 0.36); sail.quadTo(mx - 120, sy + mh * 0.2, mx - 150, sy); sail.close()
            c.drawPath(sail, paint("#B8A98A", 0.8))
            c.drawPath(sail, paint(COOL, 0.3, stroke=3))
        c.drawLine(mx, -60 - mh, mx + 260, -60, paint("#3A2440", 0.6, stroke=3))
    for k in range(9):
        c.drawCircle(-500 + k * 110, 20, 16, paint("#120A18"))
    # lantern at the stern
    glow(c, -560, -200, 260, "amber", 0.55 * lantern)
    c.drawLine(-560, -150, -560, -260, paint("#3A2440", stroke=8))
    c.drawRRect(rr(-585, -250, -535, -190, 8), paint("gold", lantern))
    c.restore()
    for k in range(6):
        p = skia.Path(); yy = 860 + k * 45
        p.moveTo(0, yy)
        for i in range(49):
            xx = i * 40
            p.lineTo(xx, yy + 10 * math.sin(xx * 0.02 + t * 1.5 + k))
        p.lineTo(W, H); p.lineTo(0, H); p.close()
        c.drawPath(p, paint(["#1A1440", "#16113A", "#120E32", "#0F0B2A", "#0C0922", "#0A071C"][k]))
    vignette(c, W, H, 0.6)
    c.restore()


def desk_lamp(c, x, y, s, a=1.0, on=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    glow(c, 60, 40, 340, "amber", 0.5 * on * a)
    c.drawRRect(rr(-90, 160, 90, 190, 12), paint("#2E2250", a))
    c.drawLine(0, 170, -60, 20, paint("#3A2A5E", a, stroke=14)); c.drawLine(-60, 20, 40, -60, paint("#3A2A5E", a, stroke=14))
    sh = skia.Path(); sh.moveTo(10, -100); sh.lineTo(130, -20); sh.lineTo(60, 40); sh.close()
    c.drawPath(sh, paint("#5A4A8A", a))
    c.drawCircle(95, 15, 16, paint("gold", on * a))
    c.restore()
