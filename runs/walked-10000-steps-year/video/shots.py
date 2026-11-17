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
def s_hook_walk(c, t, t0):
    """Frame 0: night street, the glowing sneakers mid-stride, the phone counter racing past 10,000 to a year."""
    street_bg(c, t)
    z = keys(t, [(t0, 1.08), (t0 + 3.0, 1.0)])
    with Cam(c, z, W / 2, 620, t=t):
        bob = 18 * math.sin(t * 7)
        sneaker(c, 560, 760 - max(0, bob), 1.35, glow_a=1.0, rot=-8 + 4 * math.sin(t * 7))
        sneaker(c, 860, 790 - max(0, -bob), 1.35, glow_a=1.0, rot=6 - 4 * math.sin(t * 7), colr="#E05A3A")
        for k in range(5):
            shoe_print(c, 1000 + k * 120, 900 + (k % 2) * 30, 0.6, rot=90, a=0.25 + 0.12 * k)
        p = span(t, t0 + 0.3, S("hook", "year", 0.3))
        steps = 10000 + 3640000 * ease(span(p, 0.15, 1.0))
        step_phone(c, 1420, 520, 0.95, steps, 10000 if steps <= 10000 else 3650000, t=t, sub="STEPS · DAY 1" if steps <= 10000 else "STEPS · 1 YEAR",
                   done_flash=1.0 - span(t, t0 + 0.8, t0 + 1.4))
        head_side(c, 230, 260, 0.45, grow=0.0, glow_a=0.35 + 0.15 * math.sin(t * 3), a=0.35)
    pill(c, W / 2, 80, 1.0, "10,000 STEPS · EVERY DAY · 1 YEAR", "coral", "cream", 40)


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
        x = 300 + (i % 5) * 330
        y = 300 if i < 5 else 820
        paper(c, x, y + (1 - ease(a)) * 200, 0.7, names[i], "STUDY", ["teal", "coral", "plum"][i % 3], (rng(i, 4) - 0.5) * 14, a)


def s_january(c, t, t0):
    desk_bg(c, t, mode="day")
    calendar_page(c, 980, 420, 1.5, "JAN", "1", rot=-4)
    pop(c, 980, 820, "NEW YEAR", t, t0 + 0.3, "plum", 48)


def s_desk(c, t, t0):
    desk_bg(c, t)
    figure(c, 700, 1000, 1.0, arm_l=60, arm_r=40, seated=True, expr="neutral")
    v = 5012 * ease(span(t, S("promise", "phone", -0.2), S("promise", "five", 0.6)))
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
    x = 200 + 900 * span(t, t0, t0 + 4.5)
    walker_sil(c, x, 830, 1.2, t, colr="#0A0618")
    pop(c, 1450, 300, "GROCERY STORE", t, S("day_one", "grocery", -0.1), "teal", 44)
    if t > S("day_one", "long", -0.2):
        pop(c, 560, 240, "THE LONG WAY BACK", t, S("day_one", "long", -0.2), "plum", 44)


def s_laps(c, t, t0):
    """Top view of the parking lot: the walker loops, a lap counter ticks."""
    c.drawRect(skia.Rect(0, 0, W, H), paint("#1C1A30"))
    for k in range(9):
        c.drawLine(360 + k * 150, 300, 360 + k * 150, 420, paint("cream", 0.6, stroke=6))
        c.drawLine(360 + k * 150, 660, 360 + k * 150, 780, paint("cream", 0.6, stroke=6))
    for k in range(8):
        c.drawRRect(rr(385 + k * 150, 310, 485 + k * 150, 410, 16), paint(["#3A6A8A", "#8A2A5C", "#C8A040", "#4A4660"][k % 4], 0.9))
    loop = skia.Path(); loop.addRRect(rr(260, 230, 1660, 850, 160))
    c.drawPath(loop, dashed(STEP, 0.5, 6, 14, 12))
    meas = skia.PathMeasure(loop, False); L = meas.getLength()
    u = ((t - t0) * 0.35) % 1
    pos, _ = meas.getPosTan(L * u)
    glow(c, pos.x(), pos.y(), 90, "gold", 0.7)
    c.drawCircle(pos.x(), pos.y(), 20, paint("gold"))
    laps = 1 + int((t - t0) * 0.35)
    big_text(c, f"LAP {laps}", W / 2, 560, 110, 1.0, "gold")
    label(c, "BUILDING PARKING LOT", W / 2, 650, 40, "sand", "extrabold")


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
    c.drawRRect(rr(420, 700, 1500, 860, 30), paint("#3A2A5E"))
    c.drawRRect(rr(420, 640, 1500, 720, 30), paint("#5A4A8A"))
    ellipse(c, 560, 650, 120, 50, paint("cream", 0.9))
    head_side(c, 640, 600, 0.35, glow_a=0.5 + 0.2 * math.sin(t * 2), a=0.9)
    for k in range(3):
        ph = ((t - t0) * 0.5 + k / 3) % 1
        label(c, "z", 760 + 60 * ph + k * 20, 520 - 160 * ph, int(40 + 30 * ph), "cream", "extrabold", 1 - ph)
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
    pedometer_box(c, 760, 860, 0.45, t=t * 3, rot=-8)
    kr_cutout(c, lambda k: draw_kr(k, 1560, 1000, 1.3, "neutral", t))
    stamp(c, 1180, 820, "AN ADVERT", span(t, S("week_one", "advert", -0.1), S("week_one", "advert", 0.2)), "coral", -12)


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
    bubble(c, 1300, 300, 860, 150, "WALKING DOESN'T WORK, BRO", 52, a=span(t, S("month_one", "walking", -0.1), S("month_one", "walking", 0.3)), tail=-1)


def s_dinner_walk(c, t, t0):
    street_bg(c, t)
    x = 300 + 1000 * span(t, t0, t0 + 6.0)
    walker_sil(c, x, 830, 1.3, t, colr="#0A0618")
    plate_meal(c, 1650, 960, 0.6)
    pop(c, W / 2, 180, "AFTER DINNER", t, S("month_one", "dinner", -0.2), "teal", 52)


def s_sugar(c, t, t0):
    explainer_bg(c, t, "deep")
    x0, y0, w, h = 300, 860, 1320, 560
    c.drawLine(x0, y0, x0 + w, y0, paint("cream", stroke=4)); c.drawLine(x0, y0, x0, y0 - h - 40, paint("cream", stroke=4))
    label(c, "BLOOD SUGAR AFTER A MEAL", x0 + 10, y0 - h - 60, 34, "sand", "extrabold", align="left")
    label(c, "TIME →", x0 + w - 60, y0 + 50, 30, "sand", "bold")
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
    label(c, "LIFT", 1450, 260, 44, "cream", "extrabold")
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
    grey_cloud(c, W / 2, 300, s_, a=0.9, t=t)
    headline(c, t, "BAD DAYS FEEL LESS BAD", S("month_three", "bad", -0.1), 110, 56, "gold")


def s_lancet(c, t, t0):
    papers_l = ["COHORT", "TRIAL", "STUDY"]
    explainer_bg(c, t, "plum")
    n = int(57 * ease(span(t, t0 + 0.2, S("month_three", "studies", 0.4))))
    for i in range(min(n, 57)):
        x = 260 + (i % 19) * 77
        y = 700 + (i // 19) * 90
        paper(c, x, y, 0.22, "", "", ["teal", "coral", "plum"][i % 3], (rng(i, 4) - 0.5) * 20, 1.0)
    big_text(c, f"{n} STUDIES", W / 2, 400, 130, 1.0, "gold")
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
    crowd(c, W / 2, 560, 11, 3, 11, t, you_p=span(t, S("month_six", "not", -0.4), S("month_six", "not", 0.4)))
    pop(c, W / 2, 160, "1 IN 3 ADULTS DON'T MOVE ENOUGH", t, S("month_six", "one", -0.2), "plum", 48)
    label(c, "LANCET GLOBAL HEALTH · 2024", W / 2, 1000, 34, "sand", "bold", span(t, S("month_six", "lancet", -0.2), S("month_six", "lancet", 0.3)))
    if t > S("month_six", "not", -0.2):
        pop(c, W / 2, 900, "NOT ANYMORE", t, S("month_six", "not", -0.1), "teal", 56)


# ================================================================ YEAR ONE (biggest escalation)
def s_silence(c, t, t0):
    c.drawRect(skia.Rect(0, 0, W, H), paint("#07050F"))
    gp = span(t, t0 + 0.3, t0 + 1.8)
    big_text(c, "365", W / 2, 560, 260, 1.0, "#2A2040")
    glow(c, W / 2, 520, 300, "amber", 0.08 * gp)


def bd_year(c, t):
    room_bg(c, t, mode="dark")
    bath_scale(c, W / 2, 760, 1.3, t=t)


def s_calc(c, t, t0):
    explainer_bg(c, t, "deep")
    rows = [("EXTRA STEPS / DAY", "≈ 5,000", t0 + 0.3), ("× CALORIES / STEP", "≈ 0.04", t0 + 1.1), ("× DAYS", "365", t0 + 1.9)]
    for i, (a, b, when) in enumerate(rows):
        al = span(t, when, when + 0.3)
        label(c, a, 520, 300 + i * 120, 50, "cream", "extrabold", al, align="left")
        label(c, b, 1400, 300 + i * 120, 56, "gold", "extrabold", al, align="right")
    al = span(t, S("year_one", "almost", -0.4), S("year_one", "almost", 0.0))
    c.drawLine(520, 640, 1400, 640, paint("cream", al, stroke=5))
    big_text(c, "≈ 10 kg LOST", W / 2, 800, 110, al, "gold")
    label(c, "ON PAPER", W / 2, 900, 44, "sand", "extrabold", al)
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
    p1 = ease(span(t, t0 + 0.2, t0 + 1.0)); p2 = ease(span(t, S("year_one", "office", -0.3), S("year_one", "office", 0.5)))
    calorie_bar(c, 700, 880, 520 * p1 + 2, "HADZA", "coral", 1.0)
    walker_sil(c, 700, 300 + 520 * (1 - p1), 0.5, t, colr="cream", a=p1)
    calorie_bar(c, 1220, 880, 510 * p2 + 2, "OFFICE WORKER", "teal", 1.0 if p2 > 0 else 0.3)
    pop(c, 960, 1025, "ABOUT THE SAME", t, S("year_one", "same", -0.1), "plum", 50)


def s_house(c, t, t0):
    explainer_bg(c, t, "plum")
    legs = ease(span(t, t0 + 0.3, S("year_one", "back", 0.3)))
    house_body(c, W / 2, 800, 1.0, t, legs=legs)
    headline(c, t, "THE TOTAL BARELY CHANGES", S("year_one", "total", -0.1), 1050, 52, "gold")


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
        head_side(c, W / 2, 600, 1.45, glow_a=0.5 + 0.3 * math.sin(t * 2), t=t)
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
    pop(c, 1500, 260, "HIPPOCAMPUS = MEMORY", t, S("payoff", "hippocampus", -0.1), "plum", 44)
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
        pop(c, 1620, 140, "10,000 · DIDN'T EVEN NOTICE", t, S("bonus", "happens", -0.2), "teal", 40)


def s_tease(c, t, t0):
    room_bg(c, t, mode="dark")
    alarm_clock(c, W / 2, 600, 1.2, t, ring=span(t, S("sign_off", "five", -0.2), S("sign_off", "five", 0.2)))
    big_text(c, "NEXT: WHAT IF YOU WOKE UP AT 5 AM FOR 30 DAYS?", W / 2, 180, 50, span(t, t0 + 0.3, t0 + 0.8), "gold")


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
    room_bg(c, t, mode="morning"); bath_scale(c, W / 2, 760, 1.3, t=t)


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
        (E("hook") + 1.9, counter(0, 9, "{:.0f}", until=S("promise", "nine", 0.6), label="STUDIES CHECKED", size=200,
                                  label_at=S("promise", "studies", -0.2), bg=papers_bg), "fade"),
        (S("promise", "first", -0.3), s_january, "iris"),
        (S("promise", "work", -0.4), s_desk, "cut"),
        (S("promise", "thats", -0.3), s_world, "whip"),
        (S("promise", "so", -0.3), s_promise_goal, "zoom"),
    ]
    day1 = [
        (B("day_one") - 0.6, scene_card("DAY 1", "The time", bd_day1), "iris"),
        (S("day_one", "six", -0.3), s_six_pm, "iris"),
        (S("day_one", "walk", -0.4), s_store, "whip"),
        (S("day_one", "then", -0.3, 2), s_laps, "cut"),
        (S("day_one", "and", -0.3), s_cost, "whip"),
        (S("day_one", "over", -0.3), s_25days, "cut"),
        (S("day_one", "eleven", -0.3), s_pacing, "fade"),
    ]
    week1 = [
        (B("week_one") - 0.6, scene_card("WEEK 1", "The myth", bd_week1), "iris"),
        (S("week_one", "your", -0.3), s_calves, "iris"),
        (S("week_one", "but", -0.3), s_sleep, "fade"),
        (S("week_one", "and", -0.3), s_why, "whip"),
        (S("week_one", "heres", -0.3), kr_react("curious", "HERE'S THE FUNNY PART"), "cut"),
        (S("week_one", "no", -0.3), layer(statement("NO DOCTOR EVER DID.", size=110, color="gold"), stamp_at("NOT SCIENCE", S("week_one", "doctor", 0.3), y=760)), "flash"),
        (S("week_one", "in", -0.3), s_pedometer, "whip"),
        (S("week_one", "why", -0.3, 2), s_kanji, "fade"),
        (S("week_one", "so", -0.3), s_meme_nobody, "cut"),
    ]
    month1 = [
        (B("month_one") - 0.6, scene_card("MONTH 1", "Sugar", bd_month1), "iris"),
        (S("month_one", "three", -0.3), s_scale_month, "iris"),
        (S("month_one", "few", -0.4), s_meme_expect, "cut"),
        (S("month_one", "friend", -0.5), s_friend, "whip"),
        (S("month_one", "but", -0.3), s_dinner_walk, "fade"),
        (S("month_one", "researchers", -0.3), s_sugar, "cut"),
        (S("month_one", "body", -0.5), s_changing, "fade"),
    ]
    month3 = [
        (B("month_three") - 0.6, scene_card("MONTH 3", "Mood", bd_month3), "iris"),
        (S("month_three", "dont", -0.4), s_no_lift, "iris"),
        (S("month_three", "and", -0.3), s_cloud, "fade"),
        (S("month_three", "huge", -0.4), s_lancet, "whip"),
        (S("month_three", "people", -0.3), s_mood_bars, "cut"),
        (S("month_three", "quick", -0.3), comment_prompt("What's your step count today?",
                                                         bg=lambda c, t: room_bg(c, t, mode="dusk")), "fade"),
    ]
    month6 = [
        (B("month_six") - 0.6, scene_card("MONTH 6", "One in three", bd_month6), "iris"),
        (S("month_six", "youve", -0.3), s_paris_rome, "iris"),
        (S("month_six", "and", -0.3), s_crowd, "whip"),
    ]
    year = [
        (E("month_six") + 0.1, s_silence, "cut"),
        (max(B("year_one") - 0.6, E("month_six") + 0.5), scene_card("DAY 365", "The scale", bd_year), "cut"),
        (S("year_one", "i", -0.3), s_calc, "fade"),
        (S("year_one", "you", -0.3), s_scale_year, "cut"),
        (S("year_one", "why", -0.3), s_hadza, "iris"),
        (S("year_one", "they", -0.3), s_cal_bars, "cut"),
        (S("year_one", "when", -0.3), s_house, "fade"),
        (S("year_one", "keeps", -0.6), s_plate, "whip"),
    ]
    payoff = [
        (B("payoff") - 0.2, kr_react("thinking", "ALL FOR NOTHING?"), "fade"),
        (S("payoff", "no", -0.3), s_head_return, "iris"),
        (S("payoff", "twenty", -0.6), s_study2011, "whip"),
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
        (B("sign_off") - 0.2, s_tease, "fade"),
        (E("sign_off") + 0.3, end_screen(), "fade"),
    ]
    out = []
    for blk in (hook, promise, day1, week1, month1, month3, month6, year, payoff, bonus, outro):
        for start, fn, tr in blk:
            k = getattr(fn, "kind", None)
            if k in ("card", "logo", "end") or fn in (s_silence, s_tease) or getattr(fn, "__name__", "") in ("comment_prompt", "kr_react", "statement"):
                out.append((start, fn, tr))
            else:
                out.append((start, CS(fn), tr))
    return out


LAST_BEAT = BEAT_KEYS[-1]
