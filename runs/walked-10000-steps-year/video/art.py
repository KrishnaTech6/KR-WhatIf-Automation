"""Topic art for 'What If You Walked 10,000 Steps Every Day for a Year?' (bottom section: walking drawings).
Base drawings copied from the Maggi run (atlas style: flat illustrated night scenes, warm lamp
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
PRESETS = {
    "you": dict(shirt="#3E5BA8", shirt_d="#26386E", pants="#23305A", hair="short", top="hoodie", cap="#E0A030"),
    "mate": dict(shirt="#C2582F", shirt_d="#7A321A", pants="#3A3A4C", hair="cap", top="tee", cap="#E0A030"),
    "her": dict(shirt="#8A2A5C", shirt_d="#561838", pants="#2E2A48", hair="long", top="tee", cap="#E0A030"),
    "kid": dict(shirt="#2E8B6A", shirt_d="#1B5A44", pants="#2A3050", hair="short", top="tee", cap="#E0A030"),
}
SKIN_L, SKIN_D = "#DFA270", "#A86A40"




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
def room_bg(c, t, lamp=1.0, moon=1.0, warn=0.0, mode="night"):
    """Hostel room. mode: night (desk lamp + moonlit window), morning (sunrise window, light shafts, lamp off),
    dark (Day 30: moon only, near black), dusk (sunset window, purple wall)."""
    if mode == "morning":
        c.drawRect(skia.Rect(0, 0, W, H), vgrad(0, H, ["#3B2A5C", "#5A3A62", "#4A2E52"]))
        c.drawRect(skia.Rect(0, H * 0.78, W, H), paint("#2A1A3A"))
        c.drawLine(0, H * 0.78, W, H * 0.78, paint("#6A4A6A", stroke=4))
        c.drawRRect(rr(1460, 110, 1820, 470, 10), vgrad(110, 470, ["#F6B26B", "#F48A6A", "#C85A7A"]))
        c.drawCircle(1600, 380, 60, paint("#FFE2A0"))
        glow(c, 1600, 380, 260, "gold", 0.5)
        c.drawRRect(rr(1460, 110, 1820, 470, 10), paint("#6A4A6A", stroke=14))
        c.drawLine(1640, 110, 1640, 470, paint("#6A4A6A", stroke=10))
        for k in range(3):   # light shafts across the room
            sh = skia.Path(); x0 = 1470 + k * 120
            sh.moveTo(x0, 130 + k * 100); sh.lineTo(x0 + 100, 130 + k * 100); sh.lineTo(x0 - 700, 1080); sh.lineTo(x0 - 900, 1080); sh.close()
            c.drawPath(sh, paint("gold", 0.06 + 0.02 * math.sin(t + k)))
        c.drawRRect(rr(120, 140, 360, 460, 6), paint("#5A3A6A"))
        c.drawCircle(240, 270, 70, paint("sunset", 0.5)); c.drawRect(skia.Rect(150, 380, 330, 400), paint("sand", 0.4))
        glow(c, 1100, 900, 700, "amber", 0.15)
        vignette(c, W, H, 0.35)
        return
    dark = mode == "dark"
    wall = ["#120C24", "#160F2E", "#100A20"] if dark else (["#2A1640", "#3A1C4A", "#24143A"] if mode == "dusk" else ["#1C1238", "#24164A", "#1A1034"])
    c.drawRect(skia.Rect(0, 0, W, H), vgrad(0, H, wall))
    c.drawRect(skia.Rect(0, H * 0.78, W, H), paint("#0E0820" if dark else "#120A24"))
    c.drawLine(0, H * 0.78, W, H * 0.78, paint("#2E1E52", stroke=4))
    if mode == "dusk":
        c.drawRRect(rr(1460, 110, 1820, 470, 10), vgrad(110, 470, ["#4E1C5E", "#8A2A5C", "#D9573D"]))
    else:
        c.drawRRect(rr(1460, 110, 1820, 470, 10), paint("#101C3E"))
        glow(c, 1700, 200, 220, COOL, 0.22 * moon)
        c.drawCircle(1720, 190, 34, paint("#DCE8FF", 0.85 * moon))
        for k in range(18):
            c.drawCircle(1470 + rng(k, 9) * 340, 120 + rng(k, 10) * 330, 1.5 + rng(k, 11) * 2, paint("cream", 0.5))
    c.drawRRect(rr(1460, 110, 1820, 470, 10), paint("#3A2A5E", stroke=14))
    c.drawLine(1640, 110, 1640, 470, paint("#3A2A5E", stroke=10))
    glow(c, 1600, 700, 600, COOL, (0.16 if dark else 0.10) * moon)
    if not dark:
        c.drawRRect(rr(120, 140, 360, 460, 6), paint("#3A1F55"))
        c.drawCircle(240, 270, 70, paint("magenta", 0.5)); c.drawRect(skia.Rect(150, 380, 330, 400), paint("sand", 0.3))
        glow(c, 260, 520, 760, "amber", 0.20 * lamp)
    if warn > 0:
        glow(c, W / 2, H * 0.6, 900, "coral", 0.25 * warn)
    vignette(c, W, H, 0.6 if dark else 0.5)


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
    """Yellow pillow pouch of instant masala noodles (our own design: a drawn noodle block, a wavy brown
    banner reading MASALA NOODLES; no oval, no wordmark), centred at (x, y), ~380x490 at s=1."""
    if a <= 0:
        return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    if a < 1:
        c.saveLayerAlpha(None, int(255 * a))
    if glow_a > 0:
        glow(c, 0, 0, 380, "gold", 0.35 * glow_a)
    sh = paint("space", 0.45); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 16))
    c.drawRRect(rr(-170, -200, 196, 250, 40), sh)
    body = _pouch_path()
    c.drawPath(body, hgrad(-200, 200, ["#D9820E", "#F6B21C", "#FFD54A", "#F2A41C", "#C8700C"], [0, 0.2, 0.45, 0.8, 1]))
    ellipse(c, -60, -90, 90, 150, paint("white", 0.16))   # pillow sheen

    def crimp(y0, sign):
        b = skia.Path(); b.moveTo(-176, y0)
        for i in range(21):
            xx = -176 + 352 * i / 20
            b.lineTo(xx, y0 + sign * (34 + (9 if i % 2 else -3)))
        b.lineTo(176, y0); b.close()
        c.drawPath(b, paint("#E8AE0E"))
        for i in range(1, 22):
            xx = -176 + 352 * i / 22
            c.drawLine(xx, y0 + sign * 4, xx, y0 + sign * 28, paint(YEL_D, 0.55, stroke=3))
    crimp(205, 1)
    if torn < 1:
        c.save()
        if torn > 0:
            e = ease_out(torn)
            c.translate(60 * e, -90 * e); c.rotate(-14 * e)
        if torn < 0.7:
            c.saveLayerAlpha(None, int(255 * (1 - torn / 0.7)))
            crimp(-205, -1)
            c.restore()
        c.restore()
    if 0 < torn < 0.6:
        v = torn / 0.6
        for k in range(6):
            c.drawCircle(-80 + k * 32, -215 - 160 * v * (0.5 + rng(k, 3)), 7, paint(NOOD, 1 - v))
    # the noodle block (drawn, our illustration)
    c.save(); c.rotate(-6)
    c.drawRRect(rr(-128, -170, 128, -6, 34), paint("#F3C24A"))
    c.save(); c.clipRRect(rr(-128, -170, 128, -6, 34))
    for r_ in range(7):
        yy = -158 + r_ * 24
        p_ = skia.Path(); p_.moveTo(-140, yy)
        for k in range(30):
            xx = -140 + k * 10
            p_.lineTo(xx, yy + 7 * math.sin(xx * 0.18 + r_ * 1.3))
        c.drawPath(p_, paint(NOOD_D, 0.9, stroke=6)); c.drawPath(p_, paint(NOOD_L, 0.9, stroke=2.4))
    c.restore()
    c.drawRRect(rr(-128, -170, 128, -6, 34), paint(NOOD_D, stroke=5))
    for k in range(3):   # loose strands curling out
        p_ = skia.Path(); x0 = 100 + k * 8; p_.moveTo(x0, -40 + k * 30)
        p_.cubicTo(x0 + 40, -60 + k * 30, x0 + 30, -10 + k * 30, x0 + 60, -20 + k * 30)
        c.drawPath(p_, paint(NOOD_D, stroke=6))
    c.restore()
    # steam curls above the block
    for k in range(3):
        p_ = skia.Path(); bx = -50 + k * 50; p_.moveTo(bx, -178)
        p_.cubicTo(bx - 16, -186, bx + 16, -196, bx, -204)
        c.drawPath(p_, paint("white", 0.75, stroke=5))
    # wavy banner
    ban = skia.Path(); ban.moveTo(-176, 40)
    ban.cubicTo(-90, 18, 90, 62, 176, 40); ban.lineTo(176, 118); ban.cubicTo(90, 140, -90, 96, -176, 118); ban.close()
    c.drawPath(ban, paint("#2E8B45"))
    c.drawPath(ban, paint("#CFF0B0", 0.7, stroke=3))
    text(c, "MASALA", 0, 102, font("extrabold", 58), paint("#FFE9B0"))
    text(c, "NOODLES", 0, 182, font("extrabold", 46), paint("#1F5E30"))
    # chilli + spice dots
    ch = skia.Path(); ch.moveTo(118, 150); ch.quadTo(150, 170, 128, 196); ch.quadTo(132, 172, 110, 160); ch.close()
    c.drawPath(ch, paint("#D8342E"))
    c.drawLine(-160, -190, -192, 180, paint("amber", 0.55, stroke=5))
    c.drawLine(160, -190, 194, 180, paint(COOL, 0.45, stroke=5))
    if dimmed > 0:
        c.drawPath(body, paint("space", dimmed))
    if num is not None:
        pill(c, 0, 310, 1.0, num, "coral", "cream", 40)
    if a < 1:
        c.restore()
    c.restore()


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
def figure(c, x, y, s, a=1.0, arm_l=110, arm_r=70, lean=0.0, belly=0.0, rim="amber", fill=None, head_tilt=0.0,
           seated=False, hair=None, top=None, shirt=None, slump=0.0, who="you", expr="neutral", back=False, puff=0.0, look=0.0):
    """Cartoon person (stylised, faceless of any real person), feet at (x, y), ~620 px tall at s=1.
    who: you | mate | her | kid presets; filled, shaded clothes, two-tone rim light, a face with an expression."""
    if a <= 0:
        return
    P = dict(PRESETS.get(who, PRESETS["you"]))
    if hair:
        P["hair"] = hair
    if top:
        P["top"] = top
    if shirt:
        P["shirt"] = shirt
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(lean)
    if a < 1:
        c.saveLayerAlpha(None, int(255 * a))
    glow(c, 0, -400, 340, rim, 0.2)
    sh = paint("space", 0.4); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 14))
    ellipse(c, 10, 0, 130, 22, sh)
    sy = 30 * slump
    legs = skia.Path()
    if not seated:
        legs.addPath(_limb(-32, -235, -38, -18, 54)); legs.addPath(_limb(32, -235, 38, -18, 54))
        feet = [(-46, -10), (46, -10)]
    else:
        legs.addPath(_limb(-32, -215, 90, -215, 54)); legs.addPath(_limb(90, -215, 96, -24, 50))
        legs.addPath(_limb(32, -215, 112, -205, 54)); legs.addPath(_limb(112, -205, 122, -24, 50))
        feet = [(104, -14), (130, -14)]
    c.drawPath(legs, hgrad(-60, 140, [P["pants"], "#151A36"]))
    for fx, fy in feet:
        c.drawRRect(rr(fx - 30, fy - 18, fx + 46, fy + 12, 12), paint("#E8E4DA"))
        c.drawRRect(rr(fx - 30, fy + 2, fx + 46, fy + 12, 6), paint("#9A94A8"))
    bw = 86 + 64 * belly
    torso = skia.Path(); torso.moveTo(-80, -448 + sy); torso.cubicTo(-96 - 44 * belly, -340, -bw, -270, -74, -205)
    torso.lineTo(74, -205); torso.cubicTo(bw, -270, 96 + 44 * belly, -340, 80, -448 + sy); torso.close()
    c.drawPath(torso, hgrad(-bw, bw, [P["shirt"], P["shirt"], P["shirt_d"]], [0, 0.45, 1]))
    if P["top"] == "hoodie":
        hood = skia.Path(); hood.addArc(skia.Rect(-66, -478 + sy, 66, -400 + sy), 180, -180)
        c.drawPath(hood, paint(P["shirt_d"], stroke=20))
        c.drawLine(-16, -425 + sy, -20, -350 + sy, paint("cream", 0.8, stroke=5)); c.drawLine(16, -425 + sy, 20, -350 + sy, paint("cream", 0.8, stroke=5))
        c.drawRRect(rr(-56, -305, 56, -250, 18), paint(P["shirt_d"], 0.8))
    else:
        v = skia.Path(); v.moveTo(-30, -448 + sy); v.quadTo(0, -405 + sy, 30, -448 + sy)
        c.drawPath(v, paint(P["shirt_d"], stroke=8))
        c.drawRect(skia.Rect(-60, -330, 60, -300), paint("cream", 0.12))
    c.drawRect(skia.Rect(-74, -225, 74, -205), paint("#1A1430", 0.6))
    arms = skia.Path(); hands = []
    for ang, sx in ((arm_l, -70), (arm_r, 70)):
        r = math.radians(ang)
        ex, ey = sx + 205 * math.cos(r), -420 + sy + 205 * math.sin(r)
        arms.addPath(_limb(sx, -420 + sy, ex, ey, 46)); hands.append((ex, ey))
    c.drawPath(arms, hgrad(-280, 280, [P["shirt"], P["shirt_d"]]))
    for hx, hy in hands:
        c.drawCircle(hx, hy, 25, hgrad(hx - 25, hx + 25, [SKIN_L, SKIN_D]))
    for clipx, colr, al in ((-1, rim, 0.9), (1, COOL, 0.6)):
        c.save(); c.clipRect(skia.Rect(-400 if clipx < 0 else 0, -700, 0 if clipx < 0 else 400, 50))
        for path_, k_ in ((torso, 1.0), (arms, 1.0), (legs, 0.6)):
            c.drawPath(path_, paint(colr, al * k_, stroke=5))
        c.restore()
    c.save(); c.translate(0, -448 + sy); c.rotate(head_tilt + 20 * slump)
    c.drawRRect(rr(-22, -36, 22, 10, 10), paint(SKIN_D))
    cartoon_head(c, 0, -96, 66, expr, P["hair"], puff=puff, look=look, cap=P["cap"], back=back, rim=rim)
    c.restore()
    if a < 1:
        c.restore()
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
def ship_scene(c, t, a=1.0, lantern=1.0, ship_x=None, ship_s=1.0):
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
    c.save(); c.translate(ship_x if ship_x is not None else W / 2, 760 + bob); c.rotate(rot); c.scale(ship_s, ship_s)
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


def desk_bg(c, t, lamp=1.0, mode="night"):
    """Close-up on the study desk: wall, desk lamp pool of light, books, a steel tumbler."""
    c.drawRect(skia.Rect(0, 0, W, H), vgrad(0, H, ["#1E1338", "#2A1A48"] if mode == "night" else ["#3B2A5C", "#5A3A62"]))
    glow(c, 330, 600, 700, "amber", 0.35 * lamp)
    c.drawRect(skia.Rect(0, 760, W, H), vgrad(760, H, [WOOD_L, WOOD_D]))
    c.drawLine(0, 760, W, 760, paint("amber", 0.5, stroke=5))
    desk_lamp(c, 230, 560, 1.3, on=lamp)
    for i, (w_, colr) in enumerate([(300, "#3A6A8A"), (280, "#8A2A5C"), (320, "#2A9D8F")]):
        c.drawRRect(rr(1660 - w_ / 2, 740 - i * 46, 1660 + w_ / 2, 786 - i * 46, 6), paint(colr))
        c.drawLine(1660 - w_ / 2 + 20, 763 - i * 46, 1660 + w_ / 2 - 20, 763 - i * 46, paint("cream", 0.3, stroke=3))
    c.drawRRect(rr(1300, 660, 1380, 780, 10), hgrad(1300, 1380, ["#9AA2B8", "#E4E8F0", "#7A8298"]))
    vignette(c, W, H, 0.5)


def _pouch_path():
    p = skia.Path()
    p.moveTo(-172, -205)
    p.quadTo(0, -228, 172, -205)
    p.cubicTo(204, -80, 204, 80, 172, 205)
    p.quadTo(0, 228, -172, 205)
    p.cubicTo(-204, 80, -204, -80, -172, -205)
    p.close()
    return p


def empty_pouch(c, x, y, s, rot=0.0, a=1.0, shade=0.0):
    """A flattened, torn, empty pouch for the 'pile of 209'."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    p = skia.Path(); p.moveTo(-170, -150)
    for i in range(9):
        p.lineTo(-170 + i * 42, -150 + (14 if i % 2 else -10))
    p.quadTo(200, 0, 170, 180); p.lineTo(-170, 190); p.quadTo(-200, 20, -170, -150); p.close()
    c.drawPath(p, paint("#D9A514", a))
    c.drawPath(p, paint("space", shade * a))
    c.drawLine(-120, -60, 100, 120, paint(YEL_D, 0.6 * a, stroke=6))
    c.drawLine(-40, -120, 60, 160, paint(YEL_L, 0.4 * a, stroke=4))
    ban = skia.Path(); ban.moveTo(-170, 40); ban.cubicTo(-80, 20, 80, 60, 170, 40); ban.lineTo(170, 100); ban.cubicTo(80, 120, -80, 80, -170, 100); ban.close()
    c.drawPath(ban, paint("#24703A", a * (1 - shade)))
    c.restore()


def salt_heap(c, x, base, h, w, t, a=1.0, red=1.0):
    """A heap of salt crystals (bottom-centre x, base y), lit by a red warning glow."""
    if h <= 2:
        return
    glow(c, x, base - h * 0.5, max(w, h) * 0.8, "coral", 0.35 * red * a)
    p = skia.Path(); p.moveTo(x - w / 2, base)
    p.cubicTo(x - w * 0.3, base - h * 0.35, x - w * 0.12, base - h, x, base - h)
    p.cubicTo(x + w * 0.12, base - h, x + w * 0.3, base - h * 0.35, x + w / 2, base)
    p.close()
    c.drawPath(p, hgrad(x - w / 2, x + w / 2, ["#F7C9BC", "#FFF4EE", "#D7DEFA"], [0, 0.4, 1]))
    c.save(); c.clipPath(p, doAntiAlias=True)
    n = int(40 + h * 0.25)
    for k in range(n):
        cx_ = x + (rng(k, 51) - 0.5) * w
        cy_ = base - rng(k, 52) * h
        sz = 5 + 6 * rng(k, 53)
        c.save(); c.translate(cx_, cy_); c.rotate(45 * rng(k, 54))
        c.drawRect(skia.Rect(-sz, -sz, sz, sz), paint("white", 0.9 * a))
        c.drawLine(-sz, -sz, sz, -sz, paint("#E76F51", 0.5 * a * red, stroke=2))
        c.restore()
    c.restore()
    ar = skia.Path(); ar.moveTo(x - w / 2, base); ar.cubicTo(x - w * 0.3, base - h * 0.35, x - w * 0.12, base - h, x, base - h)
    c.drawPath(ar, paint("coral", 0.8 * a * red, stroke=6))
    ar2 = skia.Path(); ar2.moveTo(x, base - h); ar2.cubicTo(x + w * 0.12, base - h, x + w * 0.3, base - h * 0.35, x + w / 2, base)
    c.drawPath(ar2, paint(COOL, 0.6 * a, stroke=5))


def _limb(x0, y0, x1, y1, w):
    L = math.hypot(x1 - x0, y1 - y0)
    p = skia.Path(); p.addRRect(rr(0, -w / 2, L, w / 2, w / 2))
    m = skia.Matrix(); m.setTranslate(x0, y0); m.preRotate(math.degrees(math.atan2(y1 - y0, x1 - x0)))
    p.transform(m)
    return p


def gut_section(c, cx, cy, r, t, a=1.0, fade=0.0):
    """Clean cross-section of the gut: a pink wall with finger-like villi and glowing bacteria in the middle."""
    c.save(); c.translate(cx, cy)
    glow(c, 0, 0, r * 1.5, "magenta", 0.35 * a)
    c.drawCircle(0, 0, r, paint("#B8406A", a))
    c.drawCircle(0, 0, r, paint("amber", 0.7 * a, stroke=6))
    c.drawCircle(0, 0, r * 0.8, paint("#6E1E48", a))
    n = 36
    for k in range(n):
        ang = 2 * math.pi * k / n
        x0, y0 = math.cos(ang) * r * 0.8, math.sin(ang) * r * 0.8
        x1, y1 = math.cos(ang) * r * 0.6, math.sin(ang) * r * 0.6
        c.drawLine(x0, y0, x1, y1, paint("#E07090", a, stroke=r * 0.07))
        c.drawCircle(x1, y1, r * 0.035, paint("#F49AB0", a))
    c.drawCircle(0, 0, r * 0.52, paint("#1C0E30", a))
    cols = ["teal", "amber", "#7FC4FF", "#9BE07A", "sand"]
    for k in range(70):
        rr_ = r * 0.48 * math.sqrt(rng(k, 61))
        ang = rng(k, 62) * 6.28 + t * 0.2 * (1 if k % 2 else -1)
        bx, by = rr_ * math.cos(ang), rr_ * math.sin(ang)
        gone = rng(k, 63) < fade
        colr = "#5A5068" if gone else cols[k % 5]
        al = (0.3 if gone else 1.0) * a
        if k % 3:
            c.save(); c.translate(bx, by); c.rotate(rng(k, 64) * 180)
            c.drawRRect(rr(-r * 0.04, -r * 0.015, r * 0.04, r * 0.015, r * 0.015), paint(colr, al)); c.restore()
        else:
            c.drawCircle(bx, by, r * 0.022, paint(colr, al))
        if not gone and k % 4 == 0:
            glow(c, bx, by, r * 0.07, colr, 0.25 * a)
    c.restore()


def fuel_gauge(c, x, y, r, p, title="NUTRIENTS", a=1.0):
    """Car fuel gauge E..F with the needle at p (0 = empty)."""
    c.drawCircle(x, y, r + 30, paint("#1C1238", a))
    c.drawCircle(x, y, r + 30, paint("cream", 0.8 * a, stroke=6))
    for k in range(9):
        ang = math.radians(210 + k * 15 * 8 / 8 * 1.0 + k * 0)
        ang = math.radians(210 - k * 30)
        c.drawLine(x + (r - 30) * math.cos(ang), y - (r - 30) * math.sin(ang), x + r * math.cos(ang), y - r * math.sin(ang),
                   paint("coral" if k < 2 else "cream", a, stroke=8))
    label(c, "E", x + (r - 80) * math.cos(math.radians(210)), y - (r - 80) * math.sin(math.radians(210)) + 18, 52, "coral", "extrabold", a)
    label(c, "F", x + (r - 80) * math.cos(math.radians(-30)), y - (r - 80) * math.sin(math.radians(-30)) + 18, 52, "cream", "extrabold", a)
    ang = math.radians(210 - 240 * clamp(p))
    c.drawLine(x, y, x + (r - 40) * math.cos(ang), y - (r - 40) * math.sin(ang), paint("coral", a, stroke=12))
    c.drawCircle(x, y, 24, paint("cream", a))
    label(c, title, x, y + r * 0.55, 40, "cream", "extrabold", a)


def shoe_print(c, x, y, s, rot=0.0, a=1.0, left=True):
    if a <= 0:
        return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s * (1 if left else -1), s)
    glow(c, 0, 0, 110, "gold", 0.3 * a)
    ellipse(c, 0, -30, 30, 50, paint("gold", a))
    ellipse(c, 4, 52, 22, 26, paint("gold", a))
    c.restore()


def blackboard(c, t, a=1.0):
    c.drawRect(skia.Rect(0, 0, W, H), vgrad(0, H, ["#1A1236", "#24164A"]))
    c.drawRRect(rr(160, 70, 1760, 560, 16), paint("#1E3A30", a))
    c.drawRRect(rr(160, 70, 1760, 560, 16), paint("#6A4A2E", a, stroke=22))
    for k in range(5):
        c.drawLine(260, 160 + k * 80, 1100 - (k % 2) * 300, 160 + k * 80, paint("cream", 0.35 * a, stroke=6))


def xray_heart(c, x, y, r, t, a=1.0):
    """X-ray inset: a circular window with a fast-straining heart and pressure pulses."""
    c.save()
    glow(c, x, y, r * 1.3, COOL, 0.35 * a)
    c.drawCircle(x, y, r, paint("#0A1A3A", a))
    cl = skia.Path(); cl.addCircle(x, y, r); c.clipPath(cl, doAntiAlias=True)
    for k in range(5):   # ribs
        c.drawLine(x - r, y - r * 0.6 + k * r * 0.3, x + r, y - r * 0.5 + k * r * 0.3, paint("#7FB2FF", 0.25 * a, stroke=10))
    for k in range(3):
        ph = (t * 1.6 + k / 3) % 1
        c.drawCircle(x, y, r * 0.3 + ph * r * 0.7, paint("coral", (1 - ph) * 0.6 * a, stroke=6))
    heart(c, x, y + 10, r / 300, t, rate=2.0, a=a)
    c.restore()
    c.drawCircle(x, y, r, paint("cream", 0.9 * a, stroke=8))


def cartoon_head(c, x, y, r, expr="neutral", hair="short", puff=0.0, look=0.0, cap="#E0A030", back=False, rim="amber"):
    """Stylised cartoon head (not a real person): skin shading, ears, hair, big eyes, brows, mouth by expression.
    expr: neutral | happy | laugh | tired | worried | shock | smug. back=True draws the back of the head."""
    c.save(); c.translate(x, y)
    hc = col("hair")
    if hair == "long":
        c.drawRRect(rr(-r * 1.08, -r * 0.9, r * 1.08, r * 1.25, r * 0.6), paint("hair"))
    for sx in (-1, 1):
        c.drawCircle(sx * r * 0.98, r * 0.08, r * 0.22, paint(SKIN_D if sx > 0 else SKIN_L))
    rx = r * (1 + 0.28 * puff)
    head = skia.Path(); head.addOval(skia.Rect(-rx, -r * 1.02, rx, r * (1.02 + 0.08 * puff)))
    c.drawPath(head, hgrad(-rx, rx, [SKIN_L, "#C98B5E", SKIN_D], [0, 0.55, 1]))
    if back:
        c.drawPath(head, paint("hair"))
    else:
        # cheeks (swell with puff)
        for sx in (-1, 1):
            c.drawCircle(sx * r * (0.52 + 0.2 * puff), r * 0.32, r * (0.16 + 0.14 * puff), paint("coral", 0.22 + 0.2 * puff))
        # eyes
        lid = {"tired": 0.45, "smug": 0.35}.get(expr, 0.0)
        er = r * (0.2 if expr == "shock" else 0.17)
        for sx in (-1, 1):
            ex, ey = sx * r * 0.36, -r * 0.05
            ellipse(c, ex, ey, er * 0.85, er, paint("white"))
            c.drawCircle(ex + look * er * 0.4, ey + er * 0.15, er * 0.5, paint("ink"))
            c.drawCircle(ex + look * er * 0.4 - er * 0.18, ey - er * 0.1, er * 0.16, paint("white"))
            if lid > 0:
                c.drawRect(skia.Rect(ex - er, ey - er * 1.1, ex + er, ey - er + 2 * er * lid), paint("#C98B5E"))
                c.drawLine(ex - er * 0.9, ey - er + 2 * er * lid, ex + er * 0.9, ey - er + 2 * er * lid, paint("#6A3A20", stroke=r * 0.05))
            # brows
            tilt = {"worried": 0.18, "tired": 0.12, "shock": -0.05, "smug": -0.1, "laugh": -0.05}.get(expr, 0.0)
            by = ey - er * 1.5 - (r * 0.08 if expr == "shock" else 0)
            c.drawLine(ex - sx * r * 0.14, by - sx * 0 - tilt * r * 0.6 * 1, ex + sx * r * 0.14, by + tilt * r * 0.6,
                       paint("hair", stroke=r * 0.08))
        # mouth
        my = r * 0.5
        if expr in ("happy", "smug"):
            m = skia.Path(); m.addArc(skia.Rect(-r * 0.28, my - r * 0.22, r * 0.28, my + r * 0.12), 20, 140)
            c.drawPath(m, paint("#5A1E1E", stroke=r * 0.07))
        elif expr == "laugh":
            m = skia.Path(); m.moveTo(-r * 0.32, my - r * 0.08); m.quadTo(0, my + r * 0.45, r * 0.32, my - r * 0.08); m.close()
            c.drawPath(m, paint("#5A1E1E")); ellipse(c, 0, my + r * 0.14, r * 0.13, r * 0.07, paint("#E76F51"))
            c.drawRect(skia.Rect(-r * 0.24, my - r * 0.08, r * 0.24, my - r * 0.01), paint("white"))
        elif expr == "shock":
            ellipse(c, 0, my + r * 0.05, r * 0.12, r * 0.16, paint("#5A1E1E"))
        elif expr == "worried":
            m = skia.Path(); m.addArc(skia.Rect(-r * 0.22, my, r * 0.22, my + r * 0.3), 200, 140)
            c.drawPath(m, paint("#5A1E1E", stroke=r * 0.07))
        elif expr == "tired":
            m = skia.Path(); m.moveTo(-r * 0.2, my + r * 0.05)
            m.cubicTo(-r * 0.07, my - r * 0.03, r * 0.07, my + r * 0.12, r * 0.2, my + r * 0.04)
            c.drawPath(m, paint("#5A1E1E", stroke=r * 0.06))
        else:
            c.drawLine(-r * 0.16, my + r * 0.04, r * 0.16, my + r * 0.04, paint("#5A1E1E", stroke=r * 0.07))
    # hair on top
    hp = skia.Path()
    if hair == "cap":
        hp.addArc(skia.Rect(-r * 1.05, -r * 1.12, r * 1.05, r * 0.25), 180, 180)
        c.drawPath(hp, paint(cap))
        c.drawRRect(rr(-r * 0.2 if not back else -r * 1.2, -r * 0.42, r * 1.35 if not back else r * 0.2, -r * 0.24, r * 0.09), paint(cap))
        c.drawPath(hp, paint("#8A5A10", 0.5, stroke=r * 0.05))
    elif hair == "bun":
        hp.addArc(skia.Rect(-r * 1.04, -r * 1.08, r * 1.04, r * 0.3), 180, 180); hp.addCircle(0, -r * 1.12, r * 0.38)
        c.drawPath(hp, paint("hair"))
    else:
        hp.moveTo(-r * 1.04, -r * 0.05); hp.cubicTo(-r * 1.15, -r * 1.25, r * 1.1, -r * 1.3, r * 1.05, -r * 0.1)
        hp.lineTo(r * 0.7, -r * 0.5); hp.lineTo(r * 0.45, -r * 0.32); hp.lineTo(r * 0.15, -r * 0.6); hp.lineTo(-r * 0.2, -r * 0.4)
        hp.lineTo(-r * 0.55, -r * 0.62); hp.lineTo(-r * 0.8, -r * 0.3); hp.close()
        c.drawPath(hp, paint("hair"))
    # rim light
    for clip_l, colr, al in ((True, rim, 0.9), (False, COOL, 0.6)):
        c.save(); c.clipRect(skia.Rect(-3 * r if clip_l else 0, -3 * r, 0 if clip_l else 3 * r, 3 * r))
        c.drawPath(head, paint(colr, al, stroke=r * 0.06)); c.restore()
    c.restore()


def iris_closeup(c, t, cx, cy, r, inner, bg=None):
    """Room scene behind, a circular close-up window (iris) at (cx, cy) radius r; inner(c) draws inside it."""
    (bg or (lambda c, t: room_bg(c, t)))(c, t)
    mask = skia.Path(); mask.setFillType(skia.PathFillType.kEvenOdd)
    mask.addRect(skia.Rect(0, 0, W, H)); mask.addCircle(cx, cy, r)
    c.drawPath(mask, paint("space", 0.55))
    c.save(); cl = skia.Path(); cl.addCircle(cx, cy, r); c.clipPath(cl, doAntiAlias=True)
    c.drawRect(skia.Rect(cx - r, cy - r, cx + r, cy + r), vgrad(cy - r, cy + r, ["#2A1A48", "#3A2450", WOOD_D]))
    glow(c, cx - r * 0.5, cy - r * 0.5, r, "amber", 0.3)
    inner(c)
    c.restore()
    c.drawCircle(cx, cy, r, paint("gold", 0.85, stroke=8))


def sleeve_hand(c, x, y, s, rot=0.0, shirt="#3E5BA8"):
    """A palm + sleeve whose fingers point to +x from (x, y): used to attach fingers/arms to a body."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawRRect(rr(-900, -150, -160, 150, 70), hgrad(-900, -160, [shirt, "#26386E"]))
    c.drawRRect(rr(-900, -150, -160, 150, 70), paint("amber", 0.5, stroke=5))
    c.drawRRect(rr(-200, -130, 40, 130, 90), paint(SKIN))
    c.drawRRect(rr(-200, -130, 40, 130, 90), paint("#8A5634", stroke=5))
    c.restore()


def skyline(c, city, x0, base, s=1.0, a=1.0):
    """City silhouette along the bottom: london (clock tower, wheel, bridge) | sydney (opera house sails, harbour bridge)."""
    colr = "#120A26"
    c.save(); c.translate(x0, base); c.scale(s, s)
    glow(c, 900, -100, 900, "sunset", 0.3 * a)
    c.drawRect(skia.Rect(-100, -60, 2000, 200), paint(colr, a))
    for k in range(18):
        h = 80 + 160 * rng(k, 91)
        c.drawRect(skia.Rect(k * 110, -h, k * 110 + 90, 0), paint(colr, a))
        for j in range(int(h // 50)):
            c.drawRect(skia.Rect(k * 110 + 20, -h + 20 + j * 46, k * 110 + 34, -h + 38 + j * 46), paint("amber", 0.35 * a))
    if city == "london":
        c.drawRect(skia.Rect(300, -520, 380, 0), paint(colr, a))
        p = skia.Path(); p.moveTo(290, -520); p.lineTo(340, -640); p.lineTo(390, -520); p.close(); c.drawPath(p, paint(colr, a))
        c.drawCircle(340, -440, 30, paint("gold", 0.9 * a))
        c.drawCircle(1300, -260, 230, paint(colr, a, stroke=10))
        for k in range(12):
            ang = k * math.pi / 6
            c.drawLine(1300, -260, 1300 + 230 * math.cos(ang), -260 + 230 * math.sin(ang), paint(colr, a, stroke=4))
            c.drawCircle(1300 + 230 * math.cos(ang), -260 + 230 * math.sin(ang), 12, paint(colr, a))
        for tx in (700, 1000):
            c.drawRect(skia.Rect(tx - 30, -360, tx + 30, 0), paint(colr, a))
        c.drawLine(670, -200, 1030, -200, paint(colr, a, stroke=24))
    else:
        for k, (sx, h) in enumerate([(380, 300), (470, 380), (560, 330), (650, 260)]):
            p = skia.Path(); p.moveTo(sx - 90, 0); p.quadTo(sx - 60, -h, sx + 40, -h * 0.95); p.quadTo(sx + 10, -h * 0.4, sx + 60, 0); p.close()
            c.drawPath(p, paint("cream", 0.85 * a)); c.drawPath(p, paint(COOL, 0.5 * a, stroke=4))
        ar = skia.Path(); ar.addArc(skia.Rect(1000, -380, 1700, 300), 180, 180)
        c.drawPath(ar, paint(colr, a, stroke=36))
        c.drawLine(960, -40, 1740, -40, paint(colr, a, stroke=26))
        for k in range(9):
            xx = 1050 + k * 70
            c.drawLine(xx, -40, xx, -40 - 300 * math.sin(math.pi * (xx - 1000) / 700) * 0.95, paint(colr, a, stroke=5))
    c.restore()


def plate_meal(c, x, y, s, a=1.0):
    """A thali plate: dal bowl, a boiled egg, paneer cubes, roti."""
    c.save(); c.translate(x, y); c.scale(s, s)
    ellipse(c, 0, 0, 260, 90, paint("#C9CCD6", a)); ellipse(c, 0, -6, 230, 74, paint("#E4E6EE", a))
    ellipse(c, -90, -20, 80, 30, paint("#8A5A2A", a)); ellipse(c, -90, -24, 66, 22, paint("#E8B33A", a))
    ellipse(c, 60, -30, 46, 30, paint("white", a)); ellipse(c, 60, -30, 22, 15, paint("#F5B21E", a))
    for k in range(4):
        c.drawRRect(rr(110 + (k % 2) * 34, -4 + (k // 2) * 28, 138 + (k % 2) * 34, 22 + (k // 2) * 28, 4), paint("#F8F0DC", a))
    ellipse(c, -10, 30, 70, 22, paint("#D8A860", a))
    c.restore()


# ================================================================ WALKING (10,000 steps) drawings
GREEN = "#3BB273"
STEP = "#FFB347"


def sneaker(c, x, y, s, a=1.0, glow_a=0.0, rot=0.0, t=0.0, colr="#E94F37"):
    """Running shoe in side view, sole bottom-centre at (x, y), ~360 px long at s=1."""
    if a <= 0:
        return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    if glow_a > 0:
        glow(c, 0, -60, 300, "gold", 0.55 * glow_a * a)
    sole = skia.Path(); sole.moveTo(-180, 0); sole.lineTo(170, 0); sole.quadTo(205, -8, 200, -40); sole.lineTo(-185, -36); sole.close()
    c.drawPath(sole, paint("#F4EFE6", a))
    c.drawLine(-178, -14, 190, -14, paint("#B9B2C6", a, stroke=6))
    up = skia.Path(); up.moveTo(-185, -36); up.cubicTo(-200, -120, -150, -170, -90, -175)
    up.lineTo(-40, -150); up.cubicTo(20, -120, 120, -100, 170, -70); up.quadTo(205, -55, 200, -40); up.close()
    c.drawPath(up, hgrad(-200, 200, [colr, "#B8322A"]))
    c.drawPath(up, paint("cream", 0.35 * a, stroke=4))
    sw = skia.Path(); sw.moveTo(-120, -60); sw.cubicTo(-40, -100, 40, -60, 120, -80)
    c.drawPath(sw, paint("cream", 0.9 * a, stroke=12))
    for k in range(4):
        c.drawLine(-60 + k * 30, -150 + k * 10, -30 + k * 30, -130 + k * 10, paint("cream", a, stroke=6))
    c.drawPath(up, paint("amber", 0.6 * a, stroke=3))
    c.restore()


def step_phone(c, x, y, s, steps, goal=10000, a=1.0, t=0.0, sub="STEPS TODAY", done_flash=0.0, clock=None):
    """Phone showing a step ring and the count. steps: number. done_flash 0..1 = green burst at the goal."""
    if a <= 0:
        return
    c.save(); c.translate(x, y); c.scale(s, s)
    glow(c, 0, 0, 380, "teal", 0.25 * a)
    if done_flash > 0:
        glow(c, 0, 0, 520, GREEN, 0.6 * done_flash * a)
    c.drawRRect(rr(-160, -320, 160, 320, 42), paint("#0B0B12", a))
    c.drawRRect(rr(-160, -320, 160, 320, 42), paint("#4B4B60", a, stroke=6))
    c.drawRRect(rr(-145, -300, 145, 300, 30), paint("#14203E", a))
    if clock:
        label(c, clock, 0, -250, 30, "sand", "bold", a)
    p = clamp(steps / goal)
    c.drawCircle(0, -40, 110, paint("#25305A", a, stroke=22))
    ring = skia.Path(); ring.addArc(skia.Rect(-110, -150, 110, 70), -90, 359.9 * p)
    c.drawPath(ring, paint(GREEN if p >= 1 else STEP, a, stroke=22))
    label(c, f"{int(steps):,}", 0, -26, 60 if steps < 100000 else (40 if steps < 1000000 else 34), "cream", "extrabold", a)
    label(c, f"/ {goal:,}", 0, 22, 26, "sand", "bold", a)
    label(c, sub, 0, 150, 30, "sand", "extrabold", a)
    for k in range(7):   # little week bars
        hh = 30 + 50 * rng(k, 77)
        c.drawRRect(rr(-105 + k * 32, 250 - hh, -85 + k * 32, 250, 6), paint(STEP if k < 6 else GREEN, 0.7 * a))
    c.restore()


def bath_scale(c, x, y, s, needle=0.0, a=1.0, t=0.0, readout=None, shake=0.0, read_col="cream"):
    """Bathroom scale seen from the front-top. needle -1..1 swings the dial. readout = big text on the window."""
    if a <= 0:
        return
    c.save(); c.translate(x + math.sin(t * 50) * 6 * shake, y); c.scale(s, s)
    sh = paint("space", 0.45); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 18))
    ellipse(c, 0, 150, 300, 40, sh)
    c.drawRRect(rr(-280, -150, 280, 150, 70), hgrad(-280, 280, ["#E8E6F0", "#B8B4C8"]))
    c.drawRRect(rr(-280, -150, 280, 150, 70), paint("cream", a, stroke=5))
    for side in (-1, 1):
        c.drawRRect(rr(side * 150 - 80, 0, side * 150 + 80, 120, 30), paint("#9A96AC", 0.6 * a))
    c.drawRRect(rr(-130, -130, 130, -20, 22), paint("#1A2238", a))
    if readout:
        label(c, readout, 0, -55, 60, read_col, "extrabold", a)
    else:
        arc = skia.Path(); arc.addArc(skia.Rect(-110, -110, 110, 110), 200, 140)
        c.save(); c.translate(0, 10)
        c.drawPath(arc, paint("sand", 0.6 * a, stroke=4))
        ang = math.radians(270 + 60 * clamp(needle, -1, 1))
        c.drawLine(0, 0, 100 * math.cos(ang), 100 * math.sin(ang), paint("coral", a, stroke=7))
        c.restore()
    c.drawPath(_hl(), paint("white", 0.25 * a, stroke=6))
    c.restore()


def _hl():
    p = skia.Path(); p.moveTo(-230, -120); p.quadTo(-260, -60, -250, 0)
    return p


def route_map(c, t, a_name, b_name, p, ax=360, ay=640, bx=1560, by=440, walker=True, bend=-220, sub=None, land="#2A2350"):
    """Stylised night map card: two city pins, a dotted route drawn to p (0..1), a walking dot at its head."""
    c.drawRect(skia.Rect(0, 0, W, H), vgrad(0, H, ["#0F1432", "#16123A"]))
    for k in range(9):   # soft land blobs (not a real coastline)
        ellipse(c, 200 + k * 200, 560 + 120 * math.sin(k * 1.7), 260, 220 + 60 * rng(k, 3), paint(land, 0.85))
    for k in range(14):
        c.drawLine(0, 80 + k * 70, W, 80 + k * 70, paint("#2E2A60", 0.25, stroke=1))
    mx, my = (ax + bx) / 2, (ay + by) / 2 + bend
    path = skia.Path(); path.moveTo(ax, ay); path.quadTo(mx, my, bx, by)
    meas = skia.PathMeasure(path, False)
    L = meas.getLength()
    seg = skia.Path(); meas.getSegment(0, L * clamp(p), seg, True)
    c.drawPath(path, dashed("sand", 0.25, 4, 10, 14))
    c.drawPath(seg, dashed(STEP, 1.0, 9, 4, 14))
    for nm, x, y in ((a_name, ax, ay), (b_name, bx, by)):
        glow(c, x, y, 90, "coral", 0.5)
        c.drawCircle(x, y, 18, paint("coral")); c.drawCircle(x, y, 18, paint("cream", stroke=4))
        pill(c, x, y + 70, 1.0, nm, "plum", "cream", 40)
    if walker and p > 0:
        pos, tan = meas.getPosTan(L * clamp(p))
        glow(c, pos.x(), pos.y(), 80, "gold", 0.7)
        c.drawCircle(pos.x(), pos.y(), 14, paint("gold"))
    if sub:
        big_text(c, sub, W / 2, 1000, 56, 1.0, "gold")
    vignette(c, W, H, 0.45)


def kanji_man(c, x, y, s, morph, a=1.0, colr="cream"):
    """The character for 10,000 drawn as three strokes; morph 0..1 turns it into a little walking man."""
    c.save(); c.translate(x, y); c.scale(s, s)
    st = paint(colr, a, stroke=26)
    m = ease(morph)
    # stroke 1: the top bar -> arms
    c.drawLine(-160, -120 + 40 * m, 160, -120 - 20 * m, st)
    # stroke 2: the hooked stroke -> body + back leg
    p = skia.Path(); p.moveTo(-20 + 20 * m, -120); p.lineTo(-20 + 20 * m, 20 - 40 * m)
    p.lineTo(110 - 40 * m, 20 - 20 * m); p.lineTo(90 - 10 * m, 170)
    c.drawPath(p, st)
    # stroke 3: the sweep -> front leg
    q = skia.Path(); q.moveTo(-20 + 20 * m, 20 - 40 * m); q.quadTo(-80, 100, -150 + 40 * m, 170)
    c.drawPath(q, st)
    if m > 0.05:
        c.drawCircle(0, -200 + 20 * (1 - m), 44 * m, paint(colr, a))
    c.restore()


def pedometer_box(c, x, y, s, a=1.0, t=0.0, rot=0.0):
    """Retro 1960s pedometer in its box: cream box, red band, a round dial, the 'MANPO-KEI' name."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    glow(c, 0, 0, 420, "gold", 0.3 * a)
    c.drawRRect(rr(-260, -300, 260, 300, 16), paint("#F1E6CF", a))
    c.drawRect(skia.Rect(-260, 120, 260, 200), paint("#C8302A", a))
    c.drawRRect(rr(-260, -300, 260, 300, 16), paint("#8A6A4A", a, stroke=6))
    c.drawCircle(0, -80, 150, paint("#D9D2C0", a)); c.drawCircle(0, -80, 150, paint("#5A4A3A", a, stroke=10))
    c.drawCircle(0, -80, 120, paint("#FFFDF5", a))
    for k in range(10):
        ang = k * math.pi / 5
        c.drawLine(100 * math.cos(ang), -80 + 100 * math.sin(ang), 116 * math.cos(ang), -80 + 116 * math.sin(ang), paint("#3A2A1A", a, stroke=4))
    ang = t * 3
    c.drawLine(0, -80, 90 * math.cos(ang), -80 + 90 * math.sin(ang), paint("#C8302A", a, stroke=6))
    kanji_man(c, -150, 160, 0.17, 0.0, a, "cream")
    label(c, "MANPO-KEI", 40, 178, 46, "cream", "extrabold", a)
    label(c, "10,000 STEP METER", 0, 260, 30, "#5A4A3A", "extrabold", a)
    c.restore()


def sugar_curve(c, x0, y0, w, h, p, kind="sit", a=1.0, colr="coral"):
    """Blood sugar after a meal: kind sit = sharp spike, walk = gentle hill. p = how much of the line is drawn."""
    path = skia.Path(); n = 60
    for i in range(n + 1):
        u = i / n
        if kind == "sit":
            v = math.exp(-((u - 0.32) ** 2) / 0.012)
        else:
            v = 0.5 * math.exp(-((u - 0.4) ** 2) / 0.05)
        X, Y = x0 + w * u, y0 - h * v
        path.moveTo(X, Y) if i == 0 else path.lineTo(X, Y)
    meas = skia.PathMeasure(path, False)
    seg = skia.Path(); meas.getSegment(0, meas.getLength() * clamp(p), seg, True)
    c.drawPath(seg, paint(colr, a, stroke=12))


def head_side(c, x, y, s, grow=0.0, glow_a=0.0, a=1.0, t=0.0, shrink=0.0, line="cream", brain=True):
    """Side-view head silhouette with a brain; the hippocampus (gold) glows and grows (grow 0..1) or shrinks."""
    c.save(); c.translate(x, y); c.scale(s, s)
    hp = skia.Path(); hp.moveTo(-40, 260); hp.lineTo(-30, 170); hp.cubicTo(-150, 120, -190, 0, -180, -80)
    hp.cubicTo(-170, -230, -40, -300, 60, -280); hp.cubicTo(190, -260, 240, -140, 220, -40)
    hp.lineTo(260, 40); hp.lineTo(225, 60); hp.cubicTo(230, 120, 200, 150, 150, 150); hp.lineTo(140, 260)
    c.drawPath(hp, paint("#1A1236", 0.85 * a))
    c.drawPath(hp, paint(line, a, stroke=7))
    if brain:
        b = skia.Path(); b.addOval(skia.Rect(-140, -250, 180, -20))
        c.drawPath(b, paint("#E58FA0", 0.35 * a))
        for k in range(6):
            w_ = skia.Path(); w_.moveTo(-120 + k * 50, -230 + 10 * (k % 2)); w_.quadTo(-100 + k * 50, -150, -130 + k * 52, -60)
            c.drawPath(w_, paint("#F2B5C0", 0.5 * a, stroke=5))
        c.drawPath(b, paint("#F2B5C0", 0.8 * a, stroke=5))
        k = 1 + 0.35 * ease(grow) - 0.25 * ease(shrink)
        if glow_a > 0:
            glow(c, 30, -90, 140 * k, "gold", 0.7 * glow_a * a)
        hc = skia.Path(); hc.moveTo(-10, -60); hc.cubicTo(20, -120 * k, 80, -120 * k, 90, -70); hc.cubicTo(60, -90, 30, -70, -10, -60)
        c.drawPath(hc, paint("gold" if shrink == 0 else "sand", (0.5 + 0.5 * glow_a) * a))
        c.drawPath(hc, paint("cream", 0.8 * a, stroke=3))
    c.restore()


def crowd(c, cx, cy, cols, rows, grey_n, t, you_p=0.0, a=1.0, sp=86):
    """Grid of little people; the first grey_n are grey (inactive), the rest coloured. you_p lifts one out to gold."""
    k = 0
    for r in range(rows):
        for q in range(cols):
            x = cx + (q - (cols - 1) / 2) * sp
            y = cy + (r - (rows - 1) / 2) * sp * 1.15
            g = k < grey_n
            colr = "#4A4660" if g else ["teal", "coral", "plum", "#3BB273"][k % 4]
            if g and k == grey_n // 2 and you_p > 0:
                colr2 = "gold"
                y -= 60 * ease(you_p); x += 0
                c.drawCircle(x, y - 26, 14, paint(colr2, a)); c.drawRRect(rr(x - 15, y - 10, x + 15, y + 30, 10), paint(colr2, a))
                glow(c, x, y, 70, "gold", 0.6 * you_p * a)
            else:
                c.drawCircle(x, y - 26, 14, paint(colr, a)); c.drawRRect(rr(x - 15, y - 10, x + 15, y + 30, 10), paint(colr, a))
            k += 1


def grey_cloud(c, x, y, s, a=1.0, t=0.0):
    c.save(); c.translate(x + 6 * math.sin(t * 1.5), y); c.scale(s, s)
    for dx, dy, r in ((-90, 10, 70), (0, -20, 95), (95, 10, 70), (40, 40, 60), (-40, 40, 60)):
        c.drawCircle(dx, dy, r, paint("#6A6880", a))
    for k in range(5):
        c.drawLine(-80 + k * 40, 90, -90 + k * 40, 130, paint(COOL, 0.6 * a, stroke=5))
    c.restore()


def calorie_bar(c, x, y, h, label_txt, colr, a=1.0, val=None):
    c.drawRRect(rr(x - 70, y - h, x + 70, y, 16), paint(colr, a))
    c.drawRRect(rr(x - 70, y - h, x + 70, y, 16), paint("cream", 0.7 * a, stroke=4))
    label(c, label_txt, x, y + 60, 38, "cream", "extrabold", a)
    if val:
        label(c, val, x, y - h - 24, 40, "gold", "extrabold", a)


def savanna_bg(c, t):
    c.drawRect(skia.Rect(0, 0, W, H), vgrad(0, H, ["#3A1C4A", "#C85A3A", "#F2A65A"], [0, 0.6, 1]))
    c.drawCircle(1450, 720, 120, paint("#FFE2A0")); glow(c, 1450, 720, 380, "gold", 0.5)
    c.drawRect(skia.Rect(0, 760, W, H), paint("#2A1420"))
    for tx in (300, 1700):   # acacia trees
        c.drawLine(tx, 760, tx + 10, 600, paint("#1A0C14", stroke=18))
        ellipse(c, tx + 10, 590, 160, 40, paint("#1A0C14"))
    vignette(c, W, H, 0.4)


def walker_sil(c, x, y, s, t, a=1.0, colr="#1A0C14", phase=0.0, stick=False):
    """Simple walking silhouette (feet at y), legs swing with t."""
    c.save(); c.translate(x, y); c.scale(s, s)
    sw = math.sin(t * 6 + phase) * 0.45
    p = paint(colr, a, stroke=22)
    c.drawLine(0, -180, 0, -80, p)
    c.drawLine(0, -80, 60 * math.sin(sw), 0, p); c.drawLine(0, -80, -60 * math.sin(sw), 0, p)
    c.drawLine(0, -160, 50 * math.sin(-sw), -100, p); c.drawLine(0, -160, -50 * math.sin(-sw), -100, p)
    c.drawCircle(0, -215, 30, paint(colr, a))
    if stick:
        c.drawLine(60, -150, 80, 0, paint(colr, a, stroke=8))
    c.restore()


def store_front(c, x, y, s, a=1.0, t=0.0):
    """Corner grocery store at night: awning, lit window with fruit crates."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRect(skia.Rect(-320, -420, 320, 0), paint("#2E2250", a))
    glow(c, 0, -200, 360, "amber", 0.45 * a)
    c.drawRect(skia.Rect(-260, -300, 260, -60), paint("#FFD58A", 0.85 * a))
    for k in range(5):
        cx_ = -200 + k * 100
        c.drawRect(skia.Rect(cx_ - 40, -110, cx_ + 40, -60), paint("#8A5A2A", a))
        for j in range(3):
            c.drawCircle(cx_ - 22 + j * 22, -120, 14, paint(["#E94F37", GREEN, "#F6C21C"][(k + j) % 3], a))
    for k in range(8):
        c.drawRect(skia.Rect(-340 + k * 85, -470, -340 + k * 85 + 85, -400), paint("#E94F37" if k % 2 else "cream", a))
    label(c, "GROCERY", 0, -330, 44, "#2E2250", "extrabold", a)
    c.restore()


def alarm_clock(c, x, y, s, t, a=1.0, ring=1.0, txt="5:00"):
    c.save(); c.translate(x + math.sin(t * 50) * 6 * ring, y); c.scale(s, s)
    glow(c, 0, 0, 320, "coral", 0.35 * ring * a)
    for side in (-1, 1):
        c.drawCircle(side * 110, -170, 56, paint("#C8302A", a))
    c.drawCircle(0, 0, 200, paint("#C8302A", a)); c.drawCircle(0, 0, 170, paint("#FFF6E0", a))
    label(c, txt, 0, 34, 110, "#1A1236", "extrabold", a)
    label(c, "AM", 0, 100, 40, "#C8302A", "extrabold", a)
    c.restore()


def house_body(c, x, y, s, t, legs=0.0, a=1.0):
    """Body as a house with 4 rooms; when LEGS lights up, the other rooms dim; the meter on top stays level."""
    c.save(); c.translate(x, y); c.scale(s, s)
    roof = skia.Path(); roof.moveTo(-360, -300); roof.lineTo(0, -520); roof.lineTo(360, -300); roof.close()
    c.drawPath(roof, paint("#3A2A5E", a))
    c.drawRect(skia.Rect(-340, -300, 340, 300), paint("#221A44", a))
    rooms = [("LEGS", -170, -150), ("REPAIR", 170, -150), ("IMMUNE", -170, 150), ("FIDGET", 170, 150)]
    for i, (nm, rx, ry) in enumerate(rooms):
        lit = 0.4 + 0.6 * legs if i == 0 else 1.0 - 0.6 * legs
        c.drawRect(skia.Rect(rx - 140, ry - 120, rx + 140, ry + 120), paint("#FFD58A", 0.15 + 0.75 * lit * a))
        c.drawRect(skia.Rect(rx - 140, ry - 120, rx + 140, ry + 120), paint("#3A2A5E", a, stroke=10))
        label(c, nm, rx, ry + 16, 42, "#1A1236" if lit > 0.5 else "sand", "extrabold", a)
    c.drawRRect(rr(-200, -620, 200, -560, 24), paint("#1A1236", a))
    c.drawRRect(rr(-190, -610, 30, -570, 18), paint(STEP, a))
    label(c, "TOTAL ENERGY", 0, -650, 36, "cream", "extrabold", a)
    c.restore()
