"""Shot list for 'What If India's Population Started Shrinking?' (style: collage).
Each shot: (start_time, fn(c, t, t0), transition). Times are anchored to words with T / at / B / E."""
import math
import skia
from art import *  # noqa: F401,F403

KER, CLS, FIF, SIX = "kerala", "classroom", "fifty", "sixties"


def cont(fn, start, z1=1.18, cx=960.0, cy=540.0, dur=6):
    """Continue a shot (its own clock keeps running from `start`) with a push-in: a new framing, not a restart."""
    return zoom(lambda c, t, t0: fn(c, t, start), 1.0 + (z1 - 1.0) * 0.6, z1, cx, cy, dur)


# ---------------------------------------------------------------- HOOK
def photos(c, t, t0, beat="hook"):
    """The family-photo thread: sepia (6 kids) -> today (2 kids, one peels away). Same framing in the payoff."""
    collage_bg(c, t)
    ty = T(beat, "yours")
    mv = ease(span(t, ty - 0.3, ty + 0.5))
    family_photo(c, 960 - 500 * mv, 600 - 40 * mv, 1.35 - 0.6 * mv, t, 2, 6, sepia=True, key="old", rot=-3)
    marker_circle(c, 960 - 500 * mv, 760 - 110 * mv, 520 - 230 * mv, 120 - 50 * mv, 1.0 if beat == "hook" else span(t, t0, t0 + 0.6))
    headline(c, "NANI'S FAMILY: 6 KIDS", 960 - 500 * mv, 110 + 10 * mv, 64 - 20 * mv, 1.0, seed=3)
    if t > ty - 0.2:
        peel = ease(span(t, T(beat, "one") - 0.1, T(beat, "one") + 0.6)) if beat == "hook" else 0.0
        family_photo(c, 1400, 540, 0.85, t, 2, 2, key="new", rot=4, p=span(t, ty - 0.2, ty + 0.3), peel=peel)
        headline(c, "YOURS: 2 KIDS", 1400, 130, 50, span(t, ty, ty + 0.5), seed=5, rot=2)
        q = span(t, ty + 0.3, ty + 0.8)
        if q > 0:
            headline(c, "6 KIDS > 2" + ("  > 1?" if beat == "hook" and t > T(beat, "one") else ""), W / 2, 980, 72, 1.0, seed=7, color="#FFF3C4", ink=RED_INK)


def s_cold(c, t, t0):
    photos(c, t, t0, "hook")


def s_shrink(c, t, t0):
    collage_bg(c, t)
    p = ease(span(t, T("hook", "shrink") - 0.6, T("hook", "shrink") + 0.8))
    k = 30 - 5 * p
    P = india_map(c, 760, 580, k)
    for i in range(90):
        if rng(i, 9) < 0.35 * p:
            continue
        x = 760 + (rng(i, 2) - 0.5) * k * 18
        y = 580 + (rng(i, 3) - 0.5) * k * 20
        c.drawCircle(x, y, 7, paint(INK, 0.55))
    dx, dy = P(77.1, 28.6)
    pop(c, dx + 90, dy - 10, "DELHI 1.2", t, t0 + 0.2, color="teal", size=26)   # the twist's object, quietly early
    headline(c, "INDIA STARTS TO SHRINK", 1420, 380, 60, span(t, t0, T("hook", "shrink") + 0.2), seed=4, rot=3)
    ts = T("hook", "shrink")
    stamp(c, 1420, 640, "SHRINKING", span(t, ts - 0.1, ts + 0.15), color="coral", rot=-8)


def s_where(c, t, t0):
    collage_bg(c, t)
    c.saveLayer(None, skia.Paint(ColorFilter=skia.ColorFilters.Blend(col("#2B2420", 0.92), skia.BlendMode.kSrcATop)))
    desk_row(c, 960, 700, 1.0, t, 12, 0, key="hd")
    c.restore()
    person(c, 1500, 900, 0.9, t, key="lonekid", i=3, child=True, female=True)
    glow(c, 1500, 820, 160, "gold", 0.45)
    stamp(c, 820, 520, "?", span(t, T("hook", "first") - 0.1, T("hook", "first") + 0.2), color="coral", rot=-6)
    headline(c, "WHERE'D THEY GO?", W / 2, 150, 64, span(t, t0, t0 + 0.6), seed=9)


# ---------------------------------------------------------------- PROMISE
def s_predict(c, t, t0):
    collage_bg(c, t)
    headline(c, "THE EASIEST FUTURE TO PREDICT", W / 2, 400, 70, span(t, t0, t0 + 1.2), seed=12)
    stamp(c, W / 2, 680, "NOT FANTASY", span(t, T("promise", "fantasy") - 0.1, T("promise", "fantasy") + 0.15), color="coral", rot=-8)
    kr_cutout(c, lambda k: draw_kr(k, 1600, 950, 1.0, "pointing", t))


def s_born(c, t, t0):
    collage_bg(c, t)
    for i in range(7):
        x = 260 + i * 200
        q = ease_out(span(t, t0 + i * 0.12, t0 + 0.4 + i * 0.12))
        if q > 0:
            xx, yy, a = jit(f"bb{i}", t)
            cutout(c, lambda k, x=x + xx, q=q, i=i: baby(k, x, 760, 1.4 * q + 0.01, i), border=6, shadow=(4, 6))
    torn_strip(c, 760, 960, 520, 90, seed=31, color="#F4EFE3")
    type_text(c, "BORN 1990", 760, 960, 52)
    dx, dy, a = jit("tag60", t)
    index_card(c, 1600 + dx, 380 + dy, 420, 240, rot=5, seed=33)
    type_text(c, "2050", 1600 + dx, 340 + dy, 72, span(t, T("promise", "sixty") - 0.2, T("promise", "sixty") + 0.3), color=RED_INK)
    type_text(c, "AGE 60", 1600 + dx, 430 + dy, 56, span(t, T("promise", "sixty"), T("promise", "sixty") + 0.4))
    red_string(c, [(860, 700), (1180, 560), (1420, 420)], span(t, T("promise", "sixty"), T("promise", "fifty") + 0.4))
    stamp(c, 1000, 380, "ALREADY BORN", span(t, T("promise", "born") - 0.1, T("promise", "born") + 0.15), color="coral", rot=-10)


# ---------------------------------------------------------------- TODAY
def s_21(c, t, t0):
    collage_bg(c, t)
    dx, dy, a = jit("c21", t)
    index_card(c, 620 + dx, 520 + dy, 640, 520, rot=-3, seed=40)
    type_text(c, "2.1", 620 + dx, 520 + dy, 230, span(t, T("today", "two") - 0.3, T("today", "two") + 0.2), color=RED_INK)
    type_text(c, "THE MAGIC NUMBER", 620 + dx, 720 + dy, 44, span(t, t0, t0 + 0.6))
    tc = T("today", "thats")
    if t > tc - 0.2:
        person(c, 1380, 560, 0.9, t, key="mum", i=1, female=True)
        person(c, 1620, 560, 0.9, t, key="dad", i=2)
        headline(c, "SAME SIZE", 1500, 960, 54, span(t, T("today", "same") - 0.3, T("today", "size") + 0.2), seed=41)


def s_replace(c, t, t0):
    collage_bg(c, t)
    person(c, 640, 520, 0.95, t, key="mum2", i=1, female=True)
    person(c, 880, 520, 0.95, t, key="dad2", i=2)
    for j in range(2):
        q = span(t, T("today", "replace") - 0.2 + j * 0.25, T("today", "replace") + 0.2 + j * 0.25)
        if q > 0:
            person(c, 640 + j * 240, 980, 0.95, t, key=f"kid{j}", i=j + 4, child=True, female=j == 0)
            marker_line(c, [(640 + j * 240, 560), (640 + j * 240, 680)], q, width=8)
    ex = T("today", "extra")
    dx, dy, a = jit("ext", t)
    if t > ex - 0.2:
        index_card(c, 1420 + dx, 600 + dy, 380, 300, rot=6, seed=43)
        type_text(c, "+ 0.1", 1420 + dx, 580 + dy, 110, span(t, ex - 0.2, ex + 0.3), color=RED_INK)
        type_text(c, "a little extra", 1420 + dx, 700 + dy, 36, span(t, ex, ex + 0.6))
    headline(c, "2 KIDS = MUM + DAD", 760, 130, 56, span(t, T("today", "replace") - 0.4, T("today", "dad") + 0.3), seed=44)


def s_19(c, t, t0):
    collage_bg(c, t)
    y21 = 430
    marker_line(c, [(160, y21), (1760, y21)], span(t, t0, t0 + 0.6), color=RED_INK, width=12)
    headline(c, "2.1 = REPLACEMENT LINE", 520, y21 - 90, 42, span(t, t0 + 0.2, t0 + 0.8), seed=46)
    tn = T("today", "one", 2)
    fall = ease(span(t, tn - 0.2, tn + 0.6))
    dx, dy, a = jit("c19", t)
    cy = 280 + 380 * fall
    index_card(c, 1100 + dx, cy + dy, 640, 250, rot=-4 + 6 * fall, seed=45)
    type_text(c, "INDIA 1.9", 1100 + dx, cy + dy, 104, 1.0, color=RED_INK)
    tb = T("today", "below")
    for i, yr in enumerate(["2020", "2021", "2022", "2023", "2024"]):
        q = ease_out(span(t, T("today", "five") - 0.2 + i * 0.15, T("today", "five") + 0.1 + i * 0.15))
        if q > 0:
            x = 360 + i * 300
            torn_strip(c, x, 960, 220 * q + 1, 80, seed=50 + i, color="#F4EFE3")
            type_text(c, yr, x, 960, 44 * q + 1, 1.0, color=RED_INK)
    stamp(c, 480, 700, "BELOW THE LINE", span(t, tb - 0.1, tb + 0.15), color="coral", rot=-8)


def s_myth(c, t, t0):
    collage_bg(c, t)
    dx, dy, a = jit("myth", t)
    index_card(c, 680 + dx, 500 + dy, 900, 440, rot=-3, seed=47)
    type_text(c, "\"INDIA IS ALREADY", 680 + dx, 440 + dy, 64, span(t, t0, t0 + 0.6))
    type_text(c, "SHRINKING\"", 680 + dx, 540 + dy, 74, span(t, t0 + 0.4, t0 + 0.9))
    tn = T("today", "its", 1)
    stamp(c, 680, 650, "MYTH", span(t, tn - 0.1, tn + 0.15), color="coral", rot=-12)
    kr_cutout(c, lambda k: draw_kr(k, 1500, 900, 1.3, "pointing", t))
    tg = T("today", "growing")
    if t > tg - 0.4:
        headline(c, "STILL GROWING", 1500, 300, 56, span(t, tg - 0.4, tg + 0.2), seed=48, color="#E5F4E4")


def s_train(c, t, t0):
    collage_bg(c, t, tint="#EFE6D2")
    br = span(t, T("today", "brakes") - 0.2, T("today", "brakes") + 0.3)
    train(c, 700, 1.0, t, t0, brake=br)
    if t < T("today", "brakes") - 0.4:
        headline(c, "INDIA = A VERY LONG TRAIN", W / 2, 170, 62, span(t, t0, t0 + 0.8), seed=50)
    else:
        headline(c, "BRAKES ON. STILL ROLLING.", W / 2, 170, 62, span(t, T("today", "brakes") - 0.4, T("today", "rolling") + 0.2), seed=51)
    # speed gauge cut-out
    gx, gy = 1640, 980
    cutout(c, lambda k: k.drawPath(paper_circle(gx, gy - 40, 120, 21), paint("#F4EFE3")))
    ang = math.radians(200 + 140 * (1 - 0.5 * br))
    c.drawLine(gx, gy - 40, gx + 95 * math.cos(ang), gy - 40 + 95 * math.sin(ang), paint(RED_INK, stroke=10))
    type_text(c, "SPEED", gx, gy + 40, 30, 1.0)


def s_long(c, t, t0):
    collage_bg(c, t, tint="#EFE6D2")
    z = keys(t, [(t0, 1.0), (t0 + 2.5, 0.62)])
    with Cam(c, z, W / 2, H / 2, t=t):
        train(c, 640, 1.0, t, t0 - 30, brake=1.0, cars=24, speed=300)
    kr_cutout(c, lambda k: draw_kr(k, 1660, 1000, 0.9, "thinking", t))
    headline(c, "VERY, VERY LONG", W / 2, 150, 60, span(t, T("today", "long") - 0.5, T("today", "long") + 0.3), seed=52)


# ---------------------------------------------------------------- 2036 KERALA
def s_kerala(c, t, t0):
    collage_bg(c, t)
    z = keys(t, [(t0, 1.0), (t0 + 1.4, 1.9)])
    with Cam(c, z, 760, 860, t=t):
        india_map(c, 960, 560, 28, highlight=("Kerala",), hcol="#C0392B")
    for i in range(5):
        x = 1260 + i * 120
        old = i == 4 and t > T(KER, "sixty") - 0.2
        person(c, x, 820, 0.7, t, key=f"k5{i}", i=i, old=old, female=i % 2 == 0)
    tm = T(KER, "more")
    headline(c, "MORE THAN 1 IN 5", 1500, 300, 52, span(t, tm - 0.2, tm + 0.6), seed=55)
    pop(c, 1740, 420, "60+", t, T(KER, "sixty") - 0.1, color="coral", size=46)


def s_house(c, t, t0):
    collage_bg(c, t, tint="#E8EEDF")
    kerala_house(c, 900, 860, 1.25, t, locks=3 * span(t, T(KER, "three") - 0.2, T(KER, "locked") + 0.2))
    person(c, 1580, 900, 1.0, t, key="gma", i=1, old=True, female=True, cloth="#E9A23B")
    pop(c, 900, 160, "4 BEDROOMS", t, T(KER, "four") - 0.1, color="teal", size=48)


def s_strings(c, t, t0):
    collage_bg(c, t, tint="#E8EEDF")
    kerala_house(c, 520, 900, 0.8, t, locks=3)
    person(c, 920, 920, 0.8, t, key="gma2", i=1, old=True, female=True, cloth="#E9A23B")
    for i, (lab, y, w) in enumerate([("DUBAI", 300, T(KER, "dubai")), ("BENGALURU", 640, T(KER, "bengaluru"))]):
        dx, dy, a = jit(f"tag{i}", t)
        if t > w - 0.5:
            index_card(c, 1520 + dx, y + dy, 480, 200, rot=4 - i * 7, seed=60 + i)
            type_text(c, lab, 1520 + dx, y - 20 + dy, 58, span(t, w - 0.4, w + 0.2), color=RED_INK)
            person(c, 1840 + dx, y + 110 + dy, 0.5, t, key=f"kid_{i}", i=i + 2, female=i == 1)
            pin(c, 1300 + dx, y - 60 + dy)
        red_string(c, [(560, 560), (1000, 400 + i * 200), (1300, y - 60)], span(t, w - 0.6, w + 0.2))


def s_phone(c, t, t0):
    collage_bg(c, t, tint="#E8EEDF")
    dx, dy, a = jit("table", t)
    c.drawRect(skia.Rect(0, 760 + dy, W, H), paint("#8B5A2B"))
    halftone(c, skia.Path().addRect(skia.Rect(0, 760, W, H)), "#3A2010", 0.25)
    ring = span(t, T(KER, "rings") - 0.2, T(KER, "rings") + 0.1) * (1 - span(t, T(KER, "visit"), T(KER, "visit") + 0.6))
    old_phone(c, 760, 720, 1.4, t, ring=ring)
    person(c, 1400, 900, 1.05, t, key="gma3", i=1, old=True, female=True, cloth="#E9A23B")
    headline(c, "SUNDAY", 760, 220, 64, span(t, T(KER, "sunday") - 0.3, T(KER, "sunday") + 0.3), seed=63)
    tv = T(KER, "family")
    stamp(c, 1300, 360, "FAMILY VISIT", span(t, tv - 0.1, tv + 0.2), color="coral", rot=-8)


# ---------------------------------------------------------------- 2046 THE CLASSROOM
def s_notwhere(c, t, t0):
    collage_bg(c, t)
    building(c, 560, 900, 1.1, t, kind="hospital", key="hosp")
    xmark(c, 560, 640, 2.4, span(t, T(CLS, "hospital") - 0.1, T(CLS, "hospital") + 0.3))
    building(c, 1360, 900, 1.1, t, kind="school", key="sch")
    tc = T(CLS, "classroom")
    marker_circle(c, 1360, 640, 330, 380, span(t, tc - 0.2, tc + 0.6))
    headline(c, "WHERE YOU SEE IT FIRST", W / 2, 120, 54, span(t, t0, t0 + 0.8), seed=65)


def s_scale(c, t, t0):
    collage_bg(c, t)
    ts = T(CLS, "fifteen")
    tilt = ease(span(t, ts - 0.8, ts + 0.6))
    (lx, ly), (rx, ry) = balance(c, 960, 700, 1.0, t, tilt)
    for i in range(3):
        person(c, lx - 100 + i * 100, ly + 10, 0.55, t, key=f"sc_c{i}", i=i, child=True, female=i == 1)
    for i in range(4):
        person(c, rx - 150 + i * 100, ry + 10, 0.55, t, key=f"sc_o{i}", i=i, old=True, female=i % 2 == 0)
    pop(c, lx, ly - 210, "UNDER 15", t, T(CLS, "children") - 0.2, color="teal", size=44)
    pop(c, rx, ry - 230, "60+", t, T(CLS, "sixty") - 0.2, color="coral", size=48)
    headline(c, "60+  >  UNDER 15", W / 2, 120, 60, span(t, ts - 0.2, ts + 0.6), seed=66)


def s_desks(c, t, t0):
    collage_bg(c, t, tint="#EFE9D6")
    tf = T(CLS, "fewer")
    gone = int(5 * span(t, tf - 0.6, tf + 0.8))
    desk_row(c, 960, 560, 1.3, t, 12, 12 - gone * 2, key="dsk")
    headline(c, "25 LAKH FEWER LITTLE KIDS", W / 2, 140, 60, span(t, T(CLS, "twentyfive") - 0.3, tf + 0.3), seed=68)
    pop(c, W / 2, 250, "IN ONE YEAR · UDISE+ 2024-25", t, T(CLS, "year") - 0.2, color="coral", size=36)


def s_japan(c, t, t0):
    collage_bg(c, t)
    building(c, 600, 940, 1.15, t, kind="school", key="jsch")
    tc = T(CLS, "close")
    stamp(c, 600, 640, "CLOSED", span(t, tc - 0.1, tc + 0.15), color="coral", rot=-10)
    dx, dy, a = jit("j450", t)
    index_card(c, 1400 + dx, 460 + dy, 560, 340, rot=4, seed=70)
    type_text(c, "JAPAN", 1400 + dx, 370 + dy, 50, span(t, t0, t0 + 0.4))
    type_text(c, "~450", 1400 + dx, 480 + dy, 130, span(t, T(CLS, "four") - 0.2, T(CLS, "fifty") + 0.2), color=RED_INK)
    type_text(c, "schools close a year", 1400 + dx, 580 + dy, 38, span(t, tc - 0.3, tc + 0.4))


def s_last2(c, t, t0):
    collage_bg(c, t, tint="#F0E9DA")
    building(c, 520, 960, 1.15, t, kind="school", key="jsch2")
    tg = T(CLS, "graduate")
    for i in range(2):
        w = span(t, t0 + 0.2, t0 + 3.5)
        person(c, 760 + i * 130 + 700 * w, 960, 0.8, t, key=f"grad{i}", i=i + 5, female=i == 0, cloth="#1B1030")
    headline(c, "THE LAST TWO STUDENTS", 1300, 200, 54, span(t, T(CLS, "last") - 0.3, tg + 0.2), seed=72)
    stamp(c, 520, 560, "CLOSED", span(t, tg + 0.2, tg + 0.45), color="coral", rot=8)


def s_bell(c, t, t0):
    collage_bg(c, t, tint="#EFE9D6")
    desk_row(c, 960, 900, 0.75, t, 6, 0, key="bd")
    bell(c, 960, 380, 1.3, t, swing=span(t, T(CLS, "works") - 0.4, T(CLS, "works")) * (1 - span(t, T(CLS, "nobody"), T(CLS, "nobody") + 0.8)))
    tn = T(CLS, "nobody")
    headline(c, "NOBODY LEFT", 1500, 640, 54, span(t, tn - 0.2, tn + 0.4), seed=74, rot=3)


# ---------------------------------------------------------------- 2050 WHO PAYS
def s_one5(c, t, t0):
    collage_bg(c, t)
    to = T(FIF, "sixty")
    for i in range(5):
        old = i == 2 and t > to - 0.3
        person(c, 400 + i * 280, 900, 1.0, t, key=f"f5{i}", i=i, old=old, female=i % 2 == 1)
    pop(c, 960, 380, "60+", t, to - 0.2, color="coral", size=54)
    headline(c, "1 IN 5 INDIANS", W / 2, 140, 64, span(t, T(FIF, "one") - 0.2, T(FIF, "five") + 0.3), seed=76)


def s_bills(c, t, t0):
    collage_bg(c, t)
    person(c, 1480, 960, 1.15, t, key="worker", i=0, cloth="#2F5D8A")
    items = [("PENSIONS", 360, 280, "pensions"), ("HOSPITALS", 420, 560, "hospitals"), ("NIGHT CARE", 380, 840, "night")]
    for i, (lab, x, y, w) in enumerate(items):
        tw = T(FIF, w)
        dx, dy, a = jit(f"bill{i}", t)
        if t > tw - 0.4:
            index_card(c, x + dx, y + dy, 420, 170, rot=(i - 1) * 5, seed=80 + i)
            type_text(c, lab, x + dx, y + dy, 52, span(t, tw - 0.3, tw + 0.2), color=RED_INK)
        red_string(c, [(x + 210, y), (1180, 620), (1440, 700)], span(t, T(FIF, "paid") - 0.4, T(FIF, "work") + 0.2))
    pop(c, 1480, 300, "PAID BY WORKERS", t, T(FIF, "work") - 0.2, color="teal", size=46)


def s_slice(c, t, t0):
    collage_bg(c, t)
    ts = T(FIF, "smaller")
    frac = 0.66 - 0.14 * ease(span(t, ts - 0.4, ts + 1.4))
    pie(c, 760, 560, 330, frac, 1.0, t, col1="#2E8B57", col2="#E9D8A6")
    pop(c, 1400, 420, "THE YOUNG", t, T(FIF, "young") - 0.2, color="teal", size=52)
    marker_line(c, [(1300, 480), (1050, 520)], span(t, T(FIF, "young"), T(FIF, "young") + 0.5), width=9)
    headline(c, "A SMALLER SLICE EVERY YEAR", W / 2, 1000, 50, span(t, ts - 0.3, ts + 0.6), seed=82)


def s_carers(c, t, t0):
    collage_bg(c, t)
    for i in range(8):
        person(c, 180 + i * 150 + (i > 3) * 760, 760 + (i % 2) * 70, 0.62, t, key=f"g{i}", i=i, old=True, female=i % 2 == 0)
    person(c, 960, 960, 1.15, t, key="young", i=3, cloth="#2E8B57")
    for i in range(8):
        x = 180 + i * 150 + (i > 3) * 760
        red_string(c, [(960, 640), (x, 560 + (i % 2) * 70)], span(t, t0 + 0.2 + i * 0.08, t0 + 0.8 + i * 0.08))
    headline(c, "WHO LOOKS AFTER THEM?", W / 2, 140, 56, span(t, t0, t0 + 0.8), seed=84)


def s_you(c, t, t0):
    collage_bg(c, t, tint="#E9E1D0")
    kr_cutout(c, lambda k: draw_kr(k, 760, 980, 1.7, "pointing", t))
    ty = T(FIF, "you")
    stamp(c, 1350, 520, "YOU", span(t, ty - 0.1, ty + 0.15), color="coral", rot=-8)


# ---------------------------------------------------------------- THE PEAK
def pop_curve(t, a, b):
    """Population curve as normalised points, drawn up to the peak and beyond."""
    return [(u, v) for u, v in [(0.0, 0.62), (0.15, 0.72), (0.3, 0.8), (0.45, 0.86), (0.55, 0.88), (0.65, 0.86), (0.8, 0.8), (1.0, 0.72)]]


def s_peak(c, t, t0):
    collage_bg(c, t, tint="#E6DCC8")
    P = pop_curve(t, 0, 0)
    up = span(t, t0, T(SIX, "people") + 0.3)
    dn = span(t, T(SIX, "goes") - 0.4, T(SIX, "down") + 0.6)
    pts = P[:5] if dn <= 0 else P
    p = up * 0.999 if dn <= 0 else 0.55 + 0.45 * dn
    line_graph(c, 200, 260, 1520, 560, pts, p, width=14)
    marker_line(c, [(200, 830), (1720, 830)], 1.0, color=INK, width=5)
    for i, yr in enumerate(["2026", "2040", "2060s", "2080", "2100"]):
        type_text(c, yr, 200 + [0, 0.3, 0.55, 0.8, 1.0][i] * 1520, 880, 36, 1.0)
    pk = (200 + 0.55 * 1520, 260 + 560 - 0.88 * 560)
    tp = T(SIX, "one")
    if t > tp - 0.3:
        pin(c, pk[0], pk[1] - 10)
        counter_text(c, 0, 170, span(t, tp - 0.3, T(SIX, "crore") + 0.2), lambda v: f"{v:.0f} CRORE", pk[0], pk[1] - 90, 64)
    tf = T(SIX, "first")
    stamp(c, 1300, 640, "FIRST FALL IN 100 YEARS", span(t, tf - 0.1, tf + 0.2), color="coral", rot=-6)


def s_fewer(c, t, t0):
    collage_bg(c, t, tint="#E6DCC8")
    for i in range(3):
        q = ease_out(span(t, t0 + i * 0.9, t0 + 0.4 + i * 0.9))
        if q <= 0:
            continue
        x = 400 + i * 560
        dx, dy, a = jit(f"yr{i}", t)
        index_card(c, x + dx, 560 + dy, 460 * q + 1, 560 * q + 1, rot=(i - 1) * 4, seed=90 + i)
        type_text(c, ["THIS YEAR", "NEXT YEAR", "YEAR AFTER"][i], x + dx, 340 + dy, 40 * q + 1)
        n = 9 - i * 3
        for j in range(n):
            px = x - 150 + (j % 3) * 150 + dx
            py = 520 + (j // 3) * 150 + dy
            c.drawCircle(px, py - 40, 24 * q, paint(SKIN[j % 4]))
            c.drawRRect(rr(px - 30 * q, py - 10, px + 30 * q, py + 60 * q, 12), paint(CLOTH[j % 8]))
    headline(c, "FEWER. THEN FEWER AGAIN.", W / 2, 120, 54, span(t, T(SIX, "fewer") - 0.3, T(SIX, "again") + 0.3), seed=92)


def s_wedding(c, t, t0):
    collage_bg(c, t, tint="#3A2A3A")
    for i in range(20):
        xx = 140 + (i % 10) * 180
        yy = 620 + (i // 10) * 260
        empty = i == 13
        cutout(c, lambda k, xx=xx, yy=yy: chair(k, xx, yy, 1.1, "#C0392B"), border=5, shadow=(4, 6))
        if not empty:
            person(c, xx, yy - 40, 0.55, t, key=f"w{i}", i=i, female=i % 3 == 0)
    te = T(SIX, "empty")
    sp = span(t, te - 0.4, te + 0.2)
    c.drawRect(skia.Rect(0, 0, W, H), paint("#000000", 0.45 * sp))
    glow(c, 140 + 3 * 180, 820, 180, "gold", 0.8 * sp)
    for i in range(14):
        a_ = 0.35 * sp
        c.drawCircle(140 + (i * 137) % 1700, 120 + (i * 53) % 260, 6, paint("gold", a_))
    headline(c, "NO HEADLINE", 520, 160, 52, span(t, T(SIX, "headline") - 0.3, T(SIX, "headline") + 0.2), seed=95)
    pop(c, 140 + 3 * 180, 520, "ONE EMPTY CHAIR", t, te - 0.2, color="coral", size=42)


def s_2100(c, t, t0):
    collage_bg(c, t, tint="#E6DCC8")
    tv = T(SIX, "expects")
    dx, dy, a = jit("c2100", t)
    index_card(c, 700 + dx, 520 + dy, 760, 460, rot=-3, seed=97)
    type_text(c, "2100 · UN", 700 + dx, 370 + dy, 50, span(t, t0, t0 + 0.4))
    v = 170 - 20 * ease(span(t, tv - 0.2, T(SIX, "crore") + 0.4))
    big_text(c, f"{v:.0f} CRORE", 700 + dx, 540 + dy, 120, 1.0, "coral")
    stamp(c, 1450, 560, "−20 CRORE", span(t, T(SIX, "twenty", 2) - 0.1, T(SIX, "twenty", 2) + 0.15), color="coral", rot=-10)


def s_papers(c, t, t0):
    collage_bg(c, t)
    tl = T(SIX, "lancet")
    for i, (mast, head, num, x, w0) in enumerate([("UN WORLD POPULATION PROSPECTS 2024", "INDIA IN 2100", "150 CRORE", 560, t0),
                                                 ("THE LANCET · 2020 STUDY", "INDIA IN 2100", "109 CRORE", 1360, tl - 0.6)]):
        q = ease_out(span(t, w0, w0 + 0.5))
        if q <= 0:
            continue
        dx, dy, a = jit(f"clip{i}", t)
        torn_strip(c, x + dx, 560 + dy, 680 * q + 1, 720 * q + 1, seed=120 + i, color="#F2EDE0", rot=-3 + i * 6)
        type_text(c, mast, x + dx, 270 + dy, 26 * q + 1, 1.0)
        c.drawLine(x - 300 + dx, 300 + dy, x + 300 + dx, 300 + dy, paint(INK, stroke=3))
        type_text(c, head, x + dx, 360 + dy, 56 * q + 1, 1.0)
        ph = skia.Path().addRect(skia.Rect(x - 260 + dx, 410 + dy, x + 260 + dx, 640 + dy))
        c.drawPath(ph, paint("#B8A889"))
        for j in range(18):
            c.drawCircle(x - 220 + dx + (j % 6) * 88, 450 + dy + (j // 6) * 80, 24, paint(SKIN[j % 4], 0.8))
        halftone(c, ph, "#000000", 0.35, step=10)
        type_text(c, num, x + dx, 730 + dy, 84 * q + 1, 1.0, color=RED_INK)
        marker_circle(c, x + dx, 730 + dy, 260, 70, span(t, w0 + 0.6, w0 + 1.3))
    headline(c, "SCIENTISTS DISAGREE", W / 2, 1000, 56, span(t, tl - 0.4, tl + 0.4), seed=125)


# ---------------------------------------------------------------- TWIST
def s_delhi(c, t, t0):
    collage_bg(c, t)
    skyline(c, 960, 960, 1.15, t, "delhi", key="dl")
    td = T("twist", "one")
    dx, dy, a = jit("t12", t)
    index_card(c, 960 + dx, 260 + dy, 520, 260, rot=-4, seed=101)
    type_text(c, "DELHI", 960 + dx, 200 + dy, 52, span(t, t0, t0 + 0.4))
    type_text(c, "1.2", 960 + dx, 300 + dy, 120, span(t, td - 0.2, td + 0.3), color=RED_INK)
    pop(c, 960, 430, "CHILDREN PER WOMAN · SRS 2024", t, td + 0.2, color="teal", size=32)


def s_tokyo(c, t, t0):
    collage_bg(c, t)
    skyline(c, 500, 1000, 0.85, t, "delhi", key="dl2")
    skyline(c, 1420, 1000, 0.85, t, "tokyo", key="tk")
    for i, (lab, v, x) in enumerate([("DELHI", "1.2", 500), ("JAPAN", "1.15", 1420)]):
        dx, dy, a = jit(f"cmp{i}", t)
        index_card(c, x + dx, 250 + dy, 420, 230, rot=-3 + i * 6, seed=103 + i)
        type_text(c, lab, x + dx, 200 + dy, 46, 1.0)
        type_text(c, v, x + dx, 290 + dy, 96, span(t, t0 + i * 0.4, t0 + 0.3 + i * 0.4), color=RED_INK)
    ts = T("twist", "same")
    stamp(c, 960, 300, "SAME", span(t, ts - 0.1, ts + 0.15), color="coral", rot=0)
    tf = T("twist", "family")
    headline(c, "JAPAN'S FAMILY SIZE", W / 2, 560, 60, span(t, tf - 0.5, tf + 0.3), seed=105)


def s_south(c, t, t0):
    collage_bg(c, t)
    tk = T("twist", "kerala")
    P = india_map(c, 820, 560, 28, highlight=("Kerala", "Tamil Nadu", "Delhi"), hcol="#C0392B",
                  ha=span(t, tk - 0.4, tk + 0.3))
    for lab, lon, lat, w in [("DELHI 1.2", 77.1, 28.6, t0), ("KERALA 1.3", 76.3, 10.0, tk), ("TAMIL NADU 1.3", 78.6, 11.0, T("twist", "tamil"))]:
        x, y = P(lon, lat)
        off = {"KERALA 1.3": (-290, 40), "TAMIL NADU 1.3": (300, 10), "DELHI 1.2": (230, 0)}[lab]
        pop(c, x + off[0], y + off[1], lab, t, w, color="coral", size=36)
    headline(c, "NOT FAR BEHIND", 1500, 900, 52, span(t, T("twist", "far") - 0.3, T("twist", "behind") + 0.2), seed=107)


def s_cities(c, t, t0):
    collage_bg(c, t)
    P = india_map(c, 820, 560, 28)
    cities = [("DELHI", 77.1, 28.6, "1.2"), ("KOLKATA", 88.4, 22.6, "1.3"), ("MUMBAI", 72.9, 19.1, "1.4"),
              ("CHENNAI", 80.3, 13.1, "1.3"), ("KOCHI", 76.3, 10.0, "1.3")]
    pts = []
    for i, (name, lon, lat, v) in enumerate(cities):
        x, y = P(lon, lat)
        q = span(t, t0 + 0.3 + i * 0.35, t0 + 0.6 + i * 0.35)
        if q > 0:
            pin(c, x, y)
            pts.append((x, y))
    if len(pts) > 1:
        red_string(c, pts, 1.0)
    headline(c, "ALREADY HERE", 1500, 300, 66, span(t, T("twist", "exists") - 0.4, T("twist", "exists") + 0.3), seed=109)
    tn = T("twist", "noticed")
    stamp(c, 1500, 640, "OUR OWN CITIES", span(t, T("twist", "cities") - 0.1, T("twist", "cities") + 0.15), color="coral", rot=-6)
    pop(c, 1500, 900, "WE JUST HAVEN'T NOTICED", t, tn - 0.3, color="teal", size=40)


# ---------------------------------------------------------------- PAYOFF
def s_back(c, t, t0):
    photos(c, t, t0, "payoff")


def s_grandkid(c, t, t0):
    collage_bg(c, t)
    family_photo(c, 960, 520, 1.05, t, 4, 1, key="gk", rot=2, old_rows=4, p=span(t, t0, t0 + 0.5))
    pop(c, 960, 940, "4 GRANDPARENTS · 1 CHILD", t, T("payoff", "four") - 0.2, color="coral", size=44)


def s_bright(c, t, t0):
    collage_bg(c, t)
    torn_strip(c, W / 2, 330, W + 80, 560, seed=117, color="#BFDDEB", shadow=False)
    c.drawCircle(1640, 200, 90, paint("#F2C14E"))
    train(c, 860, 1.2, t, t0, cars=3, speed=220)
    labels = [("EMPTIER TRAINS", "emptier"), ("CLEANER AIR", "cleaner"), ("MORE SPACE", "space")]
    for i, (lab, w) in enumerate(labels):
        pop(c, 480 + i * 480, 420, lab, t, T("payoff", w) - 0.2, color=["teal", "teal", "coral"][i], size=44)
    headline(c, "NOT THE END OF THE WORLD", W / 2, 260, 52, span(t, t0, t0 + 0.8), seed=111)


def s_ready(c, t, t0):
    collage_bg(c, t)
    kr_cutout(c, lambda k: draw_kr(k, 620, 980, 1.5, "thinking", t))
    tn = T("payoff", "now")
    headline(c, "GET READY", 1350, 420, 80, span(t, T("payoff", "ready") - 0.3, T("payoff", "ready") + 0.3), seed=113)
    stamp(c, 1350, 640, "NOW", span(t, tn - 0.1, tn + 0.15), color="coral", rot=-8)


def s_tease(c, t, t0):
    collage_bg(c, t)
    c.drawRect(skia.Rect(0, 620, W, 1000), paint("#5A5550"))
    for i in range(8):
        c.drawRect(skia.Rect(i * 260 + 40, 805, i * 260 + 180, 815), paint("#F4EFE3"))
    for i in range(18):
        x = 120 + (i % 6) * 330 + (i // 6 % 2) * 150
        y = 700 + (i // 6) * 110
        dx, dy, a = jit(f"car{i}", t)
        cutout(c, lambda k, x=x + dx, y=y + dy, i=i: car(k, x, y, 0.85, CLOTH[i % 8]), border=5, shadow=(4, 6))
    headline(c, "NEXT: WHAT IF EVERY INDIAN FAMILY OWNED A CAR?", W / 2, 200, 52, span(t, t0, t0 + 1.2), seed=115)
    stamp(c, W / 2, 430, "COMING NEXT", span(t, t0 + 1.2, t0 + 1.45), color="coral", rot=-6)


# ---------------------------------------------------------------- the list
def SHOTS():
    L = [
        (0.0, s_cold, "cut"),
        (T("hook", "keep") - 0.2, s_shrink, "whip"),
        (T("hook", "and", 2) - 0.2, s_where, "fade"),
        (E("hook") + 0.1, logo_sting(), "flash"),
        (T("promise", "and") - 0.2, s_predict, "fade"),
        (T("promise", "because") - 0.2, s_born, "fade"),
        (B("today") - 0.6, card("TODAY", "The magic number"), "iris"),
        (T("today", "magic") - 0.3, s_21, "fade"),
        (T("today", "two", 2) - 0.3, s_replace, "fade"),
        (T("today", "indias") - 0.3, s_19, "whip"),
        (T("today", "heres") - 0.2, s_myth, "fade"),
        (T("today", "think") - 0.2, s_train, "fade"),
        (T("today", "our") - 0.2, s_long, "zoom"),
        (B(KER) - 0.6, card("2036", "Kerala"), "iris"),
        (T(KER, "go") - 0.2, s_kerala, "fade"),
        (T(KER, "picture") - 0.2, s_house, "fade"),
        (T(KER, "her") - 0.2, s_strings, "fade"),
        (T(KER, "on") - 0.2, s_phone, "fade"),
        (B(CLS) - 0.6, card("2046", "The classroom"), "iris"),
        (T(CLS, "not") - 0.2, s_notwhere, "fade"),
        (T(CLS, "around") - 0.2, s_scale, "fade"),
        (T(CLS, "and") - 0.2, s_desks, "fade"),
        (T(CLS, "japan") - 0.2, s_japan, "whip"),
        (T(CLS, "some") - 0.2, s_last2, "fade"),
        (T(CLS, "the", 2) - 0.2, s_bell, "fade"),
        (B(FIF) - 0.6, card("2050", "Who pays"), "iris"),
        (T(FIF, "one") - 0.3, s_one5, "fade"),
        (T(FIF, "pensions") - 0.3, s_bills, "fade"),
        (T(FIF, "and", 1) - 0.2, s_slice, "fade"),
        (T(FIF, "somebody") - 0.2, s_carers, "fade"),
        (T(FIF, "and", 2) - 0.2, s_you, "zoom"),
        (B(SIX) - 0.3, card("EARLY 2060s", "The peak"), "cut"),
        (T(SIX, "india") - 0.3, s_peak, "fade"),
        (T(SIX, "next") - 0.2, s_fewer, "fade"),
        (T(SIX, "no") - 0.2, s_wedding, "fade"),
        (T(SIX, "by") - 0.2, s_2100, "fade"),
        (T(SIX, "and", 2) - 0.2, s_papers, "fade"),
        (B("twist") - 0.6, card("TODAY", "Already here"), "iris"),
        (T("twist", "in", 1) - 0.2, s_delhi, "fade"),
        (T("twist", "japan") - 0.3, s_tokyo, "whip"),
        (T("twist", "kerala") - 0.5, s_south, "fade"),
        (T("twist", "shrinking") - 0.4, s_cities, "fade"),
        (B("payoff") - 0.6, card("THE PHOTO", "Back to nani"), "iris"),
        (B("payoff") + 0.4, s_back, "fade"),
        (T("payoff", "your", 2) - 0.2, s_grandkid, "fade"),
        (T("payoff", "thats") - 0.2, s_bright, "fade"),
        (T("payoff", "but") - 0.2, s_ready, "fade"),
        (T("payoff", "so", 2) - 0.2, comment_prompt("One child, two, or none?"), "fade"),
        (T("payoff", "next") - 0.2, s_tease, "cut"),
        (E("payoff") + 0.3, end_screen(), "fade"),
    ]
    L.sort(key=lambda x: x[0])
    # long hero shots get a new framing (a slow push-in on the running shot) every ~3.5 s
    out = []
    for i, (st, fn, tr) in enumerate(L):
        out.append((st, fn, tr))
        nxt = L[i + 1][0] if i + 1 < len(L) else st
        name = getattr(fn, "__name__", "")
        if not name.startswith("s_") or nxt - st < 5.0:
            continue
        n = int((nxt - st) / 3.5)
        for j in range(1, n + 1):
            s2 = st + j * (nxt - st) / (n + 1)
            cx, cy = [(760, 600), (1180, 580), (960, 640)][j % 3]
            out.append((s2, cont(fn, st, 1.2 + 0.05 * (j % 2), cx, cy), "cut"))
    out.sort(key=lambda x: x[0])
    return out
