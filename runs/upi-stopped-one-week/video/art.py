"""Topic art for 'What If UPI Stopped Working for One Week?' (collage style: paper cut-outs, tape, stamps).
Every drawing takes (c, x, y, s, t, ...) and draws itself as a cut-out with its own stop-motion jitter."""
import math
import skia
from krwi.lib import *  # noqa: F401,F403
from krwi.art import *  # noqa: F401,F403

GREEN, RED, BLUE = "#2E8B57", "#C0392B", "#2F5D8A"
NOTE = "#B9A3C9"        # Rs 500 note (stone grey / lilac)
STEEL = "#B8BEC6"


def rr(x0, y0, x1, y1, r):
    return skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), r, r)


def _j(key, t, x, y, amt=3.0):
    dx, dy, a = jit(key, t, amt)
    return x + dx, y + dy, a


# ---------------------------------------------------------------- small pieces
def qr(k, x, y, size, seed=3, dead=0.0):
    """A QR-code pattern (not a real code) centred on (x, y)."""
    n = 21
    cell = size / n
    k.drawRect(skia.Rect(x - size / 2 - cell, y - size / 2 - cell, x + size / 2 + cell, y + size / 2 + cell), paint("#FFFFFF"))
    ink = paint("#16161A", 1 - 0.55 * dead)
    for i in range(n):
        for j in range(n):
            finder = (i < 7 and j < 7) or (i >= n - 7 and j < 7) or (i < 7 and j >= n - 7)
            if finder:
                ii, jj = i % 14 if i < 7 else i - (n - 7), j % 14 if j < 7 else j - (n - 7)
                on = ii in (0, 6) or jj in (0, 6) or (2 <= ii <= 4 and 2 <= jj <= 4)
            else:
                on = rng(seed * 997 + i * 31 + j) > 0.52
            if on:
                k.drawRect(skia.Rect(x - size / 2 + i * cell, y - size / 2 + j * cell,
                                     x - size / 2 + (i + 1) * cell + 0.5, y - size / 2 + (j + 1) * cell + 0.5), ink)


def qr_sticker(c, x, y, s, t, key="qr", dead=0.0, cross=0.0):
    x, y, a = _j(key, t, x, y)

    def d(k):
        k.save(); k.rotate(a * 0.4 - 3, x, y)
        k.drawRRect(rr(x - 95 * s, y - 120 * s, x + 95 * s, y + 120 * s, 14 * s), paint("#5B2C83"))
        qr(k, x, y + 10 * s, 130 * s, dead=dead)
        f = font("extrabold", 26 * s)
        w = text_w("SCAN & PAY", f)
        k.drawString("SCAN & PAY", x - w / 2, y - 80 * s, f, paint("#FFFFFF"))
        k.restore()
    cutout(c, d, border=8)
    if cross > 0:
        marker_line(c, [(x - 110 * s, y - 130 * s), (x + 110 * s, y + 130 * s)], cross, width=16)
        marker_line(c, [(x + 110 * s, y - 130 * s), (x - 110 * s, y + 130 * s)], max(0, cross * 2 - 1), width=16)


def chai(c, x, y, s, t, key="chai", steam=True):
    x, y, a = _j(key, t, x, y)

    def d(k):
        g = skia.Path(); g.moveTo(x - 70 * s, y - 110 * s); g.lineTo(x + 70 * s, y - 110 * s)
        g.lineTo(x + 52 * s, y + 110 * s); g.lineTo(x - 52 * s, y + 110 * s); g.close()
        k.drawPath(g, paint("#E8E2D0", 0.9))
        tea = skia.Path(); tea.moveTo(x - 64 * s, y - 70 * s); tea.lineTo(x + 64 * s, y - 70 * s)
        tea.lineTo(x + 52 * s, y + 104 * s); tea.lineTo(x - 52 * s, y + 104 * s); tea.close()
        k.drawPath(tea, paint("#B5651D")); halftone(k, tea, "#5A2E0C", 0.45, step=12)
        for i in range(5):     # glass ridges
            k.drawLine(x - 58 * s + i * 29 * s, y - 100 * s, x - 46 * s + i * 23 * s, y + 104 * s, paint("#FFFFFF", 0.35, stroke=3 * s))
    cutout(c, d)
    if steam:
        for i in range(3):
            p = skia.Path(); xx = x - 30 * s + i * 30 * s
            p.moveTo(xx, y - 130 * s)
            for kk in range(1, 5):
                p.lineTo(xx + math.sin(t * 3 + kk + i) * 12 * s, y - 130 * s - kk * 30 * s)
            c.drawPath(p, paint("#FFFFFF", 0.55, stroke=5 * s))


def phone(c, x, y, s, t, key="phone", screen="failed", p=1.0, rot=-4):
    """Smartphone cut-out. screen: failed | success | qr | blank | scan."""
    x, y, a = _j(key, t, x, y, 2.0)

    def d(k):
        k.save(); k.rotate(rot + a * 0.3, x, y)
        k.drawRRect(rr(x - 170 * s, y - 330 * s, x + 170 * s, y + 330 * s, 40 * s), paint("#1E1E24"))
        k.drawRRect(rr(x - 150 * s, y - 300 * s, x + 150 * s, y + 300 * s, 24 * s), paint("#F7F5EF"))
        if screen in ("failed", "success"):
            ok = screen == "success"
            colr = GREEN if ok else RED
            k.drawCircle(x, y - 70 * s, 85 * s * (0.6 + 0.4 * ease_out(p)), paint(colr))
            if ok:
                m = skia.Path(); m.moveTo(x - 40 * s, y - 70 * s); m.lineTo(x - 10 * s, y - 40 * s); m.lineTo(x + 45 * s, y - 105 * s)
            else:
                m = skia.Path(); m.moveTo(x - 35 * s, y - 105 * s); m.lineTo(x + 35 * s, y - 35 * s)
                m.moveTo(x + 35 * s, y - 105 * s); m.lineTo(x - 35 * s, y - 35 * s)
            k.drawPath(m, paint("#FFFFFF", stroke=18 * s))
            for li, line in enumerate(["PAYMENT", "SUCCESSFUL" if ok else "FAILED"]):
                f = font("extrabold", 46 * s)
                w = text_w(line, f)
                k.drawString(line, x - w / 2, y + 70 * s + li * 56 * s, f, paint(colr))
            f = font("bold", 34 * s); w = text_w("₹10", f)
            k.drawString("₹10", x - w / 2, y + 200 * s, f, paint(INK))
        elif screen in ("qr", "scan"):
            qr(k, x, y - 20 * s, 210 * s, seed=5)
            if screen == "scan":
                yy = y - 125 * s + 210 * s * ((t * 0.8) % 1)
                k.drawLine(x - 120 * s, yy, x + 120 * s, yy, paint("#E53935", 0.9, stroke=6 * s))
        k.restore()
    cutout(c, d)


def person(c, x, y, s, t, color="#3D5A80", key="p", walk=0.0, bag=False, phone_glow=False, flip=False):
    """Faceless paper figure, feet at (x, y). walk>0 swings the legs."""
    x, y, a = _j(key, t, x, y, 2.0)
    sw = math.sin(t * 7 + rng(hash(key) % 97) * 6) * 18 * walk

    def d(k):
        k.save()
        if flip:
            k.scale(-1, 1); k.translate(-2 * x, 0)
        leg = paint("#2A2A33", stroke=26 * s)
        k.drawLine(x - 14 * s, y - 120 * s, x - 14 * s + sw * s, y, leg)
        k.drawLine(x + 14 * s, y - 120 * s, x + 14 * s - sw * s, y, leg)
        k.drawRRect(rr(x - 48 * s, y - 280 * s, x + 48 * s, y - 110 * s, 30 * s), paint(color))
        halftone(k, skia.Path().addRRect(rr(x - 48 * s, y - 280 * s, x + 48 * s, y - 110 * s, 30 * s)), "#000000", 0.25, step=14)
        k.drawCircle(x, y - 320 * s, 40 * s, paint("#8D5A3B"))
        k.drawCircle(x, y - 338 * s, 38 * s, paint("#1B1030")) if rng(hash(key) % 89) > 0.4 else None
        k.drawCircle(x, y - 316 * s, 34 * s, paint("#A8704A"))
        if bag:
            k.drawRect(skia.Rect(x - 110 * s, y - 290 * s, x - 40 * s, y - 190 * s), paint("#E07A1F"))
            k.drawRect(skia.Rect(x - 110 * s, y - 290 * s, x - 40 * s, y - 270 * s), paint("#B85E10"))
        if phone_glow:
            k.drawRRect(rr(x + 30 * s, y - 230 * s, x + 62 * s, y - 175 * s, 6 * s), paint("#1E1E24"))
        k.restore()
    cutout(c, d, border=7, shadow=(5, 8))
    if phone_glow:
        glow(c, x + (-46 if flip else 46) * s, y - 200 * s, 60 * s, "gold", 0.5)


def atm(c, x, y, s, t, key="atm", screen="ATM", out=0.0):
    x, y, a = _j(key, t, x, y, 1.5)

    def d(k):
        k.drawRRect(rr(x - 170 * s, y - 520 * s, x + 170 * s, y, 18 * s), paint("#C9472B"))
        halftone(k, skia.Path().addRect(skia.Rect(x - 170 * s, y - 520 * s, x + 170 * s, y)), "#5A1408", 0.3)
        k.drawRect(skia.Rect(x - 170 * s, y - 520 * s, x + 170 * s, y - 440 * s), paint("#F4EFE3"))
        f = font("extrabold", 52 * s); w = text_w("ATM", f)
        k.drawString("ATM", x - w / 2, y - 462 * s, f, paint("#C9472B"))
        k.drawRect(skia.Rect(x - 120 * s, y - 400 * s, x + 120 * s, y - 240 * s), paint("#123247" if out < 0.5 else "#2A2A2A"))
        k.drawRect(skia.Rect(x - 90 * s, y - 200 * s, x + 90 * s, y - 120 * s), paint("#2A2A33"))
        for i in range(3):
            for j in range(3):
                k.drawRect(skia.Rect(x - 80 * s + i * 56 * s, y - 196 * s + j * 25 * s, x - 36 * s + i * 56 * s, y - 176 * s + j * 25 * s), paint("#9AA0A6"))
        k.drawRect(skia.Rect(x - 100 * s, y - 95 * s, x + 100 * s, y - 80 * s), paint("#1A1A1A"))
    cutout(c, d)
    if out > 0:
        torn_strip(c, x, y - 320 * s, 300 * s, 130 * s, seed=4, color="#FFF3C4", rot=-6)
        type_text(c, "TEMPORARILY", x, y - 345 * s, 30 * s, out)
        type_text(c, "OUT OF SERVICE", x, y - 300 * s, 30 * s, max(0, out * 1.6 - 0.6), color=RED_INK)


def door(c, x, y, s, t, colr, name, key="door", shut=1.0):
    x, y, a = _j(key, t, x, y)

    def d(k):
        k.drawRect(skia.Rect(x - 95 * s, y - 330 * s, x + 95 * s, y), paint("#6B4A2B"))
        k.drawRect(skia.Rect(x - 80 * s, y - 315 * s, x + 80 * s, y), paint(colr))
        for yy in (-280, -160):
            k.drawRect(skia.Rect(x - 60 * s, y + yy * s, x + 60 * s, y + (yy + 100) * s), paint("#000000", 0.12))
        k.drawCircle(x + 55 * s, y - 150 * s, 10 * s, paint("gold"))
    cutout(c, d)
    torn_strip(c, x, y + 50 * s, 220 * s, 64 * s, seed=hash(name) % 50, rot=-2)
    type_text(c, name, x, y + 50 * s, 44 * s)


def house(c, x, y, s, t, key="house"):
    x, y, a = _j(key, t, x, y)

    def d(k):
        k.drawRect(skia.Rect(x - 200 * s, y - 260 * s, x + 200 * s, y), paint("#E8D5A9"))
        halftone(k, skia.Path().addRect(skia.Rect(x - 200 * s, y - 260 * s, x + 200 * s, y)), "#7A5A2A", 0.25)
        r = skia.Path(); r.moveTo(x - 240 * s, y - 250 * s); r.lineTo(x, y - 420 * s); r.lineTo(x + 240 * s, y - 250 * s); r.close()
        k.drawPath(r, paint("#A33B2B"))
        k.drawRect(skia.Rect(x - 50 * s, y - 150 * s, x + 50 * s, y), paint("#4A3020"))
    cutout(c, d)


def rupee_note(c, x, y, s, t, key="note", rot=0.0, colr=NOTE, val="500"):
    x, y, a = _j(key, t, x, y)

    def d(k):
        k.save(); k.rotate(rot + a * 0.3, x, y)
        k.drawRRect(rr(x - 170 * s, y - 75 * s, x + 170 * s, y + 75 * s, 8 * s), paint(colr))
        halftone(k, skia.Path().addRRect(rr(x - 170 * s, y - 75 * s, x + 170 * s, y + 75 * s, 8 * s)), "#3A2A4A", 0.25, step=12)
        k.drawCircle(x + 70 * s, y, 48 * s, paint("#FFFFFF", 0.45))
        f = font("extrabold", 54 * s)
        k.drawString("₹" + val, x - 150 * s, y + 18 * s, f, paint("#2A1E3A"))
        k.restore()
    cutout(c, d, border=6, shadow=(4, 6))


def note_stack(c, x, y, s, n, t, key="stack"):
    """A pile of n paper notes, bottom at y."""
    for i in range(int(n)):
        rupee_note(c, x + (rng(i, 3) - 0.5) * 16 * s, y - i * 26 * s, s, t, key=f"{key}{i % 7}", rot=(rng(i, 4) - 0.5) * 6)


def cart(c, x, y, s, t, key="cart"):
    """Sabzi cart with tomatoes, wheels at y."""
    x, y, a = _j(key, t, x, y, 2.0)

    def d(k):
        k.drawRect(skia.Rect(x - 300 * s, y - 210 * s, x + 300 * s, y - 150 * s), paint("#8B5A2B"))
        for i in range(26):
            tx = x - 270 * s + (i % 13) * 45 * s
            ty = y - 225 * s - (i // 13) * 34 * s
            k.drawCircle(tx, ty, 26 * s, paint("#D93A2B"))
            k.drawCircle(tx - 8 * s, ty - 8 * s, 6 * s, paint("#FFFFFF", 0.5))
            k.drawCircle(tx, ty - 24 * s, 6 * s, paint("#2E7D32"))
        k.drawLine(x + 300 * s, y - 180 * s, x + 420 * s, y - 120 * s, paint("#5A3A1A", stroke=14 * s))
        for wx in (-200, 200):
            k.drawCircle(x + wx * s, y - 60 * s, 60 * s, paint("#2A2A2A"))
            k.drawCircle(x + wx * s, y - 60 * s, 20 * s, paint("#9AA0A6"))
    cutout(c, d)


def counter_shop(c, x, y, s, t, key="kirana"):
    """Kirana counter with jars on a shelf; returns the QR spot."""
    x, y, a = _j(key, t, x, y, 1.5)

    def d(k):
        k.drawRect(skia.Rect(x - 520 * s, y - 640 * s, x + 520 * s, y - 610 * s), paint("#6B4A2B"))
        for i in range(8):
            jx = x - 450 * s + i * 128 * s
            k.drawRRect(rr(jx - 46 * s, y - 750 * s, jx + 46 * s, y - 640 * s, 14 * s), paint("#DDE8E8", 0.85))
            k.drawRect(skia.Rect(jx - 40 * s, y - 715 * s, jx + 40 * s, y - 645 * s),
                       paint(["#E3B23C", "#C0392B", "#7B4B2A", "#F1E3C0", "#6A994E"][i % 5]))
            k.drawRect(skia.Rect(jx - 48 * s, y - 770 * s, jx + 48 * s, y - 750 * s), paint("#C9472B"))
        k.drawRect(skia.Rect(x - 560 * s, y - 330 * s, x + 560 * s, y), paint("#A8743F"))
        halftone(k, skia.Path().addRect(skia.Rect(x - 560 * s, y - 330 * s, x + 560 * s, y)), "#4A2A10", 0.3)
        k.drawRect(skia.Rect(x - 580 * s, y - 350 * s, x + 580 * s, y - 320 * s), paint("#6B4A2B"))
    cutout(c, d)


def notebook(c, x, y, s, t, lines, p, key="khata"):
    x, y, a = _j(key, t, x, y, 1.5)

    def d(k):
        k.save(); k.rotate(-3 + a * 0.3, x, y)
        k.drawRect(skia.Rect(x - 380 * s, y - 260 * s, x + 380 * s, y + 260 * s), paint("#8E1B1B"))
        k.drawRect(skia.Rect(x - 360 * s, y - 245 * s, x + 360 * s, y + 245 * s), paint("#F6F0DC"))
        for i in range(9):
            k.drawLine(x - 340 * s, y - 170 * s + i * 50 * s, x + 340 * s, y - 170 * s + i * 50 * s, paint("#7FA7C9", 0.6, stroke=2))
        k.drawLine(x - 250 * s, y - 240 * s, x - 250 * s, y + 240 * s, paint("#D9534F", 0.7, stroke=3))
        k.drawLine(x, y - 245 * s, x, y + 245 * s, paint("#000000", 0.25, stroke=4))
        k.restore()
    cutout(c, d)
    n = len(lines)
    for i, ln in enumerate(lines):
        q = clamp((p * n) - i, 0, 1)
        if q > 0:
            type_text(c, ln, x - 140 * s, y - 180 * s + i * 50 * s, 32 * s, q, color="#1F3A93", align="left")


def dabba(c, x, y, s, t, open_p=0.0, key="dabba"):
    x, y, a = _j(key, t, x, y, 1.5)

    def d(k):
        k.drawRRect(rr(x - 160 * s, y - 220 * s, x + 160 * s, y, 30 * s), paint(STEEL))
        lin(k, x - 160 * s, 0, x + 160 * s, 0, ["#8A9098", "#E8ECF0", "#9AA0A8", "#D0D6DC"], [0, 0.35, 0.7, 1],
            rect=skia.Rect(x - 160 * s, y - 220 * s, x + 160 * s, y))
        for yy in (-170, -60):
            k.drawLine(x - 160 * s, y + yy * s, x + 160 * s, y + yy * s, paint("#7A8088", stroke=4 * s))
    if open_p > 0:
        for i in range(4):
            rupee_note(c, x - 40 * s + i * 25 * s, y - 220 * s - 90 * s * ease_out(open_p) + i * 8 * s, 0.55 * s, t,
                       key=f"dn{i}", rot=-20 + i * 14, colr=[NOTE, "#E8A15A", NOTE, "#7FB77E"][i], val=["500", "200", "500", "100"][i])
    cutout(c, d)
    lid_y = y - 230 * s - 160 * s * ease_out(open_p)
    lx = x + 120 * s * ease_out(open_p)

    def lid(k):
        k.save(); k.rotate(25 * ease_out(open_p), lx, lid_y)
        k.drawRRect(rr(lx - 170 * s, lid_y - 25 * s, lx + 170 * s, lid_y + 15 * s, 14 * s), paint("#CBD1D8"))
        k.restore()
    cutout(c, lid, border=6)


def keypad_phone(c, x, y, s, t, key="kp"):
    x, y, a = _j(key, t, x, y, 1.5)

    def d(k):
        k.drawRRect(rr(x - 110 * s, y - 260 * s, x + 110 * s, y + 260 * s, 30 * s), paint("#2E3440"))
        k.drawRect(skia.Rect(x - 80 * s, y - 220 * s, x + 80 * s, y - 60 * s), paint("#9FD8A8"))
        f = font("extrabold", 30 * s); w = text_w("UPI 123PAY", f)
        k.drawString("UPI 123PAY", x - w / 2, y - 130 * s, f, paint("#112233"))
        for i in range(3):
            for j in range(4):
                k.drawRRect(rr(x - 80 * s + i * 56 * s, y - 30 * s + j * 62 * s, x - 34 * s + i * 56 * s, y + 18 * s + j * 62 * s, 10 * s), paint("#C8CDD4"))
    cutout(c, d)


def pie(c, x, y, r, frac, p, t, col1="#C0392B", col2="#E9D8A6", key="pie", split2=None):
    """Paper pie: frac of the circle in col1 (drawn on over p). split2 = (frac_a, col_a) to split the slice in two."""
    x, y, a = _j(key, t, x, y, 2.0)

    def d(k):
        k.drawPath(paper_circle(x, y, r, 5), paint(col2))
        sweep = 360 * frac * ease(p)
        if split2:
            fa, ca = split2
            sa = 360 * fa * ease(p)
            pa = skia.Path(); pa.moveTo(x, y); pa.arcTo(skia.Rect(x - r, y - r, x + r, y + r), -90, sa, False); pa.close()
            k.drawPath(pa, paint(ca)); halftone(k, pa, "#000000", 0.3)
            pb = skia.Path(); pb.moveTo(x, y); pb.arcTo(skia.Rect(x - r, y - r, x + r, y + r), -90 + sa, sweep - sa, False); pb.close()
            k.drawPath(pb, paint(col1)); halftone(k, pb, "#000000", 0.3)
        else:
            pa = skia.Path(); pa.moveTo(x, y); pa.arcTo(skia.Rect(x - r, y - r, x + r, y + r), -90, sweep, False); pa.close()
            k.drawPath(pa, paint(col1)); halftone(k, pa, "#000000", 0.3)
    cutout(c, d)


def headline(c, s, x, y, size, p, seed=2, rot=-2, color="#F4EFE3", ink=INK):
    f = font("extrabold", size)
    w = text_w(s, f)
    torn_strip(c, x, y, w + size * 1.6, size * 1.9, seed=seed, color=color, rot=rot)
    type_text(c, s, x, y, size, p, color=ink)


def stall(c, t, cam_z=1.0):
    """The chai stall: wooden counter, kettle, chai glass, QR sticker. Same framing in the hook and the payoff."""
    collage_bg(c, t)
    # awning
    for i in range(9):
        x0 = i * 220 - 20
        c.drawRect(skia.Rect(x0, 0, x0 + 110, 150), paint("#D9573D"))
        c.drawRect(skia.Rect(x0 + 110, 0, x0 + 220, 150), paint("#F4EFE3"))
    tx, ty, a = _j("counter", t, 0, 0, 1.5)

    def d(k):
        k.drawRect(skia.Rect(-40 + tx, 760 + ty, W + 40, H + 40), paint("#8B5A2B"))
        halftone(k, skia.Path().addRect(skia.Rect(-40, 760, W + 40, H + 40)), "#3A2010", 0.3)
        k.drawRect(skia.Rect(-40 + tx, 740 + ty, W + 40, 775 + ty), paint("#6B3F1D"))
        # kettle
        k.drawRRect(rr(160 + tx, 520 + ty, 400 + tx, 745 + ty, 60), paint(STEEL))
        k.drawLine(400 + tx, 600 + ty, 480 + tx, 540 + ty, paint("#9AA0A8", stroke=22))
        k.drawRect(skia.Rect(250 + tx, 490 + ty, 310 + tx, 520 + ty), paint("#6B7078"))
    cutout(c, d)


def CamC(c, zoom=1.0, cx=W / 2, cy=H / 2, t=0.0):
    """Cam that never shows past the frame edge: the centre is clamped for the current zoom."""
    mx, my = (W / 2) * (1 - 1 / max(zoom, 1.0)), (H / 2) * (1 - 1 / max(zoom, 1.0))
    return Cam(c, zoom, clamp(cx, W / 2 - mx, W / 2 + mx), clamp(cy, H / 2 - my, H / 2 + my), t=t)


def nozzle(c, x, y, s, t, key="nozzle"):
    """Petrol pump nozzle with its hose."""
    x, y, a = _j(key, t, x, y, 2.0)

    def d(k):
        hose = skia.Path(); hose.moveTo(x - 520 * s, y + 420 * s)
        hose.cubicTo(x - 500 * s, y + 100 * s, x - 300 * s, y + 260 * s, x - 150 * s, y + 60 * s)
        k.drawPath(hose, paint("#1E1E24", stroke=44 * s))
        body = skia.Path(); body.moveTo(x - 170 * s, y - 20 * s); body.lineTo(x + 120 * s, y - 120 * s)
        body.lineTo(x + 160 * s, y - 40 * s); body.lineTo(x - 120 * s, y + 90 * s); body.close()
        k.drawPath(body, paint("#E9C46A")); halftone(k, body, "#7A5A10", 0.35)
        k.drawLine(x + 130 * s, y - 90 * s, x + 330 * s, y - 40 * s, paint("#9AA0A6", stroke=34 * s))
        k.drawRRect(rr(x - 110 * s, y + 40 * s, x + 30 * s, y + 90 * s, 20 * s), paint("#2A2A33"))
    cutout(c, d)


def auto(c, x, y, s, t, key="auto"):
    """Auto-rickshaw cut-out (yellow-green), wheels at y + 110 s."""
    x, y, a = _j(key, t, x, y, 2.0)

    def d(k):
        body = skia.Path(); body.moveTo(x - 180 * s, y + 80 * s); body.lineTo(x - 170 * s, y - 60 * s)
        body.quadTo(x - 60 * s, y - 150 * s, x + 120 * s, y - 120 * s); body.lineTo(x + 180 * s, y + 80 * s); body.close()
        k.drawPath(body, paint("#2E7D32"))
        k.drawRect(skia.Rect(x - 175 * s, y - 10 * s, x + 180 * s, y + 80 * s), paint("#F2C230"))
        halftone(k, body, "#000000", 0.25, step=12)
        k.drawRect(skia.Rect(x - 120 * s, y - 100 * s, x + 20 * s, y - 15 * s), paint("#1E1E24", 0.7))
        for wx in (-130, 140):
            k.drawCircle(x + wx * s, y + 100 * s, 38 * s, paint("#1E1E24"))
            k.drawCircle(x + wx * s, y + 100 * s, 14 * s, paint("#9AA0A6"))
    cutout(c, d)
