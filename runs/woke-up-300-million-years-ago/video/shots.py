"""Shot list for the main video. Each shot: (start_time, fn(c, t, t0), transition)."""
import math
import skia
from art import *  # noqa
from timeline import T, B, E, TOTAL
from logo import draw_logo, chapter_card, end_card

# ---------------------------------------------------------------- helpers
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


def corner_gauge(c, t, val=30, alert=False):
    gauge(c, 1770, 150, 95, val, t, True, alert)


def card(value, name):
    def f(c, t, t0):
        chapter_card(c, W, H, value, name, span(t, t0, t0 + 1.4), t)
    return f


# ---------------------------------------------------------------- HOOK
def s_wake(c, t, t0):
    td = T("hook", "dragonfly")
    z = keys(t, [(t0, 1.15), (td + 2, 1.0)])
    with Cam(c, z, W / 2, H / 2, t=t):
        swamp_scene(c, t, cam_x=(t - t0) * 6)
        # blanket in the foreground (you, in bed)
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-100, 880, W + 100, H + 200), 120, 120), paint("teal"))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-100, 880, W + 100, H + 200), 120, 120), paint("#207A6F", stroke=10))
        for i in range(6):
            fp = skia.Path(); fp.moveTo(100 + i * 330, 1080); fp.quadTo(200 + i * 330, 960, 330 + i * 330, 940)
            c.drawPath(fp, paint("#207A6F", 0.9, stroke=8))
        for i in range(30):
            c.drawCircle(60 + (i * 137) % W, 930 + (i * 53) % 140, 6, paint("sand", 0.35))
        # dragonfly lands
        # already sitting on your chest from frame 0; wings twitch, then a slow flutter
        dragonfly(c, 960, 710, 1.7, 0.6 + (t * 0.12 if t < td else t * 0.35), ang=math.sin(t * 0.7) * 3, a=1)
    eye_open(c, keys(t, [(t0, 0.55), (t0 + 0.4, 0.4), (t0 + 1.4, 1.0)]), t)


def s_wings(c, t, t0):
    slide_bg(c, t)
    glow(c, W / 2, H / 2, 800, "teal", 0.18)
    dragonfly(c, W / 2, 500, 1.6, t, ang=0)
    # ghost arm beside the right wing
    a = ease_out(span(t, t0 + 0.4, t0 + 1.2))
    arm = paint("sand", 0.75 * a, stroke=6); arm.setPathEffect(skia.DashPathEffect.Make([18, 12], 0))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(W / 2 + 60, 300, W / 2 + 60 + 400 * a + 1, 360), 30, 30), arm)
    c.drawCircle(W / 2 + 60 + 400 * a + 30, 330, 38 * a + 1, arm)
    if a > 0.5:
        big_text(c, "YOUR ARM", W / 2 + 280, 270, 40, (a - 0.5) * 2, "sand", "bold")
    big_text(c, "~70 cm WINGS", W / 2, 160, 84, span(t, t0 + 0.2, t0 + 0.6), "gold")


def s_spark(c, t, t0):
    ts, tf = T("hook", "spark"), T("hook", "fire")
    with Cam(c, keys(t, [(t0, 1.0), (tf + 1.5, 1.12)]), 900, 700, t=t, shake=4 if t > tf else 0):
        swamp_scene(c, t, cam_x=200)
        if t >= ts - 0.3:
            y = keys(t, [(ts - 0.3, 300), (ts + 0.4, 960)], ease_out)
            glow(c, 900, y, 40, "gold", 0.95)
            c.drawCircle(900, y, 7, paint("gold"))
        if t > ts + 0.4:
            fire_wall(c, 900 + (t - ts - 0.4) * 500, 1010, t, 1.0, 0.55)
    corner_gauge(c, t, keys(t, [(t0, 21), (t0 + 1.0, 30)]), alert=t > tf)


def s_scary(c, t, t0):
    with Cam(c, keys(t, [(t0, 1.0), (t0 + 6, 1.18)]), W / 2, 620, t=t):
        swamp_scene(c, t, night=0.6)
        sx = keys(t, [(t0, 700), (t0 + 6, 1100)])
        millipede(c, sx, 960, 0.9, t, 16, 0.35)  # a hint behind the ferns
        ferns_ground(c, 1010, t, 1.0, seed=3)
    dragonfly(c, keys(t, [(t0, 900), (t0 + 2.5, 2300)]), keys(t, [(t0, 700), (t0 + 2.5, 120)]), 0.9, t, ang=-40)


# ---------------------------------------------------------------- PROMISE
def s_logo(c, t, t0):
    night_sky(c, W, H, t)
    draw_logo(c, W / 2, H / 2, 1.25, span(t, t0, t0 + 2.5), t)
    finish(c, W, H, t)


def s_timebed(c, t, t0):
    slide_bg(c, t)
    glow(c, W / 2, 700, 600, "plum", 0.4)
    # time-machine bed: bed + spinning clock dial on the headboard
    bed(c, W / 2 + 160, 900, 1.4)
    cx, cy = W / 2 - 180, 560
    c.drawCircle(cx, cy, 110, paint("deep")); c.drawCircle(cx, cy, 110, paint("gold", stroke=8))
    ang = -t * 400 if t > T("promise", "pretend") else 0
    c.save(); c.rotate(ang, cx, cy); c.drawLine(cx, cy, cx, cy - 80, paint("cream", stroke=8)); c.restore()
    c.save(); c.rotate(ang * 0.1, cx, cy); c.drawLine(cx, cy, cx + 55, cy, paint("cream", stroke=10)); c.restore()
    draw_kr(c, W / 2 + 420, 860, 1.0, "happy" if t > T("promise", "pretend") else "thinking", t)
    pop(c, W / 2 + 420, 330, "NOT REALLY POSSIBLE", t, T("promise", "nobody") + 0.3, "plum", 36)
    if t > T("promise", "pretend"):
        glow(c, cx, cy, 300, "gold", 0.3 + 0.2 * math.sin(t * 9))


def s_counter(c, t, t0):
    slide_bg(c, t)
    glow(c, W / 2, H / 2, 700, "magenta", 0.3)
    p = span(t, t0, T("promise", "back") + 0.3)
    counter_text(c, 0, 300, p, lambda v: f"−{v:,.0f},000,000 YEARS", W / 2, 560, 104)
    for i in range(14):
        a = (t * 3 + i * 0.6) % (2 * math.pi)
        r = 520 + 30 * math.sin(t + i)
        c.drawCircle(W / 2 + math.cos(a) * r, H / 2 + math.sin(a) * r * 0.5, 5, paint("gold", 0.5))
    if t > T("promise", "before"):
        trex(c, W / 2, 900, 0.7, 0.5)
        xmark(c, W / 2, 780, 1.4, span(t, T("promise", "dinosaurs"), T("promise", "dinosaurs") + 0.5))
        big_text(c, "BEFORE EVEN THE DINOSAURS", W / 2, 200, 56, span(t, T("promise", "before"), T("promise", "before") + 0.4), "sand", "bold")


# ---------------------------------------------------------------- MINUTE 1
def s_breath(c, t, t0):
    with Cam(c, keys(t, [(t0, 1.05), (t0 + 6, 1.0)]), W / 2, H / 2, t=t):
        swamp_scene(c, t, cam_x=-100)
    o2_dots(c, 1100, 900, t, 50, 1.0, ease(span(t, t0 + 0.5, t0 + 1.5)))
    draw_kr(c, 760, 1000, 1.2, "happy" if t > T("minute", "good") else "neutral", t)
    if t > T("minute", "good"):
        big_text(c, "...strangely good", 760, 300, 70, span(t, T("minute", "good"), T("minute", "good") + 0.4), "cream", "serif_italic")
    corner_gauge(c, t, 30)


def jar(c, x, y, frac, label, t, p, color):
    h = 420
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 130, y - h, x + 130, y), 30, 30), paint("deep", 0.8))
    fh = h * frac * ease(p)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 130, y - fh, x + 130, y), 30, 30), paint(color, 0.9))
    for i in range(int(18 * frac * ease(p))):
        c.drawCircle(x - 100 + rng(i) * 200, y - rng(i, 2) * fh, 8, paint("cream", 0.5))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 130, y - h, x + 130, y), 30, 30), paint("cream", stroke=5))
    text(c, label, x, y + 70, font("bold", 44), paint("sand"))


def s_jars(c, t, t0):
    slide_bg(c, t)
    t1, t2 = T("minute", "today"), T("minute", "here")
    jar(c, 620, 820, 0.2, "TODAY", t, span(t, t1, t1 + 0.8), "teal")
    jar(c, 1300, 820, 0.33, "300 MILLION YEARS AGO", t, span(t, t2, t2 + 0.8), "amber")
    if t > t1 + 0.5:
        big_text(c, "1/5", 620, 300, 110, span(t, t1 + 0.5, t1 + 0.9), "teal")
    if t > t2 + 0.5:
        big_text(c, "1/3", 1300, 300, 110, span(t, t2 + 0.5, t2 + 0.9), "gold")
    big_text(c, "OXYGEN IN THE AIR", W / 2, 120, 50, span(t, t0, t0 + 0.4), "cream", "bold")


def s_ok(c, t, t0):
    swamp_scene(c, t, cam_x=-100)
    glow(c, W / 2, 700, 500, "teal", 0.25)
    draw_kr(c, W / 2, 1000, 1.3, "happy", t)
    pop(c, W / 2, 330, "YOUR BODY: OK", t, t0 + 0.3, "teal", 44)
    corner_gauge(c, t, 30)


def s_match(c, t, t0):
    tw = T("minute", "whoosh")
    tl = T("minute", "strike")
    shake = 6 * (1 - span(t, tw, tw + 0.6)) if t > tw else 0
    with Cam(c, keys(t, [(t0, 1.0), (tw, 1.15)]), 900, 600, shake=shake, t=t):
        swamp_scene(c, t, cam_x=-100)
        draw_kr(c, 760, 1000, 1.25, "shocked" if t > tw else "curious", t)
        # match in hand
        c.drawLine(900, 700, 1000, 600, paint("#C9A26A", stroke=10))
        c.drawCircle(1000, 600, 12, paint("coral"))
        if t > tl + 0.4:
            k = 0.4 if t < tw else keys(t, [(tw, 0.4), (tw + 0.4, 3.2)], back_out)
            flame(c, 1000, 600, k, t)
    if t > tw:
        big_text(c, "WHOOSH", 1300, 260, 120, span(t, tw, tw + 0.3), "gold")
    corner_gauge(c, t, 30)


def s_remember(c, t, t0):
    slide_bg(c, t)
    flame(c, W / 2, 760, 3.0, t)
    big_text(c, "Remember this.", W / 2, 260, 84, span(t, t0 + 0.2, t0 + 0.6), "cream", "serif_italic")


# ---------------------------------------------------------------- HOUR 1
def s_spot(c, t, t0):
    with Cam(c, keys(t, [(t0, 1.0), (t0 + 10, 1.08)]), W / 2, H / 2, t=t):
        swamp_scene(c, t, cam_x=(t - t0) * 10, seed=5)
    if t > T("hour1", "spot"):
        big_text(c, "Can you spot it?", W / 2, 180, 70, span(t, T("hour1", "spot"), T("hour1", "spot") + 0.4), "gold", "serif_italic")
    for i, (w, lbl) in enumerate([("flowers", "FLOWERS"), ("grass", "GRASS"), ("birds", "BIRDS")]):
        tt = T("hour1", w)
        if t > tt:
            x = 560 + i * 400
            pop(c, x, 380, lbl, t, tt, "plum", 44)
            xmark(c, x, 380, 1.0, span(t, tt + 0.3, tt + 0.8))
    if t > T("hour1", "none"):
        big_text(c, "NONE OF THEM EXIST YET", W / 2, 560, 56, span(t, T("hour1", "none"), T("hour1", "none") + 0.4), "cream", "bold")


def building(c, x, base, h, a=1.0):
    d = paint("sand", 0.8 * a, stroke=4); d.setPathEffect(skia.DashPathEffect.Make([14, 10], 0))
    c.drawRect(skia.Rect(x - 90, base - h, x + 90, base), d)
    for f in range(10):
        y = base - h + f * h / 10
        c.drawLine(x - 90, y, x + 90, y, paint("sand", 0.35 * a, stroke=2))
        for k in range(3):
            c.drawRect(skia.Rect(x - 70 + k * 50, y + 14, x - 40 + k * 50, y + 40), paint("gold", 0.35 * a))


def s_tall(c, t, t0):
    ts, tt, tn = T("hour1", "scaly"), T("hour1", "tall"), T("hour1", "tenstorey")
    # start close on the scaly bark, then pull back to show the whole 30 m tree
    z = keys(t, [(t0, 2.6), (ts + 1.0, 2.6), (tt + 0.3, 1.0)])
    cy = keys(t, [(t0, 760), (ts + 1.0, 760), (tt + 0.3, 540)])
    with Cam(c, z, keys(t, [(ts + 1.0, 860), (tt + 0.3, W / 2)]), cy, t=t):
        swamp_sky(c, t)
        water(c, 990, t)
        lycopsid(c, 860, 1010, 540, 70, t, 3)
        building(c, 1180, 1010, 900, ease_out(span(t, tt, tt + 0.6)))
        draw_kr(c, 640, 1010, 0.28, "shocked", t)
    if t > ts and t < tt:
        pop(c, 1450, 820, "SCALY, LIKE SNAKE SKIN", t, ts, "plum", 40)
    if t > tt + 0.3:
        big_text(c, "30 m = 10 STOREYS", 1560, 560, 60, span(t, tt + 0.3, tt + 0.7), "gold")


def s_trex(c, t, t0):
    swamp_scene(c, t, cam_x=50)
    x = keys(t, [(t0, -400), (t0 + 0.6, 1000)], back_out)
    trex(c, x, 980, 1.6)
    stamp(c, 1000, 520, "WAY TOO EARLY", span(t, T("hour1", "early"), T("hour1", "early") + 0.4))


def s_timeline(c, t, t0):
    slide_bg(c, t)
    y = 560
    c.drawLine(200, y, 1720, y, paint("sand", stroke=6))
    def mark(x, lbl, sub, colr, p):
        if p <= 0:
            return
        c.drawCircle(x, y, 18 * back_out(p), paint(colr))
        text(c, lbl, x, y - 50, font("extrabold", 52), paint(colr, ease_out(p)))
        text(c, sub, x, y + 80, font("semibold", 36), paint("cream", ease_out(p)))
    mark(380, "YOU", "300 million years ago", "teal", span(t, t0, t0 + 0.4))
    mark(820, "DINOSAURS", "230 million years ago", "gold", span(t, t0 + 0.8, t0 + 1.2))
    mark(1600, "TODAY", "", "cream", span(t, t0 + 1.2, t0 + 1.6))
    p = ease(span(t, T("hour1", "seventy"), T("hour1", "seventy") + 1.0))
    if p > 0:
        arc = skia.Path(); arc.moveTo(380, y - 110); arc.quadTo(600, y - 260, 380 + 440 * p, y - 110 - (0 if p > 0.99 else 0))
        c.drawPath(arc, paint("gold", stroke=6))
        big_text(c, "+70 MILLION YEARS", 600, y - 300, 60, p, "gold")


# ---------------------------------------------------------------- HOUR 3
def s_millipede(c, t, t0):
    tm = T("hour3", "millipede")
    tb = T("hour3", "bed")
    with Cam(c, keys(t, [(t0, 1.2), (tb, 1.0)]), 900, 800, t=t):
        swamp_scene(c, t, cam_x=0, seed=7)
        bed(c, 1150, 880, 1.0)
        hx = keys(t, [(t0, -200), (tm, 500), (tb + 1.0, 1700)])
        millipede(c, hx, 960, 1.05, t, 13)
    if t > tb:
        big_text(c, "LONGER THAN YOUR BED", W / 2, 180, 72, span(t, tb, tb + 0.4), "gold")
        big_text(c, "~2.6 m", W / 2, 270, 52, span(t, tb + 0.3, tb + 0.7), "sand", "bold")


def s_eats(c, t, t0):
    swamp_scene(c, t, cam_x=0, seed=7)
    millipede(c, 1750 + (t - t0) * 30, 900, 0.9, t, 13)
    draw_kr(c, 520, 1000, 1.2, "neutral", t, look=(1, 0.2))
    pop(c, 1150, 520, "EATS PLANTS", t, t0 + 0.3, "teal", 46)
    if t > T("hour3", "probably", 2):
        pop(c, 1150, 620, "(PROBABLY)", t, T("hour3", "probably", 2), "plum", 34)


def ruler(c, x, y, L, p):
    c.drawRect(skia.Rect(x, y, x + L * ease(p), y + 50), paint("amber"))
    for i in range(int(14 * ease(p)) + 1):
        xx = x + i * L / 14
        c.drawLine(xx, y, xx, y + (30 if i % 2 == 0 else 18), paint("deep", stroke=3))


def s_overhead(c, t, t0):
    swamp_scene(c, t, cam_x=80)
    dx = keys(t, [(t0, 2300), (t0 + 1.4, 1100)])
    dy = keys(t, [(t0, 100), (t0 + 1.4, 380)])
    dragonfly(c, dx, dy, 1.1, t, ang=0)
    draw_kr(c, 480, 1000, 1.15, "shocked", t, look=(0.6, -1))
    if t > t0 + 1.4:
        ruler(c, 1100 - 286, 560, 572, span(t, t0 + 1.4, t0 + 2.2))
        big_text(c, "70 cm", 1100, 680, 60, span(t, t0 + 2.0, t0 + 2.4), "gold")
    if t > T("hour3", "hunter"):
        pop(c, 1100, 160, "A HUNTER", t, T("hour3", "hunter"), "coral", 48)


def s_why(c, t, t0):
    slide_bg(c, t)
    glow(c, W / 2, 600, 600, "plum", 0.4)
    draw_kr(c, 640, 980, 1.35, "thinking", t)
    k = back_out(span(t, t0 + 0.2, t0 + 0.6))
    c.save(); c.translate(1200, 520); c.scale(k, k)
    text(c, "?", 0, 120, font("extrabold", 360), paint("gold"))
    c.restore()
    big_text(c, "WHY SO HUGE?", 1200, 900, 70, span(t, t0 + 0.4, t0 + 0.8), "cream")


def bug_body(c, x, y, s, t, o2=0.5, grow=1.0):
    c.save(); c.translate(x, y); c.scale(s * grow, s * grow)
    body = skia.Path(); body.addOval(skia.Rect(-320, -110, 320, 110))
    c.drawPath(body, paint("#3E5E3A", 0.55)); c.drawPath(body, paint("cream", 0.8, stroke=4))
    c.drawCircle(-360, 0, 70, paint("#3E5E3A", 0.55)); c.drawCircle(-360, 0, 70, paint("cream", 0.8, stroke=4))
    for k in range(3):   # legs + antennae so it reads as an insect
        lx = -180 + k * 140
        c.drawLine(lx, 100, lx - 40, 200, paint("cream", 0.7, stroke=6)); c.drawLine(lx - 40, 200, lx - 10, 260, paint("cream", 0.7, stroke=6))
    c.drawLine(-410, -40, -520, -150, paint("cream", 0.7, stroke=5)); c.drawLine(-400, -50, -470, -190, paint("cream", 0.7, stroke=5))
    # spiracles + branching tubes
    for i in range(6):
        sx = -250 + i * 100
        c.drawCircle(sx, -110, 10, paint("gold"))
        for side in (-1, 1):
            p = skia.Path(); p.moveTo(sx, -110)
            p.quadTo(sx + side * 30, -40, sx + side * 50, 20 + 40 * rng(i, side))
            c.drawPath(p, paint("#9FE3E0", 0.85, stroke=6))
            c.drawLine(sx + side * 50, 20 + 40 * rng(i, side), sx + side * 80, 70, paint("#9FE3E0", 0.6, stroke=3))
    # oxygen dots flowing in
    n = int(10 + 50 * o2)
    for i in range(n):
        ph = (t * 0.5 + rng(i)) % 1.0
        sx = -250 + (i % 6) * 100
        depth = 60 + 120 * o2
        c.drawCircle(sx + (rng(i, 3) - 0.5) * 50, -170 + ph * (60 + depth), 7, paint("#9FE3E0", 1 - ph * 0.7))
    c.restore()


def s_tubes(c, t, t0):
    slide_bg(c, t)
    tl = T("hour3", "lungs")
    a = 1 - span(t, T("hour3", "air", 1), T("hour3", "air", 1) + 0.5)
    if a > 0:  # human lungs icon first
        for side in (-1, 1):
            c.drawOval(skia.Rect(W / 2 + side * 60 - 70, 380, W / 2 + side * 60 + 70, 640), paint("coral", 0.7 * a))
        c.drawLine(W / 2, 300, W / 2, 420, paint("coral", a, stroke=14))
        pop(c, W / 2, 760, "LUNGS (YOU)", t, tl, "plum", 40)
    else:
        bug_body(c, W / 2 + 160, 540, 1.8, t, 0.4)
        pop(c, W / 2, 900, "TINY AIR TUBES (BUGS)", t, T("hour3", "air", 1) + 0.5, "teal", 40)


def s_bigger(c, t, t0):
    slide_bg(c, t)
    tm = T("hour3", "more")
    g = keys(t, [(tm, 0.7), (T("hour3", "bigger") + 0.5, 1.15)])
    o2 = keys(t, [(tm, 0.3), (T("hour3", "deeper"), 1.0)])
    bug_body(c, W / 2 + 160, 560, 1.4, t, o2, g)
    gauge(c, 260, 200, 110, keys(t, [(tm, 21), (tm + 1.2, 30)]), t)
    if t > T("hour3", "bigger"):
        big_text(c, "MORE OXYGEN = BIGGER BUGS?", W / 2, 980, 60, span(t, T("hour3", "bigger"), T("hour3", "bigger") + 0.4), "gold")


def s_papers(c, t, t0):
    slide_bg(c, t)
    a1 = ease_out(span(t, t0, t0 + 0.5)); a2 = ease_out(span(t, T("hour3", "fighting") - 0.4, T("hour3", "fighting")))
    paper(c, 640, 560 + (1 - a1) * 300, 1.2, "YES!", "Oxygen = giants", "teal", -4, a1)
    if a2 > 0:
        paper(c, 1280, 560 + (1 - a2) * 300, 1.2, "HMM...", "Not so simple", "coral", 5, a2)
        sh = 8 * math.sin(t * 30) * (1 - span(t, T("hour3", "fighting"), T("hour3", "fighting") + 1))
        big_text(c, "SCIENTISTS STILL ARGUE", W / 2 + sh, 140, 64, a2, "cream")


def s_poll(c, t, t0):
    swamp_scene(c, t, night=0.3)
    millipede(c, 820, 900, 1.0, t, 11)
    dragonfly(c, 1420, 640, 0.9, t, ang=0)
    text(c, "VS", W / 2 + 60, 720, font("extrabold", 120), paint("gold"))
    comment_card(c, W / 2, 180, 1.0, "Giant millipede or giant dragonfly?", span(t, T("hour3", "comments") - 0.6, T("hour3", "comments")), t)


# ---------------------------------------------------------------- NIGHT 1
def s_storm(c, t, t0):
    swamp_scene(c, t, night=0.8)
    clouds(c, 120, t, ease(span(t, t0, t0 + 1.5)))
    rain(c, t, ease(span(t, t0 + 0.5, t0 + 2)))


def s_bolt(c, t, t0):
    tl = T("night", "lightning")
    fl = 1 - span(t, tl + 0.05, tl + 0.5)
    shake = 10 * fl if t > tl else 0
    with Cam(c, 1.0, W / 2, H / 2, shake=shake, t=t):
        swamp_scene(c, t, night=0.8, burn=0.0)
        clouds(c, 120, t)
        rain(c, t)
        if tl - 0.1 < t < tl + 0.6:
            bolt(c, 1000, 0, 400, 3, fl)
        if t > tl + 0.2:
            flame(c, 1000, 420, keys(t, [(tl + 0.2, 0.3), (tl + 2, 1.6)]), t)
    if tl < t < tl + 0.15:
        c.drawRect(skia.Rect(0, 0, W, H), paint("cream", 0.85))


def s_alert(c, t, t0):
    slide_bg(c, t)
    gauge(c, W / 2, 540, 300, 30, t, True, alert=True)
    big_text(c, "REMEMBER?", W / 2, 150, 72, span(t, t0 + 0.2, t0 + 0.6), "coral")


def s_split(c, t, t0):
    # left: our world (wet leaves smoke)
    c.save(); c.clipRect(skia.Rect(0, 0, W / 2, H))
    lin(c, 0, 0, 0, H, ["#1E2A3A", "#2C3A40"])
    for i in range(8):
        c.drawOval(skia.Rect(150 + i * 80, 820, 260 + i * 80, 860), paint("#4E7A3E"))
    for i in range(12):
        ph = (t * 0.3 + rng(i)) % 1
        c.drawCircle(500 + math.sin(t + i) * 40, 800 - ph * 500, 30 + 40 * ph, paint("#8A8A9A", 0.35 * (1 - ph)))
    text(c, "OUR WORLD", W / 4, 160, font("extrabold", 64), paint("cream"))
    text(c, "wet leaves just smoke", W / 4, 240, font("semibold", 40), paint("sand"))
    c.restore()
    c.save(); c.clipRect(skia.Rect(W / 2, 0, W, H))
    lin(c, 0, 0, 0, H, ["#2A0F1A", "#4A1A1A"])
    for i in range(8):
        c.drawOval(skia.Rect(W / 2 + 150 + i * 80, 820, W / 2 + 260 + i * 80, 860), paint("#4E7A3E"))
    if t > T("night", "here"):
        for i in range(7):
            flame(c, W / 2 + 200 + i * 90, 840, 1.2 + 0.4 * rng(i), t, i)
    text(c, "300 MILLION YEARS AGO", W * 0.75, 160, font("extrabold", 56), paint("gold"))
    text(c, "damp plants keep burning", W * 0.75, 240, font("semibold", 40), paint("sand"))
    c.restore()
    c.drawLine(W / 2, 0, W / 2, H, paint("cream", stroke=4))


def s_runs(c, t, t0):
    tr = T("night", "runs")
    front = keys(t, [(t0, 200), (tr, 700), (tr + 3, 2200)])
    with Cam(c, 1.0, W / 2, H / 2, shake=3, t=t):
        swamp_scene(c, t, night=0.75, burn=1.0)
        fire_wall(c, front, 1000, t, 1.0, 1.4)
        kx = keys(t, [(t0, 1300), (tr + 3, 1750)])
        draw_kr(c, kx, 1000, 1.1, "worried", t, look=(-1, 0), flip=True)
    if t > tr:
        big_text(c, "IT RUNS.", W / 2, 200, 120, span(t, tr, tr + 0.3), "coral")


def s_coal(c, t, t0):
    slide_bg(c, t)
    coal_seam(c, 260, 300, 1400, 520, t, ease(span(t, t0, t0 + 1.2)))
    tb = T("night", "burnt")
    if t > tb - 0.3:
        p = ease(span(t, tb - 0.3, tb + 0.4))
        cx, cy = 1100, 560
        c.save(); clip = skia.Path(); clip.addCircle(cx, cy, 200 * p); c.clipPath(clip, doAntiAlias=True)
        c.drawRect(skia.Rect(0, 0, W, H), paint("#0E0B0A"))
        for i in range(40):
            x = cx - 200 + rng(i) * 400; y = cy - 200 + rng(i, 2) * 400
            c.drawRect(skia.Rect(x, y, x + 30, y + 10), paint("#4A4440"))
            c.drawLine(x, y + 5, x + 30, y + 5, paint("#6A6460", stroke=2))
        c.restore()
        c.drawCircle(cx, cy, 200 * p, paint("gold", stroke=10))
        c.drawLine(cx + 140 * p, cy + 140 * p, cx + 260 * p, cy + 260 * p, paint("gold", stroke=22))
        pop(c, 1100, 900, "TINY BITS OF BURNT WOOD", t, tb + 0.3, "plum", 40)
    if t > T("night", "again", 1):
        big_text(c, "FIRES, AGAIN AND AGAIN", W / 2, 180, 60, span(t, T("night", "again", 1), T("night", "again", 1) + 0.4), "coral")


def s_air(c, t, t0):
    swamp_scene(c, t, night=0.85, burn=1.0)
    fire_wall(c, 2000, 1020, t, 0.6, 0.9)
    gauge(c, W / 2, 470, 230, 30, t, True, alert=True)
    if t > T("night", "air"):
        big_text(c, "IT'S THE AIR.", W / 2, 160, 96, span(t, T("night", "air"), T("night", "air") + 0.3), "cream")


# ---------------------------------------------------------------- YEAR 1
def s_globe(c, t, t0):
    slide_bg(c, t)
    tc = T("year", "crashing")
    merge = span(t, tc, T("year", "piece") + 0.3)
    globe(c, W / 2, 540, 380, t, ice=0.0, india=0.0, merge=merge)
    if t > T("year", "where"):
        pop(c, W / 2, 110, "INDIA IS NOT WHERE YOU LEFT IT", t, T("year", "where"), "plum", 40)
    if t > T("year", "piece"):
        big_text(c, "ONE GIANT PIECE", W / 2, 1010, 56, span(t, T("year", "piece"), T("year", "piece") + 0.4), "gold")


def s_ice(c, t, t0):
    slide_bg(c, t)
    ti = T("year", "ice")
    with Cam(c, keys(t, [(t0, 1.0), (ti + 1, 1.3)]), W / 2, keys(t, [(t0, 540), (ti + 1, 680)]), t=t):
        globe(c, W / 2, 540, 380, t, ice=ease(span(t, ti - 0.5, ti + 0.8)), india=ease(span(t, t0, t0 + 0.6)), merge=1)
    if t > T("year", "south"):
        pop(c, W / 2, 110, "FAR DOWN SOUTH", t, T("year", "south"), "teal", 44)
    if t > ti:
        big_text(c, "UNDER THICK ICE", W / 2, 1000, 64, span(t, ti, ti + 0.4), "cream")


def s_odisha(c, t, t0):
    tb = T("year", "boulders")
    if t < tb:
        slide_bg(c, t)
        P = india_map(c, W / 2, 560, 28)
        ox, oy = P(84.5, 20.6)
        pin = back_out(span(t, T("year", "odisha"), T("year", "odisha") + 0.4))
        if pin > 0:
            c.drawCircle(ox, oy - 40 * pin, 22 * pin, paint("coral"))
            c.drawLine(ox, oy, ox, oy - 30 * pin, paint("coral", stroke=6))
            pill(c, ox + 180, oy - 60, 1.0, "ODISHA", "coral", "cream", 38)
    else:
        lin(c, 0, 0, 0, H, ["#6A88A8", "#C9D8E0"])
        c.drawRect(skia.Rect(0, 760, W, H), paint("#7A6A50"))
        glacier(c, 0.35, t, 160)
        boulders(c, W / 2, 900, 2.0, t)
        pop(c, W / 2, 140, "CARRIED BY MOVING ICE", t, tb + 0.2, "teal", 46)


def s_contrast(c, t, t0):
    c.save(); c.clipRect(skia.Rect(0, 0, W / 2, H))
    swamp_scene(c, t)
    text(c, "MIDDLE OF THE EARTH", W / 4, 120, font("extrabold", 50), paint("gold"))
    c.restore()
    c.save(); c.clipRect(skia.Rect(W / 2, 0, W, H))
    lin(c, 0, 0, 0, H, ["#4A6A8A", "#DDEFF4"])
    c.save(); c.translate(W / 2 + 480, 0)
    india_map(c, 0, 600, 17, ice=ease(span(t, T("year", "frozen") - 0.5, T("year", "frozen") + 0.3)))
    c.restore()
    text(c, "INDIA", W * 0.75, 120, font("extrabold", 50), paint("space"))
    c.restore()
    c.drawLine(W / 2, 0, W / 2, H, paint("cream", stroke=4))
    if t > T("year", "frozen"):
        big_text(c, "FROZEN", W * 0.75, 1000, 80, span(t, T("year", "frozen"), T("year", "frozen") + 0.3), "space")


# ---------------------------------------------------------------- TWIST
def s_fall(c, t, t0):
    tf = T("twist", "die")
    ang = keys(t, [(tf, 0), (tf + 1.5, 70)], lambda v: v * v)
    swamp_sky(c, t)
    water(c, 820, t)
    c.save(); c.rotate(ang, 1000, 900)
    lycopsid(c, 1000, 900, 700, 70, t, 5)
    c.restore()
    if t > T("twist", "rot"):
        stamp(c, W / 2, 260, "DOESN'T ROT", span(t, T("twist", "rot"), T("twist", "rot") + 0.4), "gold", -6)
    big_text(c, "Why so much oxygen?", W / 2, 120, 60, 1 - span(t, tf, tf + 0.4), "cream", "serif_italic")


def s_bury(c, t, t0):
    slide_bg(c, t)
    tb, tq = T("twist", "buried"), T("twist", "squeezed")
    nl = int(1 + 6 * span(t, T("twist", "fall"), tq))
    for i in range(nl):
        y = 900 - i * 70
        c.drawRect(skia.Rect(260, y - 70, 1660, y), paint(["#5A4A32", "#3A3A2A", "#4A3C2E", "#2E2620"][i % 4]))
        if i == 0:
            for k in range(5):
                c.drawLine(300 + k * 270, y - 35, 520 + k * 270, y - 40, paint("#7A6644", stroke=14))
    p = span(t, tq, tq + 1.5)
    if p > 0:
        coal_seam(c, 260, 900 - 140 * (1 - p * 0.4), 1400, 140, t)
        pop(c, W / 2, 140, "SQUEEZED INTO COAL", t, tq, "plum", 48)
    if t > T("twist", "millions"):
        big_text(c, "MILLIONS OF YEARS", W / 2, 260, 52, span(t, T("twist", "millions"), T("twist", "millions") + 0.3), "gold", "bold")


def s_why2(c, t, t0):
    slide_bg(c, t)
    a1 = ease_out(span(t, T("twist", "maybe", 1) - 0.2, T("twist", "maybe", 1) + 0.3))
    a2 = ease_out(span(t, T("twist", "maybe", 2) - 0.2, T("twist", "maybe", 2) + 0.3))
    big_text(c, "Why didn't they rot?", W / 2, 140, 66, span(t, t0, t0 + 0.4), "cream", "serif_italic")
    if a1 > 0:
        paper(c, 640, 600 + (1 - a1) * 300, 1.1, "FUNGI?", "Wood-eaters not ready", "teal", -4, a1)
    if a2 > 0:
        paper(c, 1280, 600 + (1 - a2) * 300, 1.1, "TOO WET?", "Swamps everywhere", "plum", 4, a2)


def s_pump(c, t, t0):
    slide_bg(c, t)
    coal_seam(c, 0, 820, W, 260, t)
    o2_dots(c, W / 2, 820, t, 70, 1.0, ease(span(t, t0, t0 + 1)))
    gauge(c, W / 2, 380, 220, keys(t, [(t0, 21), (t0 + 2.5, 30)]), t)


# ---------------------------------------------------------------- PAYOFF
COAL_STATES = ("Jharkhand", "Odisha", "Chhattisgarh", "West Bengal", "Telangana", "Madhya Pradesh", "Maharashtra")


def s_coalmap(c, t, t0):
    slide_bg(c, t)
    ha = ease(span(t, T("payoff", "coal") - 0.6, T("payoff", "coal") + 0.4))
    india_map(c, W / 2, 560, 28, highlight=COAL_STATES, hcol="#2A2420", ha=ha)
    if ha > 0.5:
        pop(c, 1500, 560, "INDIA'S COAL", t, T("payoff", "coal"), "plum", 48)


def bulb(c, x, y, on, t, coal=True):
    if on:
        glow(c, x, y, 140, "gold", 0.6)
    c.drawCircle(x, y, 70, paint("gold" if on else "#4A4458"))
    c.drawRect(skia.Rect(x - 36, y + 60, x + 36, y + 110), paint("#9A8E78"))
    if on and coal:
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 24, y + 140, x + 24, y + 180), 8, 8), paint("#2A2420"))


def s_units(c, t, t0):
    slide_bg(c, t)
    for i in range(4):
        on = i < 3 and t > T("payoff", "three") + 0.25 * i
        bulb(c, 480 + i * 320, 520, on, t, coal=True)
    if t > T("payoff", "coal", 2):
        big_text(c, "3 OUT OF 4 UNITS = COAL", W / 2, 900, 70, span(t, T("payoff", "coal", 2), T("payoff", "coal", 2) + 0.4), "gold")


def s_switch(c, t, t0):
    ts = T("payoff", "switch")
    room(c, t, 1.0 if t > ts else 0.2)
    if t <= ts:
        c.drawRect(skia.Rect(0, 0, W, H), paint("#05030C", 0.55))
    switch(c, 1100, 520, 1.6, 1.0 if t > ts else 0.0, t)
    draw_kr(c, 560, 1000, 1.25, "pointing" if t > ts else "curious", t)
    if t > ts:
        # the forest glowing inside the wire
        a = ease(span(t, ts, ts + 0.8))
        c.drawLine(1100, 740, 1100, 1080, paint("gold", a, stroke=16))
        glow(c, 1100, 900, 220, "gold", 0.45 * a)
        c.save(); c.translate(1100, 960); c.scale(0.18, 0.18)
        for i in range(3):
            lycopsid(c, -300 + i * 300, 0, 800, 70, t, i)
        c.restore()
        big_text(c, "IT'S IN YOUR LIGHT SWITCH", W / 2, 150, 66, span(t, ts, ts + 0.4), "gold")


def s_chimney(c, t, t0):
    slide_bg(c, t)
    c.drawRect(skia.Rect(0, 860, W, H), paint("#1A1424"))
    for x in (700, 1000):
        c.drawRect(skia.Rect(x - 60, 420, x + 60, 860), paint("#4A4458"))
        c.drawRect(skia.Rect(x - 60, 460, x + 60, 490), paint("coral", 0.7))
        carbon_dots(c, x, 420, t, 30, 0.8, ease(span(t, t0, t0 + 1)))
    big_text(c, "CARBON GOES BACK INTO THE SKY", W / 2, 150, 60, span(t, T("payoff", "carbon") - 0.2, T("payoff", "carbon") + 0.2), "cream")
    if t > T("payoff", "happening"):
        pop(c, W / 2, 260, "HAPPENING RIGHT NOW", t, T("payoff", "happening"), "coral", 44)


def s_bring(c, t, t0):
    swamp_scene(c, t, cam_x=40)
    draw_kr(c, 1500, 1000, 1.2, "happy", t)
    comment_card(c, W / 2 - 180, 300, 1.0, "What would you bring back?", span(t, t0 + 0.2, t0 + 0.8), t)


def s_room(c, t, t0):
    room(c, t)
    bed(c, 700, 1000, 1.6, blanket="teal")
    fan(c, W / 2, 200, 1.2, t, 5)
    if t > T("payoff", "forest"):
        a = ease(span(t, T("payoff", "forest"), T("payoff", "forest") + 1))
        glow(c, W / 2, 200, 260, "#9FE3A0", 0.35 * a)
        big_text(c, "a forest, 300 million years old", W / 2, 620, 60, a, "cream", "serif_italic")
    eye_open(c, span(t, t0, t0 + 1.4), t)


def s_tease(c, t, t0):
    lin(c, 0, 0, 0, H, ["#C98A4A", "#E9C88A"])
    glow(c, W * 0.75, 260, 300, "gold", 0.7)
    c.drawRect(skia.Rect(0, 640, W, H), paint("#9A6A3A"))
    for i in range(40):
        x = rng(i) * W; y = 660 + rng(i, 2) * 420
        c.drawLine(x, y, x + 90 * (rng(i, 3) - 0.5) * 2, y + 50, paint("#5A3A1A", stroke=4))
    big_text(c, "NEXT: NO MONSOON FOR A WHOLE YEAR?", W / 2, 260, 64, span(t, t0 + 0.3, t0 + 0.8), "space")


def s_end(c, t, t0):
    end_card(c, W, H, span(t, t0, t0 + 2.0), t)


# ---------------------------------------------------------------- the list
def SHOTS():
    L = [
        (0.0, s_wake, "cut"),
        (T("hook", "wings") - 0.2, s_wings, "fade"),
        (T("hook", "outside") - 0.2, s_spark, "fade"),
        (T("hook", "scariest") - 0.3, s_scary, "fade"),
        (E("hook") + 0.1, s_logo, "flash"),
        (T("promise", "nobody") - 0.3, s_timebed, "iris"),
        (T("promise", "three") - 0.3, s_counter, "zoom"),
        (B("minute") - 0.6, card("MINUTE 1", "The air"), "iris"),
        (T("minute", "you", 1) - 0.1, s_breath, "fade"),
        (T("minute", "today") - 0.3, s_jars, "fade"),
        (T("minute", "dont") - 0.2, s_ok, "fade"),
        (T("minute", "fire") - 0.2, s_match, "whip"),
        (T("minute", "remember") - 0.2, s_remember, "fade"),
        (B("hour1") - 0.6, card("HOUR 1", "The forest"), "iris"),
        (T("hour1", "you", 1) - 0.2, s_spot, "fade"),
        (T("hour1", "trees") - 0.2, s_tall, "fade"),
        (T("hour1", "dinosaurs") - 0.2, s_trex, "whip"),
        (T("hour1", "first") - 0.2, s_timeline, "fade"),
        (B("hour3") - 0.6, card("HOUR 3", "The giants"), "iris"),
        (T("hour3", "something") - 0.2, s_millipede, "fade"),
        (T("hour3", "good") - 0.2, s_eats, "fade"),
        (T("hour3", "above") - 0.2, s_overhead, "whip"),
        (T("hour3", "so", 1) - 0.2, s_why, "fade"),
        (T("hour3", "heres") - 0.2, s_tubes, "zoom"),
        (T("hour3", "more") - 0.2, s_bigger, "fade"),
        (T("hour3", "least") - 0.6, s_papers, "fade"),
        (T("hour3", "quick") - 0.2, s_poll, "fade"),
        (B("night") - 0.3, card("NIGHT 1", "The fire"), "cut"),
        (T("night", "clouds") - 0.2, s_storm, "fade"),
        (T("night", "lightning") - 0.6, s_bolt, "cut"),
        (T("night", "now") - 0.2, s_alert, "zoom"),
        (T("night", "our") - 0.2, s_split, "fade"),
        (T("night", "fire") - 0.3, s_runs, "whip"),
        (T("night", "and", 1) - 0.2, s_coal, "fade"),
        (T("night", "so") - 0.2, s_air, "fade"),
        (B("year") - 0.6, card("YEAR 1", "Where is India?"), "iris"),
        (T("year", "but") - 0.2, s_globe, "fade"),
        (T("year", "india", 3) - 0.3, s_ice, "zoom"),
        (T("year", "proof") - 0.2, s_odisha, "fade"),
        (T("year", "middle") - 0.6, s_contrast, "fade"),
        (B("twist") - 0.6, card("TODAY", "300 million years later · The twist"), "iris"),
        (T("twist", "because") - 0.2, s_fall, "fade"),
        (T("twist", "fall") - 0.2, s_bury, "fade"),
        (T("twist", "why", 2) - 0.2, s_why2, "fade"),
        (T("twist", "either") - 0.2, s_pump, "fade"),
        (B("payoff") - 0.3, s_coalmap, "zoom"),
        (T("payoff", "today") - 0.2, s_units, "fade"),
        (T("payoff", "so", 1) - 0.2, s_switch, "fade"),
        (T("payoff", "every", 2) - 0.2, s_chimney, "fade"),
        (T("payoff", "if") - 0.2, s_bring, "fade"),
        (T("payoff", "wake") - 0.3, s_room, "cut"),
        (T("payoff", "next") - 0.2, s_tease, "cut"),
        (E("payoff") + 0.3, s_end, "fade"),
    ]
    return L


TRANS = {"cut": 0.0, "fade": 0.35, "iris": 0.5, "zoom": 0.4, "whip": 0.3, "flash": 0.25}


def render_frame(c, t, shots=None):
    shots = shots or SHOTS()
    idx = max(i for i, s in enumerate(shots) if s[0] <= t or i == 0)
    st, fn, tr = shots[idx]
    d = TRANS[tr]
    p = span(t, st, st + d) if d else 1.0
    if p < 1 and idx > 0:
        pst, pfn, _ = shots[idx - 1]
        pfn(c, t, pst)
        if tr == "iris":
            c.save(); clip = skia.Path(); clip.addCircle(W / 2, H / 2, ease(p) * 1150); c.clipPath(clip, doAntiAlias=True)
            fn(c, t, st); c.restore()
        elif tr == "flash":
            fn(c, t, st); c.drawRect(skia.Rect(0, 0, W, H), paint("cream", 1 - p))
        elif tr == "whip":
            c.saveLayerAlpha(None, int(255 * ease(p))); c.translate((1 - ease(p)) * 300, 0); fn(c, t, st); c.restore()
        elif tr == "zoom":
            c.saveLayerAlpha(None, int(255 * ease(p))); k = 1.25 - 0.25 * ease(p)
            c.translate(W / 2, H / 2); c.scale(k, k); c.translate(-W / 2, -H / 2); fn(c, t, st); c.restore()
        else:
            c.saveLayerAlpha(None, int(255 * ease(p))); fn(c, t, st); c.restore()
    else:
        fn(c, t, st)
    finish(c, W, H, t)
    return shots[idx]
