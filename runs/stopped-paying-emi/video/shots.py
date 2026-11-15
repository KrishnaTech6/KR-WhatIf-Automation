"""Shot list for 'What If You Stopped Paying Your EMI?' (style: collage).
Each shot: (start_time, fn(c, t, t0), transition). Times are anchored to words with T / at / B / E."""
import math
import skia
from art import *  # noqa: F401,F403

GREY = "#5C6670"


def cont(fn, start, z1=1.18, cx=960.0, cy=540.0, dur=6):
    """Continue a shot (its own clock keeps running from `start`) with a push-in: a new framing, not a restart."""
    return zoom(lambda c, t, t0: fn(c, t, start), 1.0 + (z1 - 1.0) * 0.6, z1, cx, cy, dur)


def kr(c, x, y, s, expr, t):
    kr_cutout(c, lambda k: draw_kr(k, x, y, s, expr, t))


# ---------------------------------------------------------------- HOOK
def s_cold(c, t, t0):
    """Frame 0: the house is the hero, the AUCTION? stamp hovers over it; a torn SMS strip says why (thumbnail echo)."""
    collage_bg(c, t)
    with CamC(c, keys(t, [(t0, 1.0), (t0 + 4, 1.08)]), 960, 600, t=t):
        house_lock(c, 960, 1040, 2.0, t)
        bob = math.sin(t * 5) * 8
        c.save(); c.translate(0, bob)
        stamp(c, 960, 640, "AUCTION?", 1.0, rot=-8)
        c.restore()
    torn_strip(c, 330, 860, 480, 150, seed=4, color="#F4C7C0", rot=-6)
    type_text(c, "SMS: EMI NOT PAID", 330, 860, 46, 1.0, color=RED_INK)
    headline(c, "EMI STOPPED", 960, 110, 96, 1.0, seed=3)


def s_91(c, t, t0):
    collage_bg(c, t)
    d = int(keys(t, [(t0, 1), (T("hook", "days") + 0.2, 91)], ease_out))
    wall_calendar(c, 560, 540, 1.25, t, d)
    loan_file(c, 1360, 600, 1.1, t, "YOUR LOAN")
    td = T("hook", "defaulter")
    stamp(c, 1360, 640, "DEFAULTER", span(t, td - 0.1, td + 0.15), rot=-10)


def s_nocourt(c, t, t0):
    collage_bg(c, t)
    court(c, 520, 900, 0.95, t)
    xmark(c, 520, 620, 2.6, span(t, t0 + 0.2, t0 + 0.6))
    house_lock(c, 1400, 920, 1.2, t, key="hl2")
    th = T("hook", "home")
    p = span(t, th - 0.2, th + 0.4)
    if p > 0:     # the stamp hovers, never lands (held back to Month 6)
        bob = math.sin(t * 5) * 10
        c.save(); c.translate(0, -60 + bob)
        stamp(c, 1400, 520, "AUCTION?", min(p, 0.55), rot=-8)
        c.restore()
    headline(c, "NO COURT NEEDED", 520, 160, 60, span(t, t0, t0 + 0.8), seed=5)


def s_sig(c, t, t0):
    collage_bg(c, t)
    tp = T("hook", "paper")
    with CamC(c, keys(t, [(t0, 1.25), (t0 + 3.5, 1.0)]), 1080, 720, t=t):
        signature_form(c, 960, 560, 1.0, t, "LOAN AGREEMENT", sig_p=span(t, t0, t0 + 1.0),
                       circle=span(t, tp - 0.1, tp + 0.6), key="form0")
    big_text(c, "?", 1500, 360, 200, span(t, tp + 0.3, tp + 0.6), "coral")


# ---------------------------------------------------------------- PROMISE
def s_papers14(c, t, t0):
    """Effort beat: 14 real documents land one by one, counter 1 -> 14."""
    collage_bg(c, t)
    names = ["RBI 2021", "RBI 2022", "RBI 2023", "RBI 2023", "RBI 2024", "SARFAESI", "RULES 2002",
             "NI ACT 138", "PSS ACT 25", "CONTRACT ACT", "CIC REGS", "SC 2019", "SC 2021", "SC 2014"]
    tf = T("promise", "fourteen")
    p = span(t, t0 + 0.2, tf + 1.2)
    n = int(p * 14 + 0.001)
    for i in range(min(14, n)):
        x = 200 + (i % 7) * 253 + (rng(i, 2) - 0.5) * 30
        y = 420 + (i // 7) * 300 + (rng(i, 3) - 0.5) * 30
        index_card(c, x, y, 240, 260, rot=(rng(i, 5) - 0.5) * 14, seed=40 + i)
        type_text(c, names[i], x, y, 36)
    counter_text(c, 0, 14, p, lambda v: f"{v:.0f} / 14", W / 2, 1000, 110, "coral")
    headline(c, "RBI RULES · LAWS · SUPREME COURT", W / 2, 140, 52, span(t, t0, t0 + 1.0), seed=8)


def s_loan(c, t, t0):
    collage_bg(c, t)
    house(c, 520, 900, 1.4, t, key="h_loan")
    dx, dy, a = jit("loancard", t)
    index_card(c, 1300 + dx, 450 + dy, 760, 300, rot=-2, seed=12)
    type_text(c, "HOME LOAN", 1300 + dx, 390 + dy, 56, span(t, t0, t0 + 0.6))
    type_text(c, "₹30 LAKH", 1300 + dx, 490 + dy, 92, span(t, t0 + 0.3, t0 + 0.9), color=RED_INK)
    te = T("promise", "your")
    index_card(c, 1300, 800, 640, 200, rot=3, seed=13)
    type_text(c, "EMI ≈ ₹26,000 / month", 1300, 800, 50, span(t, te, te + 0.8))


def s_dont(c, t, t0):
    collage_bg(c, t)
    wallet(c, 640, 600, 1.2, t)
    type_text(c, "WALLET: ₹0", 640, 880, 56, 1.0, color=RED_INK)
    kr(c, 1380, 940, 1.35, "worried", t)
    headline(c, "THIS MONTH: ₹0", 640, 260, 70, span(t, t0 + 0.2, t0 + 0.9), seed=14)


# ---------------------------------------------------------------- DAY 1
def s_midnight(c, t, t0):
    collage_bg(c, t, tint="#20263A")
    wall_clock(c, 420, 420, 1.0, t, 0, 0)
    # the auto-debit arrow flies at an empty account and bounces off
    tk = T("day_one", "knocks")
    p = span(t, tk - 0.3, tk + 0.5)
    q = span(t, tk + 0.5, tk + 1.2)
    ax = 700 + 600 * ease(p) - 350 * ease_out(q)
    ay = 560 - 120 * math.sin(math.pi * q)
    dx, dy, a = jit("acct", t)
    index_card(c, 1500 + dx, 560 + dy, 420, 300, rot=3, seed=20)
    type_text(c, "YOUR ACCOUNT", 1500 + dx, 470 + dy, 40)
    type_text(c, "₹0", 1500 + dx, 590 + dy, 130, 1.0, color=RED_INK)
    torn_strip(c, ax, ay, 300, 90, seed=21, color="#FFF3C4", rot=-4 + 30 * q)
    type_text(c, "AUTO-DEBIT >>", ax, ay, 40)
    te = T("day_one", "empty")
    stamp(c, 1500, 740, "EMPTY", span(t, te - 0.1, te + 0.15), rot=-6)
    type_text(c, "12:00 AM", 420, 680, 48, 1.0, color="#F4EFE3")


def s_computer(c, t, t0):
    collage_bg(c, t)
    dx, dy, a = jit("comp", t)

    def d(k):
        k.drawRRect(rr(560 + dx, 260 + dy, 1100 + dx, 640 + dy, 18), paint("#D8D2C2"))
        k.drawRect(skia.Rect(600 + dx, 300 + dy, 1060 + dx, 600 + dy), paint("#123247"))
        k.drawRect(skia.Rect(780 + dx, 640 + dy, 880 + dx, 720 + dy), paint("#B8B0A0"))
        k.drawRect(skia.Rect(680 + dx, 720 + dy, 980 + dx, 760 + dy), paint("#B8B0A0"))
    cutout(c, d)
    type_text(c, "DAY-END RUN", 830, 380, 40, 1.0, color="#9FD8A8")
    type_text(c, "LOAN #4471", 830, 450, 40, span(t, t0 + 0.3, t0 + 0.9), color="#9FD8A8")
    to = T("day_one", "overdue")
    stamp(c, 830, 540, "OVERDUE", span(t, to - 0.1, to + 0.15), rot=-6)
    tm = T("day_one", "manager")
    headline(c, "NOT A MANAGER.", 1460, 400, 54, span(t, min(t0 + 0.6, tm - 0.3), tm + 0.3), seed=22)
    tc = T("day_one", "computer", 2)
    headline(c, "A COMPUTER.", 1460, 560, 66, span(t, min(t0 + 1.2, tc - 0.3), tc + 0.3), seed=23, color="#FFF3C4")


def s_sms(c, t, t0):
    collage_bg(c, t)
    tb = T("day_one", "bounced")
    tf = T("day_one", "fine")
    lines = [("EMI BOUNCED", "#C0392B"), ("FINE ₹500\n+ GST", "#7A4B2A")]
    p = max(0.5 * span(t, t0, t0 + 0.4), 0.5 * span(t, tb - 0.3, tb + 0.2)) + 0.5 * span(t, min(t0 + 1.4, tf - 0.3), min(t0 + 1.8, tf + 0.2))
    smartphone(c, 760, 560, 1.15, t, lines, p, title="2 NEW SMS", key="sp2", rot=3)
    kr(c, 1450, 960, 1.3, "shocked", t)
    pop(c, 1450, 260, "GOOD MORNING...", t, t0 + 0.2, color="coral", size=48)


def s_fine(c, t, t0):
    collage_bg(c, t)
    dx, dy, a = jit("fine", t)
    index_card(c, 760 + dx, 520 + dy, 820, 440, rot=-3, seed=24)
    type_text(c, "BOUNCE CHARGE", 760 + dx, 400 + dy, 62, span(t, t0, t0 + 0.6))
    type_text(c, "₹500 + GST", 760 + dx, 530 + dy, 104, span(t, t0 + 0.3, t0 + 0.9), color=RED_INK)
    type_text(c, "a fine for the failed auto-debit", 760 + dx, 640 + dy, 38, span(t, t0 + 0.7, t0 + 1.4))
    pill(c, 1500, 400, 1.2, "HDFC BANK (2025)", "teal", size=36)
    rupee_note(c, 1500, 720, 1.1, t, key="fn1", rot=-8)


def s_fear(c, t, t0):
    """The tangled spiral of interest-on-interest gets cut into one flat tag."""
    collage_bg(c, t)
    tc = T("day_one", "cant")
    cut = span(t, tc - 0.1, tc + 0.6)
    cx, cy = 760, 560
    if cut < 1:
        pth = skia.Path(); pth.moveTo(cx, cy)
        for i in range(1, 160):
            an = i * 0.2
            r = 4 + i * 1.8
            pth.lineTo(cx + r * math.cos(an + t), cy + r * math.sin(an + t))
        c.drawPath(pth, paint(RED_INK, 1 - cut, stroke=9))
        type_text(c, "interest on interest on...", cx, 180, 54, span(t, t0, t0 + 0.8), color=RED_INK)
    if cut > 0.15:
        torn_strip(c, cx, 880, 560 * ease_out(cut) + 1, 140, seed=26, color="#FFF3C4", rot=-3)
        type_text(c, "FLAT PENAL CHARGE", cx, 880, 50, cut)
    if t < tc:
        stamp(c, cx, 960, "FEAR", span(t, t0 + 0.4, t0 + 0.6), rot=-8)
    ts = T("day_one", "since")
    dx, dy, a = jit("rbi24", t)
    index_card(c, 1300 + dx, 560 + dy, 620, 420, rot=3, seed=27)
    pin(c, 1300 + dx, 360 + dy)
    type_text(c, "RBI RULE · 2024", 1300 + dx, 440 + dy, 50, span(t, min(t0 + 0.5, ts - 0.2), ts + 0.5), color=BANKBLUE)
    type_text(c, "ONE flat charge", 1300 + dx, 550 + dy, 48, span(t, min(t0 + 0.8, ts + 0.3), ts + 1.0))
    type_text(c, "NO interest on it", 1300 + dx, 640 + dy, 48, span(t, min(t0 + 1.1, ts + 0.9), ts + 1.6), color=RED_INK)


def s_still(c, t, t0):
    collage_bg(c, t)
    wallet(c, 760, 640, 1.3, t, key="wallet2")
    kr(c, 1420, 940, 1.35, "neutral", t)
    te = T("day_one", "empty", 2)
    headline(c, "STILL EMPTY", 760, 260, 70, span(t, t0 + 0.2, t0 + 0.8), seed=28)


# ---------------------------------------------------------------- DAY 30
def s_desk(c, t, t0):
    """Missed calls pile up: the counter escalates and the call slips stack on the desk."""
    collage_bg(c, t)
    dx, dy, a = jit("desk", t)
    c.drawRect(skia.Rect(0, 760 + dy, W, H), paint("#8B5E3C"))
    halftone(c, skia.Path().addRect(skia.Rect(0, 760, W, H)), "#3A2010", 0.25)
    ring = 1.0 if (t - t0) % 1.6 < 1.1 else 0.0
    smartphone(c, 760, 500, 0.95, t, [("UNKNOWN\nNUMBER", GREY)], 1.0, key="sp3", rot=-2, buzz=ring, avatar=True)
    n = int(keys(t, [(t0, 1), (t0 + 2.5, 7), (t0 + 6.5, 23)], ease))
    for i in range(min(n, 23)):
        x = 1260 + (rng(i, 3) - 0.5) * 360
        y = 900 - i * 14
        index_card(c, x, y, 260, 90, rot=(rng(i, 4) - 0.5) * 24, seed=200 + i)
        type_text(c, "MISSED CALL", x, y, 30, 1.0, color=RED_INK)
    headline(c, f"MISSED CALLS: {n}", 1300, 200, 70, 1.0, seed=29)
    chai(c, 1700, 640, 0.75, t, key="deskchai", steam=t < t0 + 4)


def s_goons(c, t, t0):
    collage_bg(c, t)
    tr = T("day_thirty", "real")
    tear = span(t, tr - 0.2, tr + 0.4)
    if tear >= 1:
        headline(c, "IN REAL LIFE:", W / 2, 400, 96, 1.0, seed=30)
        stamp(c, W / 2, 640, "RBI RULES", span(t, tr + 0.3, tr + 0.5), rot=-6)
        return
    c.save(); c.translate(0, 900 * ease(tear)); c.rotate(-12 * tear, 960, 540)
    dx, dy, a = jit("poster", t)
    c.drawRect(skia.Rect(420 + dx, 120 + dy, 1500 + dx, 980 + dy), paint("#2A2A33"))
    type_text(c, "IN MOVIES...", 960 + dx, 210 + dy, 70, 1.0, color="#F2B44C")
    door(c, 760, 900, 1.6, t, "#6B4A2B", "FLAT 4B", key="mdoor")
    kick = math.sin(min(1, (t - t0) * 2) * math.pi) * 40
    person(c, 1150 + kick, 920, 1.5, t, color="#1B1B1B", key="goon1", walk=0.6)
    person(c, 1330, 920, 1.4, t, color="#2B2B2B", key="goon2")
    c.restore()
    if tear > 0.6:
        headline(c, "IN REAL LIFE:", W / 2, 400, 96, span(t, tr, tr + 0.4), seed=30)
        stamp(c, W / 2, 640, "RBI RULES", span(t, tr + 0.3, tr + 0.5), rot=-6)


def s_rule(c, t, t0):
    collage_bg(c, t)
    wall_clock(c, 620, 560, 1.4, t, 8 + (t - t0) * 0.6, ((t - t0) * 36) % 60, key="clk2", window=(8, 19))
    tb = T("day_thirty", "eight")
    ta = T("day_thirty", "seven")
    dx, dy, a = jit("rule", t)
    index_card(c, 1380 + dx, 520 + dy, 680, 440, rot=2, seed=31)
    type_text(c, "RBI RULE · 2022", 1380 + dx, 380 + dy, 46, 1.0, color=BANKBLUE)
    type_text(c, "Recovery calls only", 1380 + dx, 470 + dy, 46, span(t, t0 + 0.3, t0 + 1.0))
    type_text(c, "8 AM", 1380 + dx, 580 + dy, 90, span(t, tb - 0.2, tb + 0.3), color=RED_INK)
    type_text(c, "– 7 PM", 1380 + dx, 680 + dy, 90, span(t, ta - 0.2, ta + 0.3), color=RED_INK)


def s_nos(c, t, t0):
    collage_bg(c, t)
    words = [("THREATS", "threats"), ("SHOUTING", "shouting"), ("SHAMING", "shaming")]
    for i, (lab, w) in enumerate(words):
        x = 400 + i * 560
        tw = T("day_thirty", w)
        dx, dy, a = jit("no" + lab, t)
        index_card(c, x + dx, 520 + dy, 440, 260, rot=(i - 1) * 4, seed=33 + i)
        type_text(c, lab, x + dx, 520 + dy, 64, span(t, tw - 0.4, tw))
        stamp(c, x + 120, 400, "NO", span(t, tw, tw + 0.2), rot=10)
    tf = T("day_thirty", "family")
    pop(c, W / 2, 860, "not even in front of your family", t, tf - 0.4, color="teal", size=44)


def s_801(c, t, t0):
    collage_bg(c, t)
    wall_clock(c, 560, 540, 1.3, t, 8, 1, key="clk3")
    ring = 1.0 if (t - t0) % 1.4 < 1.0 else 0.0
    smartphone(c, 1100, 560, 0.85, t, [("AGENT\nCALLING...", GREY)], 1.0, key="sp4", rot=4, buzz=ring, avatar=True)
    kr(c, 1600, 960, 1.25, "neutral", t)
    headline(c, "8:01 AM", 560, 160, 80, span(t, t0 + 0.2, t0 + 0.8), seed=36)


# ---------------------------------------------------------------- DAY 31
def s_sma(c, t, t0):
    collage_bg(c, t)
    ts = T("day_thirty_one", "s")
    loan_file(c, 760, 560, 1.4, t, "YOUR LOAN", tag="SMA-1" if t > ts - 0.2 else None, key="file2")
    tm = T("day_thirty_one", "special")
    dx, dy, a = jit("smacard", t)
    if t > tm - 0.4:
        index_card(c, 1460 + dx, 520 + dy, 600, 300, rot=3, seed=38)
        type_text(c, "SPECIAL", 1460 + dx, 460 + dy, 58, span(t, tm - 0.3, tm + 0.2))
        type_text(c, "MENTION ACCOUNT", 1460 + dx, 560 + dy, 52, span(t, tm, tm + 0.6), color=RED_INK)
    headline(c, "1 FULL EMI MISSED", 760, 160, 60, span(t, t0, t0 + 0.8), seed=39)


def s_report(c, t, t0):
    collage_bg(c, t)
    bank(c, 420, 820, 1.0, t)
    dx, dy, a = jit("report", t)
    index_card(c, 1460 + dx, 520 + dy, 620, 640, rot=2, seed=41)
    type_text(c, "CREDIT REPORT", 1460 + dx, 280 + dy, 50, 1.0, color=CIBILGRN)
    for i in range(5):
        type_text(c, "paid on time" if i < 4 else "MISSED!", 1460 + dx, 380 + dy + i * 75, 40,
                  1.0 if i < 4 else span(t, t0 + 1.2, t0 + 1.8), color=INK if i < 4 else RED_INK)
    red_string(c, [(560, 520), (1160, 520)], span(t, t0 + 0.2, t0 + 1.2))
    pin(c, 560, 520); pin(c, 1160, 520)
    tw = T("day_thirty_one", "two")
    pop(c, 860, 330, "EVERY 2 WEEKS", t, min(t0 + 0.8, tw - 0.2), color="coral", size=50)


def s_meter(c, t, t0):
    collage_bg(c, t)
    tf = T("day_thirty_one", "fall")
    t1 = min(t0 + 1.0, tf - 0.2)
    v = keys(t, [(t0, 0.78), (t1, 0.78), (t1 + 1.6, 0.42)], ease)
    score_meter(c, 960, 680, 1.5, t, v)
    marker_line(c, [(1300, 420), (1360, 640)], span(t, t1, t1 + 0.6), width=14)
    big_text(c, "FALLING", 1420, 380, 60, span(t, t1 + 0.3, t1 + 0.8), "coral")
    headline(c, "YOUR SCORE", 960, 160, 66, span(t, t0, t0 + 0.7), seed=43)


def s_rejected(c, t, t0):
    collage_bg(c, t)
    smartphone(c, 560, 560, 0.85, t, [("NO-COST\nEMI", BANKBLUE)], 1.0, key="sp5", rot=-6)
    dx, dy, a = jit("ccard", t)

    def d(k):
        k.drawRRect(rr(1150 + dx, 380 + dy, 1690 + dx, 720 + dy, 30), paint("#2B2B44"))
        k.drawRect(skia.Rect(1150 + dx, 450 + dy, 1690 + dx, 510 + dy), paint("#111111"))
        k.drawRRect(rr(1200 + dx, 560 + dy, 1290 + dx, 630 + dy, 10), paint("#D4A017"))
    cutout(c, d)
    type_text(c, "CREDIT CARD UPGRADE", 1420 + dx, 680 + dy, 32, 1.0, color="#F4EFE3")
    r1, r2 = T("day_thirty_one", "rejected"), T("day_thirty_one", "rejected", 2)
    stamp(c, 560, 600, "REJECTED", span(t, r1 - 0.1, r1 + 0.15), rot=-12)
    stamp(c, 1420, 560, "REJECTED", span(t, r2 - 0.1, r2 + 0.15), rot=8)


def s_7yrs(c, t, t0):
    collage_bg(c, t)
    torn_strip(c, W / 2, 520, 1760, 260, seed=51, color="#FDFCF7", rot=-1)
    for i in range(7):
        q = span(t, t0 + 0.2 + i * 0.18, t0 + 0.45 + i * 0.18)
        x = 260 + i * 233
        type_text(c, f"YEAR {i + 1}", x, 470, 44, q)
        type_text(c, "X", x, 570, 80, q, color=RED_INK)
    stamp(c, W / 2, 840, "7 YEARS", span(t, t0 + 1.6, t0 + 1.8), rot=-6)
    type_text(c, "your missed EMI stays on record", W / 2, 1010, 46, span(t, t0 + 0.8, t0 + 1.5))


def s_breathe(c, t, t0):
    """The positive pause: warm, calm, the clock is not final."""
    collage_bg(c, t, tint="#F6E7C8")
    kr(c, 560, 960, 1.45, "happy", t)
    th = T("day_thirty_one", "breathe")
    headline(c, "BREATHE.", 1300, 300, 96, span(t, t0 + 0.2, t0 + 0.8), seed=58, color="#FFF3C4")
    ta = T("day_thirty_one", "almost")
    dx, dy, a = jit("hope", t)
    index_card(c, 1300 + dx, 640 + dy, 760, 300, rot=-2, seed=59)
    type_text(c, "Almost all of this", 1300 + dx, 590 + dy, 50, span(t, min(t0 + 0.8, ta - 0.2), ta + 0.6))
    type_text(c, "CAN STILL BE STOPPED", 1300 + dx, 690 + dy, 56, span(t, min(t0 + 1.4, ta + 0.5), ta + 1.2), color=CIBILGRN)


# ---------------------------------------------------------------- DAY 60
def s_dadphone(c, t, t0):
    collage_bg(c, t, tint="#E9DCC4")
    ring = 1.0 if (t - t0) % 1.6 < 1.1 else 0.0
    old_phone(c, 700, 700, 1.5, t, ring=ring)
    figure(c, 1420, 1040, 2.2, t, key="dad", color="#6D597A", old=True)
    tf = T("day_sixty", "fathers")
    headline(c, "YOUR FATHER'S PHONE", W / 2, 160, 62, span(t, t0 + 0.3, t0 + 1.0), seed=61)


def s_guarantor(c, t, t0):
    collage_bg(c, t)
    tg = T("day_sixty", "guarantor")
    with CamC(c, keys(t, [(t0, 1.0), (tg + 0.5, 1.15)]), 1050, 760, t=t):
        signature_form(c, 900, 560, 1.0, t, "LOAN AGREEMENT", sig_p=1.0, circle=span(t, tg - 0.2, tg + 0.5),
                       key="form1", label="GUARANTOR")
    figure(c, 1560, 1040, 1.9, t, key="dad2", color="#6D597A", old=True)


def s_same(c, t, t0):
    collage_bg(c, t)
    bank(c, 960, 420, 0.8, t, key="bank2")
    to = T("day_sixty", "owes")
    v = keys(t, [(t0, 0.75), (t0 + 2.5, 0.75), (t0 + 4.0, 0.4)], ease)
    score_meter(c, 480, 800, 0.8, t, v, key="m_you", label="YOU")
    score_meter(c, 1440, 800, 0.8, t, keys(t, [(t0, 0.85), (t0 + 2.5, 0.85), (t0 + 4.0, 0.5)], ease), key="m_dad", label="DAD")
    red_string(c, [(960, 460), (480, 640)], span(t, t0 + 0.2, t0 + 0.9))
    red_string(c, [(960, 460), (1440, 640)], span(t, t0 + 0.6, t0 + 1.3))
    pop(c, 960, 160, "A GUARANTOR OWES WHAT YOU OWE", t, to - 0.6, color="coral", size=48)


def s_never(c, t, t0):
    collage_bg(c, t, tint="#E9DCC4")
    figure(c, 700, 960, 1.6, t, key="dad3", color="#6D597A", old=True)
    dx, dy, a = jit("dadcard", t)
    index_card(c, 1350 + dx, 420 + dy, 640, 220, rot=-3, seed=63)
    type_text(c, "BORROWED: ₹0", 1350 + dx, 420 + dy, 66, span(t, t0, t0 + 0.6))
    tb = T("day_sixty", "but")
    index_card(c, 1350, 720, 640, 220, rot=3, seed=64)
    type_text(c, "OWES: ALL OF IT", 1350, 720, 62, span(t, min(t0 + 0.8, tb - 0.2), tb + 0.6), color=RED_INK)


# ---------------------------------------------------------------- DAY 91
def s_npa(c, t, t0):
    collage_bg(c, t)
    loan_file(c, 760, 600, 1.5, t, "YOUR LOAN", key="file3")
    tn = T("day_ninety_one", "n")
    stamp(c, 760, 640, "NPA", span(t, tn - 0.1, tn + 0.15), rot=-12)
    tp = T("day_ninety_one", "nonperforming")
    dx, dy, a = jit("npacard", t)
    index_card(c, 1460 + dx, 440 + dy, 600, 240, rot=3, seed=66)
    type_text(c, "NON-PERFORMING", 1460 + dx, 410 + dy, 48, span(t, min(t0 + 0.6, tp - 0.2), tp + 0.5))
    type_text(c, "ASSET", 1460 + dx, 480 + dy, 48, span(t, min(t0 + 1.0, tp + 0.2), tp + 0.7))
    tb = T("day_ninety_one", "bad")
    headline(c, "= A BAD LOAN", 1460, 760, 70, span(t, min(t0 + 1.4, tb - 0.3), tb + 0.3), seed=67)


def s_trays(c, t, t0):
    """The bank's ledger: your loan moves from GOOD LOANS to BAD LOANS."""
    collage_bg(c, t)
    dx, dy, a = jit("ledger", t)
    index_card(c, 960 + dx, 600 + dy, 1500, 760, rot=-1, seed=71)
    c.drawLine(960 + dx, 300 + dy, 960 + dx, 940 + dy, paint(INK, stroke=6))
    type_text(c, "GOOD LOANS", 590 + dx, 300 + dy, 64, 1.0, color=CIBILGRN)
    type_text(c, "BAD LOANS", 1330 + dx, 300 + dy, 64, 1.0, color=RED_INK)
    for i in range(4):
        type_text(c, f"loan #{4402 + i * 13}", 590 + dx, 420 + dy + i * 90, 40, 1.0)
    tp = T("day_ninety_one", "problem")
    p = ease(span(t, min(t0 + 0.8, tp - 0.6), min(t0 + 1.8, tp + 0.2)))
    fx = 590 + 740 * p
    fy = 760 - 200 * math.sin(math.pi * p)
    loan_file(c, fx, fy, 0.9, t, "YOUR LOAN", key="file4", rot=-3 + 20 * math.sin(math.pi * p))
    stamp(c, 1330, 820, "NPA", span(t, min(t0 + 1.9, tp + 0.2), min(t0 + 2.1, tp + 0.4)), rot=-10)
    headline(c, "THE BANK'S BOOKS", W / 2, 110, 60, span(t, t0, t0 + 0.8), seed=72)


def s_sarfaesi(c, t, t0):
    collage_bg(c, t)
    headline(c, "THE SARFAESI ACT, 2002", W / 2, 150, 78, span(t, t0, t0 + 1.0), seed=74)
    type_text(c, "one of India's toughest loan laws", W / 2, 270, 46, span(t, t0 + 0.6, t0 + 1.3))
    tj = T("day_ninety_one", "judge")
    court(c, 620, 900, 0.75, t, key="court2")
    xmark(c, 620, 700, 2.6, span(t, min(t0 + 1.4, tj - 0.3), min(t0 + 1.8, tj + 0.1)))
    torn_strip(c, 1380, 560, 640, 150, seed=75, color="#FFF3C4", rot=3)
    type_text(c, "NO JUDGE NEEDED", 1380, 560, 58, span(t, min(t0 + 1.6, tj - 0.2), min(t0 + 2.2, tj + 0.4)), color=RED_INK)
    house(c, 1380, 1000, 0.8, t, key="h_sf")
    p = ease(span(t, t0 + 3.0, t0 + 4.2))
    if p > 0:
        torn_strip(c, 1380 + 120 * p, 820, 220, 70, seed=76, color="#F4C7C0", rot=-8)
        type_text(c, "BANK", 1380 + 120 * p, 820, 40, 1.0, color=RED_INK)


# ---------------------------------------------------------------- MONTH 4
def s_letter(c, t, t0):
    collage_bg(c, t)
    t6 = T("month_four", "sixty")
    lines = [("FROM: YOUR BANK", 34, BANKBLUE), ("NOTICE · SECTION 13(2)", 40, INK),
             ("PAY IN 60 DAYS", 56, RED_INK), ("or we take possession", 36, INK)]
    with CamC(c, keys(t, [(t0, 1.0), (t6 + 0.5, 1.2)]), 960, 420, t=t):
        typed_letter(c, 960, 540, 1.0, t, lines, span(t, t0 + 0.2, t6 + 0.6))
    big_text(c, "polite.", 1600, 360, 60, span(t, T("month_four", "polite") - 0.2, T("month_four", "polite") + 0.2), "sand")


def s_drawer(c, t, t0):
    collage_bg(c, t)
    p = ease(span(t, T("month_four", "drawer") - 0.8, T("month_four", "drawer") + 0.2))
    dx, dy, a = jit("drawer", t)

    def back(k):
        k.drawRect(skia.Rect(500 + dx, 640 + dy, 1420 + dx, 1040 + dy), paint("#8B5E3C"))
        halftone(k, skia.Path().addRect(skia.Rect(500, 640, 1420, 1040)), "#3A2010", 0.35)
    cutout(c, back)
    for i in range(4):   # older unopened notices already inside
        index_card(c, 650 + i * 210, 690 - (i % 2) * 30, 240, 140, rot=(rng(i, 9) - 0.5) * 16, seed=120 + i)
        type_text(c, "NOTICE", 650 + i * 210, 680 - (i % 2) * 30, 38, 1.0, color=RED_INK)
    typed_letter(c, 960, 380 + 360 * p, 0.55, t, [("NOTICE", 40, RED_INK)], 1.0, key="letter2", rot=-8 + 6 * p)

    def front(k):
        k.drawRect(skia.Rect(470 + dx, 760 + dy, 1450 + dx, 1080 + dy), paint("#7A5232"))
        for j in range(9):
            k.drawLine(480 + dx, 790 + dy + j * 32, 1440 + dx, 800 + dy + j * 32 + (rng(j, 4) - 0.5) * 14, paint("#4A2E18", 0.45, stroke=4))
        k.drawRect(skia.Rect(900 + dx, 860 + dy, 1020 + dx, 890 + dy), paint("#D4A017"))
    cutout(c, front)
    stamp(c, 1300, 460, "IGNORED", span(t, T("month_four", "drawer"), T("month_four", "drawer") + 0.2), rot=10)
    pop(c, 960, 200, "READ TWICE. PUT AWAY.", t, t0 + 0.3, color="coral", size=50)


# ---------------------------------------------------------------- MONTH 6 (the escalation)
def s_door(c, t, t0):
    collage_bg(c, t, tint="#2A2630")
    door(c, 960, 880, 1.9, t, "#5A3A22", "FLAT 4B", key="odoor")
    person(c, 520, 1000, 1.7, t, color="#2F3E5C", key="off1", bag=True)
    person(c, 1400, 1000, 1.7, t, color="#2F3E5C", key="off2", flip=True)
    tp = T("month_six", "possession")
    stamp(c, 960, 300, "POSSESSION", span(t, min(t0 + 1.0, tp - 0.1), min(t0 + 1.2, tp + 0.15)), rot=-6)


def s_notice(c, t, t0):
    collage_bg(c, t, tint="#C9B99A")
    dx, dy, a = jit("pnotice", t)
    door(c, 960, 1080, 2.6, t, "#5A3A22", "", key="ndoor")
    index_card(c, 960 + dx, 520 + dy, 900, 640, rot=-1, seed=80)
    type_text(c, "POSSESSION NOTICE", 960 + dx, 300 + dy, 58, span(t, t0, t0 + 0.6), color=RED_INK)
    type_text(c, "Under SARFAESI Act, 2002", 960 + dx, 400 + dy, 40, span(t, t0 + 0.3, t0 + 0.9))
    type_text(c, "This property is now in", 960 + dx, 520 + dy, 44, span(t, t0 + 0.6, t0 + 1.2))
    type_text(c, "possession of the bank", 960 + dx, 590 + dy, 44, span(t, t0 + 0.9, t0 + 1.5))
    tape(c, 560, 220, 170, 50, -14); tape(c, 1360, 220, 170, 50, 14)
    stamp(c, 1250, 760, "SEALED", span(t, t0 + 2.2, t0 + 2.4), rot=-10)


def s_papers2(c, t, t0):
    collage_bg(c, t)
    tn = T("month_six", "newspapers")
    with CamC(c, keys(t, [(t0, 1.0), (t0 + 3, 1.08)]), 900, 500, t=t):
        newspaper(c, 820, 700, 1.75, t, "THE DAILY NEWS", "DEFAULTER: R. SHARMA, FLAT 4B", span(t, t0 + 0.3, t0 + 1.2), key="np1", rot=-2)
        marker_circle(c, 820, 385, 500, 110, span(t, t0 + 1.0, t0 + 1.6), width=16)
    if t > tn - 0.5:
        newspaper(c, 1620, 640, 0.9, t, "DAINIK SAMACHAR", "SUCHNA: R. SHARMA",
                  span(t, tn - 0.3, tn + 0.6), key="np2", rot=6)
    tl = T("month_six", "language")
    pop(c, 1560, 1030, "+ ONE IN YOUR OWN LANGUAGE", t, tl - 0.4, color="teal", size=40)


def s_colony(c, t, t0):
    collage_bg(c, t, tint="#F2E3C6")
    newspaper(c, 960, 690, 1.25, t, "THE DAILY NEWS", "DEFAULTER: R. SHARMA, FLAT 4B", 1.0, key="cn0", rot=-3)
    for i, (x, y) in enumerate(((330, 860), (1590, 860), (1600, 420))):
        chai(c, x, y, 0.9, t, key=f"cchai{i}")
    tc = T("month_six", "chai")
    headline(c, "THE WHOLE COLONY READS IT", W / 2, 110, 58, span(t, t0, t0 + 0.8), seed=84)
    pop(c, 330, 1010, "with morning chai", t, min(t0 + 1.0, tc - 0.5), color="coral", size=44)


def s_auction(c, t, t0):
    collage_bg(c, t)
    ta = T("month_six", "auction")
    with CamC(c, keys(t, [(t0, 1.0), (ta + 0.4, 1.15)]), 960, 560, t=t):
        house_lock(c, 960, 960, 1.9, t, lock_p=1.0, key="hl3")
        stamp(c, 960, 520, "AUCTION", span(t, min(t0 + 0.8, ta - 0.1), min(t0 + 1.0, ta + 0.15)), rot=-10)
    headline(c, "BANK AUCTION NOTICE", 1480, 900, 50, span(t, t0 + 1.2, t0 + 1.9), seed=87, color="#FFF3C4")
    headline(c, "30 DAYS LATER", 420, 160, 60, span(t, t0, t0 + 0.7), seed=86)


def s_surplus(c, t, t0):
    """Example sale: a ₹42 lakh pile splits into ₹28 lakh for the bank and ₹14 lakh back to you (to scale)."""
    collage_bg(c, t)
    headline(c, "EXAMPLE: HOUSE SOLD FOR ₹42 LAKH", W / 2, 120, 58, span(t, t0, t0 + 0.8), seed=88)
    tb = T("month_six", "extra")
    sp = ease(span(t, t0 + 1.2, t0 + 2.4))
    back = ease(span(t, min(t0 + 2.4, tb - 0.3), min(t0 + 3.4, tb + 0.6)))
    n_bank, n_you = 14, 7
    xb = 960 - 380 * sp
    xy = 960 + 380 * sp + 250 * back
    note_stack(c, xb, 900, 0.9, n_bank, t, key="bk")
    note_stack(c, xy, 900 - n_bank * 23 * (1 - sp), 0.9, n_you, t, key="yu")
    if sp > 0.5:
        torn_strip(c, xb, 980, 380, 90, seed=93, color="#F4C7C0")
        type_text(c, "BANK: ₹28 LAKH", xb, 980, 44, 1.0, color=RED_INK)
        torn_strip(c, xy, 980, 380, 90, seed=94, color="#CDE8C4")
        type_text(c, "YOU: ₹14 LAKH", xy, 980, 44, 1.0, color=CIBILGRN)
    if back > 0.5:
        big_text(c, "BACK TO YOU", xy, 380, 60, back, "teal")


# ---------------------------------------------------------------- TWIST
def s_notcrime(c, t, t0):
    collage_bg(c, t)
    handcuffs(c, 600, 560, 1.6, t)
    tn = T("twist", "crime")
    xmark(c, 600, 560, 2.8, span(t, tn - 0.1, tn + 0.3))
    headline(c, "NOT A CRIME", 1360, 400, 84, span(t, min(t0 + 0.4, tn - 0.3), tn + 0.3), seed=90)
    stamp(c, 600, 300, "JAIL?", span(t, t0 + 0.2, t0 + 0.4), rot=-8)
    signature_form(c, 1400, 760, 0.45, t, "AGREEMENT", sig_p=1.0, circle=1.0, key="form2")


def s_sc(c, t, t0):
    collage_bg(c, t)
    court(c, 560, 920, 0.9, t, key="court3")
    dx, dy, a = jit("sc", t)
    index_card(c, 1360 + dx, 520 + dy, 760, 420, rot=2, seed=92)
    type_text(c, "SUPREME COURT · 2019", 1360 + dx, 390 + dy, 46, span(t, t0, t0 + 0.6), color=BANKBLUE)
    type_text(c, "unable to repay", 1360 + dx, 500 + dy, 56, span(t, t0 + 0.5, t0 + 1.1))
    type_text(c, "is NOT cheating", 1360 + dx, 600 + dy, 70, span(t, t0 + 1.0, t0 + 1.6), color=RED_INK)


def s_mandate(c, t, t0):
    collage_bg(c, t)
    ta = T("twist", "autodebit")
    tb = T("twist", "bounced")
    signature_form(c, 560, 560, 0.95, t, "AUTO-DEBIT MANDATE", sig_p=1.0, circle=span(t, ta - 0.2, ta + 0.5), key="form3")
    cheque(c, 1400, 560, 1.0, t, bounced=span(t, tb - 0.1, tb + 0.15))
    red_string(c, [(760, 820), (1250, 640)], span(t, ta + 0.3, tb))
    pin(c, 760, 820); pin(c, 1250, 640)
    pop(c, 1400, 860, "= LIKE A BOUNCED CHEQUE", t, tb - 0.5, color="coral", size=46)


def s_2yrs(c, t, t0):
    collage_bg(c, t)
    dx, dy, a = jit("2y", t)
    index_card(c, 760 + dx, 540 + dy, 860, 480, rot=-2, seed=95)
    type_text(c, "CAN MEAN UP TO", 760 + dx, 400 + dy, 50, span(t, t0, t0 + 0.6))
    type_text(c, "2 YEARS IN JAIL", 760 + dx, 520 + dy, 84, span(t, t0 + 0.4, t0 + 1.0), color=RED_INK)
    type_text(c, "Payment & Settlement Systems Act, s.25", 760 + dx, 640 + dy, 30, span(t, t0 + 0.8, t0 + 1.4))
    tr = T("twist", "rare")
    stamp(c, 1500, 420, "RARE", span(t, tr - 0.1, tr + 0.15), rot=8)
    trl = T("twist", "real")
    stamp(c, 1500, 700, "REAL", span(t, trl - 0.1, trl + 0.15), rot=-8)


def s_signature(c, t, t0):
    collage_bg(c, t)
    handcuffs(c, 500, 520, 1.1, t, key="cuffs2")
    xmark(c, 500, 520, 2.0, 1.0)
    type_text(c, "THE LOAN", 500, 780, 56)
    ts = T("twist", "signature")
    signature_form(c, 1380, 560, 0.75, t, "MANDATE", sig_p=1.0, circle=span(t, ts - 0.2, ts + 0.4), key="form4")
    type_text(c, "YOUR SIGNATURE", 1380, 940, 56, span(t, ts - 0.3, ts + 0.3), color=RED_INK)


# ---------------------------------------------------------------- PAYOFF
def s_unlock(c, t, t0):
    collage_bg(c, t, tint="#F6E7C8")
    peel = span(t, t0 + 0.4, t0 + 1.6)
    house(c, 760, 960, 1.9, t, key="h_u")
    if peel < 1:
        c.save(); c.translate(500 * ease(peel), -300 * ease(peel)); c.rotate(40 * peel, 760, 520)
        stamp(c, 760, 520, "AUCTION", 1.0, rot=-10)
        c.restore()
    tm = T("payoff", "money")
    headline(c, "IT WANTS ITS MONEY", 1420, 260, 60, span(t, t0 + 0.2, t0 + 0.9), seed=101, color="#FFF3C4")
    if peel > 0.3:
        padlock(c, 760 + 300 * ease(peel), 880 - 400 * ease(peel), 1.6, t, key="pop_lock")


def s_callbank(c, t, t0):
    collage_bg(c, t, tint="#F6E7C8")
    bank(c, 1420, 900, 1.1, t, key="bank3")
    dx, dy, a = jit("call90", t)
    index_card(c, 620 + dx, 480 + dy, 760, 520, rot=-2, seed=103)
    type_text(c, "CALL BEFORE DAY 90", 620 + dx, 330 + dy, 54, span(t, t0, t0 + 0.6), color=CIBILGRN)
    tt = T("payoff", "time")
    type_text(c, "+ ask for more time", 620 + dx, 460 + dy, 46, span(t, min(t0 + 0.6, tt - 0.3), tt + 0.3))
    ts = T("payoff", "smaller")
    type_text(c, "+ ask for a smaller EMI", 620 + dx, 550 + dy, 46, span(t, min(t0 + 1.2, ts - 0.3), ts + 0.3))


def s_climb(c, t, t0):
    collage_bg(c, t, tint="#E3F0DC")
    v = keys(t, [(t0, 0.42), (t0 + 3.0, 0.72)], ease)
    score_meter(c, 960, 700, 1.5, t, v, key="m_up")
    headline(c, "SLOWLY CLIMBS BACK", 960, 160, 66, span(t, t0 + 0.4, t0 + 1.1), seed=105, color="#FFF3C4")


def s_badmonth(c, t, t0):
    collage_bg(c, t, tint="#F6E7C8")
    tm = T("payoff", "month")
    tl = T("payoff", "life")
    headline(c, "A BAD MONTH.", W / 2, 400, 104, span(t, min(t0 + 0.2, tm - 0.3), tm + 0.3), seed=107)
    headline(c, "NOT A BAD LIFE.", W / 2, 640, 104, span(t, min(t0 + 0.8, tl - 0.4), tl + 0.3), seed=108, color="#FFF3C4")
    marker_line(c, [(520, 720), (760, 720)], span(t, min(t0 + 1.4, tl), min(t0 + 1.8, tl + 0.4)))


def s_pickup(c, t, t0):
    """Callback to frame 0: same phone, same house, now you're calling the bank first."""
    collage_bg(c, t, tint="#F6E7C8")
    house(c, 1420, 900, 1.35, t, key="hl")
    tc = T("payoff", "call", 2)
    calling = t > tc - 0.3
    smartphone(c, 640, 560, 1.15, t, [("CALLING\nYOUR BANK...", CIBILGRN)] if calling else [("EMI DUE", BANKBLUE)],
               1.0, title="BANK", buzz=0.0 if calling else 1.0)
    if calling:
        pop(c, 1420, 300, "YOU CALL FIRST", t, tc - 0.2, color="teal", size=56)


def s_tease(c, t, t0):
    collage_bg(c, t, tint="#2A2630")
    p = 1 - ease(span(t, t0 + 0.2, t0 + 1.0)) + ease(span(t, t0 + 1.6, t0 + 2.6))
    for side in (-1, 1):
        dx = side * (40 + 160 * (1 - p))
        torn_strip(c, 960 + dx + side * 230, 600, 460, 380, seed=110 + side, color="#EDE6D3", rot=side * 4 * (1 - p))
    type_text(c, "1947", 960, 600, 120, 1.0, color=INK)
    if p > 0.9 and t > t0 + 2:
        tape(c, 960, 480, 180, 54, -10); tape(c, 960, 720, 180, 54, 12)
        marker_circle(c, 960, 600, 300, 200, span(t, t0 + 2.6, t0 + 3.4))
    headline(c, "NEXT: WHAT IF INDIA AND PAKISTAN NEVER SPLIT?", W / 2, 160, 50, span(t, t0, t0 + 1.2), seed=112)


# ---------------------------------------------------------------- the list
def SHOTS():
    L = [
        # HOOK
        (0.0, s_cold, "cut"),
        (T("hook", "in") - 0.2, s_91, "whip"),
        (T("hook", "no") - 0.2, s_nocourt, "fade"),
        (T("hook", "and") - 0.25, s_sig, "fade"),
        (E("hook") + 0.1, logo_sting(), "flash"),
        # PROMISE
        (E("hook") + 2.1, s_papers14, "fade"),
        (T("promise", "say") - 0.2, s_loan, "fade"),
        (T("promise", "and", 2) - 0.2, s_dont, "fade"),
        # DAY 1
        (B("day_one") - 0.6, card("DAY 1", "The bounce"), "iris"),
        (T("day_one", "youre") - 0.3, s_midnight, "fade"),
        (T("day_one", "that") - 0.2, s_computer, "fade"),
        (T("day_one", "wake") - 0.4, s_sms, "whip"),
        (T("day_one", "thats") - 0.2, s_fine, "fade"),
        (T("day_one", "your", 2) - 0.2, s_fear, "fade"),
        (T("day_one", "that", 3) - 0.2, s_still, "fade"),
        # DAY 30
        (B("day_thirty") - 0.6, card("DAY 30", "The calls"), "iris"),
        (T("day_thirty", "youre") - 0.3, s_desk, "fade"),
        (T("day_thirty", "in") - 0.2, s_goons, "whip"),
        (T("day_thirty", "that") - 0.2, s_rule, "fade"),
        (T("day_thirty", "no") - 0.2, s_nos, "fade"),
        (T("day_thirty", "so") - 0.2, s_801, "fade"),
        # DAY 31
        (B("day_thirty_one") - 0.6, card("DAY 31", "The score"), "iris"),
        (T("day_thirty_one", "youve") - 0.3, s_sma, "fade"),
        (T("day_thirty_one", "every") - 0.2, s_report, "fade"),
        (T("day_thirty_one", "so") - 0.2, s_meter, "fade"),
        (T("day_thirty_one", "that", 1) - 0.2, s_rejected, "whip"),
        (T("day_thirty_one", "and", 3) - 0.2, s_7yrs, "fade"),
        (T("day_thirty_one", "quick") - 0.3, s_breathe, "fade"),
        (T("day_thirty_one", "so", 2) - 0.2, comment_prompt("EMI bounced tomorrow: who do you call first?"), "fade"),
        # DAY 60
        (B("day_sixty") - 0.6, card("DAY 60", "Dad's phone"), "iris"),
        (T("day_sixty", "a") - 0.2, s_dadphone, "fade"),
        (T("day_sixty", "remember") - 0.2, s_guarantor, "fade"),
        (T("day_sixty", "in") - 0.2, s_same, "fade"),
        (T("day_sixty", "he", 2) - 0.2, s_never, "fade"),
        # DAY 91
        (B("day_ninety_one") - 0.6, card("DAY 91", "Bad loan"), "iris"),
        (T("day_ninety_one", "your") - 0.3, s_npa, "fade"),
        (T("day_ninety_one", "youre") - 0.2, s_trays, "fade"),
        (T("day_ninety_one", "and") - 0.2, s_sarfaesi, "fade"),
        # MONTH 4
        (B("month_four") - 0.6, card("MONTH 4", "The letter"), "iris"),
        (T("month_four", "a") - 0.3, s_letter, "fade"),
        (T("month_four", "you") - 0.2, s_drawer, "fade"),
        # MONTH 6 (after the hard silence)
        (B("month_six") - 0.4, card("MONTH 6", "The keys"), "cut"),
        (T("month_six", "bank") - 0.2, s_door, "fade"),
        (T("month_six", "a") - 0.2, s_notice, "fade"),
        (T("month_six", "your") - 0.2, s_papers2, "fade"),
        (T("month_six", "the") - 0.2, s_colony, "fade"),
        (T("month_six", "thirty") - 0.2, s_auction, "fade"),
        (T("month_six", "one", 2) - 0.2, s_surplus, "fade"),
        # TWIST
        (B("twist") - 0.6, card("DAY 1", "The signature"), "iris"),
        (T("twist", "not") - 0.2, s_notcrime, "fade"),
        (T("twist", "the", 2) - 0.2, s_sc, "fade"),
        (T("twist", "but") - 0.2, s_mandate, "whip"),
        (T("twist", "it", 2) - 0.2, s_2yrs, "fade"),
        (T("twist", "the", 4) - 0.2, s_signature, "fade"),
        # PAYOFF
        (B("payoff") - 0.3, s_unlock, "fade"),
        (T("payoff", "so") - 0.2, s_callbank, "fade"),
        (T("payoff", "start") - 0.2, s_climb, "fade"),
        (T("payoff", "one") - 0.2, s_badmonth, "zoom"),
        (T("payoff", "so", 2) - 0.2, s_pickup, "fade"),
        (T("payoff", "ever") - 0.2, comment_prompt("Ever got that EMI bounce SMS? Yes or no?"), "fade"),
        (T("payoff", "next", 2) - 0.2, s_tease, "cut"),
        (E("payoff") + 0.3, end_screen(), "fade"),
    ]
    L.sort(key=lambda x: x[0])
    return _split_long(L)


FRAMES = [(1.12, 820, 520), (1.14, 1100, 580), (1.1, 960, 460), (1.15, 1040, 640)]


def _split_long(L, every=3.6):
    """Any shot held longer than ~4 s gets push-in re-framings (same clock, new framing) every ~3.6 s."""
    from krwi.timeline import TOTAL
    out = []
    for i, (st, fn, tr) in enumerate(L):
        out.append((st, fn, tr))
        end = L[i + 1][0] if i + 1 < len(L) else TOTAL
        name = getattr(fn, "__name__", "")
        if not name.startswith("s_") or end - st <= 4.4:
            continue
        n = int((end - st - 0.8) // every)
        for k in range(1, n + 1):
            z, cx, cy = FRAMES[(i + k) % len(FRAMES)]
            out.append((st + k * (end - st) / (n + 1), cont(fn, st, z, cx, cy), "cut"))
    out.sort(key=lambda x: x[0])
    return out
