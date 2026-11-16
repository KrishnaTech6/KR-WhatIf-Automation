"""Shot list: What If You Ate Only Maggi for 30 Days? (atlas style).
Threads: (1) the hero bowl on the hostel shelf opens and closes the video; (2) dashed outlines of the missing foods
(veg, fruit, lemon) haunt the packet shots; (3) a small lemon sits unnoticed at the shelf edge from Day 1 and pays off
at the end. The 'Maggi beat': three packet-tear pops on Day 1 (fast), the same three slowed and dim on Day 30."""
import math
import skia
from krwi.lib import *  # noqa: F401,F403
from art import *  # noqa: F401,F403
from art import _limb


def S(beat, word, off=0.0, n=1):
    return at(beat, word, off, n)


def headline(c, t, s, t_in, y=110, size=64, color="cream", t_out=None):
    p = span(t, t_in, t_in + 0.35)
    if t_out is not None:
        p -= span(t, t_out, t_out + 0.25)
    big_text(c, s, W / 2, y, size, p, color)


# ================================================================ HOOK
def s_hook_bowl(c, t, t0):
    """Frame 0: the bowl, packet #210, the pile of 209 empty pouches, a salt heap 3x the daily limit, DAY 30."""
    room_bg(c, t, warn=0.7)
    z = keys(t, [(t0, 1.07), (t0 + 2.4, 1.0)])
    with Cam(c, z, W / 2, 560, t=t):
        pts = []
        for i in range(34):
            u = rng(i, 1) - 0.5
            mh = 330 * (1 - (2 * u) ** 2)
            pts.append((720 + u * 1150, 760 - rng(i, 2) * mh, (rng(i, 3) - 0.5) * 70, i))
        for x_, y_, r_, i in sorted(pts, key=lambda q: -q[1]):
            empty_pouch(c, x_, y_, 0.42, r_, shade=0.2 + 0.35 * rng(i, 4))
        pill(c, 300, 380, 1.0, "209 EMPTY", "plum", "cream", 38)
        table_top(c, 860)
        bowl(c, 740, 740, 1.15, t, warn=1.0)
        # salt heap: 3x the daily limit
        lim = 150
        salt_heap(c, 1530, 940, 3 * lim, 380, t)
        c.drawLine(1180, 940 - lim, 1780, 940 - lim, dashed("cream", 0.95, 5, 16, 10))
        label(c, "DAILY LIMIT", 1330, 940 - lim - 16, 32, "cream", "extrabold", align="right")
        big_text(c, "3×", 1530, 940 - 3 * lim - 30, 90, 1.0, "coral")
        calendar_page(c, 1690, 290, 0.7, "DAY", "30", rot=8)
    pill(c, W / 2, 110, 1.0, "PACKET #210", "coral", "cream", 64)


def s_hook_pile(c, t, t0):
    """30 calendar pages tear off while the packets pile up: 7 a day -> 210."""
    room_bg(c, t, warn=0.4)
    p = span(t, t0 + 0.1, S("hook", "days", 0.2))
    day = max(1, int(1 + 29 * p))
    n = 7 * day
    shown = min(60, int(n * 60 / 210 + 0.999))
    k = 0
    for r in range(5):
        for j in range(14 - r):
            if k >= shown:
                break
            x = 620 + (j - (13 - r) / 2) * 76
            y = 930 - r * 92
            packet(c, x, y, 0.3, t, rot=(rng(k, 3) - 0.5) * 16)
            k += 1
    for i in range(min(day - 1, 9)):   # torn pages on the floor
        calendar_page(c, 1160 + rng(i, 5) * 640, 930 + rng(i, 6) * 30, 0.42, "DAY", str(i + 1), rot=(rng(i, 7) - 0.5) * 70)
    calendar_page(c, 1420, 470, 1.25, "DAY", str(day), rot=6)
    big_text(c, f"{n} PACKETS", 1420, 820, 72, 1.0, "gold")
    headline(c, t, "ONLY MAGGI · 30 DAYS", S("hook", "only", -0.2), 120, 64)


def s_hook_meals(c, t, t0):
    explainer_bg(c, t, "magenta")
    for i, (w, word) in enumerate([("BREAKFAST", "breakfast"), ("LUNCH", "lunch"), ("DINNER", "dinner")]):
        tw = S("hook", word, -0.1)
        p = span(t, tw, tw + 0.3)
        if p > 0:
            x = 400 + i * 560
            packet(c, x, 560, 0.85 * back_out(p), t, rot=(i - 1) * 6, torn=span(t, tw + 0.2, tw + 0.6))
            pop(c, x, 900, w, t, tw, ["teal", "plum", "magenta"][i], 50)


def s_hook_salt(c, t, t0):
    """3x salt: one jar = your daily limit; next to it, your heap grows 3 times taller."""
    explainer_bg(c, t, "deep")
    tt = S("hook", "three", -0.3)
    lim = 240
    salt_jar(c, 560, 960, 0.5, 0.95)
    hp = span(t, t0 + 0.2, tt + 1.0)
    h = lim * (0.3 + 2.7 * ease(hp))
    for k in (1, 2, 3):
        a_ = 0.9 if h >= k * lim - 2 else 0.25
        c.drawLine(1050, 960 - k * lim, 1700, 960 - k * lim, dashed("cream", a_, 4, 14, 10))
        label(c, f"{k}×", 1760, 960 - k * lim + 14, 40, "cream" if a_ > 0.5 else "sand", "extrabold", a_, align="left")
    salt_heap(c, 1360, 960, h, 520, t)
    c.drawLine(380, 960 - lim, 1050, 960 - lim, dashed("cream", 0.5, 4, 14, 10))
    label(c, "YOUR LIMIT", 560, 1040, 44, "cream", "extrabold")
    label(c, "YOU", 1360, 1040, 52, "coral", "extrabold")
    headline(c, t, "3× SALT", tt, 140, 110, "coral")


def s_hook_missing(c, t, t0):
    """The real damage isn't printed: dashed outlines of what's missing around the packet."""
    room_bg(c, t, mode="dusk", warn=0.5)
    packet(c, W / 2, 560, 1.15, t, glow_a=0.6)
    tr = S("hook", "real", -0.1)
    items = [(560, 330, "lemon"), (1360, 330, "peas"), (520, 820, "egg"), (1400, 820, "veg")]
    for i, (x, y, kind) in enumerate(items):
        a = span(t, tr + i * 0.3, tr + i * 0.3 + 0.4)
        if a <= 0:
            continue
        if kind == "lemon":
            lemon(c, x, y, 1.6, a, outline=True)
        else:
            c.drawCircle(x, y, 90, dashed("gold", a, 5, 14, 9))
        label(c, kind.upper(), x, y + 150, 34, "gold", "bold", a)
    headline(c, t, "NOT ON THE PACKET", S("hook", "printed", -0.2), 1010, 60, "coral")


# ================================================================ PROMISE
def papers_bg(c, t):
    explainer_bg(c, t, "plum")
    t0 = E("hook") + 1.9
    dt = (S("promise", "twelve", 0.6) - t0) / 12
    names = ["LABEL", "ICMR", "WHO", "STUDY", "LABEL", "REPORT", "J NUTR", "STUDY", "LABEL", "FACT CHECK", "NIH", "STUDY"]
    for i in range(12):
        a = span(t, t0 + dt * i, t0 + dt * i + 0.3)
        if a <= 0:
            continue
        side = -1 if i % 2 == 0 else 1
        x = W / 2 + side * (470 + (i // 2 % 3) * 170)
        y = 260 + (i // 2) * 105
        paper(c, x, y + 30 * (1 - ease_out(a)), 0.42, names[i], "", ["teal", "magenta", "plum"][i % 3], rot=side * (6 + i), a=a)


def s_promise_kr(c, t, t0):
    explainer_bg(c, t, "plum")
    draw_kr(c, W / 2, 1020, 2.1, "curious", t)
    pop(c, W / 2, 180, "HOW DID YOU GET HERE?", t, S("promise", "how", -0.2), "plum", 56)


def s_flashback(c, t, t0):
    room_bg(c, t, mode="dusk")
    p = span(t, t0, S("promise", "ago", 0.2))
    d = max(0, int(round(30 - 30 * ease(p))))
    calendar_page(c, W / 2, 520, 1.6, "DAY", str(d) if d > 0 else "0", rot=-4)
    big_text(c, "30 DAYS AGO", W / 2, 1000, 70, span(t, S("promise", "thirty", -0.1), S("promise", "thirty", 0.3)), "gold")


def s_roommate(c, t, t0):
    room_bg(c, t)
    bunk(c, 1450, 900, 0.9)
    shake = math.sin(t * 18) * 4 * span(t, S("promise", "laughed", -0.2), S("promise", "laughed", 0.3))
    figure(c, 760 + shake, 960, 1.15, arm_l=110, arm_r=70, head_tilt=-16 + shake * 2)
    bubble(c, 1220, 300, 760, 150, "BET YOU CAN'T!", 64, a=span(t, S("promise", "bet", -0.1), S("promise", "bet", 0.3)), tail=-1)
    big_text(c, "HA HA HA", 760, 200, 56, span(t, S("promise", "laughed", -0.1), S("promise", "laughed", 0.3)) - span(t, S("promise", "bet", -0.2), S("promise", "bet", 0.1)), "sand")


def s_bet_cash(c, t, t0):
    explainer_bg(c, t, "deep")
    table_top(c, 760)
    for i in range(10):
        p = span(t, t0 + 0.08 * i, t0 + 0.08 * i + 0.4)
        if p > 0:
            note(c, W / 2 - 40 + i * 8, 640 - i * 14 - 200 * (1 - ease_out(p)), 1.6, rot=(rng(i, 4) - 0.5) * 12, a=p)
    big_text(c, "₹5,000", W / 2, 260, 140, span(t, S("promise", "five", -0.1), S("promise", "five", 0.3)), "gold")
    label(c, "10 × ₹500", W / 2, 360, 40, "sand", "bold", span(t, t0 + 0.6, t0 + 1.0))


def s_rule(c, t, t0):
    explainer_bg(c, t, "magenta")
    for i in range(3):
        x = 520 + i * 440
        ellipse(c, x, 640, 170, 50, paint("cream"))
        ellipse(c, x, 640, 120, 32, paint("#D6CFC0"))
        packet(c, x, 520, 0.42, t, rot=(i - 1) * 8)
    headline(c, t, "ONE RULE: NO SKIPPING MEALS", S("promise", "rule", -0.3), 200, 70, "gold")
    stamp(c, W / 2, 880, "3 MEALS A DAY", span(t, S("promise", "skipping", -0.1), S("promise", "skipping", 0.3)), "teal", -4)


def s_how_many(c, t, t0):
    explainer_bg(c, t, "plum")
    packet(c, W / 2, 560, 1.1, t, rot=math.sin(t * 2) * 4)
    for i in range(3):
        a = span(t, t0 + 0.2 + 0.25 * i, t0 + 0.5 + 0.25 * i)
        big_text(c, "?", W / 2 + (i - 1) * 440, 300 + (i % 2) * 200 if i != 1 else 230, 160, a, "gold")
    headline(c, t, "HOW MANY PACKETS?", S("promise", "how", -0.2, 2), 1010, 64)


def s_calories(c, t, t0):
    """Body as a fuel tank: 2,100 kcal needed; one packet = 300 fills a seventh."""
    explainer_bg(c, t, "deep")
    tn = S("promise", "two", -0.1, 1)
    tp = S("promise", "packet", -0.2)
    body_outline(c, 620, 1000, 1.1, water=0.0, t=t)
    meter(c, 1300, 940, 180, 640, span(t, tp, tp + 0.6) / 7, "gold", "2,100 kcal / DAY", None, a=span(t, tn, tn + 0.4))
    for k in range(1, 7):
        c.drawLine(1210, 940 - 8 - (624) * k / 7, 1390, 940 - 8 - 624 * k / 7, dashed("sand", 0.5 * span(t, tn, tn + 0.4), 3, 10, 8))
    if t > tp:
        packet(c, 1620, 820, 0.45, t)
        pop(c, 1620, 1000, "1 PACKET ≈ 300", t, tp, "plum", 40)
    headline(c, t, "YOUR BODY NEEDS", t0 + 0.1, 110, 60, "sand", t_out=tn + 0.2)


def s_seven(c, t, t0):
    explainer_bg(c, t, "deep")
    ts = S("promise", "seven", -0.3)
    meter(c, 1400, 940, 180, 640, span(t, t0, ts + 0.3), "gold", "2,100 kcal", None)
    for i in range(7):
        p = span(t, t0 + 0.2 * i, t0 + 0.2 * i + 0.35)
        if p > 0:
            packet(c, 300 + (i % 4) * 230, 420 + (i // 4) * 380 - 100 * (1 - ease_out(p)), 0.55, t, a=p, num=None)
    big_text(c, "= 7 PACKETS", 1400, 1040, 64, span(t, ts, ts + 0.3), "gold")
    for i, w in enumerate(["every", "single", "day"]):
        tw = S("promise", w, -0.05, 1 if w != "day" else 2)
        pop(c, 420 + i * 340, 1000, w.upper() + ".", t, tw, ["coral", "magenta", "plum"][i], 48)


def s_handshake(c, t, t0):
    room_bg(c, t)
    p = span(t, t0, S("promise", "shook", 0.2))
    shake = 12 * math.sin(t * 12) * span(t, S("promise", "shook", 0), S("promise", "hand", 0.4))
    figure(c, 640, 980, 1.2, arm_l=150, arm_r=-8 + 10 * ease(p), rim="amber")
    figure(c, 1280, 980, 1.2, arm_l=188 - 10 * ease(p), arm_r=60, rim="amber", hair="cap", top="tee")
    c.drawCircle(W / 2, 520 + shake, 46, paint(NIGHT))
    glow(c, W / 2, 520, 200, "gold", 0.35 * p)
    headline(c, t, "DEAL.", S("promise", "shook", 0), 160, 96, "gold")


# ================================================================ DAY 1
def s_shelf(c, t, t0):
    room_bg(c, t, mode="morning")
    shows = [span(t, S("day_one", "line", -0.1) + 0.32 * i, S("day_one", "line", 0.2) + 0.32 * i) for i in range(7)]
    with Cam(c, keys(t, [(t0, 1.0), (t0 + 5, 1.08)]), W / 2, 600, t=t):
        shelf(c, W / 2, 700, 1500, t, 7, shows, lemon_a=1.0, ps=0.5)
        glow(c, W / 2, 500, 700, "gold", 0.15 * shows[-1])
    headline(c, t, "LIKE TROPHIES", S("day_one", "trophies", -0.2), 1000, 64, "gold")


def s_film(c, t, t0):
    room_bg(c, t, mode="morning")
    shelf(c, 600, 840, 1000, t, 7, None, ps=0.32)
    c.save(); c.translate(1470, 540); c.rotate(-6); c.scale(1.0, 1.0)
    glow(c, 0, 0, 380, "teal", 0.3)
    c.drawRRect(rr(-160, -320, 160, 320, 42), paint("#0B0B12"))
    c.drawRRect(rr(-160, -320, 160, 320, 42), paint("#4B4B60", stroke=6))
    c.save(); c.clipRRect(rr(-145, -300, 145, 300, 30))
    c.drawRect(skia.Rect(-145, -300, 145, 300), paint("#3B2A5C"))
    c.translate(0, 40); c.scale(0.27, 0.27); c.translate(-600, -760)
    shelf(c, 600, 840, 1000, t, 7, None, ps=0.32)
    c.restore()
    c.drawCircle(-100, -260, 12, paint("coral", 0.5 + 0.5 * math.sin(t * 6)))
    label(c, "REC", -40, -250, 30, "coral", "extrabold")
    c.restore()
    for i, s_ in enumerate(["LOL", "7 A DAY?!", "BRO NO"]):
        bubble(c, 300 + i * 330, 200 + (i % 2) * 120, 290, 100, s_, 40, "teal", "cream",
               span(t, S("day_one", "group", -0.3) + 0.3 * i, S("day_one", "group", 0) + 0.3 * i), tail=-1)
    headline(c, t, "FOR THE GROUP CHAT", S("day_one", "group", -0.3), 1030, 56, "cream")


def s_india(c, t, t0):
    """600 crore servings: bowls light up across the complete India map."""
    tp = S("day_one", "six", -0.2)
    explainer_bg(c, t, "deep")
    k = 30
    cx, cy = 720, 560
    india_map(c, cx, cy, k)
    P = lambda lon, lat: (cx + (lon - 82.5) * k, cy - (lat - 22) * k * 1.08)
    cities = [(77.2, 28.6), (72.9, 19.1), (88.4, 22.6), (80.3, 13.1), (77.6, 13.0), (78.5, 17.4), (73.9, 18.5),
              (75.8, 26.9), (80.9, 26.8), (85.1, 25.6), (72.6, 23.0), (76.3, 10.0), (91.7, 26.1), (75.9, 31.3),
              (81.6, 21.3), (85.8, 20.3), (77.4, 23.3), (83.3, 17.7), (74.8, 34.1), (78.1, 9.9)]
    for i, (lo, la) in enumerate(cities):
        a = span(t, tp + 0.12 * i, tp + 0.12 * i + 0.3)
        if a > 0:
            x, y = P(lo, la)
            glow(c, x, y, 60, "gold", 0.6 * a)
            c.save(); c.translate(x, y); c.scale(0.09 * back_out(a), 0.09 * back_out(a))
            ellipse(c, 0, 0, 300, 82, paint("#F7E6C4"))
            body = skia.Path(); body.moveTo(-300, 0); body.cubicTo(-292, 170, -150, 245, 0, 245); body.cubicTo(150, 245, 292, 170, 300, 0); body.close()
            c.drawPath(body, paint(RED)); ellipse(c, 0, 4, 280, 70, paint(NOOD))
            c.restore()
    counter_text(c, 0, 600, span(t, tp, S("day_one", "servings", 0.3)), lambda v: f"{v:.0f} CRORE", 1500, 480, 96, "gold")
    label(c, "servings", 1500, 560, 48, "cream", "bold", span(t, tp, tp + 0.4))
    label(c, "in 15 months", 1500, 650, 44, "sand", "bold", span(t, S("day_one", "fifteen", -0.2), S("day_one", "fifteen", 0.2)))
    pop(c, 1500, 800, "≈ 4 BOWLS FOR EVERY INDIAN", t, S("day_one", "months", 0.2), "plum", 38)


def s_cost(c, t, t0):
    """₹100 a day: seven packets on one side, one pizza on the other."""
    explainer_bg(c, t, "plum")
    for i in range(7):
        packet(c, 220 + (i % 4) * 150, 380 + (i // 4) * 260, 0.4, t, rot=(i - 3) * 3, a=span(t, t0 + 0.1 * i, t0 + 0.1 * i + 0.3))
    label(c, "YOUR WHOLE DAY", 450, 860, 44, "sand", "bold")
    big_text(c, "≈ ₹100", 450, 960, 80, span(t, S("day_one", "hundred", -0.2), S("day_one", "hundred", 0.2)), "gold")
    pa = span(t, S("day_one", "cheaper", -0.2), S("day_one", "cheaper", 0.2))
    if pa > 0:
        c.save(); c.translate(1420, 520); c.scale(back_out(pa), back_out(pa))
        c.drawCircle(0, 0, 260, paint("#D9A04A")); c.drawCircle(0, 0, 225, paint("#E2572E"))
        c.drawCircle(0, 0, 215, paint("#F6D27A", 0.85))
        for k in range(9):
            c.drawCircle(150 * math.cos(k * 0.7), 150 * math.sin(k * 0.7) * 0.95, 26, paint("#B8302A"))
        for k in range(4):
            c.drawLine(0, 0, 260 * math.cos(k * math.pi / 4), 260 * math.sin(k * math.pi / 4), paint("#C98A3A", stroke=6))
            c.drawLine(0, 0, -260 * math.cos(k * math.pi / 4), -260 * math.sin(k * math.pi / 4), paint("#C98A3A", stroke=6))
        c.restore()
        label(c, "ONE PIZZA", 1420, 860, 44, "sand", "bold", pa)
        big_text(c, "₹300+", 1420, 960, 80, pa, "coral")
    c.drawLine(W / 2 + 20, 240, W / 2 + 20, 1000, paint("cream", 0.3, stroke=4))
    headline(c, t, "CHEAPER THAN ONE PIZZA", S("day_one", "cheaper", -0.2), 120, 60, "cream")


def s_two_min(c, t, t0):
    explainer_bg(c, t, "magenta")
    bowl(c, 760, 600, 1.0, t)
    p = span(t, t0, t0 + 1.5)
    c.drawCircle(1460, 560, 220, paint("#1C1238"))
    arc = skia.Path(); arc.addArc(skia.Rect(1260, 360, 1660, 760), -90, 360 * p)
    c.drawPath(arc, paint("gold", stroke=30))
    big_text(c, "2:00", 1460, 590, 96, 1.0, "cream")
    headline(c, t, "2 MINUTES A PACKET", t0 + 0.1, 120, 60, "gold")


def maggi_beat(beat, words, slow=False):
    """Three packet-tear pops, one per spoken 'Maggi'. slow=True: Day 30 version (dim, heavy, no labels)."""
    def s_maggi_beat(c, t, t0):
        if slow:
            room_bg(c, t, lamp=0.3, moon=0.4)
            dim(c, 0.55)
        else:
            explainer_bg(c, t, "magenta")
        names = ["BREAKFAST", "LUNCH", "DINNER"]
        for i in range(3):   # dashed empty slots wait for each packet
            x = 400 + i * 560
            c.drawRRect(rr(x - 180, 560 - 230, x + 180, 560 + 230, 24), dashed("sand", 0.35 if slow else 0.6, 5, 16, 12))
        for i, tw in enumerate(words):
            p = span(t, tw - 0.15, tw + (0.35 if slow else 0.15))
            if p <= 0:
                continue
            x = 400 + i * 560
            k = back_out(p) if not slow else ease_out(p)
            torn = span(t, tw, tw + (0.9 if slow else 0.4))
            packet(c, x, 560, 0.95 * k, t, rot=(i - 1) * 7, torn=torn, dimmed=0.6 if slow else 0.0)
            if not slow:
                glow(c, x, 560, 300, "gold", 0.4 * (1 - span(t, tw, tw + 0.5)))
                pop(c, x, 960, names[i], t, tw - 0.45, ["teal", "plum", "magenta"][i], 50)
            else:
                label(c, f"#{208 + i}", x, 960, 56, "cream", "extrabold", 0.9 * p)
        if not slow:
            headline(c, t, "MAGGI. MAGGI. MAGGI.", t0 + 0.1, 120, 64, "gold")
    return s_maggi_beat


# ================================================================ DAY 3
def s_mirror(c, t, t0):
    room_bg(c, t, mode="morning")
    ellipse(c, W / 2, 540, 400, 480, paint("#8A6A4A"))
    ellipse(c, W / 2, 540, 370, 450, paint("#1E2A50"))
    glow(c, W / 2, 400, 360, COOL, 0.2)
    c.save(); cl = skia.Path(); cl.addOval(skia.Rect(W / 2 - 370, 90, W / 2 + 370, 990)); c.clipPath(cl, doAntiAlias=True)
    head_outline(c, W / 2, 520, 1.25, puff=span(t, S("day_three", "face", -0.3), S("day_three", "puffy", 0.4)), t=t)
    c.restore()
    hl = skia.Path(); hl.addArc(skia.Rect(W / 2 - 330, 140, W / 2 + 330, 940), 200, 40)
    c.drawPath(hl, paint("white", 0.25, stroke=14))
    pop(c, 1550, 300, "PUFFY", t, S("day_three", "puffy", -0.1), "coral", 56)


def s_ring(c, t, t0):
    explainer_bg(c, t, "deep")
    finger_ring(c, W / 2 + 40, 560, 1.6, t, swell=span(t, t0, t0 + 1.0), tug=span(t, S("day_three", "slide", -0.3), S("day_three", "slide", 0)))
    headline(c, t, "STUCK", S("day_three", "wont", -0.1), 200, 90, "coral")


def s_bottles(c, t, t0):
    """Water pours into a body outline that puffs up."""
    explainer_bg(c, t, "deep")
    tb = S("day_three", "two", -0.2)
    pour = span(t, t0, S("day_three", "lunch", 0.3))
    c.save(); c.translate(1150, 1060); c.scale(1.0 + 0.16 * pour, 1.0); c.translate(-1150, -1060)
    body_outline(c, 1150, 1060, 0.85, water=0.15 + 0.55 * pour, t=t)
    c.restore()
    c.save(); c.translate(900, 120); c.rotate(125)
    water_bottle(c, 0, 0, 0.9, 1 - 0.6 * pour)
    c.restore()
    st = skia.Path(); st.moveTo(1173, 311); st.cubicTo(1185, 330, 1170, 360, 1150, 395)
    c.drawPath(st, paint("#4FA3E0", 0.9, stroke=16))
    for i in range(2):
        a_ = span(t, tb + 0.4 * i, tb + 0.4 * i + 0.3)
        water_bottle(c, 1620 + i * 140, 1000, 0.55 * (0.6 + 0.4 * back_out(a_)) if a_ > 0 else 0.33, 0.0 if a_ > 0 else 1.0, a=0.5 + 0.5 * a_)
    big_text(c, "2 BOTTLES", 1700, 680, 64, span(t, tb, tb + 0.3), "gold")
    label(c, "before lunch", 1700, 750, 44, "cream", "bold", span(t, S("day_three", "lunch", -0.4), S("day_three", "lunch", -0.1)))


def s_jar_one(c, t, t0):
    explainer_bg(c, t, "plum")
    tp = S("day_three", "packet", -0.1)
    salt_jar(c, 760, 980, 1.25, 0.36 * span(t, tp, S("day_three", "third", 0.2)))
    packet(c, 1460, 520, 0.8, t, torn=span(t, tp, tp + 0.4))
    pop(c, 760, 220, "YOUR DAILY SALT LIMIT", t, t0 + 0.2, "plum", 44)
    big_text(c, "36%", 1460, 930, 110, span(t, S("day_three", "third", -0.2), S("day_three", "third", 0.2)), "gold")
    label(c, "of it in ONE packet", 1460, 1010, 40, "sand", "bold", span(t, S("day_three", "third", 0), S("day_three", "third", 0.4)))


def s_jar_seven(c, t, t0):
    explainer_bg(c, t, "deep")
    tp = S("day_three", "seven", -0.2)
    f = span(t, tp, tp + 1.2)
    salt_jar(c, W / 2, 1000, 1.05, min(1.0, f * 2.52), over=max(0.0, f * 2.52 - 1) / 1.52)
    for i in range(7):
        a = span(t, tp + 0.1 * i, tp + 0.1 * i + 0.25) - span(t, tp + 0.3 + 0.1 * i, tp + 0.6 + 0.1 * i)
        packet(c, W / 2 + (i - 3) * 160, 180, 0.3, t, a=max(0, a), rot=180)
    big_text(c, "7 × 36% = 252%", 1500, 520, 64, span(t, tp + 0.6, tp + 0.9), "coral")
    big_text(c, "≈ 3× THE LIMIT", 1500, 620, 52, span(t, tp + 1.0, tp + 1.3), "gold")


def s_hold_water(c, t, t0):
    explainer_bg(c, t, "deep")
    body_outline(c, 760, 1050, 1.0, water=0.45 + 0.35 * span(t, t0, S("day_three", "dilute", 0.4)), t=t)
    for i in range(6):
        ph = (t * 0.8 + i / 6) % 1
        d = skia.Path(); x, y = 1250 + (i % 3) * 140, 300 + ph * 400
        d.moveTo(x, y - 40); d.cubicTo(x + 30, y, x + 30, y + 20, x, y + 20); d.cubicTo(x - 30, y + 20, x - 30, y, x, y - 40)
        c.drawPath(d, paint("#4FA3E0", math.sin(math.pi * ph)))
    headline(c, t, "HOLDING EXTRA WATER", t0 + 0.1, 130, 64, "cream")
    label(c, "to dilute the salt", 1400, 900, 52, "cream", "extrabold", span(t, t0 + 0.4, t0 + 0.8))


def s_pressure(c, t, t0):
    explainer_bg(c, t, "magenta")
    heart(c, 640, 560, 1.4, t, rate=1.6)
    gauge(c, 1360, 700, 260, 0.35 + 0.45 * span(t, t0, S("day_three", "harder", 0.4)))
    headline(c, t, "WORKING HARDER", S("day_three", "work", -0.2), 130, 64, "coral")


# ================================================================ WEEK 1
def s_bathroom(c, t, t0):
    room_bg(c, t, lamp=0.4)
    c.drawRRect(rr(560, 160, 1040, 1000, 12), paint("#3A2A5E"))
    c.drawRRect(rr(600, 200, 1000, 560, 8), paint("#2E2250")); c.drawRRect(rr(600, 600, 1000, 960, 8), paint("#2E2250"))
    c.drawCircle(950, 600, 20, paint("gold"))
    pill(c, 800, 120, 1.0, "OCCUPIED", "coral", "cream", 40)
    p = span(t, t0, S("week_one", "nothing", 0.2))
    c.drawCircle(1460, 500, 220, paint("#1C1238")); c.drawCircle(1460, 500, 220, paint("cream", stroke=8))
    ang = math.radians(-90 + 360 * 4 * ease(p))
    c.drawLine(1460, 500, 1460 + 170 * math.cos(ang), 500 + 170 * math.sin(ang), paint("gold", stroke=10))
    c.drawLine(1460, 500, 1460 + 110 * math.cos(ang / 12), 500 + 110 * math.sin(ang / 12), paint("cream", stroke=14))
    big_text(c, f"{int(20 * ease(p))} MIN", 1460, 840, 72, 1.0, "gold")
    headline(c, t, "NOTHING.", S("week_one", "nothing", -0.1), 1020, 64, "sand")


def s_fibre(c, t, t0):
    explainer_bg(c, t, "deep")
    tf = S("week_one", "fibre", -0.3)
    meter(c, 720, 940, 200, 600, 2.0 / 30 * span(t, tf, tf + 0.6), "coral", "1 PACKET", "≈ 2 g", a=span(t, t0, t0 + 0.3))
    meter(c, 1200, 940, 200, 600, span(t, tf + 0.4, tf + 1.2), "#9BE07A", "YOU NEED", "≈ 30 g", a=span(t, tf + 0.2, tf + 0.5))
    headline(c, t, "FIBRE", tf, 120, 80, "gold")
    label(c, "nothing to push with", 1620, 600, 40, "sand", "bold", span(t, S("week_one", "push", -0.3), S("week_one", "push", 0.1)))


def s_mom_call(c, t, t0):
    desk_bg(c, t)
    phone(c, W / 2 + 120, 520, 1.25, t, "call", ring=1.0 - span(t, S("week_one", "heard", 0), S("week_one", "heard", 0.4)) * 0.6)
    label(c, "heard about the bet...", W / 2 + 120, 1010, 46, "cream", "bold", span(t, S("week_one", "heard", -0.2), S("week_one", "heard", 0.2)))


def s_wax(c, t, t0):
    desk_bg(c, t, lamp=0.8)
    phone(c, 520, 560, 0.95, t, "call", ring=0.0)
    bubble(c, 1260, 330, 820, 260, "WAX!!", 150, "cream", "coral", span(t, S("week_one", "wax", -0.2), S("week_one", "wax", 0.1)), tail=-1)
    label(c, "\"Maggi is coated in wax!\"", 1200, 570, 46, "cream", "bold", span(t, S("week_one", "beta", -0.1), S("week_one", "beta", 0.3)))
    label(c, "\"It stays in your stomach for days!\"", 1200, 640, 42, "cream", "bold", span(t, S("week_one", "stays", -0.1), S("week_one", "stays", 0.3)))


def s_factcheck(c, t, t0):
    desk_bg(c, t, lamp=0.6)
    for i, (title, sub) in enumerate([("FACT CHECK", "2020"), ("FACT CHECK", "AFP"), ("NESTLÉ", "no wax")]):
        a = span(t, t0 + 0.2 + 0.35 * i, t0 + 0.6 + 0.35 * i)
        if i == 2:
            a = span(t, S("week_one", "nestle", -0.3), S("week_one", "nestle", 0.1))
        paper(c, 520 + i * 440, 600, 0.9, title, sub, ["teal", "plum", "magenta"][i], rot=(i - 1) * 5, a=a)
    bubble(c, W / 2, 140, 400, 110, "WAX!!", 70, "cream", "coral", 1.0 - span(t, S("week_one", "no", -0.1), S("week_one", "no", 0.2)))


def s_mom_right(c, t, t0):
    explainer_bg(c, t, "plum")
    tw = S("week_one", "wrong", -0.2)
    tr = S("week_one", "right", -0.2)
    c.drawRRect(rr(220, 300, 900, 760, 30), paint("#1C1238")); c.drawRRect(rr(220, 300, 900, 760, 30), paint("coral", stroke=6))
    c.drawRRect(rr(1020, 300, 1700, 760, 30), paint("#1C1238")); c.drawRRect(rr(1020, 300, 1700, 760, 30), paint("teal", stroke=6))
    label(c, "THE WAX", 560, 480, 64, "cream", "extrabold", span(t, tw, tw + 0.3))
    xmark(c, 560, 620, 1.3, span(t, tw + 0.2, tw + 0.6))
    label(c, "THE WORRY", 1360, 480, 64, "cream", "extrabold", span(t, tr, tr + 0.3))
    pa = span(t, tr + 0.2, tr + 0.6)
    if pa > 0:
        ck = skia.Path(); ck.moveTo(1290, 620); ck.lineTo(1340, 670); ck.lineTo(1340 + 90 * ease_out(pa), 670 - 110 * ease_out(pa))
        c.drawPath(ck, paint("#3BB273", stroke=16))
    headline(c, t, "MOM IS...", t0 + 0.1, 170, 60, "sand")
    label(c, "WRONG", 560, 860, 52, "coral", "extrabold", span(t, tw, tw + 0.3))
    label(c, "RIGHT", 1360, 860, 52, "#3BB273", "extrabold", span(t, tr, tr + 0.3))


def s_what_isnt(c, t, t0):
    """The problem is what isn't in the packet: dashed outlines of the missing foods."""
    room_bg(c, t)
    packet(c, W / 2, 560, 1.1, t)
    ti = S("week_one", "isnt", -0.2, 2)
    stuff = [(500, 330, "VEG"), (1420, 330, "DAL"), (500, 800, "FRUIT"), (1420, 800, "LEMON")]
    for i, (x, y, s_) in enumerate(stuff):
        a = span(t, ti - 0.6 + 0.25 * i, ti - 0.3 + 0.25 * i)
        if s_ == "LEMON":
            lemon(c, x, y, 1.5, a, outline=True)
        else:
            c.drawCircle(x, y, 100, dashed("gold", a, 5, 14, 9))
        label(c, s_, x, y + 16, 40, "gold", "extrabold", a)
    headline(c, t, "IT'S WHAT ISN'T IN IT", ti - 0.2, 1010, 60, "coral")


# ================================================================ DAY 10
def s_gut_zoom(c, t, t0):
    """Iris zoom from the body into a clean cross-section of the gut."""
    explainer_bg(c, t, "deep")
    tz = S("day_ten", "inside", -0.2)
    p = span(t, tz, tz + 1.0)
    q = span(t, tz + 1.0, tz + 1.6)
    if p < 1:
        figure(c, W / 2, 1060, 1.5, arm_l=105, arm_r=75, hair="short")
        glow(c, W / 2, 640, 160, "magenta", 0.7)
        r = 1150 - 890 * ease(p)
        mask = skia.Path(); mask.setFillType(skia.PathFillType.kEvenOdd)
        mask.addRect(skia.Rect(0, 0, W, H)); mask.addCircle(W / 2, 640, r)
        c.drawPath(mask, paint("space", 0.92 * ease(p)))
        c.drawCircle(W / 2, 640, r, paint("gold", 0.8 * ease(p), stroke=6))
        if p > 0.5:
            c.save(); cl = skia.Path(); cl.addCircle(W / 2, 640, r); c.clipPath(cl, doAntiAlias=True)
            c.drawRect(skia.Rect(0, 0, W, H), paint("space", ease(span(p, 0.5, 1.0))))
            gut_section(c, W / 2, 640, 250, t, a=ease(span(p, 0.5, 1.0)))
            c.restore()
    else:
        c.drawRect(skia.Rect(0, 0, W, H), paint("space", 0.6))
        gut_section(c, W / 2, 640 - 100 * ease(q), 250 + 150 * ease(q), t)
    headline(c, t, "NOT YOU.", S("day_ten", "arent", -0.1), 120, 72, "gold", t_out=tz)
    headline(c, t, "TRILLIONS OF BACTERIA", S("day_ten", "trillions", -0.6), 1020, 60, "gold")


def s_gut_hungry(c, t, t0):
    explainer_bg(c, t, "deep")
    gut_city(c, W / 2, 560, 1.0, t, plates=span(t, S("day_ten", "fed", -0.4), S("day_ten", "fed", 0)))
    headline(c, t, "THEY EAT FIBRE", t0 + 0.1, 120, 60, "gold", t_out=S("day_ten", "fed", -0.5))
    headline(c, t, "10 DAYS OF EMPTY PLATES", S("day_ten", "fed", -0.3), 1010, 58, "coral")


def s_london(c, t, t0):
    explainer_bg(c, t, "plum")
    loc_card(c, W / 2, 520, 1.25, "LONDON", "2015", "Prof. Tim Spector + his son", pin_p=span(t, S("day_ten", "london", -0.3), S("day_ten", "london", 0.2)))


def s_fastfood(c, t, t0):
    room_bg(c, t, mode="dusk")
    figure(c, 560, 1000, 1.1, arm_l=160, arm_r=20)
    for i in range(10):
        a = span(t, t0 + 0.15 * i, t0 + 0.15 * i + 0.25)
        x, y = 1000 + (i % 5) * 160, 380 + (i // 5) * 260
        if a <= 0:
            continue
        c.save(); c.translate(x, y); c.scale(back_out(a), back_out(a))
        ellipse(c, 0, -30, 60, 40, paint("#E0A050")); c.drawRect(skia.Rect(-62, -20, 62, 0), paint("#7A3A1A"))
        c.drawRect(skia.Rect(-60, -6, 60, 6), paint("#4AA84A")); ellipse(c, 0, 14, 60, 20, paint("#E0A050"))
        label(c, f"DAY {i + 1}", 0, 90, 26, "sand", "bold")
        c.restore()
    headline(c, t, "ONLY FAST FOOD · 10 DAYS", S("day_ten", "only", -0.2), 120, 60, "gold")


def s_forty(c, t, t0):
    """100 dots = his gut bacteria types; 40 fade out."""
    explainer_bg(c, t, "deep")
    tf = S("day_ten", "forty", -0.2)
    fp = span(t, tf, S("day_ten", "gone", 0.3))
    cols = ["teal", "amber", "#7FC4FF", "magenta", "#9BE07A"]
    idx = sorted(range(100), key=lambda j: rng(j, 77))
    for i in range(100):
        x, y = 420 + (i % 10) * 76, 260 + (i // 10) * 70
        gone = i in idx[:int(40 * ease(fp))]
        c.drawCircle(x, y, 26, paint("#5A5068" if gone else cols[i % 5], 0.25 if gone else 1.0))
        if not gone:
            glow(c, x, y, 40, cols[i % 5], 0.12)
    counter_text(c, 0, 40, fp, lambda v: f"−{v:.0f}%", 1450, 560, 150, "coral")
    label(c, "of bacteria types", 1450, 660, 46, "cream", "bold", span(t, tf, tf + 0.4))
    label(c, "gone in 10 days", 1450, 740, 46, "sand", "bold", span(t, S("day_ten", "gone", -0.2), S("day_ten", "gone", 0.2)))


def s_quit_bet(c, t, t0):
    room_bg(c, t)
    figure(c, 560, 1000, 1.1, arm_l=150, arm_r=-40)
    calendar_page(c, 1300, 500, 1.4, "QUIT BY", "15?", rot=6)
    bubble(c, 760, 230, 560, 120, "DAY 15. MAX.", 50, a=span(t, S("day_ten", "quit", -0.3), S("day_ten", "quit", 0)), tail=-1)


# ================================================================ DAY 20
def s_biryani(c, t, t0):
    room_bg(c, t, lamp=0.7)
    bunk(c, 420, 1000, 0.95)
    figure(c, 330, 800, 0.62, arm_l=110, arm_r=70, seated=True, fill="#2A1E4A")
    figure(c, 1520, 1000, 0.95, arm_l=150, arm_r=200, seated=True, fill="#2A1E4A", head_tilt=-6)
    biryani_box(c, 1060, 900, 0.95, t, open_p=span(t, S("day_twenty", "biryani", -0.2), S("day_twenty", "biryani", 0.6)))
    pill(c, 1650, 130, 1.0, "9:00 PM", "plum", "cream", 46)
    headline(c, t, "BIRYANI. RIGHT NEXT TO YOU.", S("day_twenty", "eats", -0.2), 140, 56, "gold")


def s_smell(c, t, t0):
    room_bg(c, t, lamp=0.7)
    figure(c, 460, 1000, 1.15, arm_l=110, arm_r=70, head_tilt=14)
    biryani_box(c, 1450, 860, 1.05, t, open_p=1.0, smell=span(t, t0, t0 + 1.4))
    headline(c, t, "YOU ALMOST QUIT", S("day_twenty", "almost", -0.2), 140, 64, "coral")


def s_not_hungry(c, t, t0):
    explainer_bg(c, t, "plum")
    tq = S("day_twenty", "surprise", -0.2)
    meter(c, W / 2, 940, 220, 620, 0.95, "#9BE07A", "HUNGER?", "FULL", a=span(t, tq, tq + 0.4))
    headline(c, t, "THE SURPRISE", tq, 120, 60, "gold")
    label(c, "not even hungry", W / 2, 1050, 44, "sand", "bold", span(t, S("day_twenty", "hungry", -0.2), S("day_twenty", "hungry", 0.2)))


def s_protein(c, t, t0):
    explainer_bg(c, t, "deep")
    tf = S("day_twenty", "forty", -0.2)
    tn = S("day_twenty", "fiftyfour", -0.2)
    # one protein bar, filled 40 of 54
    x0, x1, y = 300, 1620, 540
    c.drawRRect(rr(x0, y - 90, x1, y + 90, 40), paint("#1C1238"))
    f = (40 / 54) * span(t, tf, tf + 0.8)
    if f > 0:
        c.drawRRect(rr(x0 + 10, y - 80, x0 + 10 + (x1 - x0 - 20) * f, y + 80, 34), paint("teal"))
        glow(c, x0 + (x1 - x0) * f, y, 120, "teal", 0.3)
    c.drawRRect(rr(x0, y - 90, x1, y + 90, 40), paint("cream", stroke=6))
    big_text(c, "40 g", x0 + (x1 - x0) * 40 / 54 * 0.5, y + 30, 80, span(t, tf, tf + 0.4), "cream")
    label(c, "NEED 54 g", x1 - 20, y - 130, 50, "gold", "extrabold", span(t, tn, tn + 0.3), align="right")
    c.drawLine(x1 - 6, y - 110, x1 - 6, y + 110, paint("gold", span(t, tn, tn + 0.3), stroke=6))
    headline(c, t, "PROTEIN: NOT THAT BAD", t0 + 0.1, 150, 64, "gold")
    label(c, "7 packets a day", x0 + 20, y + 170, 42, "sand", "bold", span(t, tf, tf + 0.4), align="left")


def s_class(c, t, t0):
    blackboard(c, t)
    tr = S("day_twenty", "read", -0.2)
    rp = span(t, tr, S("day_twenty", "times", 0.2))
    n = 1 + int(4 * rp)
    book(c, W / 2 - 200, 790, 0.85, t, hl_line=3)
    for k in range(1, n):   # the same line, again and again
        yy = 600 - k * 90
        c.drawRRect(rr(420, yy - 22, 900, yy + 18, 10), paint("#FFE57A", 0.75 - 0.1 * k))
        c.drawLine(440, yy, 880, yy, paint("#9A8FA8", stroke=8))
    label(c, "SAME LINE...", 1300, 220, 64, "cream", "extrabold", span(t, tr, tr + 0.3))
    label(c, f"×{n}", 1450, 420, 140, "gold", "extrabold", span(t, tr, tr + 0.3) - span(t, S("day_twenty", "times", -0.2), S("day_twenty", "times", 0.1)))
    c.save(); c.translate(1450, 780); c.scale(1.8, 1.8); c.translate(-1450, -780)
    stamp(c, 1450, 780, "×5", span(t, S("day_twenty", "times", -0.1), S("day_twenty", "times", 0.25)), "coral", -10)
    c.restore()
    pop(c, 1650, 990, "HEAVY", t, S("day_twenty", "heavy", -0.1), "plum", 50)


def s_battery(c, t, t0):
    desk_bg(c, t, lamp=0.6)
    phone(c, W / 2 + 80, 600, 1.25, t, "battery", pct=5, ring=0.0)
    headline(c, t, "STUCK AT 5%", S("day_twenty", "phone", -0.3), 120, 64, "coral")


def s_korea(c, t, t0):
    explainer_bg(c, t, "plum")
    paper(c, 620, 560, 1.15, "J NUTR", "2014", "teal", rot=-4, a=span(t, t0, t0 + 0.4))
    big_text(c, "10,711", 1350, 470, 120, span(t, S("day_twenty", "ten", -0.1), S("day_twenty", "ten", 0.3)), "gold")
    label(c, "Korean adults", 1350, 560, 52, "cream", "bold", span(t, S("day_twenty", "korean", -0.2), S("day_twenty", "korean", 0.2)))
    pop(c, 1350, 700, "SOUTH KOREA", t, S("day_twenty", "korean", 0), "plum", 40)


def s_twice(c, t, t0):
    explainer_bg(c, t, "deep")
    tw = S("day_twenty", "twice", -0.2)
    days = ["M", "T", "W", "T", "F", "S", "S"]
    for i in range(7):
        x = 240 + i * 240
        c.drawRRect(rr(x - 105, 330, x + 105, 690, 22), paint("#1C1238")); c.drawRRect(rr(x - 105, 330, x + 105, 690, 22), paint("cream", 0.5, stroke=4))
        label(c, days[i], x, 400, 48, "sand", "bold")
        if i in (1, 4):
            p = span(t, tw + (0 if i == 1 else 0.3), tw + 0.3 + (0 if i == 1 else 0.3))
            if p > 0:
                packet(c, x, 545, 0.48 * back_out(p), t)
    headline(c, t, "WOMEN · NOODLES 2× A WEEK", S("day_twenty", "women", -0.2), 190, 60, "gold")
    label(c, "higher odds of...", W / 2, 860, 56, "cream", "bold", span(t, S("day_twenty", "higher", -0.2), S("day_twenty", "higher", 0.2)))


def s_three_icons(c, t, t0):
    explainer_bg(c, t, "magenta")
    for i, (k, w, lab) in enumerate([("belly", "belly", "BELLY FAT"), ("sugar", "sugar", "BLOOD SUGAR"), ("bp", "pressure", "BLOOD PRESSURE")]):
        tw = S("day_twenty", w, -0.6)
        x = 420 + i * 540
        icon_disc(c, x, 520, 170, k, span(t, tw, tw + 0.35))
        label(c, lab, x, 780, 42, "cream", "extrabold", span(t, tw, tw + 0.35))
    headline(c, t, "ALL TOGETHER", S("day_twenty", "together", -0.2), 160, 64, "coral")


def s_seven_a_day(c, t, t0):
    explainer_bg(c, t, "deep")
    ts = S("day_twenty", "seven", -0.3)
    label(c, "STUDY", 360, 330, 52, "cream", "extrabold")
    for i in range(2):
        packet(c, 300 + i * 120, 500, 0.26, t)
    label(c, "2 / week", 360, 680, 52, "cream", "extrabold")
    n = int(49 * span(t, ts, ts + 1.4))
    for i in range(n):
        packet(c, 700 + (i % 7) * 104, 300 + (i // 7) * 110, 0.2, t)
    big_text(c, "YOU:", 1620, 520, 72, span(t, ts + 0.6, ts + 0.9), "coral")
    big_text(c, "49 / week", 1620, 620, 72, span(t, ts + 0.6, ts + 0.9), "coral")
    headline(c, t, "YOU'RE ON 7 A DAY", ts, 140, 64, "gold")


# ================================================================ DAY 30
def s_silence(c, t, t0):
    """The hard cut: near-black room, one rim-lit empty bowl (never fully black)."""
    c.drawRect(skia.Rect(0, 0, W, H), paint("#07050F"))
    glow(c, W / 2 - 300, 560, 380, "amber", 0.16)
    glow(c, W / 2 + 300, 560, 380, COOL, 0.14)
    bowl(c, W / 2, 600, 0.85, t, steam_a=0.0, empty=True)
    c.drawRect(skia.Rect(0, 0, W, H), paint("space", 0.25))
    rim = skia.Path(); rim.moveTo(W / 2 - 255, 600); rim.cubicTo(W / 2 - 248, 745, W / 2 - 128, 808, W / 2, 808)
    c.drawPath(rim, paint("amber", 0.8, stroke=6))
    rim2 = skia.Path(); rim2.moveTo(W / 2 + 255, 600); rim2.cubicTo(W / 2 + 248, 745, W / 2 + 128, 808, W / 2, 808)
    c.drawPath(rim2, paint(COOL, 0.7, stroke=5))


def s_last_packet(c, t, t0):
    room_bg(c, t, mode="dark")
    dim(c, 0.3)
    shelf(c, W / 2, 820, 1500, t, 0, None, lemon_a=1.0, ps=0.42)
    packet(c, W / 2, 470, 1.0, t, torn=span(t, S("day_thirty", "packet", 0), S("day_thirty", "packet", 0.8)), glow_a=0.4)
    pill(c, W / 2, 120, 1.0, "PACKET #210", "plum", "cream", 56)


def s_money(c, t, t0):
    desk_bg(c, t, lamp=0.5)
    p = span(t, S("day_thirty", "hands", -0.2), S("day_thirty", "thousand", 0.3))
    for i in range(6):
        note(c, 1700 - 1100 * ease(p) + i * 14, 820 - i * 10, 1.4, rot=-6 + i * 2)
    hx = 1700 - 1100 * ease(p) + 170
    c.drawPath(_limb(hx, 800, W + 80, 1120, 90), paint("#3A2A6A"))
    c.drawCircle(hx, 800, 50, paint(SKIN))
    c.drawPath(_limb(hx, 800, W + 80, 1120, 90), paint("amber", 0.6, stroke=5))
    big_text(c, "₹5,000", 760, 260, 120, span(t, S("day_thirty", "five", -0.1), S("day_thirty", "five", 0.3)), "gold")
    stamp(c, 760, 480, "BET: WON", span(t, S("day_thirty", "won", -0.1), S("day_thirty", "won", 0.25)), "teal", -8)


def s_body_lost(c, t, t0):
    explainer_bg(c, t, "deep")
    body_outline(c, W / 2, 1060, 1.0, t=t)
    glow(c, W / 2, 600, 400, "coral", 0.25 * span(t, t0, t0 + 1.0))
    stamp(c, W / 2, 520, "LOST", span(t, S("day_thirty", "lost", -0.1), S("day_thirty", "lost", 0.25)), "coral", -10)
    headline(c, t, "BUT YOUR BODY...", t0 + 0.05, 120, 64, "sand")


def s_stairs(c, t, t0):
    room_bg(c, t, mode="dark")
    stairs(c, W / 2, 820, 1.0)
    st = span(t, S("day_thirty", "climb", -0.2), S("day_thirty", "ache", 0.4))
    k = min(5, int(st * 3))
    sub = (st * 3) % 1
    x = W / 2 - 600 + 85 + k * 170 + 170 * ease(sub) * 0.0
    y = 820 - k * 90
    figure(c, x, y, 0.62, arm_l=120, arm_r=60, lean=10, head_tilt=18)
    headline(c, t, "ONE STEP AT A TIME", S("day_thirty", "one", -0.2), 120, 64, "cream")
    pop(c, 1580, 860, "LEGS ACHE", t, S("day_thirty", "legs", -0.1), "coral", 46)


def s_vitc(c, t, t0):
    explainer_bg(c, t, "deep")
    tz = S("day_thirty", "zero", -0.3)
    p = 1 - span(t, t0, tz + 0.4)
    meter(c, 760, 960, 230, 680, p * 0.9, "#F59A2A", "VITAMIN C", "≈ 0" if t > tz else None)
    for i in range(6):
        packet(c, 1250 + (i % 3) * 190, 330 + (i // 3) * 270, 0.36, t)
    label(c, "VITAMIN C IN A PACKET: 0", 1430, 960, 40, "sand", "bold", span(t, tz, tz + 0.4))
    headline(c, t, "30 DAYS · ALMOST ZERO", tz, 110, 56, "coral")


def s_gums(c, t, t0):
    c.drawRect(skia.Rect(0, 0, W, H), paint("#0E0A1C"))
    glow(c, W / 2, H / 2, 600, "coral", 0.2)
    pill(c, W / 2, 140, 1.0, "+ A FEW MORE WEEKS", "plum", "cream", 46)
    toothbrush(c, W / 2 - 80, 520, 1.4, t, drop=span(t, S("day_thirty", "bleed", -0.3), S("day_thirty", "bleed", 0.6)))
    headline(c, t, "GUMS BLEED", S("day_thirty", "gums", -0.1), 980, 64, "coral")


def s_bruise(c, t, t0):
    c.drawRect(skia.Rect(0, 0, W, H), paint("#0E0A1C"))
    arm_bruise(c, W / 2, 560, 1.0, span(t, t0, t0 + 0.8))
    headline(c, t, "BRUISES FROM NOWHERE", t0 + 0.1, 180, 64, "#B48AE0")


def s_cut(c, t, t0):
    c.drawRect(skia.Rect(0, 0, W, H), paint("#0E0A1C"))
    finger_cut(c, W / 2, 560, 1.1, t)
    headline(c, t, "CUTS STOP HEALING", t0 + 0.1, 180, 64, "coral")


# ================================================================ TWIST
def s_ship(c, t, t0):
    """The hostel room dissolves into an old sailing ship; the desk lamp becomes the stern lantern."""
    td = S("twist", "name", 0.0)
    d = span(t, td - 0.6, td + 0.4)
    if d < 1:
        room_bg(c, t, lamp=1.0)
        desk_lamp(c, 360, 560, 1.4)
    ship_scene(c, t, a=d)
    pa = span(t, S("twist", "scurvy", -0.1), S("twist", "scurvy", 0.3))
    if pa > 0:
        big_text(c, "SCURVY", W / 2, 990, 150 * (1.4 - 0.4 * back_out(pa)), pa, "coral")
    label(c, "the sailors' disease", W / 2, 1050, 40, "sand", "bold", span(t, S("twist", "disease", -0.2), S("twist", "disease", 0.2)))


def s_ship_room(c, t, t0):
    """Then and now, side by side, nothing cut by the divider."""
    wp = ease(span(t, t0, t0 + 0.5))
    c.save(); c.clipRect(skia.Rect(0, 0, W / 2, H))
    ship_scene(c, t, ship_x=W / 4 + 20, ship_s=0.58)
    c.drawRect(skia.Rect(0, 0, W / 2, H), paint("space", 0.2))
    c.restore()
    c.save(); c.clipRect(skia.Rect(W / 2, 0, W, H))
    room_bg(c, t)
    shelf(c, 1440, 820, 700, t, 3, None, ps=0.4)
    desk_lamp(c, 1080, 620, 1.1)
    c.restore()
    c.drawLine(W / 2, 0, W / 2, H * wp, paint("cream", stroke=6))
    pill(c, W / 4, 90, 1.0, "1700s · SHIPS", "teal", "cream", 44)
    pill(c, 3 * W / 4, 90, 1.0, "2026 · HOSTEL", "coral", "cream", 44)


def s_timeline(c, t, t0):
    explainer_bg(c, t, "deep")
    tt = S("twist", "tiredness", -0.3)
    tb = S("twist", "bleeding", -0.3)
    x0, x1, y = 200, 1720, 600
    p = span(t, t0, S("twist", "months", 0.3))
    c.drawLine(x0, y, x0 + (x1 - x0) * p, y, paint("cream", stroke=8))
    marks = [(0.0, "DAY 0"), (0.25, "WEEKS"), (0.6, "1 MONTH"), (1.0, "3 MONTHS")]
    for f, s_ in marks:
        if p >= f - 0.01:
            c.drawCircle(x0 + (x1 - x0) * f, y, 16, paint("cream"))
            label(c, s_, x0 + (x1 - x0) * f, y + 80, 36, "sand", "bold", align="center" if 0 < f < 1 else ("left" if f == 0 else "right"))
    a1 = span(t, tt, tt + 0.4)
    if a1 > 0:
        pill(c, x0 + (x1 - x0) * 0.25, y - 140, a1, "TIREDNESS", "amber", "ink", 44)
    a2 = span(t, tb, tb + 0.4)
    if a2 > 0:
        c.drawRRect(rr(x0 + (x1 - x0) * 0.6, y - 40, x1, y + 40, 20), paint("coral", 0.5 * a2))
        pill(c, x0 + (x1 - x0) * 0.8, y - 140, a2, "BLEEDING", "coral", "cream", 44)
    headline(c, t, "NO VITAMIN C", t0 + 0.1, 160, 64, "gold")


def s_sydney(c, t, t0):
    explainer_bg(c, t, "plum")
    loc_card(c, 620, 520, 1.0, "SYDNEY", "2016", "Westmead Institute", pin_p=span(t, S("twist", "sydney", -0.3), S("twist", "sydney", 0.2)), colr="coral")
    tp = S("twist", "twelve", -0.2)
    for i in range(12):
        a = span(t, tp + 0.07 * i, tp + 0.07 * i + 0.25)
        figure(c, 1210 + (i % 6) * 100, 520 + (i // 6) * 300, 0.4, a=a, belly=0.6 if i in (1, 4, 7, 9, 10) else 0.0, arm_l=110, arm_r=70, hair=["short", "long", "bun", "cap"][i % 4])
    big_text(c, "12 PATIENTS", 1460, 1000, 64, span(t, tp, tp + 0.3), "gold")
    pop(c, 1460, 120, "SOME OVERWEIGHT", t, S("twist", "overweight", -0.2), "coral", 44)


def s_wellfed(c, t, t0):
    room_bg(c, t, mode="dusk")
    figure(c, 700, 1040, 1.35, belly=0.9, arm_l=120, arm_r=60, hair="bun", top="tee")
    meter(c, 1400, 940, 200, 640, 0.02, "#F59A2A", "VITAMIN C", "EMPTY")
    headline(c, t, "LOOKED WELL FED", S("twist", "looked", -0.2), 120, 64, "gold")


# ================================================================ PAYOFF
def s_refill(c, t, t0):
    room_bg(c, t, mode="morning")
    tv = S("payoff", "vitamin", -0.4)
    meter(c, 640, 960, 230, 680, 0.15 + 0.75 * span(t, t0, S("payoff", "days", 0.3)), "#F59A2A", "VITAMIN C", None)
    lemon(c, 1340, 480, 2.2, glow_a=0.5)
    headline(c, t, "THE GOOD NEWS", t0 + 0.1, 120, 64, "gold")
    label(c, "signs fade within days", 1340, 820, 60, "cream", "extrabold", span(t, tv, tv + 0.4))


def s_lemon_shelf(c, t, t0):
    """Callback to Day 1: the same shelf; a spotlight finds the lemon that was there all along."""
    room_bg(c, t, mode="morning")
    shelf(c, W / 2 - 60, 720, 1500, t, 7, None, lemon_a=0.0, ps=0.46)
    lx, ly = 1700, 684
    lemon(c, lx, ly, 0.75, glow_a=0.8 * span(t, t0 + 0.4, t0 + 1.4))
    sp = span(t, t0 + 0.3, t0 + 1.4)
    mask = skia.Path(); mask.setFillType(skia.PathFillType.kEvenOdd)
    mask.addRect(skia.Rect(0, 0, W, H)); mask.addCircle(lx, ly, 1400 - 1280 * ease(sp))
    c.drawPath(mask, paint("space", 0.7 * ease(sp)))
    c.drawCircle(lx, ly, 1400 - 1280 * ease(sp), paint("gold", 0.7 * ease(sp), stroke=5))
    headline(c, t, "IT WAS THERE SINCE DAY 1", t0 + 1.0, 1010, 60, "gold")


def s_bloom(c, t, t0):
    room_bg(c, t, mode="morning")
    table_top(c, 830)
    pe = span(t, S("payoff", "peas", -0.3), S("payoff", "peas", 0.4))
    eg = span(t, S("payoff", "egg", -0.3), S("payoff", "egg", 0.3))
    le = span(t, S("payoff", "lemon", -0.3), S("payoff", "lemon", 0.3))
    vg = span(t, S("payoff", "lemon", 0.3), S("payoff", "same", 0.4))
    bowl(c, W / 2, 600, 1.25, t, veg=vg, peas=max(pe, vg), egg=max(eg, vg), lemon_p=max(le, vg))
    if vg > 0:
        glow(c, W / 2, 600, 700, "gold", 0.2 * vg)
    for i, (w, lab_, col_) in enumerate([("peas", "+ PEAS", "#3BB273"), ("egg", "+ EGG", "amber"), ("lemon", "+ LEMON", "gold")]):
        pop(c, 300 + i * 0 , 300 + i * 150, lab_, t, S("payoff", w, -0.2), "teal" if i == 0 else "plum" if i == 1 else "magenta", 48)
    headline(c, t, "SAME 2 MINUTES", S("payoff", "same", -0.2), 120, 64, "gold")


def tease_bg(c, t):
    explainer_bg(c, t, "teal")
    t1 = S("payoff", "ten", -0.4)
    p = span(t, t1, S("payoff", "steps", 1.0))
    n = 14
    for i in range(n):
        u = i / (n - 1)
        x = 160 + u * 1600
        y = 960 - 120 * math.sin(u * math.pi * 0.9) + (22 if i % 2 else -22)
        a_ = clamp((p * n - i) * 1.5)
        shoe_print(c, x, y, 1.1, rot=80 - 30 * u, a=a_, left=i % 2 == 0)
    c.drawRRect(rr(W / 2 - 360, 400, W / 2 + 360, 700, 40), paint("#0E0A1C", 0.75))
    c.drawRRect(rr(W / 2 - 360, 400, W / 2 + 360, 700, 40), paint("gold", 0.8, stroke=5))
    counter_text(c, 0, 10000, p, lambda v: f"{v:,.0f}", W / 2, 590, 160, "cream")
    label(c, "STEPS TODAY", W / 2, 665, 44, "gold", "extrabold")


# ================================================================ the list
def SHOTS():
    hook = [
        (0.0, s_hook_bowl, "cut"),
        (S("hook", "youve", -0.15), s_hook_pile, "zoom"),
        (S("hook", "breakfast", -0.3), s_hook_meals, "whip"),
        (S("hook", "every", -0.2), s_hook_salt, "cut"),
        (S("hook", "and", -0.2, 2), s_hook_missing, "fade"),
        (E("hook") + 0.1, logo_sting(), "flash"),
    ]
    promise = [
        (E("hook") + 1.9, counter(0, 12, "{:.0f}", until=S("promise", "twelve", 0.6), label="LABELS · STUDIES · HEALTH REPORTS", size=200,
                                  label_at=S("promise", "labels", -0.2), bg=papers_bg), "fade"),
        (S("promise", "so", -0.3), s_promise_kr, "cut"),
        (S("promise", "thirty", -0.4), s_flashback, "iris"),
        (S("promise", "roommate", -0.4), s_roommate, "fade"),
        (S("promise", "five", -0.3), s_bet_cash, "whip"),
        (S("promise", "one", -0.3, 2), s_rule, "cut"),
        (S("promise", "so", -0.3, 2), s_how_many, "whip"),
        (S("promise", "your", -0.3, 2), s_calories, "fade"),
        (S("promise", "so", -0.3, 3), s_seven, "cut"),
        (S("promise", "you", -0.3, 4), s_handshake, "fade"),
    ]
    day1 = [
        (B("day_one") - 0.6, scene_card("DAY 1", "The dream", bd_day1), "iris"),
        (S("day_one", "you", -0.2), s_shelf, "iris"),
        (S("day_one", "your", -0.3, 2), s_film, "cut"),
        (S("day_one", "youre", -0.3), kr_react("pointing", "YOU'RE NOT ALONE"), "whip"),
        (S("day_one", "india", -0.3), s_india, "fade"),
        (S("day_one", "your", -0.3, 3), s_cost, "whip"),
        (S("day_one", "two", -0.3), s_two_min, "cut"),
        (S("day_one", "breakfast", -0.3), maggi_beat("day_one", [T("day_one", "maggi", 2), T("day_one", "maggi", 3), T("day_one", "maggi", 4)]), "cut"),
        (S("day_one", "easiest", -0.3), kr_react("happy", "EASIEST ₹5,000 EVER", line_at=S("day_one", "easiest", 0)), "flash"),
    ]
    day3 = [
        (B("day_three") - 0.6, scene_card("DAY 3", "The salt", bd_day3), "iris"),
        (S("day_three", "you", -0.2), s_mirror, "iris"),
        (S("day_three", "your", -0.3, 2), s_ring, "cut"),
        (S("day_three", "youve", -0.3), s_bottles, "cut"),
        (S("day_three", "thats", -0.3), s_jar_one, "fade"),
        (S("day_three", "seven", -0.4), s_jar_seven, "cut"),
        (S("day_three", "holds", -0.3), s_hold_water, "fade"),
        (S("day_three", "your", -0.3, 5), s_pressure, "cut"),
        (S("day_three", "you", -0.3, 2), s_cant_feel, "fade"),
    ]
    week1 = [
        (B("week_one") - 0.6, scene_card("WEEK 1", "Mom's call", bd_week1), "iris"),
        (S("week_one", "twenty", -0.3), s_bathroom, "iris"),
        (S("week_one", "maggi", -0.3), s_fibre, "cut"),
        (S("week_one", "then", -0.3), s_mom_call, "whip"),
        (S("week_one", "beta", -0.3), s_wax, "cut"),
        (S("week_one", "factcheckers", -0.3), layer(s_factcheck, stamp_at("FALSE", S("week_one", "no", -0.05), y=600)), "cut"),
        (S("week_one", "moms", -0.3), s_mom_right, "fade"),
        (S("week_one", "the", -0.3, 5), s_what_isnt, "cut"),
    ]
    day10 = [
        (B("day_ten") - 0.6, scene_card("DAY 10", "The bacteria", bd_day10), "iris"),
        (S("day_ten", "and", -0.3), s_gut_zoom, "iris"),
        (S("day_ten", "they", -0.3), s_gut_hungry, "cut"),
        (S("day_ten", "in", -0.3), s_london, "whip"),
        (S("day_ten", "only", -0.3), s_fastfood, "cut"),
        (S("day_ten", "by", -0.3), s_forty, "fade"),
        (S("day_ten", "your", -0.3, 2), s_quit_bet, "whip"),
        (S("day_ten", "whats", -0.3), comment_prompt("Longest you've survived on just Maggi?",
                                                     bg=lambda c, t: room_bg(c, t)), "fade"),
    ]
    day20 = [
        (B("day_twenty") - 0.6, scene_card("DAY 20", "The biryani", bd_day20), "iris"),
        (S("day_twenty", "nine", -0.3), s_biryani, "iris"),
        (S("day_twenty", "the", -0.3), s_smell, "cut"),
        (S("day_twenty", "and", -0.3, 2), s_not_hungry, "fade"),
        (S("day_twenty", "protein", -0.3), s_protein, "cut"),
        (S("day_twenty", "but", -0.3), s_class, "whip"),
        (S("day_twenty", "heavy", 0.3), s_battery, "cut"),
        (S("day_twenty", "because", -0.3), s_full_fed, "fade"),
        (S("day_twenty", "a", -0.3, 1), s_korea, "whip"),
        (S("day_twenty", "women", -0.3), s_twice, "cut"),
        (S("day_twenty", "belly", -0.5), s_three_icons, "cut"),
        (S("day_twenty", "youre", -0.3, 2), s_seven_a_day, "zoom"),
    ]
    day30 = [
        (E("day_twenty") + 0.1, s_silence, "cut"),
        (B("day_thirty") - 0.6, scene_card("DAY 30", "You won", bd_day30), "cut"),
        (S("day_thirty", "maggi", -0.4), maggi_beat("day_thirty", [T("day_thirty", "maggi", 1), T("day_thirty", "maggi", 2), T("day_thirty", "maggi", 3)], slow=True), "fade"),
        (S("day_thirty", "the", -0.3), s_last_packet, "fade"),
        (S("day_thirty", "your", -0.3), s_money, "cut"),
        (S("day_thirty", "but", -0.3), s_body_lost, "cut"),
        (S("day_thirty", "you", -0.3, 2), s_stairs, "fade"),
        (S("day_thirty", "in", -0.3), s_vitc, "cut"),
        (S("day_thirty", "keep", -0.3), s_gums, "cut"),
        (S("day_thirty", "bruises", -0.2), s_bruise, "cut"),
        (S("day_thirty", "small", -0.2), s_cut, "cut"),
    ]
    twist = [
        (B("twist") - 0.6, scene_card("THE TWIST", "Scurvy", bd_twist), "iris"),
        (S("twist", "this", -0.3), s_ship, "iris"),
        (S("twist", "showing", -0.2), s_ship_room, "cut"),
        (S("twist", "the", -0.3, 3), s_stages, "fade"),
        (S("twist", "and", -0.3), s_sydney, "whip"),
        (S("twist", "some", -0.3), s_wellfed, "cut"),
        (S("twist", "you", -0.3), statement("FULL EVERY DAY.", sub="...and still starving.", at_t=S("twist", "you", -0.1),
                                            bg=lambda c, t: (explainer_bg(c, t, "deep"), bowl(c, W / 2, 860, 0.5, t, warn=0.6)), color="gold", size=96), "fade"),
    ]
    payoff = [
        (B("payoff") - 0.2, s_refill, "fade"),
        (S("payoff", "so", -0.3), s_lemon_shelf, "iris"),
        (S("payoff", "add", -0.4), s_bloom, "fade"),
        (S("payoff", "whats", -0.3), comment_prompt("What's your secret Maggi add-on?", bg=lambda c, t: (room_bg(c, t), bowl(c, W / 2, 900, 0.45, t, veg=1.0))), "fade"),
        (S("payoff", "next", -0.3), tease("NEXT: 10,000 STEPS A DAY", bg=tease_bg), "flash"),
        (S("payoff", "but", -0.3), kr_react("happy", "THE NEXT WHAT IF", line_at=S("payoff", "next", -0.1, 2)), "fade"),
        (E(LAST_BEAT) + 0.3, end_screen(), "fade"),
    ]
    return hook + promise + day1 + day3 + week1 + day10 + day20 + day30 + twist + payoff


LAST_BEAT = BEAT_KEYS[-1]


def scene_card(value, name, backdrop):
    """Chapter card over its own scene backdrop (dimmed), in the brand card's type and dashed ring."""
    def f(c, t, t0):
        p = span(t, t0, t0 + 1.4)
        backdrop(c, t)
        g = skia.Paint(AntiAlias=True)
        g.setShader(skia.GradientShader.MakeRadial(skia.Point(W / 2, H / 2), 900, [col("space", 0.55), col("space", 0.85)]))
        c.drawRect(skia.Rect(0, 0, W, H), g)
        cx, cy = W / 2, H / 2 - 30
        glow(c, cx, cy, 420, "plum", 0.45)
        ring = ease(span(p, 0.0, 0.5))
        c.save(); c.rotate(t * 8.0, cx, cy)
        path = skia.Path(); path.addArc(skia.Rect(cx - 420, cy - 420, cx + 420, cy + 420), -90, 359.9 * ring)
        c.drawPath(path, dashed("teal", 0.75, 3, 14, 12))
        c.restore()
        k = back_out(span(p, 0.1, 0.55))
        if k > 0:
            c.save(); c.translate(cx, cy + 60); c.scale(k, k)
            text(c, value, 0, 0, font("extrabold", 150), paint("gold"))
            c.restore()
        a = ease_out(span(p, 0.4, 0.8))
        if a > 0:
            text(c, name, cx, cy + 170 + (1 - a) * 20, font("semibold", 52), paint("cream", a))
    f.kind = "card"
    f.__name__ = "card"
    return f


def bd_day1(c, t):
    room_bg(c, t, mode="morning")
    calendar_page(c, 330, 520, 1.5, "DAY", "1", rot=-6)
    calendar_page(c, 1600, 600, 1.2, "DAY", "2", rot=8, a=0.6)


def bd_day3(c, t):
    room_bg(c, t, mode="morning")
    ellipse(c, W / 2, 540, 420, 500, paint("#8A6A4A"))
    ellipse(c, W / 2, 540, 390, 470, paint("#1E2A50"))
    head_outline(c, W / 2, 520, 1.3, puff=0.8, t=t)


def bd_week1(c, t):
    desk_bg(c, t)
    phone(c, 1620, 520, 1.1, t, "call", ring=1.0)


def bd_day10(c, t):
    explainer_bg(c, t, "magenta")
    gut_section(c, W / 2, H / 2, 470, t)


def bd_day20(c, t):
    room_bg(c, t)
    biryani_box(c, W / 2, 820, 1.3, t, open_p=1.0)


def bd_day30(c, t):
    room_bg(c, t, mode="dark")
    stairs(c, W / 2, 860, 1.0)


def bd_twist(c, t):
    ship_scene(c, t)


def s_cant_feel(c, t, t0):
    """Calm figure; an X-ray inset shows the heart straining."""
    room_bg(c, t, mode="dusk")
    figure(c, 560, 1000, 1.1, arm_l=100, arm_r=80, seated=True, hair="short")
    xa = span(t, t0 + 0.2, t0 + 0.7)
    c.drawLine(590, 600, 1150, 520, dashed("cream", 0.6 * xa, 4, 12, 10))
    c.drawCircle(590, 600, 14, paint("coral", xa))
    if xa > 0:
        c.save(); c.translate(1380, 520); c.scale(ease_out(xa), ease_out(xa)); c.translate(-1380, -520)
        xray_heart(c, 1380, 520, 270, t, a=xa)
        c.restore()
    headline(c, t, "YOU CAN'T FEEL IT.", S("day_three", "cant", -0.3), 120, 72, "cream")
    label(c, "But it's happening.", 1380, 870, 50, "coral", "extrabold", span(t, S("day_three", "happening", -0.5), S("day_three", "happening", -0.1)))


def s_full_fed(c, t, t0):
    """Full is not fed: a stuffed belly next to an empty fuel gauge."""
    room_bg(c, t, lamp=0.8)
    figure(c, 560, 1040, 1.2, belly=1.0, arm_l=120, arm_r=60, hair="short")
    pop(c, 860, 700, "FULL", t, t0 + 0.2, "#3BB273", 54)
    ga = span(t, S("day_twenty", "fed", -0.6), S("day_twenty", "fed", -0.2))
    fuel_gauge(c, 1340, 600, 280, 0.9 - 0.85 * ga, "NUTRIENTS")
    headline(c, t, "FULL ≠ FED", S("day_twenty", "full", -0.3), 150, 110, "gold")


def s_stages(c, t, t0):
    """Scurvy, stage by stage: weeks = tiredness, 1-3 months = bleeding gums and bruises."""
    tt = S("twist", "tiredness", -0.3)
    tb = S("twist", "bleeding", -0.3)
    room_bg(c, t, mode="dark")
    s1 = span(t, tt, tt + 0.8)
    s2 = span(t, tb, tb + 0.8)
    figure(c, 640, 1050, 1.45, arm_l=100 + 6 * s1, arm_r=80 - 6 * s1, slump=0.7 * s1, hair="short", lean=-4 * s1)
    glow(c, 640, 600, 400, "coral", 0.3 * s2)
    if s2 > 0:
        for k, (bx, by) in enumerate([(560, 520), (740, 600), (520, 700), (700, 420)]):
            ellipse(c, bx, by, 30 * s2, 20 * s2, paint("#6A3A9A", 0.8))
        d = skia.Path(); d.moveTo(820, 260); d.cubicTo(850, 310, 850, 330, 820, 330); d.cubicTo(790, 330, 790, 310, 820, 260)
        c.drawPath(d, paint("#D8262E", s2))
    for i, (lab_, sub_, tm, colr) in enumerate([("WEEKS", "tired, weak", tt, "amber"), ("1–3 MONTHS", "gums bleed, bruises", tb, "coral")]):
        a_ = span(t, tm, tm + 0.4)
        y_ = 380 + i * 260
        c.drawRRect(rr(1120, y_ - 90, 1800, y_ + 90, 30), paint("#1C1238", 0.9 * a_))
        c.drawRRect(rr(1120, y_ - 90, 1800, y_ + 90, 30), paint(colr, a_, stroke=6))
        label(c, lab_, 1460, y_ - 10, 60, colr, "extrabold", a_)
        label(c, sub_, 1460, y_ + 55, 40, "cream", "bold", a_)
    headline(c, t, "NO VITAMIN C", t0 + 0.1, 130, 64, "gold")
