"""Topic art for 'What If You Woke Up at 5 AM for 30 Days?' (base copied from the phone-free run)
and earlier: 'What If You Didn't Use Your Phone for 30 Days?' (atlas style: flat illustrated night scenes,
rim light, sunset sky, dashed 'missing' outlines). Every drawing is a pure function of its inputs and t."""
import math
import skia
from krwi.lib import *  # noqa: F401,F403
from krwi.art import *  # noqa: F401,F403

WOOD, WOOD_D, WOOD_L = "#8A5A3C", "#5E3B26", "#B07A52"
SCREEN = "#0F1A2E"
APPS = ["#E76F51", "#2A9D8F", "#F2B44C", "#8A2A5C", "#4C8BF5", "#3BB273"]


def rr(x0, y0, x1, y1, r):
    return skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), r, r)


def dashed(color, a=1.0, stroke=6, on=18, off=12):
    p = paint(color, a, stroke=stroke)
    p.setPathEffect(skia.DashPathEffect.Make([on, off], 0))
    return p


def label(c, s, x, y, size, color="cream", kind="bold", a=1.0, align="center"):
    text(c, s, x, y, font(kind, size), paint(color, a), align)


# ---------------------------------------------------------------- backgrounds
def dusk_bg(c, t, warm=1.0):
    """Atlas sunset sky over a low city skyline (Indian roofs, a water tank, a temple dome)."""
    night_sky(c, W, H, t, horizon=H * 0.78)
    glow(c, W * 0.5, H * 0.95, 1100, "sunset", 0.35 * warm)
    glow(c, W * 0.5, H * 1.05, 700, "amber", 0.25 * warm)
    sky = skia.Path()
    x = -20
    i = 0
    sky.moveTo(-20, H)
    while x < W + 40:
        w = 90 + 110 * rng(i, 7)
        h = 120 + 200 * rng(i, 8)
        sky.lineTo(x, H - h); sky.lineTo(x + w, H - h)
        x += w; i += 1
    sky.lineTo(W + 40, H); sky.close()
    c.drawPath(sky, paint("#140A26"))
    # a few lit windows
    for k in range(60):
        wx, wy = rng(k, 3) * W, H - 40 - rng(k, 4) * 150
        c.drawRect(skia.Rect(wx, wy, wx + 12, wy + 16), paint("amber", 0.35 + 0.3 * rng(k, 5)))
    # temple dome + water tank silhouettes
    c.drawCircle(W * 0.18, H - 300, 70, paint("#140A26"))
    c.drawRect(skia.Rect(W * 0.18 - 6, H - 420, W * 0.18 + 6, H - 360), paint("#140A26"))
    c.drawRect(skia.Rect(W * 0.8 - 70, H - 380, W * 0.8 + 70, H - 300), paint("#140A26"))
    c.drawLine(W * 0.8 - 50, H - 300, W * 0.8 - 70, H - 200, paint("#140A26", stroke=10))
    c.drawLine(W * 0.8 + 50, H - 300, W * 0.8 + 70, H - 200, paint("#140A26", stroke=10))


def room_bg(c, t, lamp=1.0):
    """A dark bedroom wall at night, one warm lamp glow."""
    c.drawRect(skia.Rect(0, 0, W, H), paint("#1A1236"))
    c.drawRect(skia.Rect(0, H * 0.72, W, H), paint("#120C26"))
    glow(c, W * 0.22, H * 0.3, 700, "amber", 0.28 * lamp)
    # window with night sky
    c.drawRRect(rr(1300, 140, 1720, 520, 12), paint("deep"))
    for k in range(25):
        c.drawCircle(1310 + rng(k, 9) * 400, 150 + rng(k, 10) * 360, 1.5 + rng(k, 11) * 2, paint("cream", 0.6))
    c.drawRRect(rr(1300, 140, 1720, 520, 12), paint("#3A2A5E", stroke=14))
    c.drawLine(1510, 140, 1510, 520, paint("#3A2A5E", stroke=10))
    vignette(c, W, H, 0.5)


# ---------------------------------------------------------------- phones
def smartphone(c, x, y, s, t, screen="feed", rot=0.0, a=1.0, glow_a=0.6, notifs=0, scroll=0.0):
    """Modern phone, centre (x, y). screen: feed | dark | lock | notifs | otp | blank."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    if glow_a > 0 and screen != "dark":
        glow(c, 0, 0, 330, "teal", glow_a * 0.5 * a)
    c.drawRRect(rr(-160, -320, 160, 320, 42), paint("#0B0B12", a))
    c.drawRRect(rr(-160, -320, 160, 320, 42), paint("#3B3B4E", a, stroke=6))
    c.drawRRect(rr(-145, -300, 145, 300, 30), paint(SCREEN if screen != "dark" else "#05050A", a))
    c.drawRRect(rr(-40, -292, 40, -276, 8), paint("#000000", a))
    c.save(); c.clipRRect(rr(-145, -300, 145, 300, 30))
    if screen == "feed":
        off = (scroll * 900) % 260
        for i in range(-1, 5):
            yy = -260 + i * 260 - off
            c.drawRRect(rr(-125, yy, 125, yy + 220, 18), paint(APPS[(i + int(scroll * 900 // 260)) % 6], 0.85 * a))
            c.drawCircle(-95, yy + 30, 16, paint("cream", 0.9 * a))
            c.drawRRect(rr(-70, yy + 20, 60, yy + 38, 9), paint("cream", 0.6 * a))
            c.drawRRect(rr(-110, yy + 170, 40, yy + 190, 9), paint("cream", 0.5 * a))
    elif screen in ("lock", "notifs"):
        label(c, "9:41", 0, -160, 86, "cream", "extrabold", a)
        label(c, "Monday", 0, -110, 30, "sand", "bold", 0.8 * a)
        n = notifs if screen == "notifs" else 0
        for i in range(min(n, 6)):
            yy = -60 + i * 64
            c.drawRRect(rr(-130, yy, 130, yy + 54, 16), paint("cream", 0.88 * a))
            c.drawCircle(-104, yy + 27, 14, paint(APPS[i % 6], a))
            c.drawRRect(rr(-80, yy + 14, 60, yy + 26, 6), paint("#33334A", 0.7 * a))
            c.drawRRect(rr(-80, yy + 32, 20, yy + 42, 5), paint("#33334A", 0.4 * a))
        if notifs > 6:
            pill(c, 0, 300 - 50, 1.0, f"+{notifs - 6} more", "coral", "cream", 30)
    elif screen == "otp":
        label(c, "OTP", 0, -60, 50, "sand", "bold", a)
        label(c, "4 8 2 1", 0, 30, 76, "gold", "extrabold", a)
    c.restore()
    c.restore()


def phone_outline(c, x, y, s, a=1.0, rot=0.0, color="sand"):
    """The 'missing phone' thread: a dashed phone-shaped outline."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawRRect(rr(-160, -320, 160, 320, 42), dashed(color, a, 8, 22, 14))
    c.restore()


def keypad_phone(c, x, y, s, t, screen="CALLS  SMS", a=1.0, rot=0.0, lit=1.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    glow(c, 0, -80, 220, "gold", 0.25 * lit * a)
    c.drawRRect(rr(-110, -250, 110, 250, 46), paint("#2E2E3A", a))
    c.drawRRect(rr(-110, -250, 110, 250, 46), paint("#55556A", a, stroke=6))
    c.drawRRect(rr(-80, -210, 80, -60, 10), paint("#9FD8A8" if lit else "#3A4A3C", a))
    label(c, screen, 0, -125, 26, "#1E3A24", "extrabold", a)
    for r in range(4):
        for k in range(3):
            c.drawRRect(rr(-75 + k * 52, -30 + r * 62, -35 + k * 52, 10 + r * 62, 12), paint("#4A4A5C", a))
            label(c, "123456789*0#"[r * 3 + k], -55 + k * 52, 2 + r * 62, 26, "cream", "bold", a)
    c.restore()


def bubble(c, x, y, s, a=1.0, color=None, i=0):
    """A notification bubble."""
    if a <= 0:
        return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRRect(rr(-150, -40, 150, 40, 22), paint("cream", 0.92 * a))
    c.drawCircle(-115, 0, 20, paint(color or APPS[i % 6], a))
    c.drawRRect(rr(-80, -16, 90, -2, 7), paint("#33334A", 0.7 * a))
    c.drawRRect(rr(-80, 8, 40, 20, 6), paint("#33334A", 0.4 * a))
    c.restore()


# ---------------------------------------------------------------- the drawer (thread 1)
def drawer(c, x, y, s, t, open_p=0.0, phone=True, lock=0.0, screen="dark", notifs=0):
    """Bedside drawer seen from the front-top. open_p 0..1 slides the drawer out and shows the phone inside."""
    c.save(); c.translate(x, y); c.scale(s, s)
    # cabinet top + body
    c.drawRect(skia.Rect(-420, -260, 420, -230), paint(WOOD_L))
    c.drawRect(skia.Rect(-400, -230, 400, 260), paint(WOOD))
    c.drawRect(skia.Rect(-400, -230, 400, 260), paint(WOOD_D, stroke=6))
    glow(c, -300, -260, 260, "amber", 0.15)
    # drawer box sliding out (drawn as a tray in perspective)
    d = 180 * ease(open_p)
    if open_p > 0:
        tray = skia.Path()
        tray.moveTo(-360, -170 + 0); tray.lineTo(360, -170); tray.lineTo(380 + d * 0.12, -170 + d); tray.lineTo(-380 - d * 0.12, -170 + d); tray.close()
        c.drawPath(tray, paint("#3A2416"))
        if phone:
            c.save(); c.translate(0, -170 + d * 0.55); c.scale(1.0, 0.45 * ease(open_p) + 0.01)
            smartphone(c, 0, 0, 0.55, t, screen=screen, rot=90, glow_a=0.0 if screen == "dark" else 0.7, notifs=notifs)
            c.restore()
    # drawer front
    c.drawRect(skia.Rect(-370, -170 + d, 370, 60 + d), paint(WOOD_L))
    c.drawRect(skia.Rect(-370, -170 + d, 370, 60 + d), paint(WOOD_D, stroke=6))
    for k in range(5):
        c.drawLine(-350, -140 + d + k * 42, 350, -150 + d + k * 42, paint(WOOD, 0.5, stroke=3))
    c.drawRRect(rr(-90, -70 + d, 90, -40 + d, 14), paint("#D9C27A"))
    # lower drawer
    c.drawRect(skia.Rect(-370, 90, 370, 240), paint(WOOD_L, 0.9))
    c.drawRect(skia.Rect(-370, 90, 370, 240), paint(WOOD_D, stroke=6))
    c.drawRRect(rr(-90, 150, 90, 180, 14), paint("#D9C27A"))
    if lock > 0:
        padlock(c, 0, 0 + d, 1.0, lock)
    c.restore()


def padlock(c, x, y, s, p=1.0):
    if p <= 0:
        return
    k = back_out(min(1.0, p))
    c.save(); c.translate(x, y); c.scale(s * k, s * k)
    sh = skia.Path(); sh.addArc(skia.Rect(-55, -130, 55, -20), 180, 180)
    c.drawPath(sh, paint("#C9CCD6", stroke=22))
    c.drawLine(-55, -75, -55, -30, paint("#C9CCD6", stroke=22))
    c.drawLine(55, -75, 55, -30, paint("#C9CCD6", stroke=22))
    c.drawRRect(rr(-85, -40, 85, 90, 22), paint("gold"))
    c.drawRRect(rr(-85, -40, 85, 90, 22), paint("#B8862E", stroke=6))
    c.drawCircle(0, 15, 14, paint("#5E3B26")); c.drawRect(skia.Rect(-6, 15, 6, 55), paint("#5E3B26"))
    c.restore()


def day_tile(c, x, y, s, a=1.0, txt="DAY"):
    if a <= 0:
        return
    c.save(); c.translate(x, y); c.scale(s, s)
    glow(c, 0, 0, 140, "gold", 0.35 * a)
    c.drawRRect(rr(-80, -95, 80, 95, 18), paint("cream", a))
    c.drawRRect(rr(-80, -95, 80, -45, 18), paint("coral", a))
    c.drawRect(skia.Rect(-80, -60, 80, -45), paint("coral", a))
    label(c, txt, 0, 40, 46, "ink", "extrabold", a)
    c.restore()


# ---------------------------------------------------------------- people, hands, pocket
def person(c, x, y, s, color="#3D5A80", phone=False, look_up=0.0, a=1.0, female=False, glow_phone=True):
    """Flat faceless figure, feet at (x, y). phone=True: head bowed over a glowing phone."""
    c.save(); c.translate(x, y); c.scale(s, s)
    bow = 0 if not phone else 22 * (1 - look_up)
    c.drawLine(-16, -120, -18, 0, paint("#22223A", a, stroke=28))
    c.drawLine(16, -120, 18, 0, paint("#22223A", a, stroke=28))
    c.drawRRect(rr(-55, -290, 55, -110, 34), paint(color, a))
    c.drawRRect(rr(-55, -290, 55, -110, 34), paint("amber", 0.35 * a, stroke=4))   # rim light
    hx, hy = bow * 0.6, -335 + bow * 0.5
    if female:
        c.drawRRect(rr(hx - 46, hy - 40, hx + 46, hy + 70, 34), paint("hair", a))
    c.drawCircle(hx, hy, 42, paint("skin", a))
    c.drawCircle(hx, hy - 18, 40, paint("hair", a))
    c.drawCircle(hx, hy + 4, 36, paint("skin", a))
    if phone:
        px, py = 45, -230
        c.drawLine(30, -260, px, py, paint(color, a, stroke=24))
        c.drawRRect(rr(px - 14, py - 26, px + 14, py + 26, 6), paint("#0B0B12", a))
        if glow_phone:
            glow(c, px, py - 40, 90, "teal", 0.55 * a)
            c.drawCircle(hx + 8, hy + 10, 30, paint("teal", 0.18 * a))
    c.restore()


def jeans_pocket(c, x, y, s, t, buzz=0.0, outline=1.0):
    """Close-up of a jeans pocket with the dashed outline of the missing phone; buzz>0 draws vibration lines."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRRect(rr(-420, -380, 420, 420, 40), paint("#2F4B7C"))
    for k in range(40):
        c.drawLine(-420 + k * 22, -380, -420 + k * 22 - 60, 420, paint("#3A5A92", 0.35, stroke=3))
    pk = skia.Path(); pk.moveTo(-260, -200); pk.lineTo(260, -200); pk.lineTo(230, 260); pk.quadTo(0, 330, -230, 260); pk.close()
    c.drawPath(pk, paint("#28426E"))
    c.drawPath(pk, dashed("amber", 0.9, 5, 14, 10))
    c.drawLine(-260, -200, 260, -200, paint("#1E3358", stroke=10))
    phone_outline(c, 0, 40, 0.62, outline, 0, "gold")
    if buzz > 0:
        jx = math.sin(t * 90) * 6 * buzz
        for side in (-1, 1):
            for k in range(3):
                r = 330 + k * 45
                p = skia.Path(); p.addArc(skia.Rect(-r + jx, -r * 0.8 + 40, r + jx, r * 0.8 + 40), -25 if side > 0 else 155, 50)
                c.drawPath(p, paint("gold", buzz * (0.9 - k * 0.25), stroke=10))
    c.restore()


def hand(c, x, y, s, rot=0.0, color="skin", point=False):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawRRect(rr(-70, 0, 70, 260, 20), paint("#3D5A80"))            # sleeve
    c.drawRRect(rr(-62, -120, 62, 30, 46), paint(color))
    for k in range(4):
        if point and k > 0:
            c.drawRRect(rr(-55 + k * 30, -150, -31 + k * 30, -95, 12), paint(color))
        else:
            c.drawRRect(rr(-55 + k * 30, -200 + (10 if k in (0, 3) else 0), -31 + k * 30, -95, 12), paint(color))
    c.drawRRect(rr(-95, -80, -55, -20, 18), paint(color))
    c.drawRRect(rr(-62, -120, 62, 30, 46), paint("skin_shade", 0.6, stroke=4))
    c.restore()


# ---------------------------------------------------------------- India's phone-locked life
ICONS = [("WALLET", "teal"), ("TICKETS", "coral"), ("MAPS", "amber"), ("BANK", "plum")]


def icon_tile(c, x, y, s, kind, a=1.0, cross=0.0):
    if a <= 0:
        return
    name, colr = {k: (k, v) for k, v in ICONS}[kind]
    c.save(); c.translate(x, y); c.scale(s * (0.6 + 0.4 * back_out(min(1, a))), s * (0.6 + 0.4 * back_out(min(1, a))))
    c.drawRRect(rr(-110, -110, 110, 110, 34), paint(colr, a))
    c.drawRRect(rr(-110, -110, 110, 110, 34), paint("cream", 0.3 * a, stroke=4))
    ink = paint("cream", a, stroke=12)
    if kind == "WALLET":
        c.drawRRect(rr(-60, -40, 60, 45, 14), ink); c.drawCircle(35, 2, 9, paint("cream", a))
    elif kind == "TICKETS":
        c.drawRRect(rr(-65, -35, 65, 35, 10), ink); c.drawLine(15, -35, 15, 35, dashed("cream", a, 6, 8, 6))
    elif kind == "MAPS":
        p = skia.Path(); p.moveTo(0, 60); p.lineTo(-38, -5); p.arcTo(skia.Rect(-42, -70, 42, 14), 160, 220, False); p.close()
        c.drawPath(p, paint("cream", a)); c.drawCircle(0, -28, 14, paint(colr, a))
    elif kind == "BANK":
        tri = skia.Path(); tri.moveTo(-70, -25); tri.lineTo(0, -65); tri.lineTo(70, -25); tri.close()
        c.drawPath(tri, paint("cream", a))
        for k in range(4):
            c.drawRect(skia.Rect(-55 + k * 34, -18, -41 + k * 34, 40), paint("cream", a))
        c.drawRect(skia.Rect(-70, 42, 70, 56), paint("cream", a))
    label(c, name, 0, 160, 34, "cream", "bold", a)
    if cross > 0:
        xmark(c, 0, 0, 1.0, cross)
    c.restore()


def ticket_row(c, cx, y, t, lit_p, n=10, lit=9):
    """10 train tickets in a row; `lit` of them turn teal (ONLINE) as lit_p goes 0->1."""
    gap = 150
    x0 = cx - gap * (n - 1) / 2
    for i in range(n):
        on = i < lit and lit_p * n > i
        colr = "teal" if on else "sand"
        x = x0 + i * gap
        c.save(); c.translate(x, y); c.rotate(-6 + 12 * rng(i, 3))
        c.drawRRect(rr(-55, -80, 55, 80, 10), paint(colr, 0.95))
        c.drawLine(-55, 20, 55, 20, dashed("ink", 0.5, 4, 8, 6))
        label(c, "PNR", 0, -30, 22, "ink", "bold", 0.7)
        c.drawCircle(0, 50, 12 if on else 0.1, paint("cream"))
        c.restore()
        if on:
            glow(c, x, y, 70, "teal", 0.3)


def city_map(c, cx, cy, w, h, t, lost=1.0):
    """A street map card with a blue 'you' dot that wanders, and a big question mark."""
    c.drawRRect(rr(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, 30), paint("#22324A"))
    c.save(); c.clipRRect(rr(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, 30))
    for k in range(9):
        x = cx - w / 2 + k * w / 8 + 30 * math.sin(k)
        c.drawLine(x, cy - h / 2, x + 80 * math.sin(k * 1.7), cy + h / 2, paint("#3E5272", stroke=18))
    for k in range(6):
        y = cy - h / 2 + k * h / 5
        c.drawLine(cx - w / 2, y, cx + w / 2, y + 60 * math.cos(k * 1.3), paint("#3E5272", stroke=14))
    c.drawRect(skia.Rect(cx + w * 0.15, cy - h * 0.35, cx + w * 0.35, cy - h * 0.1), paint("#2E6B4A", 0.8))
    c.restore()
    dx = cx + math.sin(t * 1.3) * 120 * lost
    dy = cy + math.sin(t * 0.9 + 1) * 70 * lost
    glow(c, dx, dy, 90, "#4C8BF5", 0.5)
    c.drawCircle(dx, dy, 22, paint("#4C8BF5")); c.drawCircle(dx, dy, 22, paint("cream", stroke=6))
    if lost > 0.2:
        big_text(c, "?", dx + 70, dy - 70, 110, lost, "gold")


def clock_ring(c, cx, cy, r, hours, p, t):
    """A 24-hour ring with an `hours` slice glowing (drawn as p goes 0->1)."""
    c.drawCircle(cx, cy, r, paint("deep", 0.9))
    c.drawCircle(cx, cy, r, paint("sand", 0.4, stroke=26))
    sw = 360 * hours / 24 * ease(p)
    arc = skia.Path(); arc.addArc(skia.Rect(cx - r, cy - r, cx + r, cy + r), -90, sw)
    glow(c, cx, cy - r * 0.5, r * 0.8, "coral", 0.25 * p)
    c.drawPath(arc, paint("coral", stroke=26))
    for k in range(24):
        a = math.radians(k * 15 - 90)
        ln = 22 if k % 6 == 0 else 10
        c.drawLine(cx + math.cos(a) * (r - 40), cy + math.sin(a) * (r - 40),
                   cx + math.cos(a) * (r - 40 - ln), cy + math.sin(a) * (r - 40 - ln), paint("sand", 0.7, stroke=4))


def metro(c, t, you_look_up=0.0):
    """Metro carriage interior: everyone bowed over glowing phones except you (centre, empty hands)."""
    c.drawRect(skia.Rect(0, 0, W, H), paint("#1C2440"))
    c.drawRect(skia.Rect(0, 0, W, 120), paint("#2A3558"))
    for k in range(6):
        x = 120 + k * 330
        c.drawRRect(rr(x, 170, x + 240, 430, 30), paint("#0E1428"))
        off = (t * 900 + k * 100) % 2400
        for j in range(3):
            lx = x + 20 + ((j * 90 - off) % 260) - 20
            c.drawLine(lx, 200, lx + 40, 400, paint("amber", 0.12, stroke=30))
        c.drawRRect(rr(x, 170, x + 240, 430, 30), paint("#46527A", stroke=8))
    c.drawLine(0, 140, W, 140, paint("#9AA3BF", stroke=10))
    for k in range(10):
        x = 60 + k * 200
        c.drawLine(x, 140, x, 200, paint("#9AA3BF", stroke=4)); c.drawCircle(x, 210, 14, paint("#9AA3BF", stroke=5))
    c.drawRect(skia.Rect(0, 820, W, H), paint("#141A30"))
    cols = ["#3D5A80", "#8A2A5C", "#2E7D6B", "#7A4E2D", "#4A3F8C", "#9C4A3A"]
    for i, x in enumerate([200, 450, 700, 1220, 1470, 1720]):
        person(c, x, 1000, 1.25, cols[i], phone=True, female=i % 2 == 1)
    person(c, W / 2, 1000, 1.35, "teal", phone=False, look_up=1.0)
    glow(c, W / 2, 520, 220, "gold", 0.15 + 0.2 * you_look_up)


def shampoo(c, x, y, s, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawRRect(rr(-80, -200, 80, 200, 46), paint("#4FC3C9"))
    c.drawRRect(rr(-40, -260, 40, -200, 10), paint("cream"))
    c.drawRRect(rr(-60, -90, 60, 90, 14), paint("cream", 0.95))
    for k in range(7):
        c.drawRRect(rr(-45, -70 + k * 22, 45 - 20 * rng(k, 2), -60 + k * 22, 4), paint("ink", 0.5))
    c.restore()


def people_icons(c, cx, y, n, lit, p, gap=150, s=1.0, colr="teal", dim_a=0.18):
    """n person icons; the first `lit` stay bright, the rest fade to dim as p goes 0->1."""
    x0 = cx - gap * (n - 1) / 2
    for i in range(n):
        a = 1.0 if i < lit else 1.0 - (1 - dim_a) * ease(p)
        x = x0 + i * gap
        c.drawCircle(x, y - 70 * s, 34 * s, paint(colr if i < lit else "sand", a))
        c.drawRRect(rr(x - 50 * s, y - 25 * s, x + 50 * s, y + 90 * s, 40 * s), paint(colr if i < lit else "sand", a))


def head_profile(c, x, y, s, t, light=0.0, pings=0.0):
    """Side profile of a head; light>0 switches on a warm glow inside (the change 'inside your head')."""
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path()
    p.moveTo(-120, 260); p.lineTo(-110, 120); p.cubicTo(-230, 60, -220, -240, 0, -260)
    p.cubicTo(180, -270, 230, -120, 200, -20); p.lineTo(250, 50); p.lineTo(205, 70); p.lineTo(215, 110)
    p.lineTo(200, 130); p.lineTo(210, 170); p.cubicTo(180, 210, 120, 200, 90, 195); p.lineTo(80, 260); p.close()
    c.drawPath(p, paint("#241845"))
    c.drawPath(p, paint("amber", 0.5, stroke=5))
    if light > 0:
        glow(c, 10, -90, 260, "gold", 0.6 * light)
        c.drawCircle(10, -90, 70 * light, paint("gold", 0.85 * light))
        for k in range(10):
            a = k * 0.628 + t * 0.6
            c.drawLine(10 + math.cos(a) * 95, -90 + math.sin(a) * 95, 10 + math.cos(a) * (95 + 50 * light),
                       -90 + math.sin(a) * (95 + 50 * light), paint("gold", 0.7 * light, stroke=8))
    for k in range(int(6 * pings)):
        bubble(c, 220 + 120 * rng(k, 3), -230 + 90 * k - 80 * rng(k, 4), 0.55, min(1.0, 6 * pings - k), i=k)
    c.restore()


def focus_test(c, cx, cy, t, calm=0.0):
    """A sustained-attention task: one target dot in the middle; distractions flicker less as calm -> 1."""
    c.drawRRect(rr(cx - 520, cy - 320, cx + 520, cy + 320, 30), paint("#0E0A22"))
    c.drawRRect(rr(cx - 520, cy - 320, cx + 520, cy + 320, 30), paint("sand", 0.3, stroke=4))
    for k in range(14):
        on = math.sin(t * (5 + k) + k * 2) > (0.2 + 0.8 * calm)
        if on:
            bubble(c, cx - 420 + rng(k, 5) * 840, cy - 250 + rng(k, 6) * 500, 0.45, 0.8 * (1 - calm), i=k)
    r = 34 + 4 * math.sin(t * 4)
    glow(c, cx, cy, 120, "gold", 0.4 + 0.4 * calm)
    c.drawCircle(cx, cy, r, paint("gold"))
    c.drawCircle(cx, cy, r + 26, paint("gold", 0.6, stroke=5))


def age_dial(c, cx, cy, r, back, t):
    """A speedometer-style dial whose needle swings back by `back` (0..1 = 0..10 years)."""
    arc = skia.Path(); arc.addArc(skia.Rect(cx - r, cy - r, cx + r, cy + r), 180, 180)
    c.drawPath(arc, paint("sand", 0.35, stroke=30))
    arc2 = skia.Path(); arc2.addArc(skia.Rect(cx - r, cy - r, cx + r, cy + r), 180 + 150, -120 * ease(back))
    c.drawPath(arc2, paint("teal", stroke=30))
    ang = math.radians(180 + 150 - 120 * ease(back))
    c.drawLine(cx, cy, cx + math.cos(ang) * (r - 40), cy + math.sin(ang) * (r - 40), paint("cream", stroke=14))
    c.drawCircle(cx, cy, 26, paint("cream"))
    label(c, "FOCUS AGE", cx, cy + 90, 40, "sand", "bold")
    label(c, f"-{10 * ease(back):.0f} YEARS", cx, cy - r - 50, 72, "gold", "extrabold", min(1.0, back * 3))


def scroll_feed(c, cx, cy, t, speed=1.0, snap=0.0):
    """An endless feed spinning past (inside a phone), then snapping shut (snap 0->1)."""
    smartphone(c, cx, cy, 1.25 * (1 - 0.3 * ease(snap)), t, "feed", scroll=t * speed, a=1 - 0.6 * ease(snap))
    if snap > 0:
        xmark(c, cx, cy, 2.0, snap)


def piggy(c, x, y, s, t, coin_p=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawOval(skia.Rect(-200, -140, 200, 140), paint("#F29CB2"))
    c.drawOval(skia.Rect(-200, -140, 200, 140), paint("#C9667F", stroke=6))
    c.drawOval(skia.Rect(170, -40, 240, 40), paint("#F29CB2")); c.drawCircle(205, -8, 8, paint("#C9667F")); c.drawCircle(205, 14, 8, paint("#C9667F"))
    for lx in (-120, -40, 60, 140):
        c.drawRRect(rr(lx - 22, 110, lx + 22, 190, 12), paint("#E58AA2"))
    c.drawCircle(110, -50, 12, paint("ink"))
    c.drawRRect(rr(-60, -140, 60, -122, 8), paint("#8A3A50"))
    if 0 < coin_p < 1:
        yy = -330 + 220 * ease(coin_p)
        c.drawRRect(rr(-90, yy - 40, 90, yy + 40, 8), paint("#7FB77E"))
        label(c, "₹100", 0, yy + 16, 40, "ink", "extrabold")
    c.restore()


def lake_scene(c, t, p):
    """Movie myth: a phone arcing into a lake at sunset, splash at the end."""
    dusk_bg(c, t, 1.2)
    c.drawRect(skia.Rect(0, H * 0.72, W, H), paint("#1D3A5A"))
    for k in range(18):
        c.drawLine(rng(k, 1) * W, H * 0.75 + rng(k, 2) * 250, rng(k, 1) * W + 120, H * 0.75 + rng(k, 2) * 250, paint("amber", 0.35, stroke=4))
    x = 380 + 1100 * p
    y = 700 - 520 * math.sin(math.pi * min(p, 1)) + (0 if p < 1 else 0)
    if p < 0.97:
        smartphone(c, x, y, 0.35, t, "feed", rot=p * 540, scroll=t)
    else:
        for k in range(14):
            a = math.radians(200 + k * 10)
            c.drawLine(1480, 800, 1480 + math.cos(a) * 140, 800 + math.sin(a) * 140, paint("cream", 0.8, stroke=10))
    person(c, 300, 1000, 1.3, "teal", phone=False)


def rooftop(c, t, warm=1.3, clothes=True):
    """Atlas hero scene: a Mumbai-style rooftop at sunset, water tank, clothes line, parapet in the foreground."""
    dusk_bg(c, t, warm)
    c.drawRect(skia.Rect(0, 900, W, H), paint("#2A1838"))
    c.drawRect(skia.Rect(0, 880, W, 910), paint("#4A2A4E"))
    c.drawLine(0, 880, W, 880, paint("amber", 0.5, stroke=4))       # rim light on the parapet
    if not clothes:
        return
    c.drawLine(1300, 420, 1900, 470, paint("#140A26", stroke=4))
    for k in range(4):
        x = 1360 + k * 130
        c.drawRect(skia.Rect(x, 430 + k * 13, x + 70, 540 + k * 13), paint(["#E76F51", "#2A9D8F", "#F2B44C", "#8A2A5C"][k], 0.85))


def auto_rickshaw(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    body = skia.Path(); body.moveTo(-150, 0); body.lineTo(-150, -150); body.quadTo(-120, -230, 20, -230)
    body.lineTo(130, -230); body.lineTo(160, -60); body.lineTo(160, 0); body.close()
    c.drawPath(body, paint("#F2C230"))
    c.drawRect(skia.Rect(-150, -240, 140, -215), paint("#2E7D32"))
    c.drawRect(skia.Rect(-90, -200, 60, -110), paint("#1A1236", 0.85))
    c.drawPath(body, paint("amber", 0.6, stroke=4))
    for wx in (-100, 110):
        c.drawCircle(wx, 0, 40, paint("#1A1230")); c.drawCircle(wx, 0, 16, paint("#9AA3BF"))
    glow(c, 160, -80, 60, "gold", 0.6)
    c.restore()


def signpost(c, x, y, s, labels):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawLine(0, 0, 0, -420, paint("#5E3B26", stroke=16))
    for i, (lab, d) in enumerate(labels):
        yy = -400 + i * 90
        p = skia.Path()
        if d > 0:
            p.moveTo(0, yy); p.lineTo(260, yy); p.lineTo(300, yy + 35); p.lineTo(260, yy + 70); p.lineTo(0, yy + 70)
        else:
            p.moveTo(0, yy); p.lineTo(-260, yy); p.lineTo(-300, yy + 35); p.lineTo(-260, yy + 70); p.lineTo(0, yy + 70)
        p.close()
        c.drawPath(p, paint(["teal", "coral", "plum"][i % 3]))
        label(c, lab, 140 * d, yy + 48, 30, "cream", "bold")
    c.restore()


def coin_stack(c, x, y, n, s=1.0):
    for k in range(n):
        yy = y - k * 16 * s
        c.drawOval(skia.Rect(x - 60 * s, yy - 14 * s, x + 60 * s, yy + 14 * s), paint("gold"))
        c.drawOval(skia.Rect(x - 60 * s, yy - 14 * s, x + 60 * s, yy + 14 * s), paint("#B8862E", stroke=3))


# ================================================================ 5 AM video additions (atlas, flat)
def alarm_clock(c, x, y, s, t, ring=0.0, bedtime=None, hour=5.0, minute=0.0, a=1.0, body="coral"):
    """Twin-bell alarm clock, face centre (x, y), face radius 100*s. ring 0..1 shakes it.
    bedtime: number on a small 'BED' sub-dial (the spot-the-difference)."""
    if a <= 0:
        return
    sh = math.sin(t * 60) * 5 * ring * s
    c.save(); c.translate(x + sh, y); c.rotate(math.sin(t * 47) * 4 * ring); c.scale(s, s)
    glow(c, 0, 0, 260, "amber", 0.28 * a * (0.6 + 0.4 * ring))
    for sx in (-1, 1):                                   # legs
        c.drawLine(sx * 55, 95, sx * 82, 150, paint("#5A1E1A", a, stroke=16))
    for sx in (-1, 1):                                   # bells
        c.save(); c.translate(sx * 68, -108); c.rotate(sx * 28)
        p = skia.Path(); p.addArc(skia.Rect(-46, -46, 46, 46), 180, 180); p.close()
        c.drawPath(p, paint("gold", a))
        c.drawRect(skia.Rect(-50, -4, 50, 8), paint("amber", a))
        c.drawCircle(-16, -26, 9, paint("cream", 0.6 * a))
        c.restore()
    hx = math.sin(t * 80) * 22 * ring
    c.drawLine(0, -100, hx, -146, paint("ink", a, stroke=8)); c.drawCircle(hx, -148, 10, paint("sand", a))
    c.drawCircle(0, 0, 122, paint(body, a))
    c.drawCircle(0, 0, 122, paint("amber", 0.6 * a, stroke=5))
    c.drawCircle(0, 0, 100, paint("cream", a))
    for k in range(12):
        an = math.radians(k * 30 - 90)
        c.drawLine(math.cos(an) * 78, math.sin(an) * 78, math.cos(an) * 92, math.sin(an) * 92, paint("ink", a, stroke=6))
    if bedtime is not None:
        c.drawCircle(0, 46, 28, paint("sand", a)); c.drawCircle(0, 46, 28, paint("ink", a, stroke=3))
        label(c, "BED", 0, 34, 12, "ink", "bold", a)
        label(c, str(bedtime), 0, 64, 24, "coral", "extrabold", a)
    ha = math.radians((hour % 12 + minute / 60) * 30 - 90); ma = math.radians(minute * 6 - 90)
    c.drawLine(0, 0, math.cos(ha) * 50, math.sin(ha) * 50, paint("ink", a, stroke=12))
    c.drawLine(0, 0, math.cos(ma) * 78, math.sin(ma) * 78, paint("ink", a, stroke=8))
    c.drawCircle(0, 0, 11, paint("coral", a))
    c.restore()
    if ring > 0:
        for k in range(3):
            ph = (t * 2 + k / 3) % 1
            r = (170 + ph * 110) * s
            for sx in (-1, 1):
                arc = skia.Path(); arc.addArc(skia.Rect(x - r, y - r, x + r, y + r), -90 + sx * 55 - 20, 40)
                c.drawPath(arc, paint("gold", (1 - ph) * 0.8 * ring * a, stroke=7 * s))


def bed_scene(c, x0, w, t, bedtime=None, ring=0.0, made=False, sleeper=True, phone_glow=0.0, tired=0.0, bright=0.0):
    """Flat bedroom panel (night wall, starry window, bed with 'you', side table + alarm clock), drawn in x0..x0+w.
    Designed at 960 wide; a wider panel keeps the room at 960 and extends the wall and floor."""
    c.save(); c.clipRect(skia.Rect(x0, 0, x0 + w, H))
    if w > 960:
        c.drawRect(skia.Rect(x0, 0, x0 + w, H), paint("#1A1236"))
        c.drawRect(skia.Rect(x0, 780, x0 + w, H), paint("#120C26"))
        x0, w = x0 + (w - 960) / 2, 960
    c.translate(x0, 0); c.scale(w / 960, 1)
    c.drawRect(skia.Rect(0, 0, 960, H), paint("#1A1236"))
    glow(c, 760, 560, 520, "amber", 0.22 + 0.15 * ring)
    c.drawRRect(rr(420, 150, 820, 500, 12), paint("deep" if bright < 0.5 else "#E9875A"))
    for k in range(22):
        c.drawCircle(430 + rng(k, 9) * 380, 160 + rng(k, 10) * 320, 1.6 + rng(k, 11) * 2, paint("cream", 0.6 * (1 - bright)))
    c.drawCircle(760, 220, 26, paint("cream", 0.85 * (1 - bright)))
    c.drawCircle(772, 212, 24, paint("deep", 1 - bright))
    c.drawRRect(rr(420, 150, 820, 500, 12), paint("#3A2A5E", stroke=14))
    c.drawLine(620, 150, 620, 500, paint("#3A2A5E", stroke=10))
    c.drawRect(skia.Rect(0, 780, 960, H), paint("#120C26"))
    # bed
    c.drawRRect(rr(20, 560, 90, 900, 20), paint(WOOD_D))
    c.drawRect(skia.Rect(40, 800, 600, 900), paint(WOOD))
    c.drawRRect(rr(40, 740, 600, 820, 22), paint("#C9C2DE"))
    c.drawRRect(rr(80, 690, 250, 760, 30), paint("cream"))
    if made:
        c.drawRRect(rr(150, 744, 600, 820, 16), paint("#3D5A80"))
        c.drawRRect(rr(150, 736, 600, 762, 10), paint("cream"))
    elif sleeper:
        c.drawCircle(170, 712, 40, paint("skin"))
        c.drawCircle(160, 698 - 6 * tired, 38, paint("hair"))
        p = skia.Path(); p.moveTo(200, 730); p.cubicTo(300, 660, 460, 680, 600, 740); p.lineTo(600, 820); p.lineTo(190, 820); p.close()
        c.drawPath(p, paint("#3D5A80"))
        c.drawPath(p, paint("amber", 0.25, stroke=4))
    # side table + clock + phone
    c.drawRect(skia.Rect(650, 800, 900, 1000), paint(WOOD_D))
    c.drawRect(skia.Rect(640, 780, 910, 806), paint(WOOD_L))
    c.drawCircle(775, 900, 8, paint("amber"))
    c.drawRRect(rr(660, 766, 740, 780, 5), paint("#0B0B12"))
    if phone_glow > 0:
        glow(c, 700, 760, 120, "teal", 0.5 * phone_glow)
    alarm_clock(c, 790, 640, 0.85, t, ring=ring, bedtime=bedtime)
    vignette(c, 960, H, 0.4)
    c.restore()


def sleep_bar(c, cx, y, start_h, end_h, p, need=7, s=1.0, color="teal", title=None):
    """Night timeline from 9 PM to 7 AM; a filled bar start_h -> end_h (24 h clock, e.g. 23 -> 5) growing with p,
    and a dashed outline of `need` hours ending at end_h (the missing hours show as the gap)."""
    w = 1300 * s; x0 = cx - w / 2
    def X(h):
        hh = (h - 21) % 24
        return x0 + w * hh / 10
    c.drawRRect(rr(x0, y - 40 * s, x0 + w, y + 40 * s, 40 * s), paint("#0E0A22"))
    for h in range(21, 32):
        hh = h % 24
        c.drawLine(X(hh), y + 52 * s, X(hh), y + 66 * s, paint("sand", 0.6, stroke=3))
        lab = f"{(hh - 1) % 12 + 1}{'PM' if 12 <= hh < 24 else 'AM'}"
        label(c, lab, X(hh), y + 100 * s, int(24 * s), "sand", "bold", 0.8)
    xs, xe = X(start_h), X(end_h)
    xn = X((end_h - need) % 24)
    c.drawRRect(rr(xn, y - 46 * s, xe, y + 46 * s, 44 * s), dashed("gold", 0.9, 5))
    fill = xs + (xe - xs) * ease(p)
    if p > 0:
        c.drawRRect(rr(xs, y - 34 * s, max(xs + 1, fill), y + 34 * s, 34 * s), paint(color))
        glow(c, (xs + fill) / 2, y, 200 * s, color, 0.25)
    hrs = ((end_h - start_h) % 24) * ease(p)
    label(c, f"{hrs:.0f} HOURS", (xs + xe) / 2, y - 70 * s, int(56 * s), "cream", "extrabold", min(1.0, p * 2))
    if title:
        label(c, title, cx, y - 160 * s, int(48 * s), "gold", "extrabold")


def battery(c, x, y, s, level, t, a=1.0):
    """Battery (brain energy): level 0..1, green -> amber -> coral as it drains; blinks when low."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRRect(rr(-90, -170, 90, 170, 26), paint("cream", a, stroke=12))
    c.drawRRect(rr(-36, -196, 36, -170, 8), paint("cream", a))
    colr = "teal" if level > 0.6 else ("amber" if level > 0.3 else "coral")
    blink = 1.0 if level > 0.3 else (0.55 + 0.45 * math.sin(t * 10))
    h = 300 * clamp(level)
    c.drawRRect(rr(-70, 150 - h, 70, 150, 14), paint(colr, a * blink))
    label(c, f"{level * 100:.0f}%", 0, 250, 52, colr, "extrabold", a)
    c.restore()


def sticky(c, x, y, s, txt, rot=-6, a=1.0):
    if a <= 0:
        return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawRect(skia.Rect(-110, -100, 120, 120), paint("#000000", 0.3 * a))
    c.drawRect(skia.Rect(-120, -110, 120, 110), paint("#F6D86B", a))
    for i, line in enumerate(txt.split("\n")):
        label(c, line, 0, -10 + i * 56, 48, "ink", "extrabold", a)
    c.restore()


def dna(c, cx, cy, w, t, lit=0, total=24, a=1.0):
    """Horizontal double helix; the first `lit` rungs light up gold."""
    n = total
    for k in range(n):
        x = cx - w / 2 + w * k / (n - 1)
        ph = k * 0.55 + t * 1.2
        y1 = cy + math.sin(ph) * 110; y2 = cy - math.sin(ph) * 110
        on = k < lit
        c.drawLine(x, y1, x, y2, paint("gold" if on else "sand", (0.95 if on else 0.3) * a, stroke=8))
        if on:
            glow(c, x, cy, 60, "gold", 0.18 * a)
        c.drawCircle(x, y1, 14, paint("teal", a)); c.drawCircle(x, y2, 14, paint("coral", a))


def owl(c, x, y, s, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawOval(skia.Rect(-70, -90, 70, 90), paint("#5E3B26", a))
    c.drawOval(skia.Rect(-46, -40, 46, 80), paint("#B07A52", a))
    for sx in (-1, 1):
        c.drawCircle(sx * 30, -40, 26, paint("cream", a)); c.drawCircle(sx * 30, -40, 12, paint("ink", a))
        c.drawLine(sx * 40, -88, sx * 62, -120, paint("#5E3B26", a, stroke=14))
    c.drawPath(_tri(0, -22, 12), paint("amber", a))
    c.restore()


def lark(c, x, y, s, t, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawOval(skia.Rect(-60, -36, 60, 36), paint("amber", a))
    c.drawCircle(52, -34, 28, paint("amber", a))
    c.drawCircle(60, -40, 6, paint("ink", a))
    c.drawPath(_tri(86, -34, 12, rot=90), paint("coral", a))
    wing = math.sin(t * 8) * 20
    c.drawPath(_poly([(-20, -10), (30, -10), (0, -70 - wing)]), paint("gold", a))
    glow(c, 0, -120, 120, "gold", 0.35 * a)
    c.restore()


def _poly(pts):
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    p.close(); return p


def _tri(x, y, r, rot=180):
    a = math.radians(rot)
    return _poly([(x + math.cos(a + k * 2.094) * r, y + math.sin(a + k * 2.094) * r) for k in range(3)])


def lab_beds(c, t, a=1.0):
    """Sleep lab at night: three beds with monitors showing brain waves."""
    c.drawRect(skia.Rect(0, 0, W, H), paint("#0B1022"))
    glow(c, W / 2, 300, 900, "teal", 0.12)
    c.drawRect(skia.Rect(0, 820, W, H), paint("#070A16"))
    for k in range(3):
        x = 380 + k * 580
        c.drawRRect(rr(x - 200, 700, x + 200, 790, 20), paint("#C9D6E6", 0.75 * a))
        c.drawRRect(rr(x - 190, 660, x - 60, 712, 18), paint("cream", 0.9 * a))
        c.drawRect(skia.Rect(x - 190, 790, x - 170, 880), paint("#3A4458")); c.drawRect(skia.Rect(x + 170, 790, x + 190, 880), paint("#3A4458"))
        c.drawRRect(rr(x + 60, 420, x + 240, 540, 12), paint("#141C30", a))
        pth = skia.Path(); pth.moveTo(x + 76, 480)
        for j in range(1, 24):
            pth.lineTo(x + 76 + j * 6.5, 480 + math.sin(j * 1.1 + t * 6 + k) * 22 * (0.5 + 0.5 * math.sin(j * 0.4)))
        c.drawPath(pth, paint("teal", a, stroke=4))
        c.drawLine(x + 150, 540, x + 150, 700, paint("#3A4458", a, stroke=6))


def reaction_screen(c, cx, cy, t, t0, slow=1.0):
    """A reaction test: a light flashes, the response time counts up; slow 0 = 0.25 s, 1 = 0.7 s, and the screen
    briefly blanks out (an attention lapse)."""
    c.drawRRect(rr(cx - 480, cy - 300, cx + 480, cy + 300, 26), paint("#0E0A22"))
    c.drawRRect(rr(cx - 480, cy - 300, cx + 480, cy + 300, 26), paint("sand", 0.35, stroke=5))
    label(c, "REACTION TEST", cx, cy - 210, 40, "sand", "bold")
    cyc = (t - t0) % 2.2
    on = cyc < 1.2
    if on:
        glow(c, cx, cy - 40, 170, "coral", 0.6)
        c.drawCircle(cx, cy - 40, 70, paint("coral"))
    rt = 0.25 + 0.46 * slow
    shown = min(rt, max(0.0, cyc - 0.05))
    lapse = slow > 0.5 and 1.25 < cyc < 1.6
    if lapse:
        c.drawRRect(rr(cx - 480, cy - 300, cx + 480, cy + 300, 26), paint("#000000", 0.7))
        label(c, "LAPSE", cx, cy - 40, 60, "coral", "extrabold")
    label(c, f"{shown:.2f} s", cx, cy + 170, 96, "coral" if shown > 0.4 else "teal", "extrabold")
    # comparison bars beside the screen: normal vs now
    for i, (lab, v, colr) in enumerate((("NORMAL", 0.25, "teal"), ("DAY 14", rt, "coral"))):
        y = cy - 120 + i * 200
        c.drawRRect(rr(cx + 540, y, cx + 540 + 260 * v / 0.75, y + 60, 14), paint(colr))
        label(c, f"{lab} {v:.2f} s", cx + 540, y - 16, 34, colr, "extrabold", align="left")


def balance(c, cx, cy, tilt, left, right, a=1.0):
    """Balance scale; tilt -1..1 (0 = level)."""
    c.drawLine(cx, cy, cx, cy + 360, paint("sand", a, stroke=14))
    c.drawRRect(rr(cx - 120, cy + 350, cx + 120, cy + 380, 12), paint("sand", a))
    ang = math.radians(10 * tilt)
    for sx, txt in ((-1, left), (1, right)):
        px = cx + sx * math.cos(ang) * 420; py = cy + sx * math.sin(ang) * 420
        c.drawLine(px, py, px, py + 150, paint("sand", 0.7 * a, stroke=4))
        c.drawRRect(rr(px - 190, py + 150, px + 190, py + 290, 20), paint("plum", a))
        for i, line in enumerate(txt.split("\n")):
            label(c, line, px, py + 212 + i * 52, 44, "cream", "extrabold", a)
    c.drawLine(cx - math.cos(ang) * 420, cy - math.sin(ang) * 420, cx + math.cos(ang) * 420, cy + math.sin(ang) * 420, paint("sand", a, stroke=14))
    c.drawCircle(cx, cy, 20, paint("gold", a))


def moon_clock(c, x, y, s, t, a=1.0):
    """A 10 PM bedtime clock: navy face, crescent moon, hands at 10:00, soft glow."""
    if a <= 0:
        return
    c.save(); c.translate(x, y); c.scale(s, s)
    glow(c, 0, 0, 320, "gold", 0.35 * a)
    c.drawCircle(0, 0, 150, paint("deep", a)); c.drawCircle(0, 0, 150, paint("gold", a, stroke=10))
    c.drawCircle(-40, -60, 40, paint("gold", a)); c.drawCircle(-24, -72, 36, paint("deep", a))
    for k in range(12):
        an = math.radians(k * 30 - 90)
        c.drawLine(math.cos(an) * 118, math.sin(an) * 118, math.cos(an) * 136, math.sin(an) * 136, paint("sand", a, stroke=6))
    c.drawLine(0, 0, math.cos(math.radians(10 * 30 - 90)) * 70, math.sin(math.radians(10 * 30 - 90)) * 70, paint("cream", a, stroke=14))
    c.drawLine(0, 0, 0, -110, paint("cream", a, stroke=9))
    c.drawCircle(0, 0, 12, paint("gold", a))
    label(c, "10 PM", 0, 220, 64, "gold", "extrabold", a)
    c.restore()


def jogger(c, x, y, s, t, a=1.0):
    """Running silhouette (movie-style 5 AM jogger)."""
    c.save(); c.translate(x, y); c.scale(s, s)
    ph = t * 9
    c.drawCircle(10, -330, 38, paint("#140A26", a))
    c.drawLine(0, -290, -10, -150, paint("#140A26", a, stroke=46))
    for k, sgn in ((0, 1), (1, -1)):
        sw = math.sin(ph + k * math.pi) * 0.7
        c.drawLine(-10, -150, -10 + math.sin(sw) * 90, -150 + math.cos(sw) * 90, paint("#140A26", a, stroke=30))
        c.drawLine(-10 + math.sin(sw) * 90, -150 + math.cos(sw) * 90, -10 + math.sin(sw) * 90 - 30 * sgn, -150 + math.cos(sw) * 90 + 80, paint("#140A26", a, stroke=26))
        c.drawLine(0, -270, math.sin(-sw) * 80, -270 + math.cos(-sw) * 70, paint("#140A26", a, stroke=22))
    c.drawLine(-30, -290, 40, -290, paint("amber", 0.5 * a, stroke=4))
    c.restore()


def desk_lamp_student(c, x, y, s, t, a=1.0):
    """A student at a desk under a lamp before sunrise (silhouette + warm lamp light)."""
    c.save(); c.translate(x, y); c.scale(s, s)
    glow(c, 120, -260, 300, "amber", 0.5 * a)
    c.drawRect(skia.Rect(-260, -120, 320, -96), paint(WOOD, a))
    c.drawLine(200, -120, 160, -320, paint("sand", a, stroke=10)); c.drawLine(160, -320, 90, -280, paint("sand", a, stroke=10))
    c.drawPath(_poly([(60, -300), (130, -260), (60, -230)]), paint("amber", a))
    c.drawRRect(rr(-160, -320, -40, -120, 40), paint("#140A26", a))
    c.drawCircle(-90, -360, 44, paint("#140A26", a))
    c.drawRect(skia.Rect(-20, -140, 120, -124), paint("cream", a))
    c.restore()
