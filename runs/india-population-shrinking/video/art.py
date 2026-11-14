"""Topic art for 'What If India's Population Started Shrinking?' (collage style: paper cut-outs, tape, stamps).
Every drawing takes (c, x, y, s, t, ...) and draws itself as a cut-out with its own stop-motion jitter."""
import math
import skia
from krwi.lib import *  # noqa: F401,F403
from krwi.art import *  # noqa: F401,F403

SEPIA = "#C9A97A"
SKIN = ["#8D5A3B", "#A8704A", "#7A4A2E", "#B07D52"]
CLOTH = ["#2F5D8A", "#C0392B", "#2E8B57", "#E07A1F", "#6C3483", "#D4A017", "#3D5A80", "#A33B2B"]
GREY_HAIR = "#D9D4CC"


def rr(x0, y0, x1, y1, r):
    return skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), r, r)


def _j(key, t, x, y, amt=3.0):
    dx, dy, a = jit(key, t, amt)
    return x + dx, y + dy, a


def headline(c, s, x, y, size, p, seed=2, rot=-2, color="#F4EFE3", ink=INK):
    f = font("extrabold", size)
    w = text_w(s, f)
    torn_strip(c, x, y, w + size * 1.6, size * 1.9, seed=seed, color=color, rot=rot)
    type_text(c, s, x, y, size, p, color=ink)


def CamC(c, zoom=1.0, cx=W / 2, cy=H / 2, t=0.0):
    """Cam that never shows past the frame edge: the centre is clamped for the current zoom."""
    mx, my = (W / 2) * (1 - 1 / max(zoom, 1.0)), (H / 2) * (1 - 1 / max(zoom, 1.0))
    return Cam(c, zoom, clamp(cx, W / 2 - mx, W / 2 + mx), clamp(cy, H / 2 - my, H / 2 + my), t=t)


# ---------------------------------------------------------------- people
def figure(k, x, y, s, i=0, old=False, child=False, female=False, cloth=None, mono=None):
    """One faceless paper person drawn on k (feet at x, y). mono = a single colour for sepia / silhouettes."""
    if child:
        s = s * 0.62
    skin = ("#8C6E50" if mono else SKIN[i % len(SKIN)])
    cl = (["#4E3B28", "#6A503A", "#5C452F"][i % 3] if mono else (cloth or CLOTH[i % len(CLOTH)]))
    hair = mono or (GREY_HAIR if old else "#1B1030")
    leg = paint(mono or "#2A2A33", stroke=24 * s)
    k.drawLine(x - 13 * s, y - 115 * s, x - 13 * s, y, leg)
    k.drawLine(x + 13 * s, y - 115 * s, x + 13 * s, y, leg)
    if female:
        body = skia.Path(); body.moveTo(x - 44 * s, y - 275 * s); body.lineTo(x + 44 * s, y - 275 * s)
        body.lineTo(x + 74 * s, y - 95 * s); body.lineTo(x - 74 * s, y - 95 * s); body.close()
        k.drawRRect(rr(x - 44 * s, y - 350 * s, x + 44 * s, y - 250 * s, 30 * s), paint(hair))
        k.drawPath(body, paint(cl))
        if not mono:
            halftone(k, body, "#000000", 0.22, step=14)
    else:
        k.drawRRect(rr(x - 46 * s, y - 275 * s, x + 46 * s, y - 108 * s, 28 * s), paint(cl))
        if not mono:
            halftone(k, skia.Path().addRRect(rr(x - 46 * s, y - 275 * s, x + 46 * s, y - 108 * s, 28 * s)), "#000000", 0.22, step=14)
    k.drawCircle(x, y - 314 * s, 38 * s, paint(skin))
    k.drawCircle(x, y - 332 * s, 37 * s, paint(hair))
    k.drawCircle(x, y - 310 * s, 33 * s, paint(skin))
    if old and not mono:
        k.drawCircle(x, y - 352 * s, 17 * s, paint(hair)) if female else None
        # spectacles
        k.drawCircle(x - 13 * s, y - 310 * s, 9 * s, paint("#2A2A33", stroke=3 * s))
        k.drawCircle(x + 13 * s, y - 310 * s, 9 * s, paint("#2A2A33", stroke=3 * s))
    if old:
        k.drawLine(x + 52 * s, y - 180 * s, x + 62 * s, y, paint(mono or "#6B3F1D", stroke=9 * s))   # walking stick


def person(c, x, y, s, t, key="p", **kw):
    x, y, a = _j(key, t, x, y, 2.0)
    cutout(c, lambda k: figure(k, x, y, s, **kw), border=7, shadow=(5, 8))


def family_photo(c, x, y, s, t, adults, kids, sepia=False, key="photo", rot=-3.0, p=1.0, peel=0.0, old_rows=0):
    """A taped family photo: `adults` standing at the back, `kids` in front. sepia = the old one.
    old_rows = number of grey-haired adults (grandparents) in the back row. peel = the last kid fades/slides out."""
    x, y, a = _j(key, t, x, y, 2.5)
    if p <= 0:
        return
    w, h = 820 * s, 600 * s
    sc = 0.6 + 0.4 * ease_out(p)

    def d(k):
        k.save()
        k.translate(x, y); k.rotate(rot); k.scale(sc, sc); k.translate(-x, -y)
        k.drawRect(skia.Rect(x - w / 2 - 26 * s, y - h / 2 - 26 * s, x + w / 2 + 26 * s, y + h / 2 + 70 * s), paint("#F6F1E4"))
        bg = "#B89868" if sepia else "#8FB8C9"
        k.drawRect(skia.Rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2), paint(bg))
        if not sepia:
            k.drawRect(skia.Rect(x - w / 2, y + h / 6, x + w / 2, y + h / 2), paint("#C9B38A"))
        k.save(); k.clipRect(skia.Rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2))
        mono = "#5A4632" if sepia else None
        back = adults
        for i in range(back):
            bx = x + (i - (back - 1) / 2) * min(150, (w - 120) / max(back, 1)) * s / s
            figure(k, bx, y + h / 2 - 40 * s, 0.95 * s, i=i + 1, old=i < old_rows, female=i % 2 == 1, mono=mono)
        for j in range(kids):
            kx = x + (j - (kids - 1) / 2) * min(118, (w - 80) / max(kids, 1))
            ky = y + h / 2 + 10 * s
            al = 1.0
            if j == kids - 1 and peel > 0:
                kx += 260 * peel * s
                ky += 120 * peel * s
            if al > 0:
                figure(k, kx, ky, 0.95 * s, i=j + 3, child=True, female=j % 2 == 0, mono=mono)
        k.restore()
        if sepia:
            halftone(k, skia.Path().addRect(skia.Rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2)), "#3A2A18", 0.25, step=10)
        k.restore()
    cutout(c, d, border=4, shadow=(8, 12))
    tape(c, x - w * 0.42 * sc, y - h * 0.55 * sc, 150 * s, 46 * s, -22 + rot)
    tape(c, x + w * 0.42 * sc, y - h * 0.55 * sc, 150 * s, 46 * s, 20 + rot)


def baby(k, x, y, s, i=0):
    k.drawOval(skia.Rect(x - 40 * s, y - 60 * s, x + 40 * s, y + 30 * s), paint(["#F4EFE3", "#F7D6E0", "#D6E6F7"][i % 3]))
    k.drawCircle(x, y - 80 * s, 34 * s, paint(SKIN[i % 4]))


# ---------------------------------------------------------------- places and things
def kerala_house(c, x, y, s, t, locks=0.0, key="khouse"):
    """A big Kerala house: sloped tiled roof, four windows; `locks` (0-3) padlocks pop onto windows 2-4."""
    x, y, a = _j(key, t, x, y)

    def d(k):
        k.drawRect(skia.Rect(x - 380 * s, y - 330 * s, x + 380 * s, y), paint("#EFE2C4"))
        halftone(k, skia.Path().addRect(skia.Rect(x - 380 * s, y - 330 * s, x + 380 * s, y)), "#7A5A2A", 0.2)
        r = skia.Path(); r.moveTo(x - 460 * s, y - 310 * s); r.lineTo(x - 260 * s, y - 520 * s)
        r.lineTo(x + 260 * s, y - 520 * s); r.lineTo(x + 460 * s, y - 310 * s); r.close()
        k.drawPath(r, paint("#A9442E")); halftone(k, r, "#000000", 0.3, step=12)
        for i in range(4):
            wx = x + (-270 + i * 180) * s
            k.drawRect(skia.Rect(wx - 55 * s, y - 270 * s, wx + 55 * s, y - 140 * s), paint("#3C6E71" if i == 0 else "#2B2B33"))
            k.drawRect(skia.Rect(wx - 62 * s, y - 278 * s, wx + 62 * s, y - 262 * s), paint("#6B3F1D"))
        k.drawRect(skia.Rect(x - 50 * s, y - 120 * s, x + 50 * s, y), paint("#6B3F1D"))
        k.drawRect(skia.Rect(x - 420 * s, y, x + 420 * s, y + 24 * s), paint("#8B6B3A"))
    cutout(c, d)
    glow(c, x - 270 * s, y - 205 * s, 70 * s, "gold", 0.35)
    for i in range(3):
        q = ease_out(clamp(locks - i, 0, 1))
        if q > 0:
            padlock(c, x + (-90 + i * 180) * s, y - 200 * s, 0.8 * s * q, t, key=f"lk{i}")


def padlock(c, x, y, s, t, key="lock"):
    x, y, a = _j(key, t, x, y, 2.0)

    def d(k):
        k.drawArc(skia.Rect(x - 30 * s, y - 70 * s, x + 30 * s, y - 10 * s), 180, 180, False, paint("#8A8F98", stroke=12 * s))
        k.drawRRect(rr(x - 46 * s, y - 30 * s, x + 46 * s, y + 46 * s, 8 * s), paint("#D4A017"))
        k.drawCircle(x, y + 6 * s, 8 * s, paint("#3A2A10"))
    cutout(c, d, border=5, shadow=(4, 6))


def old_phone(c, x, y, s, t, ring=0.0, key="oldphone"):
    x, y, a = _j(key, t, x, y, 2.0)
    sh = math.sin(t * 50) * 6 * ring

    def d(k):
        k.drawRRect(rr(x - 150 * s, y - 70 * s, x + 150 * s, y + 90 * s, 30 * s), paint("#A33B2B"))
        halftone(k, skia.Path().addRRect(rr(x - 150 * s, y - 70 * s, x + 150 * s, y + 90 * s, 30 * s)), "#000000", 0.25)
        k.drawRRect(rr(x - 170 * s + sh, y - 130 * s, x + 170 * s + sh, y - 70 * s, 26 * s), paint("#7E2A1E"))
        k.drawCircle(x, y + 15 * s, 50 * s, paint("#F4EFE3"))
        for i in range(10):
            an = i / 10 * 2 * math.pi
            k.drawCircle(x + 34 * s * math.cos(an), y + 15 * s + 34 * s * math.sin(an), 6 * s, paint("#3A2A20"))
    cutout(c, d)
    if ring > 0:
        for i in range(3):
            r = 200 * s + i * 50 * s + (t * 120) % 50
            c.drawArc(skia.Rect(x - r, y - r - 60 * s, x + r, y + r - 60 * s), -60, 30, False, paint(RED_INK, 0.8 * ring, stroke=8))
            c.drawArc(skia.Rect(x - r, y - r - 60 * s, x + r, y + r - 60 * s), -150, 30, False, paint(RED_INK, 0.8 * ring, stroke=8))


def train(c, y, s, t, t0, brake=0.0, key="train", cars=14, speed=520):
    """A long paper train rolling left to right; `brake` (0-1) shows sparks under the wheels."""
    dx, dy, a = jit(key, t, 1.5)
    off = (t - t0) * speed * (1 - 0.55 * brake)
    k_len = 430 * s
    track = paint("#5A4632", stroke=10)
    c.drawLine(-50, y + 70 * s, W + 50, y + 70 * s, track)
    for i in range(30):
        tx = (i * 90 - off * 0.0) % (W + 100) - 50
        c.drawLine(tx, y + 62 * s, tx + 30, y + 86 * s, paint("#6B5A44", stroke=6))
    for i in range(cars):
        cx0 = -i * (k_len + 20 * s) + off - 100
        if cx0 > W + 50 or cx0 + k_len < -60:
            continue

        def d(k, cx0=cx0, i=i):
            colr = "#2F5D8A" if i else "#A33B2B"
            k.drawRRect(rr(cx0 + dx, y - 170 * s + dy, cx0 + k_len + dx, y + 40 * s + dy, 22 * s), paint(colr))
            k.drawRect(skia.Rect(cx0 + dx, y - 10 * s + dy, cx0 + k_len + dx, y + 10 * s + dy), paint("#F2B44C"))
            for wdx in range(5):
                wx = cx0 + 40 * s + wdx * 78 * s + dx
                k.drawRect(skia.Rect(wx, y - 130 * s + dy, wx + 50 * s, y - 70 * s + dy), paint("#F4EFE3"))
            for wh in (70, k_len / s - 70):
                k.drawCircle(cx0 + wh * s + dx, y + 50 * s + dy, 26 * s, paint("#2A2A33"))
        cutout(c, d, border=6, shadow=(4, 6))
        if brake > 0:
            for wh in (70, k_len / s - 70):
                for j in range(4):
                    ang = rng(i * 7 + j + int(t * 12), 3) * 1.2 + 3.4
                    sx, sy = cx0 + wh * s, y + 70 * s
                    c.drawLine(sx, sy, sx + math.cos(ang) * 50, sy + math.sin(ang) * 40, paint("gold", 0.9 * brake, stroke=4))


def desk_row(c, x, y, s, t, n, kids, key="desks"):
    """Rows of school desks; the first `kids` desks have a child behind them."""
    for i in range(n):
        dx = x + (i % 6 - 2.5) * 230 * s
        dy = y + (i // 6) * 210 * s
        if i < kids:
            person(c, dx, dy - 10 * s, 0.75 * s, t, key=f"{key}k{i}", i=i, child=True, female=i % 2 == 0)

        def d(k, dx=dx, dy=dy):
            k.drawRect(skia.Rect(dx - 90 * s, dy - 80 * s, dx + 90 * s, dy - 60 * s), paint("#8B5A2B"))
            k.drawLine(dx - 80 * s, dy - 60 * s, dx - 80 * s, dy + 10 * s, paint("#5A3A1B", stroke=8 * s))
            k.drawLine(dx + 80 * s, dy - 60 * s, dx + 80 * s, dy + 10 * s, paint("#5A3A1B", stroke=8 * s))
        cutout(c, d, border=5, shadow=(4, 6))


def bell(c, x, y, s, t, swing=0.0, key="bell"):
    x, y, a = _j(key, t, x, y, 1.5)
    ang = math.sin(t * 9) * 18 * swing

    def d(k):
        k.save(); k.translate(x, y); k.rotate(ang)
        b = skia.Path(); b.moveTo(-90 * s, 120 * s); b.cubicTo(-90 * s, -40 * s, -40 * s, -110 * s, 0, -110 * s)
        b.cubicTo(40 * s, -110 * s, 90 * s, -40 * s, 90 * s, 120 * s); b.close()
        k.drawPath(b, paint("#D4A017")); halftone(k, b, "#5A3A00", 0.3, step=12)
        k.drawRect(skia.Rect(-110 * s, 110 * s, 110 * s, 135 * s), paint("#B8860B"))
        k.drawCircle(0, 150 * s, 22 * s, paint("#6B4A00"))
        k.drawRect(skia.Rect(-10 * s, -150 * s, 10 * s, -110 * s), paint("#5A3A1B"))
        k.restore()
    cutout(c, d)


def building(c, x, y, s, t, kind="hospital", key="bld"):
    x, y, a = _j(key, t, x, y)

    def d(k):
        k.drawRect(skia.Rect(x - 220 * s, y - 420 * s, x + 220 * s, y), paint("#F4EFE3" if kind == "hospital" else "#E8C27A"))
        halftone(k, skia.Path().addRect(skia.Rect(x - 220 * s, y - 420 * s, x + 220 * s, y)), "#7A5A2A", 0.18)
        for r in range(3):
            for cc in range(3):
                k.drawRect(skia.Rect(x + (-170 + cc * 120) * s, y + (-380 + r * 100) * s, x + (-110 + cc * 120) * s, y + (-320 + r * 100) * s), paint("#5C8FB0"))
        if kind == "hospital":
            k.drawRect(skia.Rect(x - 20 * s, y - 520 * s, x + 20 * s, y - 430 * s), paint("#C0392B"))
            k.drawRect(skia.Rect(x - 45 * s, y - 495 * s, x + 45 * s, y - 455 * s), paint("#C0392B"))
        elif kind == "school":
            r2 = skia.Path(); r2.moveTo(x - 250 * s, y - 410 * s); r2.lineTo(x, y - 540 * s); r2.lineTo(x + 250 * s, y - 410 * s); r2.close()
            k.drawPath(r2, paint("#A33B2B"))
            k.drawCircle(x, y - 450 * s, 34 * s, paint("#F4EFE3"))
            k.drawLine(x, y - 450 * s, x, y - 472 * s, paint(INK, stroke=4 * s)); k.drawLine(x, y - 450 * s, x + 16 * s, y - 450 * s, paint(INK, stroke=4 * s))
        k.drawRect(skia.Rect(x - 45 * s, y - 110 * s, x + 45 * s, y), paint("#4A3020"))
    cutout(c, d)


def balance(c, x, y, s, t, tilt, key="scale"):
    """A paper balance: tilt > 0 = the right pan goes down."""
    x, y, a = _j(key, t, x, y, 1.5)
    ang = 14 * tilt
    L = 420 * s
    lx, ly = x - L * math.cos(math.radians(ang)), y - 260 * s - L * math.sin(math.radians(ang))
    rx, ry = x + L * math.cos(math.radians(ang)), y - 260 * s + L * math.sin(math.radians(ang))

    def d(k):
        k.drawRect(skia.Rect(x - 16 * s, y - 260 * s, x + 16 * s, y + 160 * s), paint("#6B3F1D"))
        k.drawRect(skia.Rect(x - 140 * s, y + 140 * s, x + 140 * s, y + 175 * s), paint("#6B3F1D"))
        k.drawLine(lx, ly, rx, ry, paint("#8B5A2B", stroke=20 * s))
        for (px, py) in ((lx, ly), (rx, ry)):
            k.drawLine(px, py, px - 110 * s, py + 170 * s, paint("#5A4632", stroke=4))
            k.drawLine(px, py, px + 110 * s, py + 170 * s, paint("#5A4632", stroke=4))
            k.drawArc(skia.Rect(px - 150 * s, py + 120 * s, px + 150 * s, py + 230 * s), 0, 180, True, paint("#C9A060"))
    cutout(c, d)
    return (lx, ly + 170 * s), (rx, ry + 170 * s)


def skyline(c, x, y, s, t, city="delhi", key="sky"):
    x, y, a = _j(key, t, x, y, 2.0)

    def d(k):
        base = "#3D5A80" if city == "delhi" else "#6C3483"
        hs = [260, 340, 200, 420, 300, 240, 380, 220] if city == "delhi" else [380, 300, 460, 260, 340, 420, 280, 320]
        for i, h in enumerate(hs):
            bx = x - 400 * s + i * 100 * s
            k.drawRect(skia.Rect(bx, y - h * s, bx + 90 * s, y), paint(base, 0.85 + 0.15 * (i % 2)))
            for r in range(int(h / 60)):
                k.drawRect(skia.Rect(bx + 20 * s, y - h * s + 30 * s + r * 60 * s, bx + 36 * s, y - h * s + 50 * s + r * 60 * s), paint("#F2D06B", 0.8))
        if city == "delhi":
            # India Gate-like arch silhouette in front
            k.drawRect(skia.Rect(x - 110 * s, y - 330 * s, x + 110 * s, y), paint("#C79A5C"))
            k.drawRect(skia.Rect(x - 50 * s, y - 230 * s, x + 50 * s, y), paint("#3A2A1A"))
            k.drawArc(skia.Rect(x - 50 * s, y - 280 * s, x + 50 * s, y - 180 * s), 180, 180, True, paint("#3A2A1A"))
            k.drawRect(skia.Rect(x - 130 * s, y - 360 * s, x + 130 * s, y - 330 * s), paint("#B5884A"))
        else:
            # lattice tower silhouette
            tw = skia.Path(); tw.moveTo(x - 90 * s, y); tw.lineTo(x - 12 * s, y - 560 * s); tw.lineTo(x + 12 * s, y - 560 * s); tw.lineTo(x + 90 * s, y); tw.close()
            k.drawPath(tw, paint("#D9573D"))
            for r in range(6):
                yy = y - r * 90 * s
                k.drawLine(x - (90 - r * 13) * s, yy, x + (90 - r * 13) * s, yy, paint("#F4EFE3", stroke=6 * s))
        k.drawRect(skia.Rect(x - 440 * s, y, x + 440 * s, y + 30 * s), paint("#5A4632"))
    cutout(c, d)


def chair(k, x, y, s, colr="#C0392B"):
    k.drawRRect(rr(x - 40 * s, y - 150 * s, x + 40 * s, y - 60 * s, 16 * s), paint(colr))
    k.drawRect(skia.Rect(x - 48 * s, y - 70 * s, x + 48 * s, y - 50 * s), paint(colr))
    k.drawLine(x - 40 * s, y - 50 * s, x - 40 * s, y, paint("#D4A017", stroke=7 * s))
    k.drawLine(x + 40 * s, y - 50 * s, x + 40 * s, y, paint("#D4A017", stroke=7 * s))


def car(k, x, y, s, colr):
    body = skia.Path(); body.moveTo(x - 120 * s, y - 20 * s); body.lineTo(x - 70 * s, y - 80 * s); body.lineTo(x + 60 * s, y - 80 * s)
    body.lineTo(x + 110 * s, y - 20 * s); body.close()
    k.drawPath(body, paint(colr))
    k.drawRRect(rr(x - 140 * s, y - 30 * s, x + 140 * s, y + 20 * s, 14 * s), paint(colr))
    k.drawRect(skia.Rect(x - 55 * s, y - 70 * s, x + 50 * s, y - 30 * s), paint("#BFD9E6"))
    k.drawCircle(x - 80 * s, y + 22 * s, 24 * s, paint("#2A2A33")); k.drawCircle(x + 80 * s, y + 22 * s, 24 * s, paint("#2A2A33"))


def line_graph(c, x0, y0, w, h, pts, p, color=RED_INK, width=12):
    """Hand-drawn line through normalised pts [(0..1, 0..1)], drawn on over p, inside the box (x0, y0, w, h)."""
    P = [(x0 + u * w, y0 + h - v * h) for u, v in pts]
    marker_line(c, P, p, color=color, width=width)
    return P


def pie(c, x, y, r, frac, p, t, col1="#C0392B", col2="#E9D8A6", key="pie"):
    """Paper pie: frac of the circle in col1 (drawn on over p)."""
    x, y, a = _j(key, t, x, y, 2.0)

    def d(k):
        k.drawPath(paper_circle(x, y, r, 5), paint(col2))
        sweep = 360 * frac * ease(p)
        pa = skia.Path(); pa.moveTo(x, y); pa.arcTo(skia.Rect(x - r, y - r, x + r, y + r), -90, sweep, False); pa.close()
        k.drawPath(pa, paint(col1)); halftone(k, pa, "#000000", 0.3)
    cutout(c, d)
