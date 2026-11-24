"""Shot list for 'What If Every Indian Got Rs 1 Crore Tomorrow?' (style: collage).
Each shot: (start_time, fn(c, t, t0), transition). Times are anchored to words with T / at / B / E.
Threads: (1) the 8 AM phone on the kitchen table opens and closes the video; (2) the paper house with the red
question mark returns in Month three to point at the grandmother; (3) the FD certificate sits on the shelf in
Hour one before it melts in Month three."""
import math
import skia
from art import *  # noqa: F401,F403

CREDIT = [("₹1,00,00,000", 54, "#1F6E43"), ("CREDITED", 46, "#1F6E43"), ("8:00 AM", 30, "#5A5A5A")]


def kitchen(c, t, lines=CREDIT, buzz=0.0, head="BANK", head_col="#1F6E43", z=1.0, cx=960, cy=540, crumble=0.0):
    """The 8 AM kitchen-table frame (opening and closing image)."""
    with CamC(c, z, cx, cy, t=t):
        collage_bg(c, t, tint="#E9DDC4")
        # window + clock on the wall
        index_card(c, 330, 250, 360, 280, rot=-2, seed=5)
        c.drawRect(skia.Rect(200, 140, 460, 360), paint("#BFD7EA"))
        c.drawLine(330, 140, 330, 360, paint("#F4EFE3", stroke=10)); c.drawLine(200, 250, 460, 250, paint("#F4EFE3", stroke=10))
        cutout(c, lambda k: k.drawPath(paper_circle(1620, 230, 110, 6), paint("#F4EFE3")))
        c.drawLine(1620, 230, 1620, 145, paint(INK, stroke=8)); c.drawLine(1620, 230, 1568, 260, paint(INK, stroke=12))
        type_text(c, "8 AM", 1620, 380, 44, 1.0)
        table(c, t)
        for i, (bx, by, r) in enumerate([(560, 830, -14), (1360, 850, 12), (700, 960, 6), (1230, 980, -8)]):
            bundle(c, bx, by, 0.85, t, key=f"kb{i}", rot=r, crumble=crumble)
        phone_msg(c, 960, 600, 1.0, t, lines, key="kphone", buzz=buzz, head=head, head_col=head_col)


# ---------------------------------------------------------------- HOOK
def s_cold(c, t, t0):
    """Frame 0: a big phone fills the frame with Rs 1,00,00,000 CREDITED, buzzing; the stamp slams across it."""
    z = keys(t, [(t0, 1.0), (t0 + 6, 1.1)])
    with CamC(c, z, 960, 520, t=t):
        collage_bg(c, t, tint="#E9DDC4")
        table(c, t, y=820)
        bundle(c, 430, 900, 0.9, t, key="cb0", rot=-14); bundle(c, 1490, 910, 0.9, t, key="cb1", rot=12)
        phone_msg(c, 960, 500, 1.3, t, [("₹1,00,00,000", 70, "#1F6E43"), ("CREDITED", 56, "#1F6E43"), ("8:00 AM", 32, "#5A5A5A")],
                  key="kphone", buzz=1.0 - span(t, t0, t0 + 2.5), rot=-3)
    tc = T("hook", "credited")
    stamp(c, 960, 800, "₹1 CRORE", span(t, tc, tc + 0.25), color="coral", rot=-12)


def s_everyone(c, t, t0):
    collage_bg(c, t)
    P = india_map(c, 700, 560, 26)
    cities = [(72.88, 19.07), (77.21, 28.61), (88.36, 22.57), (80.27, 13.08), (77.59, 12.97), (78.49, 17.38),
              (73.86, 18.52), (72.57, 23.02), (75.79, 26.91), (80.95, 26.85), (85.14, 25.6), (76.27, 9.93),
              (91.74, 26.14), (81.63, 21.25), (74.87, 31.63), (83.0, 25.3), (77.4, 23.26), (85.82, 20.3)]
    for i, (lo, la) in enumerate(cities):
        q = back_out(span(t, t0 + 0.2 + i * 0.09, t0 + 0.45 + i * 0.09))
        if q > 0:
            x, y = P(lo, la)
            cutout(c, lambda k, x=x, y=y, q=q: k.drawRRect(rr(x - 18 * q, y - 30 * q, x + 18 * q, y + 30 * q, 6 * q), paint("#1E1E24")), border=4)
            c.drawRect(skia.Rect(x - 12 * q, y - 22 * q, x + 12 * q, y + 18 * q), paint("#3FBF6F"))
    headline(c, "EVERY INDIAN", 1450, 330, 76, span(t, T("hook", "every") - 0.1, T("hook", "every") + 0.6), seed=3)
    tall = T("hook", "all")
    big_text(c, "146 CRORE", 1450, 560, 120, span(t, tall, tall + 0.5), "coral")
    type_text(c, "× ₹1 CRORE EACH", 1450, 680, 54, span(t, tall + 0.4, tall + 1.0))


def s_who(c, t, t0):
    collage_bg(c, t)
    house(c, 960, 900, 1.6, t, key="thehouse")
    for i, (fx, colr, fem) in enumerate([(-170, "#3D5A80", False), (-50, "#9C4F2E", True), (70, "#7B5E8B", True), (180, "#4F772D", False)]):
        q = ease_out(span(t, t0 + 0.1 + i * 0.12, t0 + 0.4 + i * 0.12))
        if q > 0:
            person(c, 960 + fx, 900, 0.55, t, color=colr, key=f"fam{i}", female=fem)
    marker_circle(c, 960, 700, 460, 360, span(t, T("hook", "loses") - 0.2, T("hook", "loses") + 0.5))
    big_text(c, "?", 1520, 380, 240, span(t, T("hook", "sitting") - 0.2, T("hook", "sitting") + 0.2), "coral")
    headline(c, "WHO LOSES MOST?", W / 2, 140, 64, span(t, T("hook", "loses") - 0.1, T("hook", "loses") + 0.6), seed=8)


# ---------------------------------------------------------------- PROMISE
def s_rules(c, t, t0):
    collage_bg(c, t)
    dx, dy, a = jit("rules", t)
    torn_strip(c, 760 + dx, 480 + dy, 1000, 560, seed=11, color="#EFE8D6", rot=-2)
    type_text(c, "THE RULES", 760 + dx, 280 + dy, 84, span(t, t0, t0 + 0.5), color=RED_INK)
    for i, (w, ln) in enumerate([("brand", "1. BRAND NEW MONEY"), ("no", "2. NO TAX"), ("one", "3. ₹1 CRORE EACH")]):
        ts = min(T("promise", w) - 0.1, t0 + 0.5 + i * 0.7)
        type_text(c, ln, 760 + dx, 420 + i * 100 + dy, 58, span(t, ts, ts + 0.5))
    tb = T("promise", "baby")
    q = back_out(span(t, tb - 0.3, tb + 0.2))
    if q > 0:
        cutout(c, lambda k: (k.drawPath(paper_circle(1500, 640, 120 * q, 3), paint("#F2C94C")),
                             k.drawRect(skia.Rect(1490, 640, 1510, 640 + 220 * q), paint("#F2C94C"))))
        type_text(c, "EVEN BABIES", 1500, 940, 52, q, color=RED_INK)
    tape(c, 300, 230, 160, 48, -18); tape(c, 1230, 230, 160, 48, 16)


def s_papers_reports(c, t, t0):
    """Effort beat: 7 reports land, tied by red string to one headline."""
    collage_bg(c, t)
    headline(c, "7 REPORTS CHECKED", W / 2, 190, 70, span(t, t0, t0 + 0.6), seed=14)
    reps = [("RBI", "Money supply"), ("UN", "Population"), ("MoSPI", "Income"), ("NITI", "Gig workers"),
            ("RBI", "Inflation"), ("JHU", "Zimbabwe"), ("CATO", "Hyperinflation")]
    for i, (ti, su) in enumerate(reps):
        ts = T("promise", "seven") - 0.6 + i * 0.25
        q = ease_out(span(t, ts, ts + 0.25))
        if q > 0:
            x = 210 + i * 250
            y = 660 + (i % 2) * 70 - (1 - q) * 300
            report(c, x, y, 0.74, t, ti, su, key=f"rep{i}", rot=(rng(i, 9) - 0.5) * 10)
            red_string(c, [(x, y - 140), (W / 2, 250)], span(t, ts + 0.2, ts + 0.6))


# ---------------------------------------------------------------- HOUR ONE
def s_check(c, t, t0):
    collage_bg(c, t)
    th = [T("hour_one", "check") + i * 0.5 for i in range(3)]
    k = sum(1 for x in th if t >= x)
    phone_msg(c, 820, 560, 1.15, t, [("BALANCE", 36, "#5A5A5A"), ("₹1,00,00,000", 54, "#1F6E43")], key="chk", rot=3)
    for i in range(k):
        x2, y2, a = jit(f"tap{i}", t)
        marker_circle(c, 820 + x2, 830 + y2, 50 + i * 22, 50 + i * 22, 1.0, seed=20 + i)
    if k:
        type_text(c, "REFRESH" if k < 3 else "STILL THERE", 820, 700, 34, 1.0, color=RED_INK)
    if t > T("hour_one", "real") - 0.1:
        stamp(c, 1420, 560, "IT'S REAL", span(t, T("hour_one", "real") - 0.1, T("hour_one", "real") + 0.15), color="coral", rot=-8)


def s_fifty(c, t, t0):
    collage_bg(c, t)
    tf = T("hour_one", "fifty")
    n = int(clamp((t - t0 - 0.3) / 0.05, 0, 50))
    for i in range(n):
        x = 300 + (i % 10) * 62 + rng(i, 2) * 8
        y = 960 - (i // 10) * 120 - rng(i, 5) * 6
        index_card(c, x, y, 120, 80, rot=(rng(i, 3) - 0.5) * 10, seed=i)
        type_text(c, "SALARY", x, y, 20, 1.0)
    headline(c, "₹1 CRORE ≈", 1420, 360, 70, span(t, t0, t0 + 0.6), seed=12)
    big_text(c, "50 YEARS", 1420, 540, 120, span(t, tf - 0.1, tf + 0.4), "coral")
    type_text(c, "of an average Indian's income", 1420, 660, 44, span(t, tf + 0.2, tf + 0.9))


def s_call(c, t, t0):
    collage_bg(c, t, tint="#EADFC8")
    # your side (left) and your mother's side (right), joined by a phone line
    person(c, 520, 980, 1.25, t, color="#3D5A80", key="you", phone_glow=True)
    person(c, 1400, 980, 1.25, t, color="#9C4F2E", key="mom", female=True, phone_glow=True, flip=True)
    red_string(c, [(580, 700), (960, 520), (1340, 700)], span(t, t0 + 0.1, t0 + 0.7))
    # thread 3: the FD certificate sits quietly on her shelf
    c.drawRect(skia.Rect(1420, 420, 1700, 440), paint("#6B4A2B"))
    fd_cert(c, 1560, 360, 0.28, t, key="fdshelf", rot=2)
    tc = T("hour_one", "crying")
    for i in range(3):
        q = span(t, tc + i * 0.2, tc + 0.6 + i * 0.2)
        if 0 < q < 1:
            c.drawCircle(1370 - i * 12, 650 + q * 120, 9, paint("#7FB3E0"))
    if t > T("hour_one", "wedding") - 0.3:
        wedding_card(c, 960, 330, 0.85, t, p=span(t, T("hour_one", "wedding") - 0.2, T("hour_one", "wedding") + 0.5))
    if t > T("hour_one", "whose") - 0.1:
        marker_circle(c, 960, 360, 260, 60, span(t, T("hour_one", "whose") - 0.1, T("hour_one", "whose") + 0.4))
        big_text(c, "?", 1200, 300, 120, span(t, T("hour_one", "whose"), T("hour_one", "whose") + 0.2), "coral")


def s_website(c, t, t0):
    collage_bg(c, t)
    dx, dy, a = jit("browser", t)
    c.drawRRect(rr(260 + dx, 160 + dy, 1660 + dx, 920 + dy, 20), paint("#1E1E24"))
    c.drawRect(skia.Rect(280 + dx, 230 + dy, 1640 + dx, 900 + dy), paint("#F7F5EF"))
    for i in range(3):
        c.drawCircle(310 + i * 34 + dx, 195 + dy, 10, paint(["#E76F51", "#E9C46A", "#2A9D8F"][i]))
    type_text(c, "BUY A CAR TODAY", 960 + dx, 300 + dy, 60, 1.0)
    for i, colr in enumerate(["#C0392B", "#2F5D8A", "#E9C46A"]):
        car(c, 520 + i * 440 + dx, 640 + dy, 0.62, t, colr=colr, key=f"wc{i}")
    te = T("hour_one", "everyone")
    v = int(keys(t, [(t0, 1), (te, 3), (te + 1.5, 2_40_00_000)], ease_out))
    pill(c, 1350 + dx, 820 + dy, 1.0, (f"{v / 1e7:.1f} CRORE VISITORS" if v >= 10**6 else f"{v:,} VISITORS"), "coral", size=36)


# ---------------------------------------------------------------- HOUR SIX
def s_showroom(c, t, t0):
    showroom(c, t)
    for i, colr in enumerate(["#C0392B", "#2F5D8A", "#4F772D"]):
        car(c, 340 + i * 420, 930, 0.75, t, colr=colr, key=f"sc{i}")
    # glass door on the right with a crowd pressing
    door_p = skia.Path().addRect(skia.Rect(1360, 300, 1780, 980))
    cutout(c, lambda k: (k.drawPath(door_p, paint("#C9D6DF")), halftone(k, door_p, "#2F5D8A", 0.25, step=14)))
    torn_strip(c, 1570, 360, 300, 60, seed=46, color="#FFF3C4")
    type_text(c, "SHOWROOM", 1570, 360, 36, 1.0, color=RED_INK)
    tc = T("hour_six", "crowd")
    n = int(keys(t, [(t0, 2), (tc, 4), (tc + 1.2, 11)]))
    c.drawRect(skia.Rect(1350, 290, 1790, 990), paint("#6B4A2B", stroke=18))
    for i in range(n):
        person(c, 1420 + (i % 6) * 62, 1000 - (i // 6) * 30, 0.62, t,
               color=["#3D5A80", "#9C4F2E", "#4F772D", "#6D597A", "#B5838D"][i % 5], key=f"cr{i}", female=i % 3 == 1)
    if t > T("hour_six", "nobody") - 0.2:
        pop(c, 1500, 220, "NOBODY WANTS TO WAIT", t, T("hour_six", "nobody") - 0.2, color="coral", size=38)


def s_tag(c, t, t0):
    showroom(c, t)
    car(c, 760, 960, 1.25, t, colr="#C0392B", key="hero")
    tch = T("hour_six", "changes")
    if t < tch:
        price_tag(c, 1450, 520, 1.3, t, "₹8 LAKH", key="tag1")
    else:
        q = span(t, tch, tch + 0.5)
        if q < 1:
            price_tag(c, 1450, 520 + q * 500, 1.3, t, "₹8 LAKH", key="tag1", rot=8 + q * 60)
        price_tag(c, 1450, 520, 1.3 * max(0.2, ease_out(span(t, tch + 0.3, tch + 0.7))), t, "₹80 LAKH", key="tag2", rot=-6)
        tape(c, 1350, 420, 140, 46, -20)
    if t > tch + 0.8:
        stamp(c, 760, 560, "SOLD OUT", span(t, tch + 0.8, tch + 1.05), color="coral", rot=-12)


def s_more(c, t, t0):
    collage_bg(c, t)
    tm = T("hour_six", "today")
    hgt = keys(t, [(tm, 2), (tm + 2.5, 14)], ease_out)
    note_stack(c, 520, 980, 0.8, hgt, t, key="ms")
    type_text(c, "MONEY", 520, 260, 64, span(t, tm, tm + 0.5), color=RED_INK)
    for i in range(3):
        car(c, 1380, 520 + i * 200, 0.55, t, colr=["#C0392B", "#2F5D8A", "#4F772D"][i], key=f"mc{i}")
    type_text(c, "CARS", 1380, 260, 64, span(t, tm + 0.3, tm + 0.8), color=RED_INK)
    red_string(c, [(700, 820), (960, 860), (1180, 820)], span(t, tm + 0.6, tm + 1.4))
    big_text(c, "≠", 960, 600, 180, span(t, T("hour_six", "not") - 0.2, T("hour_six", "not") + 0.2), "coral")


# ---------------------------------------------------------------- DAY THREE
def s_door(c, t, t0):
    collage_bg(c, t, tint="#E3D7BE")
    door(c, 960, 900, 1.6, t, "#9C4F2E", "HOME", key="frontdoor")
    # broom leaning, no footprints
    c.save(); c.rotate(12, 1420, 900)
    c.drawRect(skia.Rect(1410, 380, 1430, 860), paint("#8B5A2B"))
    cutout(c, lambda k: k.drawPath(_broom(1420, 860), paint("#D9B46A")))
    c.restore()
    td = T("day_three", "doorbell")
    big_text(c, "DING?", 1500, 300, 90, span(t, td, td + 0.4), "coral")
    if t > td + 0.6:
        xmark(c, 1500, 300, 1.2, span(t, td + 0.6, td + 0.9))
    if t > T("day_three", "she") - 0.2:
        pop(c, 560, 260, "SHE HAS ₹1 CRORE TOO", t, T("day_three", "she") - 0.2, color="plum", size=40)


def _broom(x, y):
    p = skia.Path(); p.moveTo(x - 20, y); p.lineTo(x + 20, y); p.lineTo(x + 80, y + 150); p.lineTo(x - 80, y + 150); p.close()
    return p


def s_app(c, t, t0):
    collage_bg(c, t)
    dx, dy, a = jit("appmap", t)
    c.drawRRect(rr(560 + dx, 120 + dy, 1360 + dx, 980 + dy, 40), paint("#1E1E24"))
    c.drawRect(skia.Rect(590 + dx, 170 + dy, 1330 + dx, 930 + dy), paint("#EAE6DA"))
    for i in range(7):
        c.drawLine(590 + dx, 250 + i * 110 + dy, 1330 + dx, 200 + i * 120 + dy, paint("#FFFFFF", stroke=14))
        c.drawLine(650 + i * 110 + dx, 170 + dy, 700 + i * 100 + dx, 930 + dy, paint("#FFFFFF", stroke=12))
    tn = T("day_three", "delivery")
    for i in range(12):
        x = 660 + rng(i, 4) * 600 + dx; y = 260 + rng(i, 6) * 580 + dy
        pin(c, x, y, "#E76F51")
        off = tn + 0.6 + i * 0.2
        if t > off:
            xmark(c, x, y, 0.45, span(t, off, off + 0.2))
    headline(c, "NO RIDERS NEARBY", 960, 960, 64, span(t, tn + 1.2, tn + 1.8), seed=33, color="#FFF3C4")
    t77 = T("day_three", "seventyseven")
    if t > t77 - 0.3:
        index_card(c, 1630, 470, 400, 340, rot=4, seed=9)
        type_text(c, "77 LAKH", 1630, 400, 70, span(t, t77 - 0.2, t77 + 0.3), color=RED_INK)
        type_text(c, "gig workers (NITI)", 1630, 470, 32, span(t, t77, t77 + 0.5))
        marker_line(c, [(1470, 410), (1790, 390)], span(t, T("day_three", "today") - 0.1, T("day_three", "today") + 0.4), width=14)
        type_text(c, "≈ 0 ONLINE", 1630, 570, 52, span(t, T("day_three", "log") - 0.2, T("day_three", "log") + 0.3), color=RED_INK)


def s_corner(c, t, t0):
    collage_bg(c, t, tint="#E6DCC6")
    c.drawRect(skia.Rect(0, 820, W, H), paint("#B8A68A"))
    house(c, 360, 830, 1.1, t, key="h1"); house(c, 1600, 830, 1.0, t, key="h2")
    # the dashed outline where the cart used to be
    for i in range(0, 600, 50):
        c.drawLine(660 + i, 560, 660 + i + 28, 560, paint(RED_INK, stroke=8))
        c.drawLine(660 + i, 880, 660 + i + 28, 880, paint(RED_INK, stroke=8))
    for j in range(0, 320, 50):
        c.drawLine(660, 560 + j, 660, 560 + j + 28, paint(RED_INK, stroke=8))
        c.drawLine(1260, 560 + j, 1260, 560 + j + 28, paint(RED_INK, stroke=8))
    c.saveLayer(None, skia.Paint(Alphaf=0.35))
    cart(c, 960, 860, 0.85, t, key="ghostcart")
    c.restore()
    stamp(c, 960, 680, "GONE", span(t, T("day_three", "gone") - 0.1, T("day_three", "gone") + 0.15), color="coral", rot=-8)
    headline(c, "THE SABZI CART", 960, 200, 60, span(t, t0, t0 + 0.6), seed=17)


def s_bread(c, t, t0):
    collage_bg(c, t, tint="#E9DDC4")
    table(c, t, y=700)
    plate_bread(c, 860, 820, 1.4, t)
    milk_packet(c, 1460, 760, 1.1, t, empty=True)
    headline(c, "CROREPATI BREAKFAST", 860, 230, 64, span(t, T("day_three", "youre") - 0.1, T("day_three", "youre") + 0.6), seed=19)
    if t > T("day_three", "milk") - 0.2:
        stamp(c, 1460, 600, "EMPTY", span(t, T("day_three", "milk") - 0.2, T("day_three", "milk") + 0.05), color="coral", rot=10)


def s_promise(c, t, t0):
    collage_bg(c, t)
    rupee_note(c, 960, 260, 1.3, t, key="pnote", colr=GOLD_NOTE, val="500")
    hands = [(420, "#4F772D", "farmer"), (960, "#3D5A80", "driver"), (1500, "#9C4F2E", "didi")]
    tp = T("day_three", "promise")
    for i, (hx, sl, lab) in enumerate(hands):
        q = ease_out(span(t, t0 + 0.4 + i * 0.25, t0 + 0.8 + i * 0.25))
        if q > 0:
            hand(c, hx, 1060 - 120 * q, 1.0, t, key=f"ph{i}", sleeve=sl)
            red_string(c, [(960, 330), (hx, 700)], span(t, tp - 0.6 + i * 0.15, tp + 0.2 + i * 0.15))
    if t > tp - 0.4:
        headline(c, "MONEY = A PROMISE", 960, 480, 70, span(t, tp - 0.3, tp + 0.4), seed=21)
    type_text(c, "that someone will work for you", 960, 580, 44, span(t, tp + 0.2, tp + 0.9))


# ---------------------------------------------------------------- WEEK TWO
def s_kidq(c, t, t0):
    collage_bg(c, t)
    notebook(c, 960, 560, 1.5, t, ["Why can't RBI", "just print more", "money and make", "everyone rich??"],
             span(t, T("week_two", "why") - 0.2, T("week_two", "rich") + 0.3), key="kidbook")
    kr_cutout(c, lambda k: draw_kr(k, 1640, 980, 1.1, "curious", t))


def s_x47(c, t, t0):
    collage_bg(c, t)
    t47 = T("week_two", "fortyseven")
    hgt = keys(t, [(t0, 8), (t47, 9), (t47 + 2.0, 24)], ease_out)
    for i in range(10):
        rupee_note(c, 980 + rng(i, 2) * 300, 820 + rng(i, 3) * 200, 0.6, t, key=f"spill{i}", rot=rng(i, 4) * 60 - 30)
    note_stack(c, 700, 1000, 0.75, hgt, t, key="x47")
    headline(c, "ALL THE MONEY IN INDIA", 960, 150, 60, span(t, t0, t0 + 0.7), seed=24)
    pill(c, 700, 300, 1.0, "CASH · BANK · FDs", "teal", size=36)
    big_text(c, "×47", 1400, 480, 260, span(t, t47 - 0.1, t47 + 0.4), "coral")
    type_text(c, "IN ONE MORNING", 1400, 680, 60, span(t, T("week_two", "morning") - 0.3, T("week_two", "morning") + 0.3), color=RED_INK)


def s_scale(c, t, t0):
    collage_bg(c, t)
    ts = T("week_two", "same")
    tilt = keys(t, [(t0, 0.0), (t0 + 0.4, -0.2), (ts, -0.2), (ts + 1.2, 1.0)], ease)
    lp, rp = scale(c, 960, 980, 1.2, t, tilt)
    note_stack(c, lp[0], lp[1] - 10, 0.45, 2 + 10 * clamp(tilt, 0, 1), t, key="sl")
    for i, w in enumerate(["tomatoes", "houses", "cars"]):
        tw = T("week_two", w)
        q = back_out(span(t, tw - 0.2, tw + 0.2))
        if q > 0:
            if i == 0:
                tomato(c, rp[0] - 90, rp[1] - 70, 0.7 * q, t, key="st")
            elif i == 1:
                house(c, rp[0] + 10, rp[1] - 10, 0.35 * q, t, key="sh")
            else:
                car(c, rp[0] + 120, rp[1] - 5, 0.3 * q, t, key="sc")
    headline(c, "SAME STUFF", rp[0] + 40, 200, 56, span(t, ts - 0.1, ts + 0.5), seed=23, rot=2)


def s_prices(c, t, t0):
    collage_bg(c, t)
    tomato(c, 620, 620, 2.2, t, key="bigtom")
    tc = T("week_two", "prices")
    v = keys(t, [(t0, 40), (tc, 40), (tc + 2.0, 1900)], ease)
    price_tag(c, 1360, 560, 1.6, t, f"₹{v:,.0f}/kg", key="tomtag", rot=-6)
    marker_line(c, [(1120, 820), (1300, 760), (1480, 700), (1700, 520)], span(t, tc, tc + 1.6), width=14)
    headline(c, "UNTIL THEY CATCH UP", 960, 160, 60, span(t, T("week_two", "catch") - 0.3, T("week_two", "catch") + 0.4), seed=25)


def s_ran(c, t, t0):
    collage_bg(c, t)
    tr = T("week_two", "ran")
    kr_cutout(c, lambda k: draw_kr(k, 330, 980, 1.1, "thinking", t))
    index_card(c, 1100, 520, 1200, 560, rot=-1, seed=27)
    type_text(c, "₹1,00,00,000 ÷ 47.5", 1100, 400, 70, span(t, tr - 0.2, tr + 0.6))
    marker_line(c, [(620, 470), (1580, 470)], span(t, tr + 0.4, tr + 0.9), width=8)
    big_text(c, "≈ ₹2 LAKH", 1100, 600, 140, span(t, T("week_two", "two", 2) - 0.2, T("week_two", "two", 2) + 0.3), "coral")
    type_text(c, "≈ one year of average income", 1100, 730, 44, span(t, T("week_two", "lakh") + 0.3, T("week_two", "lakh") + 1.0))


# ---------------------------------------------------------------- MONTH TWO
def s_mandi(c, t, t0):
    collage_bg(c, t, tint="#DCCFB2")
    onion_sack(c, 1240, 940, 1.3, t)
    person(c, 1620, 980, 1.25, t, color="#F4EFE3", key="farmer")
    tn = T("month_two", "notes")
    q = span(t, tn, tn + 0.8)
    note_stack(c, 640 - q * 260, 900, 0.75, 5, t, key="rej")
    if t > tn + 0.2:
        stamp(c, 640, 700, "NO NOTES", span(t, tn + 0.2, tn + 0.45), color="coral", rot=-12)
    for i, (w, x) in enumerate([("gold", 380), ("rice", 640), ("phone", 900)]):
        tw = T("month_two", w)
        qq = back_out(span(t, tw - 0.2, tw + 0.2))
        if qq > 0:
            if i == 0:
                gold_coin(c, x, 300, qq, t)
            elif i == 1:
                cutout(c, lambda k, x=x, qq=qq: k.drawRRect(rr(x - 80 * qq, 230, x + 80 * qq, 380, 30), paint("#F1E3C0")))
                type_text(c, "RICE", x, 310, 40 * qq + 1, 1.0)
            else:
                phone_msg(c, x, 310, 0.3 * qq + 0.01, t, [], key="trade", head="", head_col="#1E1E24")
    pill(c, 1500, 200, 1.0, "A FARMER IN NASHIK", "plum", size=40)


def s_zim(c, t, t0):
    collage_bg(c, t)
    dx, dy, a = jit("zimpaper", t)
    torn_strip(c, 960 + dx, 300 + dy, 1500, 220, seed=29, color="#F4EFE3", rot=-1.5)
    type_text(c, "ZIMBABWE, 2008", 960 + dx, 270 + dy, 96, span(t, T("month_two", "zimbabwe") - 0.2, T("month_two", "zimbabwe") + 0.5))
    type_text(c, "Government prints money to pay its bills", 960 + dx, 360 + dy, 44,
              span(t, T("month_two", "government") - 0.1, T("month_two", "bills") + 0.2))
    # printing press: notes sliding out from the start of the shot
    def press(k):
        body = skia.Path().addRRect(rr(80, 560, 420, 1000, 24))
        k.drawPath(body, paint("#6D597A")); halftone(k, body, "#1E1E24", 0.35, step=12)
        k.drawRect(skia.Rect(380, 700, 470, 760), paint("#2A2A33"))
        for i, ry in enumerate((660, 900)):
            k.drawCircle(250, ry, 70, paint("#B8BEC6")); k.drawCircle(250, ry, 24, paint("#4A4E57"))
    cutout(c, press)
    torn_strip(c, 250, 1010, 240, 60, seed=44, color="#FFF3C4")
    type_text(c, "MONEY PRESS", 250, 1010, 32, 1.0, color=RED_INK)
    for i in range(10):
        q = span(t, t0 + i * 0.3, t0 + 1.4 + i * 0.3)
        if q > 0:
            rupee_note(c, 520 + q * 1150, 680 + (i % 3) * 110, 0.7, t, key=f"zn{i}", rot=(rng(i) - 0.5) * 20, colr="#9CC5A1", val="Z$")


def s_double(c, t, t0):
    collage_bg(c, t)
    td = T("month_two", "doubled")
    days = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]
    for i, dn in enumerate(days):
        q = ease_out(span(t, td - 0.3 + i * 0.3, td + i * 0.3))
        if q > 0:
            x = 260 + i * 280
            index_card(c, x, 520, 230, 300, rot=(rng(i) - 0.5) * 6, seed=50 + i)
            type_text(c, dn, x, 430, 44, 1.0)
            type_text(c, f"{2 ** i}×", x, 560, 80 * q + 1, 1.0, color=RED_INK)
    headline(c, "PRICES DOUBLED ~EVERY DAY", 960, 860, 62, span(t, td, td + 0.7), seed=31)


def s_bignote(c, t, t0):
    collage_bg(c, t)
    big_note(c, 960, 520, 1.25, t)
    tw = T("month_two", "stopped")
    for i in range(int(12 * span(t, tw, tw + 1.6))):
        rupee_note(c, 200 + rng(i, 3) * 1500, 1000 - (t - tw) * 120 * rng(i, 5), 0.4, t, key=f"lit{i}", rot=rng(i, 7) * 80 - 40,
                   colr="#9CC5A1", val="Z$")
    if t > tw - 0.2:
        stamp(c, 1260, 820, "WORTHLESS", span(t, tw - 0.2, tw + 0.05), color="coral", rot=-10)


# ---------------------------------------------------------------- MONTH THREE
def s_remember(c, t, t0):
    collage_bg(c, t)
    house(c, 960, 900, 1.6, t, key="thehouse")
    for i, (fx, colr, fem) in enumerate([(-170, "#3D5A80", False), (-50, "#9C4F2E", True), (70, "#7B5E8B", True), (180, "#4F772D", False)]):
        if i == 2:
            grandma(c, 960 + fx, 900, 0.55, t, key="fam2")
        else:
            person(c, 960 + fx, 900, 0.55, t, color=colr, key=f"fam{i}", female=fem)
    tg = T("month_three", "grandmother")
    marker_circle(c, 1030, 760, 90, 130, span(t, tg - 0.3, tg + 0.3), width=14)
    big_text(c, "?", 1520, 380, 240, 1.0 - span(t, tg - 0.3, tg), "coral")
    if t > tg - 0.1:
        headline(c, "YOUR GRANDMOTHER", 960, 150, 66, span(t, tg - 0.1, tg + 0.5), seed=33)


def s_dadi(c, t, t0):
    collage_bg(c, t, tint="#E9DDC4")
    grandma(c, 560, 1000, 1.6, t, key="dadi_big")
    steel_tin(c, 880, 980, 1.0, t)
    tf = T("month_three", "forty")
    yrs = int(keys(t, [(tf - 0.3, 1986), (tf + 2.5, 2026)]))
    index_card(c, 1420, 420, 560, 300, rot=3, seed=35)
    type_text(c, "SAVINGS BOOK", 1420, 330, 44, 1.0, color=RED_INK)
    type_text(c, f"{yrs}", 1420, 440, 96, span(t, tf - 0.3, tf + 0.2))
    type_text(c, "+₹500  +₹200  +₹1,000", 1420, 520, 34, span(t, T("month_three", "little") - 0.2, T("month_three", "little") + 0.5))


def s_fd(c, t, t0):
    collage_bg(c, t)
    tn = T("month_three", "now")
    melt = span(t, tn, T("month_three", "twenty") + 0.6)
    fd_cert(c, 960, 520, 1.25, t, val="₹10,00,000" if melt < 0.6 else "≈ ₹20,000", melt=melt, key="fdbig")
    ts = T("month_three", "safety")
    if t < tn:
        pill(c, 960, 900, 1.0, "HER SAFETY", "teal", size=44) if t > ts - 0.2 else None
    tw = T("month_three", "twenty")
    if t > tw - 0.1:
        marker_circle(c, 960, 490, 330, 90, span(t, tw - 0.1, tw + 0.5), width=14)
    if t > T("month_three", "twenty") + 0.1:
        stamp(c, 1420, 820, "MELTED", span(t, T("month_three", "melted") - 0.2, T("month_three", "melted") + 0.05), color="coral", rot=-8)


def s_equal(c, t, t0):
    collage_bg(c, t)
    for i in range(4):
        x = 330 + i * 420
        if i == 2:
            grandma(c, x, 1000, 0.9, t, key="eq2")
        else:
            person(c, x, 1000, 0.9, t, color=["#3D5A80", "#9C4F2E", "", "#4F772D"][i], key=f"eq{i}", female=i == 1)
        note_stack(c, x + 120, 1000, 0.4, 4, t, key=f"eqs{i}")
    tb = T("month_three", "but")
    q = span(t, tb, tb + 0.8)
    if q < 1:
        note_stack(c, 1300, 1000, 0.4, 4 * (1 - q), t, key="oldsav")
    marker_circle(c, 1170, 820, 200, 240, span(t, tb + 0.3, tb + 0.9))
    if t > tb - 0.2:
        headline(c, "SAME CRORE. SAVINGS GONE.", 960, 160, 60, span(t, tb, tb + 0.7), seed=37)


# ---------------------------------------------------------------- PAYOFF
def s_real(c, t, t0):
    collage_bg(c, t)
    dx, dy, a = jit("notice", t)
    torn_strip(c, 960 + dx, 420 + dy, 1300, 420, seed=39, color="#F4EFE3", rot=-1)
    type_text(c, "THIS PART IS REAL", 960 + dx, 300 + dy, 70, span(t, t0, t0 + 0.6), color=RED_INK)
    tt = T("payoff", "target")
    ta = T("payoff", "already")
    type_text(c, "A SLOW VERSION IS ALREADY HAPPENING", 960 + dx, 400 + dy, 46, span(t, t0 + 0.6, ta + 0.4))
    type_text(c, "RBI INFLATION TARGET", 960 + dx, 500 + dy, 56, span(t, tt - 0.3, tt + 0.4))
    tf = T("payoff", "four")
    big_text(c, "4% A YEAR", 960, 700, 130, span(t, tf - 0.2, tf + 0.3), "coral")
    for i, (yr, pr) in enumerate([("2026", "₹40"), ("2027", "₹41.6"), ("2028", "₹43.3"), ("2029", "₹45")]):
        q = span(t, tf + 0.5 + i * 0.4, tf + 0.8 + i * 0.4)
        if q > 0:
            price_tag(c, 330 + i * 430, 930, 0.75, t, pr, key=f"yr{i}", rot=-4 + i * 3)
            type_text(c, yr, 330 + i * 430 - 15, 1030, 34, q)
    tape(c, 360, 230, 160, 48, -16); tape(c, 1560, 230, 160, 48, 14)


def s_18(c, t, t0):
    collage_bg(c, t)
    t18 = T("payoff", "eighteen")
    yrs = int(keys(t, [(t0, 2026), (t18 + 0.4, 2044)]))
    index_card(c, 520, 520, 520, 520, rot=-3, seed=41)
    type_text(c, "CALENDAR", 520, 330, 40, 1.0, color=RED_INK)
    type_text(c, f"{yrs}", 520, 540, 150, 1.0)
    tomato(c, 1250, 600, 1.1, t, key="t18")
    p = span(t, t18 - 0.6, t18 + 0.4)
    price_tag(c, 1560, 520, 1.1, t, "₹40" if p < 0.5 else "₹80", key="t18tag", rot=-8)
    if p > 0.5:
        stamp(c, 1500, 820, "PRICES ×2", span(t, t18, t18 + 0.25), color="coral", rot=-8)


def s_drip(c, t, t0):
    collage_bg(c, t)
    tm = T("payoff", "melts")
    melt = 0.15 + 0.25 * span(t, tm - 0.4, tm + 1.0)
    fd_cert(c, 960, 500, 1.0, t, melt=melt, key="fddrip")
    for i in range(3):
        q = ((t - t0) * 0.7 + i / 3) % 1
        c.drawCircle(760 + i * 200, 760 + q * 260, 14, paint("#F3E7C9", 1 - q))
    pill(c, 960, 960, 1.0, "A LITTLE, EVERY YEAR", "plum", size=44)


def s_saver(c, t, t0):
    collage_bg(c, t)
    grandma(c, 480, 1000, 1.25, t, key="saver")
    steel_tin(c, 760, 980, 0.9, t, key="tin2")
    index_card(c, 1300, 480, 860, 420, rot=2, seed=43)
    type_text(c, "COMMENT:", 1300, 340, 48, span(t, t0, t0 + 0.4), color=RED_INK)
    type_text(c, "Who's the best saver", 1300, 450, 56, span(t, t0 + 0.2, t0 + 0.8))
    type_text(c, "in your family?", 1300, 530, 56, span(t, t0 + 0.4, t0 + 1.0))
    ts = T("payoff", "send")
    if t > ts - 0.2:
        pill(c, 1300, 650, 1.0, "SEND THIS TO THEM", "coral", size=40)


# ---------------------------------------------------------------- BONUS
def s_skill(c, t, t0):
    collage_bg(c, t)
    for i, (hx, sl) in enumerate([(420, "#4F772D"), (960, "#7B5E8B"), (1500, "#3D5A80")]):
        q = ease_out(span(t, t0 + 0.2 + i * 0.3, t0 + 0.6 + i * 0.3))
        if q > 0:
            hand(c, hx, 1080 - 140 * q, 1.15, t, key=f"sk{i}", sleeve=sl)
    for i, lab in enumerate(["FARMER", "TAILOR", "YOU"]):
        torn_strip(c, 420 + i * 540, 390, 260, 70, seed=70 + i)
        type_text(c, lab, 420 + i * 540, 390, 40, span(t, t0 + 0.5 + i * 0.3, t0 + 1.0 + i * 0.3))
    tp = T("bonus", "printed")
    stamp(c, 960, 240, "PRICELESS", span(t, tp + 0.3, tp + 0.55), color="coral", rot=-8)
    type_text(c, "Money can be printed. Skill can't.", 960, 110, 52, span(t, tp - 0.5, tp + 0.3))


def s_kyc(c, t, t0):
    tb = T("bonus", "bank")
    lines = CREDIT if t < tb - 0.2 else [("PLEASE", 44, "#B3261E"), ("UPDATE", 50, "#B3261E"), ("YOUR KYC", 50, "#B3261E")]
    kitchen(c, t, lines=lines, buzz=1.0 - span(t, t0, t0 + 1.5), head="BANK", head_col="#1F6E43" if t < tb - 0.2 else "#B3261E",
            z=keys(t, [(t0, 1.12), (t0 + 5, 1.0)]), cx=960, cy=560)
    if t > T("bonus", "update") - 0.1:
        kr_cutout(c, lambda k: draw_kr(k, 1620, 1000, 0.95, "worried", t))


def s_tease(c, t, t0):
    collage_bg(c, t)
    days = ["MON", "TUE", "WED", "THU", "FRI"]
    tf = T("bonus", "fourday")
    for i, dn in enumerate(days):
        x = 360 + i * 300
        off = ease(span(t, tf + 0.2, tf + 0.9)) if dn == "FRI" else 0.0
        index_card(c, x + off * 200, 560 + off * 500, 240, 300, rot=(rng(i) - 0.5) * 6 + off * 40, seed=60 + i)
        type_text(c, dn, x + off * 200, 560 + off * 500, 64, 1.0, color=RED_INK if dn == "FRI" else INK)
    headline(c, "NEXT: WHAT IF INDIA HAD A 4-DAY WORK WEEK?", W / 2, 160, 50, span(t, t0, t0 + 1.0), seed=62)


def cont(fn, start, z1=1.18, cx=960.0, cy=540.0, dur=6):
    """Continue a shot (its own clock keeps running from `start`) with a push-in: a new framing, not a restart."""
    return zoom(lambda c, t, t0: fn(c, t, start), 1.0 + (z1 - 1.0) * 0.6, z1, cx, cy, dur)


# ---------------------------------------------------------------- the list
def SHOTS():
    s_ = {}
    s_["rep"] = T("promise", "i") - 0.2
    s_["call"] = T("hour_one", "you", 2) - 0.2
    s_["show"] = T("hour_six", "you") - 0.2
    s_["app"] = T("day_three", "delivery") - 0.3
    s_["x47"] = T("week_two", "heres") - 0.2
    s_["sc"] = T("week_two", "same") - 0.3
    s_["mandi"] = T("month_two", "farmer") - 0.4
    s_["fd"] = T("month_three", "for") - 0.2
    s_["real"] = B("payoff") - 0.1
    L = [
        (0.0, s_cold, "cut"),
        (T("hook", "not") - 0.2, s_everyone, "whip"),
        (T("hook", "and") - 0.25, s_who, "fade"),
        (E("hook") + 0.1, logo_sting(), "flash"),
        (E("hook") + 2.1, s_rules, "fade"),
        (s_["rep"], s_papers_reports, "fade"),
        (B("hour_one") - 0.6, card("HOUR 1", "The buzz"), "iris"),
        (T("hour_one", "check") - 0.5, s_check, "fade"),
        (T("hour_one", "for") - 0.2, s_fifty, "fade"),
        (s_["call"], s_call, "fade"),
        (T("hour_one", "then") - 0.2, s_website, "whip"),
        (B("hour_six") - 0.6, card("HOUR 6", "The showroom"), "iris"),
        (s_["show"], s_showroom, "fade"),
        (T("hour_six", "so") - 0.2, s_tag, "zoom"),
        (T("hour_six", "today") - 0.3, s_more, "fade"),
        (T("hour_six", "comment") - 0.6, comment_prompt("In one word: what would you buy first?"), "fade"),
        (B("day_three") - 0.6, card("DAY 3", "Nobody comes"), "iris"),
        (T("day_three", "doorbell") - 0.5, s_door, "fade"),
        (s_["app"], s_app, "whip"),
        (T("day_three", "sabzi") - 0.5, s_corner, "fade"),
        (T("day_three", "youre") - 0.3, s_bread, "fade"),
        (T("day_three", "thats") - 0.2, s_promise, "fade"),
        (B("week_two") - 0.6, card("WEEK 2", "The numbers"), "iris"),
        (T("week_two", "why") - 0.4, s_kidq, "fade"),
        (s_["x47"], s_x47, "whip"),
        (s_["sc"], s_scale, "fade"),
        (T("week_two", "so") - 0.2, s_prices, "fade"),
        (T("week_two", "ran") - 0.5, s_ran, "zoom"),
        (B("month_two") - 0.3, card("MONTH 2", "Nobody trusts the rupee"), "cut"),
        (s_["mandi"], s_mandi, "fade"),
        (T("month_two", "this") - 0.2, s_zim, "fade"),
        (T("month_two", "at") - 0.2, s_double, "whip"),
        (T("month_two", "they") - 0.2, s_bignote, "zoom"),
        (B("month_three") - 0.6, card("MONTH 3", "The saver"), "iris"),
        (T("month_three", "remember") - 0.2, s_remember, "fade"),
        (s_["fd"], s_dadi, "fade"),
        (T("month_three", "before") - 0.3, s_fd, "fade"),
        (T("month_three", "she", 2) - 0.2, s_equal, "fade"),
        (s_["real"], s_real, "fade"),
        (T("payoff", "at") - 0.2, s_18, "whip"),
        (T("payoff", "nobody") - 0.2, s_drip, "fade"),
        (T("payoff", "tell") - 0.2, s_saver, "fade"),
        (B("bonus") - 0.1, s_skill, "fade"),
        (T("bonus", "eight") - 0.3, s_kyc, "whip"),
        (T("bonus", "next") - 0.2, s_tease, "cut"),
        (E("bonus") + 0.3, end_screen(), "fade"),
        # pushes inside long shots (a new framing every 2-4 s)
        (T("hook", "every") + 0.6, cont(s_everyone, T("hook", "not") - 0.2, 1.15, 1300, 520), "cut"),
        (T("promise", "seven") + 0.9, cont(s_papers_reports, s_["rep"], 1.08, 960, 600), "cut"),
        (T("hour_one", "wedding") - 0.3, cont(s_call, s_["call"], 1.2, 960, 420), "cut"),
        (T("hour_six", "crowd") + 0.6, cont(s_showroom, s_["show"], 1.2, 1500, 640), "cut"),
        (T("hour_six", "changes") + 0.7, cont(s_tag, T("hour_six", "so") - 0.2, 1.2, 1100, 640), "cut"),
        (T("day_three", "seventyseven") - 0.4, cont(s_app, s_["app"], 1.12, 1300, 600), "cut"),
        (T("day_three", "money") - 0.2, cont(s_promise, T("day_three", "thats") - 0.2, 1.15, 960, 520), "cut"),
        (T("week_two", "morning") - 0.4, cont(s_x47, s_["x47"], 1.2, 1300, 520), "cut"),
        (T("week_two", "cars") + 0.3, cont(s_scale, s_["sc"], 1.2, 1100, 640), "cut"),
        (T("month_two", "wants") - 0.2, cont(s_mandi, s_["mandi"], 1.2, 700, 420), "cut"),
        (T("month_two", "government") - 0.2, cont(s_zim, T("month_two", "this") - 0.2, 1.15, 960, 500), "cut"),
        (T("month_two", "and", 2) - 0.2, cont(s_bignote, T("month_two", "they") - 0.2, 1.15, 1100, 600), "cut"),
        (T("month_three", "ten") - 0.3, cont(s_dadi, s_["fd"], 1.2, 1300, 460), "cut"),
        (T("month_three", "now") - 0.2, cont(s_fd, T("month_three", "before") - 0.3, 1.15, 960, 500), "cut"),
        (T("payoff", "but") - 0.2, cont(s_drip, T("payoff", "nobody") - 0.2, 1.1, 960, 620), "cut"),
        (T("bonus", "money") - 0.2, cont(s_skill, B("bonus") - 0.1, 1.15, 960, 400), "cut"),
        (T("bonus", "update") - 0.2, cont(s_kyc, T("bonus", "eight") - 0.3, 1.2, 1100, 560), "cut"),
        (T("promise", "no") - 0.2, cont(s_rules, E("hook") + 2.1, 1.15, 900, 480), "cut"),
        (T("week_two", "fortyseven") - 0.3, cont(s_x47, s_["x47"], 1.12, 1100, 560), "cut"),
        (T("week_two", "two", 2) - 0.3, cont(s_ran, T("week_two", "ran") - 0.5, 1.2, 1100, 600), "cut"),
        (T("payoff", "send") - 0.2, cont(s_saver, T("payoff", "tell") - 0.2, 1.2, 1200, 560), "cut"),
        (T("bonus", "but") - 0.2, cont(s_tease, T("bonus", "next") - 0.2, 1.15, 960, 420), "cut"),
                (T("day_three", "didi") - 0.2, cont(s_door, T("day_three", "doorbell") - 0.5, 1.1, 860, 640), "cut"),
        (T("month_three", "lifetime") - 0.2, cont(s_equal, T("month_three", "she", 2) - 0.2, 1.2, 1170, 760), "cut"),
    ]
    L.sort(key=lambda x: x[0])
    from krwi.timeline import TOTAL
    extra = []
    for i, (st, fn, tr) in enumerate(L):
        nm = getattr(fn, "__name__", "")
        d = (L[i + 1][0] if i + 1 < len(L) else TOTAL) - st
        if d > 4.5 and nm not in ("f", "logo_sting", "end_screen", "comment_prompt", "card", "s_cold"):
            extra.append((st + d / 2, cont(fn, st, 1.08, 900 + 60 * (i % 3), 560), "cut"))
    L += extra
    L.sort(key=lambda x: x[0])
    return L
