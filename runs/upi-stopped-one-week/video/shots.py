"""Shot list for 'What If UPI Stopped Working for One Week?' (style: collage).
Each shot: (start_time, fn(c, t, t0), transition). Times are anchored to words with T / at / B / E."""
import math
import skia
from art import *  # noqa: F401,F403


# ---------------------------------------------------------------- HOOK
def s_cold(c, t, t0):
    """Frame 0: the chai stall, the phone already says PAYMENT FAILED; the stamp slams in."""
    with CamC(c, keys(t, [(t0, 1.1), (t0 + 6, 1.18)]), 960, 560, t=t):
        stall(c, t)
        chai(c, 460, 640, 1.4, t)
        qr_sticker(c, 1500, 580, 1.05, t, key="stallqr", dead=0.3)
        phone(c, 940, 540, 1.15, t, screen="failed", p=span(t, t0, t0 + 0.4))
    pop(c, 400, 860, "\u20b910 CHAI", t, t0 + 0.6, color="coral", size=60)
    stamp(c, 1560, 930, "PAYMENT FAILED", span(t, t0 + 1.0, t0 + 1.25), color="coral", rot=-8)


def s_stopped(c, t, t0):
    collage_bg(c, t)
    headline(c, "82 CRORE PAYMENTS A DAY", W / 2, 260, 88, span(t, t0, t0 + 0.9), seed=3)
    # payments flying across, then freezing
    frz = T("hook", "gone")
    for i in range(14):
        tt = min(t, frz)
        x = (rng(i, 2) * W + (tt - t0) * (500 + 300 * rng(i))) % (W + 200) - 100
        y = 560 + rng(i, 5) * 380
        qr_sticker(c, x, y, 0.55, t, key=f"fly{i}", dead=1.0 if t > frz else 0.0)
    pop(c, W / 2, 420, "\u2248 9,500 EVERY SECOND", t, t0 + 1.0, color="coral", size=52)
    stamp(c, W / 2, 700, "STOPPED", span(t, frz, frz + 0.25), color="coral", rot=-8)


def s_week(c, t, t0):
    collage_bg(c, t)
    days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    for i, dname in enumerate(days):
        x = 250 + i * 236
        dx, dy, a = jit(f"day{i}", t)
        index_card(c, x + dx, 540 + dy, 210, 280, rot=(rng(i) - 0.5) * 6, seed=i + 2)
        type_text(c, dname, x + dx, 470 + dy, 44)
        type_text(c, "NO UPI", x + dx, 610 + dy, 42, 1.0, color=RED_INK)
        xmark(c, x, 560, 1.2, span(t, t0 + 0.2 + i * 0.22, t0 + 0.4 + i * 0.22))
    headline(c, "FOR 7 DAYS", W / 2, 860, 64, span(t, t0 + 0.3, t0 + 1.0), seed=6, rot=1.5)


def s_who(c, t, t0):
    collage_bg(c, t)
    c.saveLayer(None, skia.Paint(ColorFilter=skia.ColorFilters.Blend(col("#3A2E26", 0.85), skia.BlendMode.kSrcATop)))
    cart(c, 960, 900, 1.2, t)
    person(c, 1500, 900, 1.15, t, color="#2B2B2B", key="sabzi")
    c.restore()
    marker_circle(c, 1100, 640, 640, 330, span(t, t0 + 0.3, t0 + 1.0))
    big_text(c, "?", 1660, 420, 220, span(t, t0 + 0.7, t0 + 1.0), "coral")
    headline(c, "HIT HARDEST?", W / 2, 150, 60, span(t, t0 + 0.2, t0 + 0.9), seed=8)


# ---------------------------------------------------------------- PROMISE
def s_clip(c, t, t0):
    collage_bg(c, t)
    dx, dy, a = jit("clip", t)
    torn_strip(c, 760 + dx, 470 + dy, 980, 520, seed=11, color="#EFE8D6", rot=-3)
    type_text(c, "UPI DOWN", 760 + dx, 330 + dy, 92, span(t, t0, t0 + 0.6))
    type_text(c, "12 APRIL 2025", 760 + dx, 450 + dy, 54, span(t, t0 + 0.4, t0 + 1.0), color=RED_INK)
    type_text(c, "Payments failed across India", 760 + dx, 560 + dy, 47, span(t, t0 + 0.8, t0 + 1.6))
    tape(c, 340, 230, 160, 48, -20); tape(c, 1180, 230, 160, 48, 18)
    # clock: a 5-hour arc sweeps
    cx, cy = 1500, 720
    cutout(c, lambda k: k.drawPath(paper_circle(cx, cy, 170, 9), paint("#F4EFE3")))
    p = ease(span(t, t0 + 0.9, t0 + 2.2))
    arc = skia.Path(); arc.moveTo(cx, cy)
    arc.arcTo(skia.Rect(cx - 150, cy - 150, cx + 150, cy + 150), -90 + 30 * 11.67 - 360, 150 * p + 0.1, False); arc.close()
    c.drawPath(arc, paint("#E76F51", 0.8))
    for h in range(12):
        an = h / 12 * 2 * math.pi
        c.drawLine(cx + 130 * math.sin(an), cy - 130 * math.cos(an), cx + 150 * math.sin(an), cy - 150 * math.cos(an), paint(INK, stroke=6))
    big_text(c, "~5 HOURS", cx, 960, 56, span(t, t0 + 1.6, t0 + 2.0), "coral")


def s_stretch(c, t, t0):
    collage_bg(c, t)
    p = ease(span(t, t0 + 0.2, t0 + 1.6))
    w = 300 + 1300 * p
    torn_strip(c, W / 2, 540, w, 220, seed=13, color="#FFF3C4", rot=-1)
    tape(c, W / 2 - w / 2, 450, 140, 46, -12); tape(c, W / 2 + w / 2, 450, 140, 46, 12)
    if p < 0.5:
        type_text(c, "5 HOURS", W / 2, 540, 80, 1.0)
    else:
        type_text(c, "1 FULL WEEK", W / 2, 540, 100, span(t, t0 + 0.9, t0 + 1.5), color=RED_INK)
        for i in range(7):
            q = ease_out(span(t, t0 + 1.2 + i * 0.12, t0 + 1.5 + i * 0.12))
            if q > 0:
                x = 420 + i * 180
                index_card(c, x, 820, 140 * q + 1, 150 * q + 1, rot=(rng(i) - 0.5) * 8, seed=80 + i)
                type_text(c, ["M", "T", "W", "T", "F", "S", "S"][i], x, 820, 60 * q + 1, 1.0, color=RED_INK)
    big_text(c, "~5 HOURS", 300, 200, 56, 1.0 - span(t, t0 + 0.6, t0 + 1.0), "coral")


# ---------------------------------------------------------------- MINUTE ONE
def s_scan(c, t, t0):
    with CamC(c, keys(t, [(t0, 1.05), (t0 + 4, 1.15)]), 1300, 560, t=t):
        stall(c, t)
        qr_sticker(c, 1500, 520, 1.1, t, key="stallqr", dead=0.3)
        phone(c, 900, 560, 0.85, t, screen="scan" if t < T("minute_one", "failed") else "failed", rot=8)
    stamp(c, 900, 600, "FAILED", span(t, T("minute_one", "failed"), T("minute_one", "failed") + 0.25), color="coral")


APPS = [("Google Pay", "#4285F4"), ("PhonePe", "#5F259F"), ("Paytm", "#00BAF2")]


def s_apps(c, t, t0):
    collage_bg(c, t)
    for i, (name, colr) in enumerate(APPS):
        x = 480 + i * 480
        x2, y2, a = jit(f"app{i}", t)
        ap = ease_out(span(t, T("minute_one", ["google", "phonepe", "paytm"][i]) - 0.3, T("minute_one", ["google", "phonepe", "paytm"][i])))
        if ap <= 0:
            continue

        def d(k, x=x + x2, y=500 + y2, colr=colr, ap=ap):
            k.drawRRect(rr(x - 150 * ap, y - 150 * ap, x + 150 * ap, y + 150 * ap, 46 * ap), paint(colr))
            halftone(k, skia.Path().addRRect(rr(x - 150 * ap, y - 150 * ap, x + 150 * ap, y + 150 * ap, 46 * ap)), "#000000", 0.25)
        cutout(c, d)
        big_text(c, ['G', 'Pe', 'Pay'][i], x + x2, 530 + y2, 110 * ap, 1.0, 'cream')
        torn_strip(c, x, 740, 320, 70, seed=20 + i)
        type_text(c, name, x, 740, 52)
        tf = T("minute_one", "failed", i + 2)
        stamp(c, x + 70, 640, "FAILED", span(t, tf, tf + 0.2), color="coral", rot=-14 + i * 8)


def s_myth(c, t, t0):
    collage_bg(c, t)
    dx, dy, a = jit("mythcard", t)
    index_card(c, 620 + dx, 520 + dy, 760, 420, rot=-3, seed=4)
    type_text(c, "\"Google Pay", 620 + dx, 430 + dy, 54, span(t, t0, t0 + 0.6))
    type_text(c, "IS UPI\"", 620 + dx, 520 + dy, 70, span(t, t0 + 0.4, t0 + 0.9))
    stamp(c, 620, 640, "MYTH", span(t, T("minute_one", "theyre") - 0.1, T("minute_one", "theyre") + 0.15), color="coral", rot=-12)
    kr_cutout(c, lambda k: draw_kr(k, 1450, 860, 1.3, "pointing", t))


def s_share(c, t, t0):
    collage_bg(c, t)
    pie(c, 640, 560, 280, 0.778, span(t, t0 + 0.2, t0 + 1.4), t, col1="#00A3E0", split2=(0.456, "#5F259F"))
    headline(c, "ALMOST 8 IN 10", 1360, 380, 64, span(t, t0 + 0.6, t0 + 1.3), seed=5)
    type_text(c, "UPI payments go through", 1360, 520, 52, span(t, t0 + 1.0, t0 + 1.8))
    type_text(c, "just 2 apps", 1360, 590, 48, span(t, t0 + 1.4, t0 + 2.2), color=RED_INK)
    pill(c, 1260, 760, 1.0, "PhonePe", "plum", size=34)
    pill(c, 1520, 760, 1.0, "Google Pay", "teal", size=34)


def s_doors(c, t, t0):
    collage_bg(c, t)
    tclosed = T("minute_one", "closed")
    xs = [300, 700, 1100]
    for i, (name, colr) in enumerate(APPS):
        door(c, xs[i], 760, 1.0, t, colr, name, key=f"door{i}")
    house(c, 1620, 820, 1.0, t)
    torn_strip(c, 1620, 900, 340, 80, seed=31, color="#FFF3C4")
    type_text(c, "UPI · NPCI", 1620, 900, 57, span(t, T("minute_one", "behind"), T("minute_one", "behind") + 0.6))
    for i in range(3):
        red_string(c, [(xs[i] + 60, 520), (1520 + i * 30, 560)], span(t, T("minute_one", "same") + i * 0.15, T("minute_one", "same") + 0.8 + i * 0.15))
    # CLOSED sign swings in
    sp = span(t, tclosed - 0.2, tclosed + 0.3)
    if sp > 0:
        sw = math.sin((t - tclosed) * 6) * 12 * math.exp(-max(0, t - tclosed) * 2)
        c.save(); c.rotate(sw, 1620, 560)
        torn_strip(c, 1620, 690, 300, 100, seed=33, color="#C0392B", rot=0)
        type_text(c, "CLOSED", 1620, 690, 58, 1.0, color="#FFFFFF")
        c.restore()


# ---------------------------------------------------------------- HOUR THREE
def s_queue(c, t, t0):
    collage_bg(c, t)
    atm(c, 1700, 940, 1.0, t)
    n20, n50 = T("hour_three", "twenty"), T("hour_three", "fifty")
    n = int(keys(t, [(t0, 6), (n20, 20), (n50, 34)]))
    for i in range(n):
        x = 1460 - (i % 20) * 70 - (i // 20) * 35
        if i >= 20:
            continue
        if x < -60:
            break
        person(c, x, 960 - (i % 2) * 18, 0.62, t, color=["#3D5A80", "#9C4F2E", "#4F772D", "#6D597A", "#B5838D"][i % 5], key=f"q{i}")
    big = "20" if t < n50 else "50"
    if t > n20:
        headline(c, f"{big} PEOPLE", 520, 200, 70, 1.0, seed=7 if big == "20" else 9, rot=-3)


def s_lakh(c, t, t0):
    collage_bg(c, t)
    atm(c, 520, 960, 0.9, t, key="atm2")
    hgt = keys(t, [(t0 + 0.3, 1), (t0 + 2.5, 22)], ease_out)
    note_stack(c, 1300, 960, 0.9, hgt, t)
    headline(c, "₹1 LAKH CRORE / DAY", 1150, 140, 66, span(t, t0, t0 + 1.0), seed=12)
    type_text(c, "moved by UPI on a normal day", 1150, 250, 47, span(t, t0 + 0.8, t0 + 1.6))


def s_paper(c, t, t0):
    """'Now all of it wants to be paper': a phone turns into a flood of notes."""
    collage_bg(c, t)
    phone(c, 540, 540, 0.9, t, screen="qr", key="ph2")
    p = span(t, t0 + 0.3, t0 + 2.0)
    for i in range(16):
        q = clamp(p * 1.6 - i * 0.04, 0, 1)
        if q <= 0:
            continue
        x = 700 + ease_out(q) * (400 + rng(i) * 900)
        y = 540 + math.sin(i * 1.7) * 300 * ease_out(q)
        rupee_note(c, x, y, 0.6, t, key=f"fl{i}", rot=(rng(i, 3) - 0.5) * 50)


def s_out(c, t, t0):
    collage_bg(c, t)
    tt = T("hour_three", "temporarily")
    with CamC(c, keys(t, [(t0, 1.0), (tt, 1.25)]), 960, 560, t=t):
        atm(c, 960, 1020, 1.25, t, key="atm3", out=span(t, tt - 0.1, tt + 1.3))
    pop(c, 420, 300, "BY LUNCH", t, t0 + 0.2, color="coral", size=64)


def s_home(c, t, t0):
    collage_bg(c, t)
    # window with dadi's dabba quietly on the shelf (thread 3)
    dx, dy, a = jit("win", t)
    c.drawRect(skia.Rect(1250 + dx, 180 + dy, 1750 + dx, 600 + dy), paint("#F2B44C", 0.85))
    c.drawRect(skia.Rect(1250 + dx, 520 + dy, 1750 + dx, 540 + dy), paint("#6B4A2B"))
    dabba(c, 1420 + dx, 520 + dy, 0.45, t, key="dab0")
    c.drawRect(skia.Rect(1240 + dx, 170 + dy, 1760 + dx, 610 + dy), paint("#6B4A2B", stroke=20))
    c.drawLine(1500 + dx, 170 + dy, 1500 + dx, 610 + dy, paint("#6B4A2B", stroke=14))
    x = 1100 - (t - t0) * 90
    person(c, x, 1010, 1.5, t, color="#3D5A80", key="walker", walk=1.0, phone_glow=True, flip=True)
    headline(c, "A PHONE FULL OF MONEY", 620, 200, 64, span(t, T("hour_three", "holding") - 0.2, T("hour_three", "holding") + 0.8), seed=15)
    type_text(c, "...that you can't use", 620, 330, 72, span(t, T("hour_three", "cant") - 0.2, T("hour_three", "cant") + 0.6), color=RED_INK)


# ---------------------------------------------------------------- NIGHT ONE
def s_roads(c, t, t0):
    collage_bg(c, t)
    p = span(t, t0, t0 + 1.2)
    # thin roads
    for i, (name, y) in enumerate([("CARDS", 300), ("NET BANKING", 820)]):
        marker_line(c, [(150, y), (1770, y)], p, color="#7A6A50", width=26)
        torn_strip(c, 480, y - 80, 520, 100, seed=40 + i)
        type_text(c, name, 480, y - 80, 64, p)
        q = span(t, t0 + 1.0 + i * 0.3, t0 + 1.5 + i * 0.3)
        marker_line(c, [(1560, y - 90), (1610, y - 40), (1720, y - 170)], q, color="#2E8B57", width=20)
        type_text(c, "STILL OPEN", 1180, y - 80, 44, q, color="#2E7D32")
    marker_line(c, [(150, 560), (1770, 560)], p, color="#3A3530", width=110)
    for i in range(10):
        c.drawLine(200 + i * 170, 560, 270 + i * 170, 560, paint("#F4EFE3", stroke=10))
    torn_strip(c, 960, 450, 640, 96, seed=44, color="#FFF3C4")
    type_text(c, "UPI · BUSIEST ROAD", 960, 450, 57, span(t, T("night_one", "u") - 0.1, T("night_one", "u") + 0.6))
    stamp(c, 1400, 560, "BLOCKED", span(t, T("night_one", "busiest"), T("night_one", "busiest") + 0.25), color="coral", rot=-8)


def s_85(c, t, t0):
    collage_bg(c, t)
    pie(c, 640, 560, 280, 0.855, span(t, t0 + 0.1, t0 + 1.3), t, col1="#C0392B")
    headline(c, "85%", 1350, 400, 150, span(t, t0 + 0.4, t0 + 0.9), seed=17)
    type_text(c, "of India's digital payments", 1390, 570, 50, span(t, t0 + 0.7, t0 + 1.5))
    type_text(c, "go through UPI", 1390, 645, 57, span(t, t0 + 1.0, t0 + 1.8), color=RED_INK)


def s_kirana(c, t, t0):
    collage_bg(c, t)
    with CamC(c, keys(t, [(t0, 1.0), (t0 + 5, 1.1)]), 960, 640, t=t):
        counter_shop(c, 960, 1080, 1.0, t)
        qr_sticker(c, 700, 600, 0.8, t, key="kqr", cross=span(t, t0 + 0.6, t0 + 1.2))
        tno = T("night_one", "no")
        dash = paint(INK, 0.8, stroke=7); dash.setPathEffect(skia.DashPathEffect.Make([22, 14], 0))
        if t > tno - 0.2:
            c.drawRRect(rr(1150, 470, 1450, 740, 20), dash)
            torn_strip(c, 1300, 610, 420, 80, seed=48, color="#FFF3C4")
            type_text(c, "NO CARD MACHINE", 1300, 610, 44, span(t, tno, tno + 0.8), color=RED_INK)
            marker_circle(c, 1300, 610, 230, 180, span(t, tno + 0.4, tno + 1.0))
    headline(c, "YOUR LOCAL KIRANA", 960, 140, 58, span(t, t0, t0 + 0.8), seed=19)


def s_wallet(c, t, t0):
    collage_bg(c, t)
    kr_cutout(c, lambda k: draw_kr(k, 380, 900, 1.2, "curious", t))
    dx, dy, a = jit("wallet", t)

    def d(k):
        k.drawRRect(rr(1100 + dx, 420 + dy, 1600 + dx, 720 + dy, 30), paint("#5A3A22"))
        k.drawRRect(rr(1100 + dx, 420 + dy, 1600 + dx, 520 + dy, 30), paint("#6E4A2E"))
    cutout(c, d)
    rupee_note(c, 1350, 400 - 60 * ease_out(span(t, t0 + 0.5, t0 + 1.2)), 0.7, t, key="wn", colr="#7FB77E", val="100")
    comment_card(c, 1150, 900, 1.0, "How much cash is in your wallet right now?", span(t, T("night_one", "tell") - 0.4, T("night_one", "tell") + 0.4), t)


# ---------------------------------------------------------------- DAY THREE
def s_tags(c, t, t0):
    collage_bg(c, t)
    dx, dy, a = jit("tag600", t)
    index_card(c, W / 2 + dx, 540 + dy, 980, 560, rot=-3, seed=8)
    type_text(c, "AVERAGE UPI PAYMENT AT A SHOP", W / 2 + dx, 380 + dy, 46, span(t, t0, t0 + 0.8))
    type_text(c, "\u2248 \u20b9600", W / 2 + dx, 540 + dy, 170, span(t, t0 + 0.4, t0 + 1.0), color=RED_INK)
    type_text(c, "(2025)", W / 2 + dx, 700 + dy, 40, 1.0)
    tape(c, W / 2 - 380, 290, 160, 50, -14); tape(c, W / 2 + 380, 290, 160, 50, 12)


def s_change(c, t, t0):
    collage_bg(c, t)
    rupee_note(c, 600, 520, 1.7, t, key="big500")
    chai(c, 1400, 560, 1.4, t, key="chai2", steam=True)
    pop(c, 1380, 300, "₹10", t, t0 + 0.4, color="coral", size=48)
    type_text(c, "UPI made exact change. Every time.", 960, 900, 55, span(t, t0, t0 + 1.0))
    tn = T("day_three", "now")
    stamp(c, 960, 560, "NO CHANGE", span(t, tn, tn + 0.25), color="coral", rot=-10)


def s_chhutta(c, t, t0):
    collage_bg(c, t)
    person(c, 560, 1040, 1.7, t, color="#9C4F2E", key="shopkeeper")
    dx, dy, a = jit("bubble", t)
    p = ease_out(span(t, t0, t0 + 0.4))
    bub = skia.Path(); bub.addOval(skia.Rect(860 + dx, 260 + dy, 860 + 900 * p + dx, 260 + 380 * p + dy))
    tail = skia.Path(); tail.moveTo(940 + dx, 560 + dy); tail.lineTo(760, 640); tail.lineTo(1040 + dx, 600 + dy); tail.close()
    cutout(c, lambda k: (k.drawPath(bub, paint("#FFFFFF")), k.drawPath(tail, paint("#FFFFFF"))))
    if p > 0.9:
        type_text(c, "CHHUTTA", 1310 + dx, 400 + dy, 92, span(t, t0 + 0.3, t0 + 0.8), color=RED_INK)
        type_text(c, "NAHI HAI", 1310 + dx, 510 + dy, 92, span(t, t0 + 0.6, t0 + 1.1), color=RED_INK)


def s_cart(c, t, t0):
    collage_bg(c, t)
    tp = T("day_three", "today")
    cart(c, 820, 980, 1.35, t)
    person(c, 1420, 980, 1.35, t, color="#4F772D", key="sabzi")
    qr_sticker(c, 380, 640, 0.5, t, key="cartqr", cross=span(t, t0 + 0.4, t0 + 1.0))
    if t > tp - 0.3:
        for i in range(4):
            x = 2100 - (t - tp + 0.3) * (330 + 40 * i) - i * 300
            person(c, x, 1010 + i % 2 * 10, 0.75, t, color=["#3D5A80", "#6D597A", "#B5838D", "#264653"][i], key=f"pass{i}", walk=1.0, flip=True)
    headline(c, "THE SABZIWALA ON YOUR CORNER", 960, 140, 50, span(t, T("day_three", "sabziwala") - 0.2, T("day_three", "sabziwala") + 1.0), seed=23)
    tc = T("day_three", "cant")
    stamp(c, 1340, 560, "CAN'T PAY", span(t, tc, tc + 0.25), color="coral", rot=-10)


# ---------------------------------------------------------------- DAY FIVE
def s_5lakh(c, t, t0):
    collage_bg(c, t)
    v = keys(t, [(t0 + 0.2, 0), (t0 + 2.4, 5)], ease_out)
    headline(c, f"₹{v:.0f} LAKH CRORE", W / 2, 330, 96, 1.0, seed=25, rot=-1)
    pop(c, W / 2, 580, "= 5 NORMAL DAYS OF UPI", t, t0 + 1.8, color="coral", size=56)
    type_text(c, "that didn't move the normal way", W / 2, 470, 42, span(t, t0 + 1.2, t0 + 2.2))
    for i in range(5):
        x = 360 + i * 300
        person(c, x, 1000, 0.75, t, color=["#3D5A80", "#9C4F2E", "#4F772D", "#6D597A", "#B5838D"][i], key=f"f5{i}")
        red_string(c, [(W / 2, 620), (x, 720)], span(t, t0 + 1.6 + i * 0.15, t0 + 2.4 + i * 0.15))


def s_rider(c, t, t0):
    collage_bg(c, t)
    x = 700 + (t - t0) * 40
    person(c, x, 1020, 1.6, t, color="#264653", key="rider", bag=True)
    phone(c, 1400, 520, 0.75, t, key="riderph", screen="blank", rot=6)
    type_text(c, "TODAY'S PAY", 1400, 300, 52, span(t, t0 + 0.4, t0 + 1.0))
    td = T("day_five", "didnt")
    stamp(c, 1400, 870, "NOT PAID", span(t, td, td + 0.25), color="coral", rot=-12)


def s_cook(c, t, t0):
    collage_bg(c, t)
    person(c, 420, 980, 1.15, t, color="#B5838D", key="cook")
    house(c, 1550, 900, 0.9, t, key="village")
    torn_strip(c, 1550, 960, 300, 70, seed=51)
    type_text(c, "HOME VILLAGE", 1550, 960, 44, 1.0)
    p = span(t, t0 + 0.3, t0 + 1.6)
    br = T("day_five", "couldnt")
    dash = paint(RED_INK, 0.9, stroke=8); dash.setPathEffect(skia.DashPathEffect.Make([26, 16], 0))
    if t < br:
        c.drawLine(560, 600, 560 + (1400 - 560) * p, 600 - 80 * math.sin(p * math.pi), dash)
    else:
        c.drawLine(560, 600, 930, 560, dash)
        c.drawLine(1050, 560, 1400, 600, dash)
        xmark(c, 990, 560, 1.4, span(t, br, br + 0.3))


def s_breathe(c, t, t0):
    collage_bg(c, t)
    tb = T("day_five", "breathes")
    k = 28
    cut = paint("#E9D8A6")
    india_map(c, 960, 560, k, a=1.0)
    still = span(t, tb + 0.6, tb + 1.4)
    for i in range(70):
        x = 800 + rng(i, 2) * 330
        y = 330 + rng(i, 3) * 480
        pulse = 0.5 + 0.5 * math.sin(t * 4 + i)
        r = 8 + 10 * pulse * (1 - still)
        c.drawCircle(x, y, r, paint("gold", 0.25 + 0.6 * (1 - still)))
    headline(c, "UPI ISN'T AN APP", 1520, 380, 54, span(t, T("day_five", "isnt") - 0.4, T("day_five", "isnt") + 0.6), seed=27)
    type_text(c, "It's how", 1520, 520, 57, span(t, tb - 0.9, tb - 0.4), color=RED_INK)
    type_text(c, "India breathes.", 1520, 600, 57, span(t, tb - 0.6, tb + 0.4), color=RED_INK)


def s_khata(c, t, t0):
    collage_bg(c, t)
    lines = ["Sharma ji - chai, biscuit", "Room 4 - sabzi", "Bittu - doodh", "Auntie - atta, dal", "Pay me when UPI is back"]
    notebook(c, 760, 560, 1.15, t, lines, span(t, T("day_five", "notebook") - 0.2, T("day_five", "back", 1) + 0.5))
    headline(c, "UDHAAR", 760, 170, 80, span(t, T("day_five", "udhaar") - 0.2, T("day_five", "udhaar") + 0.4), seed=29)
    to = T("day_five", "oldest")
    torn_strip(c, 1560, 760, 520, 150, seed=30, color="#FFF3C4", rot=4) if t > to - 0.2 else None
    if t > to - 0.2:
        type_text(c, "INDIA'S OLDEST", 1560, 730, 52, span(t, to - 0.2, to + 0.4))
        type_text(c, "PAYMENT APP", 1560, 790, 52, span(t, to + 0.2, to + 0.8), color=RED_INK)


# ---------------------------------------------------------------- DAY SEVEN
def s_never(c, t, t0):
    collage_bg(c, t)
    with CamC(c, keys(t, [(t0, 1.0), (t0 + 4, 1.1)]), 960, 540, t=t):
        for i in range(9):
            rupee_note(c, 260 + i * 180, 820 + (i % 3) * 40, 0.8, t, key=f"nv{i}", rot=(rng(i) - 0.5) * 40,
                       colr=[NOTE, "#E8A15A", "#7FB77E"][i % 3], val=["500", "200", "100"][i % 3])
        headline(c, "THE CASH NEVER LEFT", W / 2, 420, 92, span(t, T("day_seven", "cash") - 0.4, T("day_seven", "left") + 0.2), seed=33, rot=-2)


def s_43(c, t, t0):
    collage_bg(c, t)
    v = keys(t, [(t0 + 0.1, 0), (t0 + 2.0, 43)], ease_out)
    headline(c, f"₹{v:.0f} LAKH CRORE", W / 2, 340, 104, 1.0, seed=35)
    type_text(c, "in notes and coins, right now", W / 2, 480, 44, span(t, t0 + 1.0, t0 + 1.8))
    note_stack(c, 430, 1000, 0.8, keys(t, [(t0, 1), (t0 + 2, 10)]), t, key="s43")
    note_stack(c, 1490, 1000, 0.8, keys(t, [(t0, 1), (t0 + 2, 10)]), t, key="t43")
    red_string(c, [(560, 760), (1360, 760)], span(t, t0 + 2.0, t0 + 2.6))
    stamp(c, W / 2, 760, "\u2248 6 WEEKS OF UPI", span(t, t0 + 2.4, t0 + 2.7), color="coral", rot=-6)


def s_both(c, t, t0):
    collage_bg(c, t)
    p = span(t, t0 + 0.2, t0 + 2.6)
    for name, colr, amp, y0, ly in [("UPI", "#5F259F", 640, 900, 0), ("CASH", "#2E8B57", 300, 860, 1)]:
        pts = []
        for i in range(31):
            u = i / 30
            if u > p:
                break
            pts.append((200 + u * 1500, y0 - amp * (u ** (2.2 if name == "UPI" else 1.1))))
        if len(pts) > 1:
            marker_line(c, pts, 1.0, color="#F4EFE3", width=40)
            marker_line(c, pts, 1.0, color=colr, width=24)
            x, y = pts[-1]
            pill(c, min(x + 60, 1700), y - 50, 1.0, name, "plum" if name == "UPI" else "teal", size=46)
    marker_line(c, [(200, 920), (1760, 920)], 1.0, color=INK, width=6)
    type_text(c, "2016", 300, 975, 46, 1.0); type_text(c, "TODAY", 1640, 975, 46, 1.0)
    headline(c, "BOTH WENT UP", 700, 160, 56, span(t, T("day_seven", "even") + 0.6, T("day_seven", "even") + 1.4), seed=37)


def s_dabba(c, t, t0):
    collage_bg(c, t)
    # kitchen shelf
    c.drawRect(skia.Rect(200, 760, 1720, 800), paint("#6B4A2B"))
    for i, xx in enumerate([380, 1450, 1620]):
        dabba(c, xx, 760, 0.5, t, key=f"jar{i}")
    td = T("day_seven", "dadis")
    dabba(c, 920, 760, 1.0, t, open_p=span(t, td + 0.4, td + 1.2), key="dabbamain")
    tr = T("day_seven", "right", 2)
    stamp(c, 960, 260, "DADI WAS RIGHT", span(t, tr - 0.1, tr + 0.2), color="coral", rot=-8)
    kr_cutout(c, lambda k: draw_kr(k, 1700, 960, 0.65, "happy", t))


def s_123(c, t, t0):
    collage_bg(c, t)
    keypad_phone(c, 620, 560, 1.4, t)
    headline(c, "NO SMARTPHONE?", 1320, 330, 60, span(t, t0, t0 + 0.8), seed=39)
    type_text(c, "UPI on a basic phone", 1320, 480, 57, span(t, t0 + 0.6, t0 + 1.4))
    tn = T("day_seven", "internet")
    stamp(c, 1320, 640, "NO INTERNET NEEDED", span(t, tn - 0.3, tn), color="coral", rot=-6)


# ---------------------------------------------------------------- PAYOFF
def s_back(c, t, t0):
    """Callback to frame 0: same stall, same framing; this time it works."""
    ts = T("payoff", "successful")
    ok = t > ts - 0.15
    with CamC(c, keys(t, [(t0, 1.1), (t0 + 6, 1.18)]), 960, 560, t=t):
        stall(c, t)
        chai(c, 460, 640, 1.4, t)
        qr_sticker(c, 1500, 580, 1.05, t, key="stallqr")
        phone(c, 940, 540, 1.15, t, screen="success" if ok else "scan", p=span(t, ts - 0.15, ts + 0.3))
    if ok:
        stamp(c, 1400, 900, "PAYMENT SUCCESSFUL", span(t, ts, ts + 0.25), color="#2E8B57", rot=-5)
        glow(c, 960, 430, 260, "gold", 0.3 * (1 - span(t, ts, ts + 1.5)))


def s_world(c, t, t0):
    collage_bg(c, t)
    pie(c, 520, 560, 300, 0.49, span(t, t0 + 0.2, t0 + 1.4), t, col1="#E07A1F", col2="#2F5D8A", key="world")
    marker_circle(c, 600, 560, 200, 330, span(t, t0 + 1.2, t0 + 1.9))
    headline(c, "NEARLY HALF", 1360, 360, 80, span(t, t0 + 0.5, t0 + 1.2), seed=41)
    type_text(c, "of the world's real-time payments", 1380, 500, 48, span(t, t0 + 0.9, t0 + 1.7))
    type_text(c, "happen in India", 1360, 570, 48, span(t, t0 + 1.3, t0 + 2.1), color=RED_INK)
    tl = T("payoff", "little")
    pop(c, 1380, 780, "...all on one little sound", t, tl - 0.4, color="coral", size=54)


# ---------------------------------------------------------------- extra shots (keep a change every 2-4 s)
def s_onedoor(c, t, t0):
    collage_bg(c, t)
    door(c, 960, 860, 1.5, t, "#5F259F", "AN APP", key="onedoor")
    headline(c, "JUST A DOOR", 960, 160, 70, span(t, t0 + 0.1, t0 + 0.8), seed=43)


def s_counted(c, t, t0):
    collage_bg(c, t)
    for i, (w, word) in enumerate([("COUNTED", "counted"), ("CARRIED", "carried"), ("KEPT IN A DRAWER", "drawer")]):
        tw = T("hour_three", word)
        q = ease_out(span(t, tw - 0.3, tw + 0.1))
        if q <= 0:
            continue
        x, y = 480 + i * 480, 520 + (i % 2) * 60
        index_card(c, x, y, 400 * q + 1, 220 * q + 1, rot=-4 + i * 4, seed=60 + i)
        type_text(c, w, x, y - 20, 40 * q + 1, 1.0)
        xmark(c, x, y + 60, 0.8, span(t, tw + 0.1, tw + 0.4))
    headline(c, "UPI MONEY WAS NEVER...", 960, 180, 54, span(t, t0, t0 + 0.8), seed=45)


def s_nocash(c, t, t0):
    collage_bg(c, t)
    for i in range(3):
        x = 420 + i * 540
        person(c, x, 980, 0.95, t, color=["#3D5A80", "#6D597A", "#264653"][i], key=f"nc{i}", phone_glow=True)
        dx, dy, a = jit(f"wl{i}", t)
        cutout(c, lambda k, x=x: k.drawRRect(rr(x + 80 + dx, 520 + dy, x + 260 + dx, 640 + dy, 20), paint("#5A3A22")))
        type_text(c, "EMPTY", x + 170, 580, 42, span(t, t0 + 0.5 + i * 0.2, t0 + 1.0 + i * 0.2), color="#F4EFE3")
    headline(c, "CASH? NOT FOR YEARS", 960, 170, 60, span(t, t0 + 0.1, t0 + 0.9), seed=47)


def s_small(c, t, t0):
    collage_bg(c, t)
    for i, (w, word) in enumerate([("CHAI", "chai"), ("AUTO", "auto"), ("DHANIYA", "dhaniya")]):
        tw = T("day_three", word)
        q = ease_out(span(t, tw - 0.2, tw + 0.2))
        if q > 0:
            x, y = 420 + i * 540, 540 + (i % 2) * 80
            tape(c, x, y - 130, 110, 40, -10 + i * 8)
            index_card(c, x, y, 320 * q + 1, 200 * q + 1, rot=6 - i * 5, seed=10 + i)
            type_text(c, w, x, y + 40, 60 * q + 1, 1.0)
            if i == 0:
                chai(c, x, y - 250, 0.9 * q + 0.01, t, key="smallchai")
            elif i == 2:
                for j in range(9):
                    c.drawCircle(x - 80 + (j % 3) * 60 + rng(j) * 20, y - 260 + (j // 3) * 50, 34 * q, paint("#4F9D2D"))
                    halftone(c, skia.Path().addCircle(x - 80 + (j % 3) * 60 + rng(j) * 20, y - 260 + (j // 3) * 50, 34 * q), "#1E4D12", 0.3, step=10)
            else:
                auto(c, x, y - 200, 0.8 * q + 0.01, t)
    headline(c, "LOTS ARE FAR SMALLER", 960, 170, 56, span(t, t0, t0 + 0.8), seed=21)


def s_growth(c, t, t0):
    collage_bg(c, t)
    p = span(t, t0 + 0.1, t0 + 1.2)
    marker_line(c, [(500, 900), (900, 700), (1150, 760), (1500, 300)], p, color="#2E8B57", width=26)
    if p >= 1:
        marker_line(c, [(1500, 300), (1400, 320)], 1.0, color="#2E8B57", width=26)
        marker_line(c, [(1500, 300), (1480, 400)], 1.0, color="#2E8B57", width=26)
    note_stack(c, 400, 1000, 0.6, 6, t, key="gr")
    stamp(c, 1150, 930, "FASTEST GROWTH IN 5 YEARS", span(t, t0 + 0.2, t0 + 0.5), color="coral", rot=-6)


def s_tease(c, t, t0):
    collage_bg(c, t)
    nozzle(c, 760, 560, 1.3, t)
    dx, dy, a = jit("ptag", t)
    index_card(c, 1350 + dx, 560 + dy, 360, 220, rot=6, seed=70)
    type_text(c, "\u20b90 / L", 1350 + dx, 560 + dy, 90, span(t, t0 + 0.4, t0 + 1.0), color=RED_INK)
    headline(c, "NEXT: WHAT IF PETROL BECAME FREE IN INDIA?", W / 2, 150, 54, span(t, t0, t0 + 1.2), seed=72)


def cont(fn, start, z1=1.18, cx=960.0, cy=540.0, dur=6):
    """Continue a shot (its own clock keeps running from `start`) with a push-in: a new framing, not a restart."""
    return zoom(lambda c, t, t0: fn(c, t, start), 1.0 + (z1 - 1.0) * 0.6, z1, cx, cy, dur)


# ---------------------------------------------------------------- the list
def SHOTS():
    m1 = T("minute_one", "heres") - 0.2
    dr = T("minute_one", "behind") - 0.3
    kr_ = T("night_one", "but") - 0.2
    wl = T("night_one", "quick") - 0.2
    ct = T("day_three", "remember") - 0.3
    kh = T("day_five", "so") - 0.2
    f43 = T("day_seven", "right") - 0.2
    bo = T("day_seven", "even") - 0.2
    p123 = T("day_seven", "smartphone") - 1.0
    bk = T("payoff", "you") - 0.2
    wd = T("payoff", "india") - 0.2
    L = [
        (0.0, s_cold, "cut"),
        (T("hook", "not") - 0.2, s_stopped, "whip"),
        (T("hook", "for") - 0.2, s_week, "fade"),
        (T("hook", "and", 2) - 0.25, s_who, "fade"),
        (E("hook") + 0.1, logo_sting(), "flash"),
        (T("promise", "u") - 0.3, s_clip, "fade"),
        (T("promise", "lets") - 0.3, s_stretch, "zoom"),
        (B("minute_one") - 0.6, card("MINUTE 1", "The chai stall"), "iris"),
        (T("minute_one", "you", 1) - 0.2, s_scan, "fade"),
        (T("minute_one", "switch") - 0.3, s_apps, "whip"),
        (m1, s_myth, "fade"),
        (T("minute_one", "almost") - 0.2, s_share, "fade"),
        (dr, s_doors, "zoom"),
        (B("hour_three") - 0.6, card("HOUR 3", "The ATM line"), "iris"),
        (T("hour_three", "line") - 0.5, s_queue, "fade"),
        (T("hour_three", "heres") - 0.2, s_lakh, "fade"),
        (T("hour_three", "all") - 0.4, s_paper, "whip"),
        (T("hour_three", "by") - 0.2, s_out, "fade"),
        (T("hour_three", "some") - 0.2, s_home, "fade"),
        (B("night_one") - 0.6, card("NIGHT 1", "The shops"), "iris"),
        (T("night_one", "u") - 0.4, s_roads, "fade"),
        (T("night_one", "about") - 0.2, s_85, "fade"),
        (kr_, s_kirana, "fade"),
        (wl, s_wallet, "zoom"),
        (B("day_three") - 0.6, card("DAY 3", "Chhutta"), "iris"),
        (T("day_three", "last") - 0.2, s_tags, "fade"),
        (T("day_three", "for") - 0.2, s_change, "fade"),
        (T("day_three", "chhutta") - 0.3, s_chhutta, "whip"),
        (ct, s_cart, "fade"),
        (B("day_five") - 0.3, card("DAY 5", "The slowdown"), "cut"),
        (T("day_five", "five", 2) - 0.3, s_5lakh, "fade"),
        (T("day_five", "delivery") - 0.3, s_rider, "fade"),
        (T("day_five", "cook") - 0.3, s_cook, "fade"),
        (T("day_five", "this") - 0.2, s_breathe, "zoom"),
        (kh, s_khata, "fade"),
        (B("day_seven") - 0.6, card("DAY 7", "The twist"), "iris"),
        (T("day_seven", "cash") - 0.6, s_never, "fade"),
        (f43, s_43, "zoom"),
        (bo, s_both, "fade"),
        (T("day_seven", "your") - 0.2, s_dabba, "fade"),
        (p123, s_123, "fade"),
        (B("payoff") - 0.6, card("DAY 8", "Back at the stall"), "iris"),
        (bk, s_back, "fade"),
        (wd, s_world, "fade"),
        (T("payoff", "so") - 0.2, comment_prompt("After this, would you keep more cash at home?"), "fade"),
        (T("payoff", "next") - 0.2, s_tease, "cut"),
        (E("payoff") + 0.3, end_screen(), "fade"),
        # splits
        (T("minute_one", "failed", 3) - 0.1, cont(s_apps, T("minute_one", "switch") - 0.3, 1.2, 960, 520), "cut"),
        (T("minute_one", "two") - 0.3, cont(s_share, T("minute_one", "almost") - 0.2, 1.2, 1300, 520), "cut"),
        (T("hour_three", "one") - 0.2, cont(s_lakh, T("hour_three", "heres") - 0.2, 1.2, 1200, 600), "cut"),
        (T("hour_three", "machine") - 0.2, cont(s_out, T("hour_three", "by") - 0.2, 1.15, 960, 600), "cut"),
        (T("day_five", "couldnt") - 0.3, cont(s_cook, T("day_five", "cook") - 0.3, 1.2, 960, 600), "cut"),
        (T("day_five", "breathes") - 0.3, cont(s_breathe, T("day_five", "this") - 0.2, 1.25, 1100, 560), "cut"),
        (T("minute_one", "doors") - 0.4, s_onedoor, "whip"),
        (T("minute_one", "change") - 0.2, cont(s_doors, dr, 1.3, 1620, 700), "cut"),
        (T("hour_three", "thats") - 0.2, s_counted, "fade"),
        (T("night_one", "and", 1) - 0.2, cont(s_kirana, kr_, 1.25, 1300, 620), "cut"),
        (T("night_one", "tell") - 0.6, cont(s_wallet, wl, 1.2, 1350, 800), "cut"),
        (T("day_three", "lots") - 0.2, s_small, "fade"),
        (T("day_three", "his") - 0.2, s_nocash, "fade"),
        (T("day_three", "today") - 0.3, s_cart, "fade"),
        (T("day_five", "oldest") - 0.4, cont(s_khata, kh, 1.25, 1300, 700), "cut"),
        (T("day_seven", "growing") - 0.2, s_growth, "zoom"),
        (T("day_seven", "not") - 0.2, cont(s_both, bo, 1.2, 1300, 500), "cut"),
        (T("day_seven", "works") - 0.2, cont(s_123, p123, 1.15, 1000, 600), "cut"),
        (T("payoff", "scan") - 0.2, cont(s_back, bk, 1.35, 1130, 520), "cut"),
        (T("payoff", "and", 2) - 0.2, cont(s_world, wd, 1.15, 1300, 560), "cut"),
        (T("payoff", "but") - 0.2, cont(s_tease, T("payoff", "next") - 0.2, 1.15), "cut"),
    ]
    L.sort(key=lambda x: x[0])
    return L
