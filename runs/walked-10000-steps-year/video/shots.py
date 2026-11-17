"""Shot list: What If You Walked 10,000 Steps Every Day for a Year? (atlas style, global audience, 2 memes).
Threads: (1) 11:50 PM bedroom pacing on Day 1 returns in the outro (now a calm walk outside); (2) a step counter in
the top-right corner ticks up chapter by chapter (3,650,000 by Day 365); (3) the gold glow in the head silhouette is
planted in the hook and on the Week 1 sleep shot, and pays off as the hippocampus."""
import math
import skia
from krwi.lib import *  # noqa: F401,F403
from art import *  # noqa: F401,F403


def S(beat, word, off=0.0, n=1):
    return at(beat, word, off, n)


def headline(c, t, s, t_in, y=110, size=64, color="cream", t_out=None):
    p = span(t, t_in, t_in + 0.35)
    if t_out is not None:
        p -= span(t, t_out, t_out + 0.25)
    big_text(c, s, W / 2, y, size, p, color)


def street_bg(c, t, mode="night"):
    """Quiet street at night: sky, rooftops with lit windows, a lamp post, the pavement."""
    sky = ["#0E0A26", "#1E1442", "#3A1C4A"] if mode == "night" else ["#2A1640", "#8A2A5C", "#D9573D"]
    c.drawRect(skia.Rect(0, 0, W, H), vgrad(0, H * 0.75, sky))
    for k in range(40):
        c.drawCircle(rng(k, 1) * W, rng(k, 2) * 380, 1.5 + rng(k, 3) * 2, paint("cream", 0.5))
    for k in range(12):
        h = 260 + 220 * rng(k, 5)
        x0 = k * 170 - 20
        c.drawRect(skia.Rect(x0, 820 - h, x0 + 150, 820), paint("#160F30"))
        for j in range(int(h // 70)):
            for q in range(2):
                if rng(k * 7 + j * 3 + q, 9) > 0.45:
                    c.drawRect(skia.Rect(x0 + 25 + q * 60, 840 - h + j * 70, x0 + 60 + q * 60, 875 - h + j * 70), paint("amber", 0.55))
    c.drawRect(skia.Rect(0, 820, W, H), vgrad(820, H, ["#2A2248", "#14102A"]))
    c.drawLine(0, 820, W, 820, paint("#4A3A7A", stroke=5))
    c.drawLine(1500, 820, 1500, 360, paint("#3A2E5E", stroke=16))
    c.drawLine(1500, 370, 1580, 370, paint("#3A2E5E", stroke=12))
    glow(c, 1580, 400, 300, "amber", 0.45)
    c.drawCircle(1580, 390, 16, paint("gold"))
    vignette(c, W, H, 0.5)


# ---------------------------------------------------------------- step counter thread (top-right)
COUNT = [("promise", 5012), ("day_one", 10000), ("week_one", 70000), ("month_one", 300000),
         ("month_three", 900000), ("month_six", 1800000), ("year_one", 3650000)]


def corner_steps(c, t):
    v = None
    for k, val in COUNT:
        if B(k) - 0.7 <= t:
            v = val
    if v is None or t > E("year_one"):
        return
    c.drawRRect(rr(W - 430, 30, W - 40, 96, 30), paint("#0E0A1C", 0.75))
    c.drawCircle(W - 395, 63, 14, paint(STEP))
    label(c, f"{v:,} steps", W - 370, 77, 34, "cream", "extrabold", align="left")


def CS(fn):
    """Wrap a scene with the corner step counter."""
    def f(c, t, t0):
        fn(c, t, t0)
        corner_steps(c, t)
    f.__name__ = getattr(fn, "__name__", "scene")
    f.kind = getattr(fn, "kind", None)
    return f


# ================================================================ HOOK
def walker_fig(c, x, y, s_, t, rim="gold", a=1.0, expr="happy", who="you"):
    """The hero figure walking: arms swing, slight bob."""
    sw = math.sin(t * 6)
    figure(c, x, y - 6 * abs(sw), s_, arm_l=100 + 25 * sw, arm_r=80 - 25 * sw, lean=2 * sw, expr=expr, rim=rim, a=a, who=who)


def s_hook_walk(c, t, t0):
    """Frame 0: sunset street, YOU walking big with gold rim light, one huge number: a year of steps."""
    street_bg(c, t, mode="dusk")
    z = keys(t, [(t0, 1.06), (t0 + 3.5, 1.0)])
    with Cam(c, z, W / 2, 620, t=t):
        glow(c, 620, 640, 420, "gold", 0.35)
        walker_fig(c, 620, 1010, 1.25, t)
        sneaker(c, 560, 1010, 0.0)
        for k in range(6):
            shoe_print(c, 900 + k * 130, 960 + (k % 2) * 34, 0.6, rot=90, a=0.5 - 0.06 * k)
    c.drawRRect(rr(880, 250, 1840, 700, 40), paint("#0E0A1C", 0.72))
    glow(c, 1360, 420, 380, "gold", 0.35)
    big_text(c, "3,650,000", 1360, 450, 170, 1.0, "gold")
    big_text(c, "STEPS IN 1 YEAR", 1360, 560, 64, 1.0, "cream")
    pill(c, 1360, 650, 1.0, "10,000 A DAY × 365", "coral", "cream", 40)
    bath_scale(c, 1420, 900, 0.55, needle=-0.03, t=t)


def s_hook_map(c, t, t0):
    p = ease(span(t, t0 + 0.2, S("hook", "moscow", 0.4)))
    route_map(c, t, "LONDON", "MOSCOW", p, sub="≈ 2,500 km" if p > 0.6 else None)


def s_hook_scale(c, t, t0):
    room_bg(c, t, mode="night")
    tw = S("hook", "barely", -0.1)
    needle = -0.05 * span(t, tw, tw + 0.4) * (1 + 0.5 * math.sin(t * 20) * (1 - span(t, tw + 0.4, tw + 0.9)))
    z = keys(t, [(t0, 1.0), (t0 + 2.5, 1.1)])
    with Cam(c, z, W / 2, 700, t=t):
        bath_scale(c, W / 2, 720, 1.4, needle=needle, t=t)
        sneaker(c, W / 2 - 160, 600, 0.6, rot=-4, a=0.9)
        sneaker(c, W / 2 + 160, 600, 0.6, rot=4, a=0.9, colr="#E05A3A")
    headline(c, t, "BARELY MOVED", tw, 160, 90, "coral")


def s_hook_head(c, t, t0):
    explainer_bg(c, t, "deep")
    g = span(t, S("hook", "grew", -0.3), S("hook", "grew", 0.8))
    z = keys(t, [(t0, 1.0), (t0 + 3.0, 1.15)])
    with Cam(c, z, W / 2, 520, t=t):
        head_side(c, W / 2, 560, 1.5, grow=g, glow_a=0.4 + 0.6 * g, t=t)
    headline(c, t, "SOMETHING GREW", S("hook", "grew", 0.1), 980, 64, "gold")


# ================================================================ PROMISE
def papers_bg(c, t):
    explainer_bg(c, t, "plum")
    t0 = E("hook") + 1.9
    dt = (S("promise", "nine", 0.6) - t0) / 9
    names = ["NATURE", "LANCET", "PNAS", "JAMA", "LANCET GH", "SPORTS MED", "PLOS ONE", "ANN FAM MED", "UK BIOBANK"]
    for i in range(9):
        a = span(t, t0 + dt * i, t0 + dt * i + 0.3)
        if a <= 0:
            continue
        x = 300 + (i % 5) * 330 if i < 5 else 465 + (i - 5) * 330
        y = 230 if i < 5 else 900
        paper(c, x, y + (1 - ease(a)) * 200, 0.7, names[i], "STUDY", ["teal", "coral", "plum"][i % 3], (rng(i, 4) - 0.5) * 14, a)


def s_january(c, t, t0):
    desk_bg(c, t, mode="day")
    calendar_page(c, 980, 420, 1.5, "JAN", "1", rot=-4)
    pop(c, 980, 820, "NEW YEAR", t, t0 + 0.3, "plum", 48)


def s_desk(c, t, t0):
    desk_bg(c, t)
    figure(c, 700, 1000, 1.0, arm_l=60, arm_r=40, seated=True, expr="neutral")
    v = round(5012 * ease(span(t, S("promise", "phone", -0.2), S("promise", "five", 0.6))))
    step_phone(c, 1350, 470, 0.95, v, t=t, clock="5:40 PM")
    headline(c, t, "≈ 5,000 STEPS A DAY", S("promise", "five", 0.0), 110, 60, "gold")


def s_world(c, t, t0):
    explainer_bg(c, t, "deep")
    cx, cy, R = W / 2, 540, 330
    glow(c, cx, cy, 520, "teal", 0.3)
    c.drawCircle(cx, cy, R, paint("#14203E"))
    for k in range(420):
        u, v = rng(k, 31) * 2 - 1, rng(k, 32) * 2 - 1
        if u * u + v * v > 1:
            continue
        lit = rng(k, 33) > 0.45
        x, y = cx + u * R, cy + v * R
        a = span(t, t0 + rng(k, 34) * 1.5, t0 + rng(k, 34) * 1.5 + 0.3)
        c.drawCircle(x, y, 6, paint("teal" if lit else "#2E3A6A", a))
    c.drawCircle(cx, cy, R, paint("cream", 0.6, stroke=4))
    pop(c, cx, 960, "WORLD AVERAGE ≈ 5,000 STEPS/DAY", t, S("promise", "average", -0.2), "plum", 46)
    pop(c, cx, 120, "STANFORD · PHONE DATA · 100+ COUNTRIES", t, S("promise", "stanford", -0.1), "teal", 40)


def s_promise_goal(c, t, t0):
    room_bg(c, t, mode="night")
    v = 10000 * ease(span(t, S("promise", "ten", -0.1), S("promise", "ten", 0.5)))
    step_phone(c, W / 2, 520, 1.15, v, sub="NEW DAILY GOAL", t=t, done_flash=span(t, S("promise", "ten", 0.4), S("promise", "ten", 0.8)) * 0.6)
    pop(c, 420, 300, "EVERY DAY", t, S("promise", "every", -0.1), "teal", 50)
    stamp(c, 1480, 760, "NO EXCUSES", span(t, S("promise", "excuses", -0.2), S("promise", "excuses", 0.1)), "coral", -10)


# ================================================================ DAY ONE
def s_six_pm(c, t, t0):
    room_bg(c, t, mode="dusk")
    figure(c, 620, 1000, 1.1, arm_l=80, arm_r=-40, who="you", expr="worried")
    step_phone(c, 1320, 500, 1.05, 2800, t=t, clock="6:00 PM")
    headline(c, t, "6 PM · 2,800", S("day_one", "two", -0.2), 110, 64, "coral")


def s_store(c, t, t0):
    street_bg(c, t)
    store_front(c, 1450, 820, 1.0, t=t)
    x = 250 + 800 * span(t, t0, t0 + 4.5)
    walker_fig(c, x, 1000, 0.95, t, rim="amber")
    pop(c, 1450, 300, "GROCERY STORE", t, S("day_one", "grocery", -0.1), "teal", 44)
    if t > S("day_one", "long", -0.2):
        pop(c, 560, 240, "THE LONG WAY BACK", t, S("day_one", "long", -0.2), "plum", 44)


def s_laps(c, t, t0):
    """Top view of the parking lot: the walker loops, a lap counter ticks."""
    c.drawRect(skia.Rect(0, 0, W, H), paint("#1C1A30"))
    for k in range(9):
        c.drawLine(360 + k * 150, 300, 360 + k * 150, 420, paint("cream", 0.6, stroke=6))
        c.drawLine(360 + k * 150, 660, 360 + k * 150, 780, paint("cream", 0.6, stroke=6))
    for row, yy in ((0, 360), (1, 720)):
        for k in range(8):
            if (k + row) % 3 == 2:
                continue
            cx_ = 435 + k * 150
            colr = ["#3A6A8A", "#8A2A5C", "#C8A040", "#4A4660"][(k + row) % 4]
            c.drawRRect(rr(cx_ - 48, yy - 62, cx_ + 48, yy + 62, 22), paint(colr))
            c.drawRRect(rr(cx_ - 36, yy - 40, cx_ + 36, yy - 10, 8), paint("#9AD0F0", 0.8))
            c.drawRRect(rr(cx_ - 36, yy + 18, cx_ + 36, yy + 40, 8), paint("#9AD0F0", 0.6))
            c.drawRRect(rr(cx_ - 48, yy - 62, cx_ + 48, yy + 62, 22), paint("cream", 0.4, stroke=3))
    loop = skia.Path(); loop.addRRect(rr(260, 230, 1660, 850, 160))
    c.drawPath(loop, dashed(STEP, 0.5, 6, 14, 12))
    meas = skia.PathMeasure(loop, False); L = meas.getLength()
    u = ((t - t0) * 0.35) % 1
    pos, _ = meas.getPosTan(L * u)
    glow(c, pos.x(), pos.y(), 110, "gold", 0.7)
    c.drawCircle(pos.x(), pos.y(), 34, paint("#3E5BA8")); c.drawCircle(pos.x(), pos.y(), 22, paint("#1A1236"))
    c.drawCircle(pos.x(), pos.y(), 34, paint("gold", stroke=5))
    laps = 1 + int((t - t0) * 0.35)
    pill(c, W / 2, 545, 1.0, f"LAP {laps}", "coral", "cream", 64)
    label(c, "YOUR BUILDING'S PARKING LOT", W / 2, 1040, 40, "sand", "extrabold")


def s_cost(c, t, t0):
    explainer_bg(c, t, "magenta")
    cx, cy = 620, 540
    c.drawCircle(cx, cy, 260, paint("#14203E")); c.drawCircle(cx, cy, 260, paint("cream", stroke=10))
    sweep = 270 * ease(span(t, t0 + 0.2, S("day_one", "two", 0.3, 2)))
    wedge = skia.Path(); wedge.moveTo(cx, cy); wedge.arcTo(skia.Rect(cx - 240, cy - 240, cx + 240, cy + 240), -90, sweep, False); wedge.close()
    c.drawPath(wedge, paint(STEP, 0.85))
    for k in range(12):
        ang = math.radians(k * 30 - 90)
        c.drawLine(cx + 220 * math.cos(ang), cy + 220 * math.sin(ang), cx + 250 * math.cos(ang), cy + 250 * math.sin(ang), paint("cream", stroke=6))
    big_text(c, "1.5 – 2 HOURS", 1340, 520, 96, span(t, S("day_one", "hour", -0.3), S("day_one", "hour", 0.2)), "gold")
    big_text(c, "EVERY DAY", 1340, 640, 56, span(t, S("day_one", "two", 0.0, 2), S("day_one", "two", 0.4, 2)), "cream", "bold")
    headline(c, t, "HIDDEN COST", S("day_one", "hidden", -0.2), 130, 72, "coral")


def s_25days(c, t, t0):
    explainer_bg(c, t, "deep")
    big_text(c, "≈ 25 FULL DAYS A YEAR", W / 2, 150, 72, span(t, S("day_one", "twentyfive", -0.2), S("day_one", "twentyfive", 0.3)), "gold")
    n = int(25 * ease(span(t, t0 + 0.2, S("day_one", "walking", 0.2))))
    for k in range(35):
        x = 480 + (k % 7) * 160
        y = 330 + (k // 7) * 140
        on = k < n
        c.drawRRect(rr(x - 62, y - 52, x + 62, y + 52, 14), paint(STEP if on else "#2A2450", 0.95))
        if on:
            walker_sil(c, x, y + 38, 0.32, t + k, colr="#1A1236", phase=k)
    label(c, "JUST WALKING", W / 2, 1040, 44, "sand", "extrabold")


def s_pacing(c, t, t0, done_word=True):
    room_bg(c, t, mode="night", lamp=0.6)
    x = W / 2 - 300 + 600 * (0.5 + 0.5 * math.sin((t - t0) * 1.2))
    figure(c, x, 1000, 1.05, arm_l=100, arm_r=80, expr="tired", lean=3 * math.sin(t * 6))
    tw = S("day_one", "done", -0.1)
    v = 9990 if t < tw else 10000
    step_phone(c, 1560, 470, 0.85, v, t=t, clock="11:50 PM", done_flash=span(t, tw, tw + 0.3) - span(t, tw + 0.8, tw + 1.3))
    if t >= tw:
        pop(c, 460, 200, "DONE.", t, tw, "teal", 64)


# ================================================================ WEEK ONE
def s_calves(c, t, t0):
    room_bg(c, t, mode="morning")
    stairs(c, 1100, 980, 1.3)
    figure(c, 900, 900, 1.05, arm_l=40, arm_r=150, expr="worried", lean=-4)
    glow(c, 880, 760, 120, "coral", 0.5 + 0.3 * math.sin(t * 8))
    pop(c, 600, 260, "OUCH", t, S("week_one", "hurt", -0.1), "coral", 64)


def s_sleep(c, t, t0):
    room_bg(c, t, mode="dark", moon=1.2)
    c.drawRRect(rr(380, 700, 1540, 860, 30), paint("#3A2A5E"))
    c.drawRRect(rr(380, 860, 420, 960, 8), paint("#2A1E48")); c.drawRRect(rr(1500, 860, 1540, 960, 8), paint("#2A1E48"))
    ellipse(c, 520, 650, 130, 50, paint("cream", 0.95))
    br = 1 + 0.02 * math.sin(t * 2)
    c.save(); c.translate(1500, 690); c.rotate(-90); c.scale(1, br)
    figure(c, 0, 0, 1.45, arm_l=80, arm_r=100, expr="tired")
    c.restore()
    blanket = skia.Path(); blanket.moveTo(760, 600); blanket.cubicTo(1000, 560 - 6 * math.sin(t * 2), 1300, 570, 1520, 610)
    blanket.lineTo(1520, 720); blanket.lineTo(760, 720); blanket.close()
    c.drawPath(blanket, hgrad(760, 1520, ["#2A9D8F", "#1B6A60"])); c.drawPath(blanket, paint("cream", 0.3, stroke=4))
    glow(c, 560, 560, 120, "gold", 0.35 + 0.15 * math.sin(t * 2))
    for k in range(3):
        ph = ((t - t0) * 0.5 + k / 3) % 1
        label(c, "z", 640 + 60 * ph + k * 20, 470 - 160 * ph, int(40 + 30 * ph), "cream", "extrabold", 1 - ph)
    pop(c, W / 2, 220, "SLEEPING LIKE A BABY", t, S("week_one", "sleeping", -0.2), "plum", 52)


def s_why(c, t, t0):
    explainer_bg(c, t, "plum")
    big_text(c, "WHY 10,000?", W / 2, 480, 170, span(t, t0, t0 + 0.4), "gold")
    kanji_man(c, 1650, 860, 0.5, 0.0, 0.35)
    big_text(c, "WHO DECIDED THAT?", W / 2, 700, 64, span(t, S("week_one", "who", -0.1), S("week_one", "who", 0.3)), "cream")


def s_pedometer(c, t, t0):
    explainer_bg(c, t, "magenta")
    k = back_out(span(t, t0, t0 + 0.5))
    pedometer_box(c, 620, 560, 1.15 * k, t=t, rot=-4)
    pop(c, 1380, 360, "JAPAN · 1960s", t, S("week_one", "nineteen", -0.1), "teal", 50)
    pop(c, 1380, 520, "A NEW PEDOMETER", t, S("week_one", "pedometer", -0.2), "plum", 46)
    pop(c, 1380, 680, "\"10,000 STEP METER\"", t, S("week_one", "meter", -0.4), "coral", 48)


def s_kanji(c, t, t0):
    explainer_bg(c, t, "deep")
    m = span(t, S("week_one", "looks", -0.1), S("week_one", "walking", 0.4))
    glow(c, W / 2, 520, 420, "gold", 0.3 + 0.3 * m)
    kanji_man(c, W / 2 - 40 + 120 * ease(span(t, S("week_one", "walking", 0.0), S("week_one", "walking", 1.2))), 560, 1.6, m, colr="cream")
    big_text(c, "10,000", W / 2, 150, 70, 1.0 - m, "gold")
    big_text(c, "A LITTLE MAN WALKING", W / 2, 960, 60, span(t, S("week_one", "little", -0.1), S("week_one", "little", 0.3)), "gold")
    label(c, "HARVARD'S I-MIN LEE", W / 2, 1040, 32, "sand", "bold", span(t, S("week_one", "harvard", 0), S("week_one", "harvard", 0.4)))


def s_meme_nobody(c, t, t0):
    """MEME 2 ('Nobody: / ...' format), redrawn: KR deadpan beside the 1960s company shouting 10,000."""
    explainer_bg(c, t, "plum")
    label(c, "Nobody:", 220, 220, 64, "cream", "extrabold", span(t, t0, t0 + 0.3), align="left")
    label(c, "1960s pedometer company:", 220, 340, 64, "cream", "extrabold", span(t, t0 + 0.5, t0 + 0.8), align="left")
    sh = 6 * math.sin(t * 40) * span(t, t0 + 0.9, t0 + 1.0)
    big_text(c, "10,000 STEPS!!", 760 + sh, 560, 120, span(t, t0 + 0.9, t0 + 1.2), "gold")
    pedometer_box(c, 380, 840, 0.42, t=t * 3, rot=-8)
    kr_cutout(c, lambda k: draw_kr(k, 1640, 1000, 1.2, "neutral", t))
    stamp(c, 940, 830, "AN ADVERT", span(t, S("week_one", "advert", -0.1), S("week_one", "advert", 0.2)), "coral", -12)


# ================================================================ MONTH ONE
def s_scale_month(c, t, t0):
    room_bg(c, t, mode="morning")
    tw = S("month_one", "few", -0.2)
    ro = None if t < tw else "-0.3 kg"
    bath_scale(c, W / 2, 760, 1.5, needle=-0.04, t=t, readout=ro, read_col="sand")
    pop(c, W / 2, 200, "300,000 STEPS", t, S("month_one", "three", -0.1), "teal", 56)


def s_meme_expect(c, t, t0):
    """MEME 1: Expectation vs Reality, redrawn with our figure."""
    def left(c, t):
        explainer_bg(c, t, "magenta")
        figure(c, W / 4, 980, 1.05, arm_l=-60, arm_r=-120, expr="happy", rim="gold")
        for k in range(3):
            for j in range(2):
                c.drawRRect(rr(W / 4 - 44 + j * 48, 640 + k * 50, W / 4 - 4 + j * 48, 682 + k * 50, 10), paint("#26386E", 0.9))
        glow(c, W / 4, 560, 300, "gold", 0.4)

    def right(c, t):
        room_bg(c, t, mode="night")
        bath_scale(c, W * 3 / 4, 760, 0.95, t=t, readout="-0.3 kg", read_col="sand")
        figure(c, W * 3 / 4 - 260, 1000, 0.8, arm_l=100, arm_r=80, expr="tired")
    split(left, right, "EXPECTATION", "REALITY", wipe_at=t0 + 0.9)(c, t, t0)


def s_friend(c, t, t0):
    room_bg(c, t)
    shake = math.sin(t * 18) * 4 * span(t, S("month_one", "laughs", -0.2), S("month_one", "laughs", 0.5))
    figure(c, 760 + shake, 980, 1.1, arm_l=110, arm_r=70, head_tilt=-14 + shake * 2, who="mate", expr="laugh")
    bubble(c, 1280, 600, 860, 150, "WALKING DOESN'T WORK, BRO", 52, a=span(t, S("month_one", "walking", -0.1), S("month_one", "walking", 0.3)), tail=-1)


def s_dinner_walk(c, t, t0):
    street_bg(c, t)
    x = 300 + 800 * span(t, t0, t0 + 6.0)
    walker_fig(c, x, 1000, 1.0, t, rim="amber")
    plate_meal(c, 1650, 960, 0.6)
    pop(c, W / 2, 180, "AFTER DINNER", t, S("month_one", "dinner", -0.2), "teal", 52)


def s_sugar(c, t, t0):
    explainer_bg(c, t, "deep")
    x0, y0, w, h = 300, 860, 1320, 560
    c.drawLine(x0, y0, x0 + w, y0, paint("cream", stroke=4)); c.drawLine(x0, y0, x0, y0 - h - 40, paint("cream", stroke=4))
    label(c, "BLOOD SUGAR AFTER A MEAL", x0 + 10, y0 - h - 60, 34, "sand", "extrabold", align="left")
    label(c, "TIME", x0 + w - 40, y0 + 50, 30, "sand", "bold")
    sugar_curve(c, x0, y0, w, h, span(t, t0 + 0.3, t0 + 1.8), "sit", 1.0, "coral")
    sugar_curve(c, x0, y0, w, h, span(t, S("month_one", "softens", -0.4), S("month_one", "softens", 1.0)), "walk", 1.0, GREEN)
    pop(c, 1000, 330, "SITTING", t, t0 + 1.0, "coral", 44)
    pop(c, 1250, 520, "A SHORT WALK", t, S("month_one", "softens", 0.2), "teal", 44)
    label(c, "7 STUDIES · UNIVERSITY OF LIMERICK, IRELAND", W / 2, 1010, 32, "sand", "bold", span(t, S("month_one", "researchers", 0), S("month_one", "researchers", 0.5)))


def s_changing(c, t, t0):
    explainer_bg(c, t, "plum")
    body_outline(c, W / 2, 980, 1.05, t=t)
    for k, (dx, dy) in enumerate([(0, -560), (0, -420), (-60, -200), (60, -120)]):
        glow(c, W / 2 + dx, 980 + dy, 90, "gold", 0.6 * span(t, t0 + 0.3 * k, t0 + 0.3 * k + 0.5))
    bath_scale(c, 1520, 820, 0.6, t=t, a=0.6)
    xmark(c, 1520, 820, 1.4, span(t, S("month_one", "looking", -0.3), S("month_one", "looking", 0.1)))
    headline(c, t, "JUST NOT WHERE YOU'RE LOOKING", S("month_one", "just", -0.1), 120, 56, "gold")


# ================================================================ MONTH THREE
def s_no_lift(c, t, t0):
    room_bg(c, t, mode="morning")
    c.drawRRect(rr(1250, 300, 1650, 900, 10), paint("#5A5470"))
    c.drawLine(1450, 300, 1450, 900, paint("#3A3450", stroke=6))
    pill(c, 1450, 250, 1.0, "LIFT", "plum", "cream", 40)
    xmark(c, 1450, 600, 2.2, span(t, S("month_three", "lift", -0.2), S("month_three", "lift", 0.2)))
    stairs(c, 640, 980, 1.2)
    figure(c, 560, 860, 1.0, arm_l=150, arm_r=40, expr="happy")
    if t > S("month_three", "calls", -0.3):
        phone(c, 900, 360, 0.45, t, "call", ring=0.0, name="BOSS")
        pop(c, 900, 120, "CALLS? WALKING.", t, S("month_three", "calls", -0.2), "teal", 46)


def s_cloud(c, t, t0):
    room_bg(c, t, mode="dusk")
    figure(c, W / 2, 1000, 1.1, arm_l=100, arm_r=80, expr="neutral" if t < S("month_three", "less", 0) else "happy")
    s_ = 1.4 - 0.9 * ease(span(t, S("month_three", "less", -0.4), S("month_three", "less", 1.0)))
    grey_cloud(c, W / 2, 150, s_ * 0.8, a=0.9, t=t)
    headline(c, t, "BAD DAYS FEEL LESS BAD", S("month_three", "bad", -0.1), 110, 56, "gold")


def s_lancet(c, t, t0):
    papers_l = ["COHORT", "TRIAL", "STUDY"]
    explainer_bg(c, t, "plum")
    n = int(57 * ease(span(t, t0 + 0.2, S("month_three", "studies", 0.4))))
    glow(c, W / 2, 900, 520, "amber", 0.35)
    for i in range(min(n, 57)):
        ang = -60 + 120 * i / 56
        c.save(); c.translate(W / 2, 1180); c.rotate(ang)
        paper(c, 0, -420, 0.42, "", "", ["teal", "coral", "plum"][i % 3], 0, 1.0)
        c.restore()
    big_text(c, f"{n} STUDIES", W / 2, 380, 130, 1.0, "gold")
    pop(c, W / 2, 180, "THE LANCET · 2025 REVIEW", t, S("month_three", "lancet", -0.2), "teal", 46)


def s_mood_bars(c, t, t0):
    a0 = S("month_three", "seven", -0.2)
    explainer_bg(c, t, "deep")
    big_text(c, "RISK OF DEPRESSION SYMPTOMS", W / 2, 170, 54, span(t, t0, t0 + 0.4))
    for i, (lab, h, colr, when) in enumerate([("2,000 STEPS", 520, "#6A6880", t0 + 0.2), ("7,000 STEPS", 405, "teal", a0)]):
        p = ease(span(t, when, when + 0.8))
        calorie_bar(c, 760 + i * 400, 900, h * p + 2, lab, colr, 1.0 if p > 0 else 0.0)
    pop(c, 1500, 520, "≈ 1/5 LOWER", t, S("month_three", "fifth", -0.1), "coral", 60)


# ================================================================ MONTH SIX
def s_paris_rome(c, t, t0):
    p = ease(span(t, t0 + 0.3, S("month_six", "rome", 0.4)))
    route_map(c, t, "PARIS", "ROME", p, ax=520, ay=330, bx=1380, by=820, bend=60, sub="6 MONTHS" if p > 0.5 else None)


def s_crowd(c, t, t0):
    explainer_bg(c, t, "magenta")
    crowd(c, W / 2, 580, 9, 3, 9, t, sp=170, you_p=span(t, S("month_six", "not", -0.4), S("month_six", "not", 0.4)))
    pop(c, W / 2, 160, "1 IN 3 ADULTS DON'T MOVE ENOUGH", t, S("month_six", "one", -0.2), "plum", 48)
    label(c, "LANCET GLOBAL HEALTH · 2024", W / 2, 1000, 34, "sand", "bold", span(t, S("month_six", "lancet", -0.2), S("month_six", "lancet", 0.3)))



# ================================================================ YEAR ONE (biggest escalation)
def s_silence(c, t, t0):
    c.drawRect(skia.Rect(0, 0, W, H), paint("#07050F"))
    gp = span(t, t0 + 0.3, t0 + 1.8)
    glow(c, W / 2, 520, 420, "amber", 0.25 * gp)
    big_text(c, "365", W / 2, 600, 300, 0.3 + 0.7 * gp, "gold")


def bd_year(c, t):
    room_bg(c, t, mode="dark")
    bath_scale(c, W / 2, 330, 1.0, t=t)


def s_calc(c, t, t0):
    explainer_bg(c, t, "deep")
    rows = [("EXTRA STEPS / DAY", "≈ 5,000", t0 + 0.3), ("× CALORIES / STEP", "≈ 0.04", t0 + 1.1), ("× DAYS", "365", t0 + 1.9)]
    for i, (a, b, when) in enumerate(rows):
        al = span(t, when, when + 0.3)
        label(c, a, 300, 240 + i * 120, 50, "cream", "extrabold", al, align="left")
        label(c, b, 1200, 240 + i * 120, 56, "gold", "extrabold", al, align="right")
    al = span(t, S("year_one", "almost", -0.4), S("year_one", "almost", 0.0))
    c.drawLine(300, 620, 1200, 620, paint("cream", al, stroke=5))
    big_text(c, "≈ 10 kg LOST", 760, 800, 100, al, "gold")
    label(c, "ON PAPER", 760, 900, 48, "cream", "extrabold", al)
    for k in range(10):
        a_ = span(t, S("year_one", "almost", -0.4 + 0.06 * k), S("year_one", "almost", -0.2 + 0.06 * k))
        y_ = 1010 - k * 52
        c.drawRRect(rr(1480, y_ - 46, 1720, y_, 12), paint("#5A5470", a_)); c.drawRRect(rr(1480, y_ - 46, 1720, y_, 12), paint("cream", 0.6 * a_, stroke=3))
        label(c, "1 kg", 1600, y_ - 12, 30, "cream", "extrabold", a_)
    if t < S("year_one", "almost", 0):
        pass


def s_scale_year(c, t, t0):
    room_bg(c, t, mode="dark")
    tw = S("year_one", "roughly", -0.1)
    ro = None if t < tw else "-2.5 kg"
    z = keys(t, [(t0, 1.0), (tw, 1.18)])
    with Cam(c, z, W / 2, 700, t=t, shake=span(t, tw, tw + 0.2) - span(t, tw + 0.3, tw + 0.8)):
        bath_scale(c, W / 2, 760, 1.6, t=t, readout=ro, read_col="coral", needle=-0.05)
    if t >= tw:
        kr_cutout(c, lambda k: draw_kr(k, 1620, 940, 1.0, "worried", t))
        pop(c, 420, 220, "NOT 10. ABOUT 2.5", t, tw + 0.2, "coral", 52)


def s_hadza(c, t, t0):
    savanna_bg(c, t)
    for k in range(5):
        x = (200 + k * 260 + (t - t0) * 120) % (W + 300) - 150
        walker_sil(c, x, 860, 1.1 - 0.08 * k, t, phase=k, stick=k % 2 == 0)
    pop(c, W / 2, 160, "THE HADZA · TANZANIA", t, S("year_one", "hadza", -0.2), "plum", 52)
    label(c, "HUNTER-GATHERERS · WALK ALL DAY", W / 2, 1010, 38, "cream", "extrabold", span(t, S("year_one", "huntergatherers", -0.1), S("year_one", "huntergatherers", 0.4)))


def s_cal_bars(c, t, t0):
    explainer_bg(c, t, "deep")
    big_text(c, "CALORIES BURNED PER DAY", W / 2, 160, 60, span(t, t0, t0 + 0.4))
    p1 = ease(span(t, t0 + 0.2, t0 + 1.0)); p2 = ease(span(t, t0 + 0.6, t0 + 1.4))
    calorie_bar(c, 700, 880, 520 * p1 + 2, "HADZA", "coral", 1.0)
    calorie_bar(c, 1220, 880, 510 * p2 + 2, "OFFICE WORKER", "teal", 1.0)
    pop(c, 960, 1025, "ABOUT THE SAME", t, S("year_one", "same", -0.1), "plum", 50)


def s_house(c, t, t0):
    """Daily energy budget: one fixed-size bar shared by LEGS, REPAIR, IMMUNE, FIDGET. Walking grows LEGS, the rest shrink."""
    street_bg(c, t, mode="dusk")
    dim(c, 0.6)
    legs = ease(span(t, t0 + 0.3, S("year_one", "back", 0.3)))
    walker_fig(c, 330, 1010, 0.95, t, rim="gold")
    x0, x1, y = 640, 1820, 520
    big_text(c, "YOUR DAILY ENERGY BUDGET", (x0 + x1) / 2, 300, 54, 1.0, "cream")
    parts = [("LEGS", 0.25 + 0.3 * legs, STEP), ("REPAIR", 0.30 - 0.12 * legs, "teal"), ("IMMUNE", 0.25 - 0.1 * legs, "#B48AE0"),
             ("FIDGET", 0.20 - 0.08 * legs, "coral")]
    x = x0
    for nm, f, colr in parts:
        w_ = (x1 - x0) * f
        c.drawRRect(rr(x + 3, y - 90, x + w_ - 3, y + 90, 22), paint(colr))
        label(c, nm, x + w_ / 2, y + 14, 40 if w_ > 220 else 30, "#1A1236", "extrabold")
        x += w_
    c.drawRRect(rr(x0 - 8, y - 98, x1 + 8, y + 98, 28), paint("cream", 0.9, stroke=6))
    label(c, "SAME TOTAL", (x0 + x1) / 2, y + 170, 46, "gold", "extrabold", span(t, S("year_one", "total", -0.2), S("year_one", "total", 0.2)))
    headline(c, t, "THE TOTAL BARELY CHANGES", S("year_one", "total", -0.1), 1040, 52, "gold")


def s_plate(c, t, t0):
    explainer_bg(c, t, "magenta")
    k = 0.6 + 0.9 * ease(span(t, S("year_one", "plate", -0.3), S("year_one", "plate", 0.5)))
    plate_meal(c, 760, 640, k)
    sneaker(c, 1420, 700, 0.55, glow_a=0.3)
    big_text(c, ">", 1150, 660, 140, span(t, S("year_one", "matters", -0.1), S("year_one", "matters", 0.3)), "gold")
    pop(c, 1420, 300, "STILL HEALTHY", t, S("year_one", "healthy", -0.2), "teal", 46)
    headline(c, t, "YOUR PLATE > YOUR STEPS", S("year_one", "matters", -0.1), 1000, 64, "gold")


# ================================================================ PAYOFF (the brain)
def s_head_return(c, t, t0):
    explainer_bg(c, t, "deep")
    z = keys(t, [(t0, 1.0), (t0 + 4.0, 1.1)])
    with Cam(c, z, W / 2, 560, t=t):
        head_side(c, W / 2, 660, 1.2, glow_a=0.5 + 0.3 * math.sin(t * 2), t=t)
    bath_scale(c, 300, 900, 0.5, t=t, a=0.35)
    headline(c, t, "NEVER ON THE SCALE", S("payoff", "never", -0.1), 130, 64, "gold")


def s_study2011(c, t, t0):
    explainer_bg(c, t, "plum")
    n = int(120 * ease(span(t, t0 + 0.2, S("payoff", "twenty", 0.4))))
    for i in range(n):
        x = 220 + (i % 20) * 78
        y = 420 + (i // 20) * 90
        walker_sil(c, x, y, 0.26, t, colr="teal" if i % 2 else "sand", phase=i)
    big_text(c, f"{n}", W / 2, 260, 120, 1.0, "gold")
    pop(c, W / 2, 110, "2011 · OLDER ADULTS · WALKED 1 YEAR", t, t0 + 0.2, "teal", 44)
    if t > S("payoff", "scanned", -0.2):
        pop(c, W / 2, 1000, "THEN: BRAIN SCANS", t, S("payoff", "scanned", -0.2), "coral", 46)


def s_hippo(c, t, t0):
    explainer_bg(c, t, "deep")
    g = span(t, S("payoff", "grown", -0.3), S("payoff", "grown", 1.0))
    z = keys(t, [(t0, 1.0), (t0 + 3.0, 1.25)])
    with Cam(c, z, W / 2 + 40, 470, t=t):
        head_side(c, W / 2, 620, 1.7, grow=g, glow_a=0.5 + 0.5 * g, t=t)
    pop(c, 1560, 120, "HIPPOCAMPUS = MEMORY", t, S("payoff", "hippocampus", -0.1), "plum", 44)
    big_text(c, "+2%", 330, 760, 150, span(t, S("payoff", "two", -0.2), S("payoff", "two", 0.3)), "gold")


def s_shrink(c, t, t0):
    def left(c, t):
        explainer_bg(c, t, "deep")
        head_side(c, W / 4, 620, 1.0, grow=1.0, glow_a=1.0, t=t)
        label(c, "WALKED: +2%", W / 4, 980, 52, "gold", "extrabold")

    def right(c, t):
        explainer_bg(c, t, "plum")
        sh = span(t, S("payoff", "shrank", -0.2), S("payoff", "shrank", 0.8))
        head_side(c, W * 3 / 4, 620, 1.0, shrink=sh, glow_a=0.0, t=t, line="sand")
        label(c, "ONLY STRETCHED: SHRANK", W * 3 / 4, 980, 46, "sand", "extrabold")
    split(left, right, "WALKERS", "STRETCHING", wipe_at=t0 + 0.2)(c, t, t0)


def s_clock_back(c, t, t0):
    explainer_bg(c, t, "deep")
    head_side(c, 600, 520, 1.1, grow=1.0, glow_a=0.9, t=t)
    cx, cy = 1360, 520
    glow(c, cx, cy, 340, "gold", 0.4)
    c.drawCircle(cx, cy, 230, paint("#14203E")); c.drawCircle(cx, cy, 230, paint("gold", stroke=10))
    ang = math.radians(-90 - 720 * ease(span(t, t0 + 0.4, S("payoff", "ageing", 0.6))))
    c.drawLine(cx, cy, cx + 170 * math.cos(ang), cy + 170 * math.sin(ang), paint("cream", stroke=12))
    c.drawLine(cx, cy, cx + 110 * math.cos(ang / 12), cy + 110 * math.sin(ang / 12), paint("cream", stroke=16))
    big_text(c, "BRAIN AGEING: 1–2 YEARS BACK", W / 2, 980, 60, span(t, S("payoff", "turned", -0.1), S("payoff", "turned", 0.4)), "gold")


# ================================================================ BONUS + OUTRO
def s_seven(c, t, t0):
    explainer_bg(c, t, "magenta")
    v = 7000 * ease(span(t, t0 + 0.1, S("bonus", "seven", 0.4)))
    step_phone(c, W / 2, 520, 1.15, v, goal=7000, t=t, sub="MOST OF THE BENEFIT", done_flash=span(t, S("bonus", "seven", 0.3), S("bonus", "seven", 0.7)))
    pop(c, 1450, 300, "BEST PART", t, t0 + 0.1, "teal", 52)


def s_callback(c, t, t0):
    tn = S("bonus", "now", -0.2)
    if t < tn:   # the Day 1 bedroom, dimmed memory
        room_bg(c, t, mode="night", lamp=0.4)
        figure(c, W / 2 + 200 * math.sin((t - t0) * 1.2), 1000, 1.05, arm_l=100, arm_r=80, expr="tired", a=0.7)
        dim(c, 0.3)
        pop(c, W / 2, 180, "REMEMBER 11:50 PM?", t, t0 + 0.2, "plum", 52)
    else:
        street_bg(c, t, mode="dusk")
        x = 400 + 800 * span(t, tn, tn + 6.0)
        figure(c, x, 1000, 1.0, arm_l=100 + 20 * math.sin(t * 6), arm_r=80 - 20 * math.sin(t * 6), expr="happy", rim="gold")
        step_phone(c, 1620, 440, 0.6, 10000, t=t, done_flash=span(t, tn + 0.4, tn + 0.8) * 0.5)
        pop(c, 1400, 140, "10,000 · DIDN'T EVEN NOTICE", t, S("bonus", "happens", -0.2), "teal", 40)


def s_tease(c, t, t0):
    explainer_bg(c, t, "deep")
    alarm_clock(c, W / 2, 600, 1.2, t, ring=span(t, S("sign_off", "five", -0.2), S("sign_off", "five", 0.2)))
    big_text(c, "NEXT: WHAT IF YOU WOKE UP AT 5 AM FOR 30 DAYS?", W / 2, 180, 50, span(t, t0 + 0.3, t0 + 0.8), "gold")



# ================================================================ extra cuts (keep shots 2-5 s)
def s_pacing_phone(c, t, t0):
    room_bg(c, t, mode="night", lamp=0.4)
    dim(c, 0.3)
    tw = S("day_one", "done", -0.1)
    v = 9990 if t < tw else 10000
    z = keys(t, [(t0, 1.0), (tw, 1.15)])
    with Cam(c, z, W / 2, 540, t=t):
        step_phone(c, W / 2, 540, 1.35, v, t=t, clock="11:50 PM", done_flash=span(t, tw, tw + 0.3) - span(t, tw + 1.0, tw + 1.6))
    if t >= tw:
        pop(c, 1450, 300, "DONE.", t, tw, "teal", 80)
    else:
        pop(c, 1450, 300, "10 MORE...", t, t0 + 0.2, "coral", 56)


def s_box_close(c, t, t0):
    explainer_bg(c, t, "magenta")
    z = keys(t, [(t0, 1.0), (t0 + 3.0, 1.25)])
    with Cam(c, z, W / 2, 620, t=t):
        pedometer_box(c, W / 2, 560, 1.3, t=t)
    pop(c, W / 2, 110, "MANPO-KEI = \"10,000 STEP METER\"", t, S("week_one", "meter", -0.5), "coral", 48)


def s_kanji_a(c, t, t0):
    explainer_bg(c, t, "deep")
    glow(c, W / 2, 520, 360, "gold", 0.3)
    kanji_man(c, W / 2, 560, 1.4, 0.0, colr="cream")
    pop(c, W / 2, 140, "THE JAPANESE SYMBOL FOR 10,000", t, S("week_one", "symbol", -0.3), "plum", 46)
    label(c, "HARVARD'S I-MIN LEE", W / 2, 1010, 36, "sand", "bold", span(t, S("week_one", "harvard", 0), S("week_one", "harvard", 0.4)))


def s_seven_studies(c, t, t0):
    explainer_bg(c, t, "plum")
    for i in range(7):
        a = span(t, t0 + 0.15 * i, t0 + 0.15 * i + 0.3)
        paper(c, 360 + i * 200, 560 + (1 - ease(a)) * 200 + 30 * (i % 2), 0.75, "STUDY", f"#{i + 1}", ["teal", "coral", "plum"][i % 3], (i - 3) * 3, a)
    pop(c, W / 2, 180, "IRELAND · 7 STUDIES POOLED", t, S("month_one", "ireland", -0.2), "teal", 50)


def s_people_steps(c, t, t0):
    def left(c, t):
        room_bg(c, t, mode="night")
        figure(c, W / 4, 1000, 1.0, arm_l=60, arm_r=40, seated=True, expr="tired")
        label(c, "2,000 / DAY", W / 4, 200, 60, "sand", "extrabold")

    def right(c, t):
        street_bg(c, t, mode="dusk")
        walker_fig(c, W * 3 / 4, 1000, 1.0, t)
        label(c, "7,000 / DAY", W * 3 / 4, 200, 60, "gold", "extrabold")
    split(left, right, None, None, wipe_at=t0 + 0.4)(c, t, t0)


def s_check_phone(c, t, t0):
    room_bg(c, t, mode="dusk")
    sh = 4 * math.sin(t * 30) * span(t, t0 + 0.2, t0 + 0.6)
    step_phone(c, W / 2 + sh, 540, 1.2, 0, t=t, sub="YOUR STEPS TODAY")
    big_text(c, "?", W / 2, 540, 140, span(t, t0 + 0.1, t0 + 0.4), "gold")
    pop(c, W / 2, 1000, "BE HONEST", t, S("month_three", "honest", -0.2), "coral", 52)


def s_you_out(c, t, t0):
    explainer_bg(c, t, "magenta")
    for k in range(5):
        figure(c, 260 + k * 170, 1000, 0.7, arm_l=60, arm_r=40, expr="tired", a=0.35, shirt="#4A4660")
    p = ease(span(t, t0 + 0.2, S("month_six", "not", 0.4)))
    walker_fig(c, 900 + 650 * p, 1000, 1.0, t, rim="gold")
    glow(c, 900 + 650 * p, 650, 300, "gold", 0.4 * p)
    pop(c, 1450, 180, "NOT ANYMORE", t, S("month_six", "not", -0.1), "teal", 60)


def s_healthy(c, t, t0):
    street_bg(c, t, mode="dusk")
    walker_fig(c, 700, 1010, 1.15, t)
    heart(c, 1350, 480, 1.1, t, rate=1.0, colr="coral")
    pop(c, 1350, 200, "WALKING = HEALTHY", t, S("year_one", "healthy", -0.2), "teal", 52)


def s_scan(c, t, t0):
    explainer_bg(c, t, "deep")
    head_side(c, W / 2, 600, 1.3, glow_a=0.3, t=t)
    for k in range(3):   # scanner rings sweeping
        ph = ((t - t0) * 0.6 + k / 3) % 1
        c.drawCircle(W / 2, 480, 200 + 260 * ph, paint("teal", (1 - ph) * 0.6, stroke=6))
    y = 260 + 440 * (0.5 + 0.5 * math.sin((t - t0) * 2))
    c.drawLine(W / 2 - 360, y, W / 2 + 360, y, paint("teal", 0.8, stroke=4))
    pop(c, W / 2, 1000, "BRAIN SCANS", t, t0 + 0.2, "coral", 52)


# ================================================================ chapter cards over their own scene
def scene_card(value, name, backdrop):
    def f(c, t, t0):
        p = span(t, t0, t0 + 1.4)
        bp = skia.Paint(); bp.setImageFilter(skia.ImageFilters.Blur(14, 14))
        c.saveLayer(None, bp)
        backdrop(c, t)
        c.restore()
        g = skia.Paint(AntiAlias=True)
        g.setShader(skia.GradientShader.MakeRadial(skia.Point(W / 2, H / 2), 900, [col("space", 0.72), col("space", 0.88)]))
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
        big_text(c, name, cx, cy + 200, 56, span(p, 0.35, 0.7), "cream", "bold")
    f.kind = "card"
    f.__name__ = "card"
    return f


def bd_day1(c, t):
    room_bg(c, t, mode="dusk"); step_phone(c, W / 2, 520, 1.0, 2800, t=t)


def bd_week1(c, t):
    room_bg(c, t, mode="morning"); stairs(c, W / 2, 900, 1.2)


def bd_month1(c, t):
    room_bg(c, t, mode="morning"); bath_scale(c, W / 2, 330, 1.0, t=t)


def bd_month3(c, t):
    room_bg(c, t, mode="dusk"); grey_cloud(c, W / 2, 400, 1.2, t=t)


def bd_month6(c, t):
    route_map(c, t, "PARIS", "ROME", 0.5, ax=520, ay=330, bx=1380, by=820, bend=60, walker=False)


# ================================================================ the list
def SHOTS():
    hook = [
        (0.0, s_hook_walk, "cut"),
        (S("hook", "thats", -0.15), s_hook_map, "whip"),
        (S("hook", "and", -0.2), s_hook_scale, "cut"),
        (S("hook", "but", -0.2), s_hook_head, "fade"),
        (E("hook") + 0.1, logo_sting(), "flash"),
    ]
    promise = [
        (E("hook") + 1.9, counter(0, 9, "{:.0f}", until=S("promise", "nine", 0.6), label=None, size=200,
                                  label_at=S("promise", "studies", -0.2), bg=papers_bg), "fade"),
        (S("promise", "first", -0.3), s_january, "iris"),
        (S("promise", "work", -0.4), s_desk, "cut"),
        (S("promise", "thats", -0.3), s_world, "whip"),
        (S("promise", "world", -0.3), counter(0, 4961, "{:,.0f}", until=S("promise", "average", 0.6), label="WORLD AVERAGE · STEPS A DAY",
                                              label_at=S("promise", "average", -0.2), bg=lambda c, t: street_bg(c, t, mode="dusk")), "cut"),
        (S("promise", "so", -0.3), s_promise_goal, "zoom"),
    ]
    day1 = [
        (B("day_one") - 0.6, scene_card("DAY 1", "The time", bd_day1), "iris"),
        (S("day_one", "six", -0.3), s_six_pm, "iris"),
        (S("day_one", "walk", -0.4), s_store, "whip"),
        (S("day_one", "then", -0.3, 2), s_laps, "cut"),
        (S("day_one", "and", -0.3), kr_react("worried", "HIDDEN COST"), "whip"),
        (S("day_one", "take", -0.9), s_cost, "cut"),
        (S("day_one", "over", -0.3), s_25days, "cut"),
        (S("day_one", "eleven", -0.3), s_pacing, "fade"),
        (S("day_one", "nine", -0.3), s_pacing_phone, "zoom"),
    ]
    week1 = [
        (B("week_one") - 0.6, scene_card("WEEK 1", "The myth", bd_week1), "iris"),
        (S("week_one", "your", -0.3), s_calves, "iris"),
        (S("week_one", "but", -0.3), s_sleep, "fade"),
        (S("week_one", "and", -0.3), s_why, "whip"),
        (S("week_one", "heres", -0.3), kr_react("curious", "HERE'S THE FUNNY PART"), "cut"),
        (S("week_one", "no", -0.3), layer(statement("NO DOCTOR EVER DID.", size=110, color="gold"), stamp_at("NOT SCIENCE", S("week_one", "doctor", 0.3), y=760)), "flash"),
        (S("week_one", "in", -0.3), s_pedometer, "whip"),
        (S("week_one", "manpokei", -0.3), s_box_close, "zoom"),
        (S("week_one", "why", -0.3, 2), s_kanji_a, "fade"),
        (S("week_one", "looks", -0.3), s_kanji, "cut"),
        (S("week_one", "so", -0.3), s_meme_nobody, "cut"),
    ]
    month1 = [
        (B("month_one") - 0.6, scene_card("MONTH 1", "Sugar", bd_month1), "iris"),
        (S("month_one", "three", -0.3), s_scale_month, "iris"),
        (S("month_one", "few", -0.4), s_meme_expect, "cut"),
        (S("month_one", "friend", -0.5), s_friend, "whip"),
        (S("month_one", "but", -0.3), s_dinner_walk, "fade"),
        (S("month_one", "researchers", -0.3), s_seven_studies, "cut"),
        (S("month_one", "even", -0.3), s_sugar, "whip"),
        (S("month_one", "body", -0.5), s_changing, "fade"),
    ]
    month3 = [
        (B("month_three") - 0.6, scene_card("MONTH 3", "Mood", bd_month3), "iris"),
        (S("month_three", "dont", -0.4), s_no_lift, "iris"),
        (S("month_three", "and", -0.3), s_cloud, "fade"),
        (S("month_three", "huge", -0.4), s_lancet, "whip"),
        (S("month_three", "people", -0.3), s_people_steps, "cut"),
        (S("month_three", "had", -0.3), s_mood_bars, "whip"),
        (S("month_three", "quick", -0.3), comment_prompt("What's your step count today?",
                                                         bg=lambda c, t: room_bg(c, t, mode="dusk")), "fade"),
        (S("month_three", "check", -0.3), s_check_phone, "cut"),
    ]
    month6 = [
        (B("month_six") - 0.6, scene_card("MONTH 6", "One in three", bd_month6), "iris"),
        (S("month_six", "youve", -0.3), s_paris_rome, "iris"),
        (S("month_six", "and", -0.3), s_crowd, "whip"),
        (S("month_six", "six", -0.3, 2), s_you_out, "fade"),
    ]
    year = [
        (E("month_six") + 0.1, s_silence, "cut"),
        (max(B("year_one") - 0.6, E("month_six") + 0.5), scene_card("DAY 365", "The scale", bd_year), "cut"),
        (S("year_one", "i", -0.3), s_calc, "fade"),
        (S("year_one", "you", -0.3), s_scale_year, "cut"),
        (S("year_one", "why", -0.3), s_hadza, "iris"),
        (S("year_one", "they", -0.3), s_cal_bars, "cut"),
        (S("year_one", "when", -0.3), s_house, "fade"),
        (S("year_one", "walking", -0.3, 2), s_healthy, "whip"),
        (S("year_one", "but", -0.3), s_plate, "cut"),
    ]
    payoff = [
        (B("payoff") - 0.2, kr_react("thinking", "ALL FOR NOTHING?"), "fade"),
        (S("payoff", "no", -0.3), s_head_return, "iris"),
        (S("payoff", "twenty", -0.6), s_study2011, "whip"),
        (S("payoff", "then", -0.3), s_scan, "cut"),
        (S("payoff", "hippocampus", -0.4), s_hippo, "zoom"),
        (S("payoff", "group", -0.6), s_shrink, "cut"),
        (S("payoff", "walkers", -0.4), s_clock_back, "fade"),
    ]
    bonus = [
        (B("bonus") - 0.2, s_seven, "flash"),
        (S("bonus", "comment", -0.3), comment_prompt("Give up Netflix... or sleep?",
                                                     bg=lambda c, t: room_bg(c, t, mode="night")), "fade"),
        (S("bonus", "remember", -0.3), s_callback, "iris"),
    ]
    outro = [
        (B("sign_off") - 0.2, zoom(s_tease, 1.0, 1.15, dur=9.0), "fade"),
        (E("sign_off") + 0.3, end_screen(), "fade"),
    ]
    out = []
    for blk in (hook, promise, day1, week1, month1, month3, month6, year, payoff, bonus, outro):
        for start, fn, tr in blk:
            k = getattr(fn, "kind", None)
            if k in ("card", "logo", "end") or fn in (s_silence,) or getattr(fn, "__name__", "") in ("comment_prompt", "kr_react", "statement", "counter", "s_tease"):
                out.append((start, fn, tr))
            else:
                out.append((start, CS(fn), tr))
    return out


LAST_BEAT = BEAT_KEYS[-1]
