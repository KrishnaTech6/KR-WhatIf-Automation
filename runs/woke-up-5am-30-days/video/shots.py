"""Shot list: What If You Woke Up at 5 AM for 30 Days? (atlas style).
Threads: (1) the split screen of two bedrooms (frame 0) returns on Day 3, Day 21 (the answer) and Day 31;
(2) the sleep bar with a dashed 7-hour outline (Day 3, Day 21, Day 30); (3) the BED sub-dial on the clock = the twist."""
import math
import skia
from krwi.lib import *  # noqa: F401,F403
from art import *  # noqa: F401,F403


def S(beat, word, off=0.0, n=1):
    return at(beat, word, off, n)


def night(c, t):
    explainer_bg(c, t, "deep")


def month_grid(c, t):
    """30-day calendar whose squares fill in with 2-hour wedges (behind the 60-hours counter)."""
    explainer_bg(c, t)
    t0 = S("day_one", "month", -0.3)
    for k in range(30):
        x = 360 + (k % 10) * 120; y = 760 + (k // 10) * 90
        on = t > t0 + 0.05 * k
        c.drawRRect(rr(x - 46, y - 36, x + 46, y + 36, 10), paint("gold" if on else "sand", 0.85 if on else 0.15))
        if on:
            label(c, "+2h", x, y + 12, 28, "ink", "extrabold")


def two_nights(c, t):
    night(c, t)
    for i, x in enumerate((720, 1200)):
        glow(c, x, 790, 160, "plum", 0.4)
        c.drawCircle(x, 790, 80, paint("gold")); c.drawCircle(x + 34, 770, 72, paint("deep"))
        c.drawCircle(x, 790, 130, dashed("coral", 0.9, 6))
        xmark(c, x, 790, 1.4, 1.0)


def alarm_row(c, t):
    explainer_bg(c, t, "plum")
    for i, (h, m) in enumerate(((5, 0), (6, 30), (7, 0), (8, 15))):
        alarm_clock(c, 330 + i * 420, 860, 0.7, t, hour=h, minute=m, ring=0.3 if i == 0 else 0.0)


# ---------------------------------------------------------------- HOOK
def _title_strip(c, t, t0, txt="SPOT THE DIFFERENCE"):
    p = span(t, t0, t0 + 0.4)
    c.drawRRect(rr(W / 2 - 340, 30, W / 2 + 340, 112, 41), paint("space", 0.8 * p))
    c.drawRRect(rr(W / 2 - 340, 30, W / 2 + 340, 112, 41), paint("gold", 0.9 * p, stroke=4))
    label(c, txt, W / 2 + 24, 88, 48, "gold", "extrabold", p)
    cx, cy = W / 2 - 290, 71
    c.drawCircle(cx, cy, 22, paint("cream", 0.25 * p, stroke=6))
    arc = skia.Path(); arc.addArc(skia.Rect(cx - 22, cy - 22, cx + 22, cy + 22), -90, 360 * ((t * 0.4) % 1))
    c.drawPath(arc, paint("gold", p, stroke=6))


def s_split_open(c, t, t0):
    with Cam(c, keys(t, [(t0, 1.08), (t0 + 4, 1.0)]), W / 2, 600, t=t):
        bed_scene(c, 0, 960, t, bedtime=11, ring=1.0)
        bed_scene(c, 960, 960, t + 0.11, bedtime=10, ring=1.0)
    c.drawLine(960, 0, 960, H, paint("cream", 0.9, stroke=6))
    _title_strip(c, t, t0)
    c.drawRRect(rr(W / 2 - 230, 976, W / 2 + 230, 1048, 36), paint("space", 0.8))
    label(c, "5 AM · 30 DAYS", W / 2, 1030, 50, "cream", "extrabold")


def s_hook_battery(c, t, t0):
    explainer_bg(c, t, "plum")
    c.drawLine(960, 0, 960, H, paint("cream", 0.5, stroke=4))
    p = span(t, t0, t0 + 2.4)
    battery(c, 480, 560, 1.2, 1 - 0.85 * ease(p), t)
    battery(c, 1440, 560, 1.2, 1.0, t)
    big_text(c, "DAY 14", W / 2, 150, 84, span(t, t0, t0 + 0.3), "gold")
    if p > 0.6:
        pop(c, 480, 960, "= 2 NIGHTS NO SLEEP?", t, t0 + 1.5, "coral", 44)


def s_split_search(c, t, t0):
    bed_scene(c, 0, 960, t, bedtime=11)
    bed_scene(c, 960, 960, t + 0.11, bedtime=10)
    c.drawLine(960, 0, 960, H, paint("cream", 0.9, stroke=6))
    _title_strip(c, t, t0, "FIND IT BEFORE DAY 21")
    # a magnifier sweeping over both rooms (never stops on the answer)
    mx = W / 2 + math.sin((t - t0) * 1.6) * 700
    my = 560 + math.cos((t - t0) * 2.3) * 200
    c.drawCircle(mx, my, 110, paint("cream", 0.12))
    c.drawCircle(mx, my, 110, paint("gold", stroke=12))
    c.drawLine(mx + 78, my + 78, mx + 170, my + 170, paint("gold", stroke=24))


# ---------------------------------------------------------------- PROMISE
def s_rules(c, t, t0):
    explainer_bg(c, t)
    alarm_clock(c, 560, 560, 1.5, t, ring=0.6)
    pop(c, 1320, 440, "ALARM: 5:00 AM", t, S("promise", "alarm", 0), "coral", 56)
    pop(c, 1320, 600, "NO SNOOZE", t, S("promise", "snooze", -0.2), "plum", 56)
    big_text(c, "THE RULES", W / 2, 150, 70, span(t, t0, t0 + 0.4), "cream")


def s_same_life(c, t, t0):
    explainer_bg(c, t, "plum")
    items = [("SAME JOB", "job", "teal"), ("SAME PHONE", "phone", "magenta"), ("SAME LATE DINNERS", "dinners", "coral")]
    for i, (lab, w, colr) in enumerate(items):
        pop(c, W / 2, 380 + i * 180, lab, t, S("promise", w, -0.2), colr, 60)
    big_text(c, "EVERYTHING ELSE STAYS", W / 2, 170, 66, span(t, t0, t0 + 0.4), "sand")


def s_papers_effort(c, t, t0):
    explainer_bg(c, t)
    names = [("Van Dongen 2003", "Sleep"), ("Jones 2019", "Nature Comms"), ("Daghlas 2021", "JAMA Psychiatry"),
             ("AASM / SRS 2015", "7+ hours"), ("Wakefit 2024", "India survey"), ("LocalCircles 2024", "India survey")]
    for i, (a, b) in enumerate(names):
        p = span(t, t0 + 0.25 * i, t0 + 0.25 * i + 0.4)
        if p > 0:
            paper(c, 360 + (i % 3) * 600, 470 + (i // 3) * 300, 0.8, a, b, ["teal", "plum", "magenta"][i % 3], rot=(i - 2.5) * 2, a=p)
    n = min(6, int((t - t0) / 0.25) + 1)
    big_text(c, f"{n} STUDIES & SURVEYS", W / 2, 160, 70, span(t, t0, t0 + 0.3), "gold")


# ---------------------------------------------------------------- DAY 1
def s_dark_delhi(c, t, t0):
    dusk_bg(c, t, 0.15)
    with Cam(c, keys(t, [(t0, 1.0), (t0 + 6, 1.08)]), W / 2, 700, t=t):
        clock_ring(c, 1500, 380, 150, 2, span(t, S("day_one", "sun", -0.2), S("day_one", "hours", 0)), t)
    label(c, "SUNRISE 6:47", 1500, 610, 44, "gold", "extrabold", span(t, S("day_one", "sun", 0), S("day_one", "sun", 0.4)))
    big_text(c, "5:00 AM · DELHI", 560, 170, 72, span(t, t0, t0 + 0.4), "cream")
    if t > S("day_one", "hours", 0):
        pop(c, 560, 300, "~2 HOURS OF DARK", t, S("day_one", "hours", 0), "plum", 48)


def s_silent(c, t, t0):
    bed_scene(c, 0, W, t, sleeper=False, made=False)
    pop(c, 1050, 420, "0 NOTIFICATIONS", t, S("day_one", "messages", -0.1), "teal", 44)
    big_text(c, "SILENT", W / 2, 150, 84, span(t, t0, t0 + 0.4), "cream")


def s_photo(c, t, t0):
    dusk_bg(c, t, 0.25)
    smartphone(c, 1300, 560, 1.0, t, "lock", rot=6)
    fl = span(t, S("day_one", "photo", 0), S("day_one", "photo", 0.15)) - span(t, S("day_one", "photo", 0.15), S("day_one", "photo", 0.5))
    if fl > 0:
        c.drawRect(skia.Rect(0, 0, W, H), paint("cream", 0.6 * fl))
    draw_kr(c, 560, 1000, 1.6, "happy", t)
    big_text(c, "C.E.O. MODE", 560, 170, 76, span(t, S("day_one", "feel", -0.1), S("day_one", "feel", 0.3)), "gold")


def s_two_hours(c, t, t0):
    explainer_bg(c, t)
    clock_ring(c, W / 2, 560, 260, 2, span(t, t0 + 0.2, t0 + 1.4), t)
    label(c, "5 TO 7 AM", W / 2, 580, 70, "cream", "extrabold", span(t, t0 + 0.4, t0 + 0.8))
    big_text(c, "+2 HOURS A DAY", W / 2, 150, 72, span(t, t0, t0 + 0.4), "gold")


# ---------------------------------------------------------------- DAY 3
def s_phone_bed(c, t, t0):
    room_bg(c, t, 0.3)
    with Cam(c, keys(t, [(t0, 1.0), (t0 + 5, 1.1)]), W / 2, 700, t=t):
        c.drawRRect(rr(300, 700, 1620, 820, 30), paint("#C9C2DE"))
        c.drawRRect(rr(340, 640, 600, 720, 34), paint("cream"))
        person_lying = skia.Path(); person_lying.moveTo(560, 720); person_lying.cubicTo(800, 640, 1200, 660, 1600, 720)
        person_lying.lineTo(1600, 820); person_lying.lineTo(560, 820); person_lying.close()
        c.drawPath(person_lying, paint("#3D5A80"))
        c.drawCircle(560, 660, 56, paint("skin")); c.drawCircle(548, 640, 54, paint("hair"))
        glow(c, 700, 600, 260, "teal", 0.55)
        smartphone(c, 720, 590, 0.35, t, "feed", rot=-20, scroll=t)
    label(c, "11:40 PM", 560, 200, 90, "gold", "extrabold", span(t, t0, t0 + 0.4))


def s_india58(c, t, t0):
    explainer_bg(c, t, "deep")
    p = span(t, S("day_three", "percent", -0.6), S("day_three", "percent", 0.8))
    india_map(c, 640, 580, 26, a=1.0)
    for k in range(int(80 * p)):
        x = 440 + rng(k, 1) * 400; y = 380 + rng(k, 2) * 420
        glow(c, x, y, 26, "teal", 0.55)
    label(c, f"{58 * ease(p):.0f}%", 1380, 560, 180, "gold", "extrabold", min(1.0, p * 3))
    label(c, "sleep after 11 PM", 1380, 660, 50, "cream", "bold", min(1.0, p * 3))
    label(c, "Wakefit Great Indian Sleep Scorecard 2024", 1380, 730, 28, "sand", "bold", 0.8 * min(1.0, p * 3))


def s_bar6(c, t, t0):
    explainer_bg(c, t)
    sleep_bar(c, W / 2, 560, 23, 5, span(t, t0 + 0.2, t0 + 1.6), title="BED 11 PM · ALARM 5 AM")
    if t > S("day_three", "less", -0.2):
        pop(c, W / 2, 860, "MAYBE LESS", t, S("day_three", "less", -0.2), "coral", 48)


def s_moved(c, t, t0):
    def left(c, t):
        explainer_bg(c, t)
        alarm_clock(c, 480, 600, 1.2, t, hour=5)
        label(c, "ALARM: MOVED", 480, 250, 56, "teal", "extrabold")
    def right(c, t):
        explainer_bg(c, t, "plum")
        alarm_clock(c, 1440, 600, 1.2, t, hour=11, body="plum")
        label(c, "BEDTIME: STUCK", 1440, 250, 56, "coral", "extrabold")
    split(left, right, wipe_at=S("day_three", "bedtime", -0.3))(c, t, t0)


# ---------------------------------------------------------------- DAY 7
def s_fine(c, t, t0):
    explainer_bg(c, t, "plum")
    draw_kr(c, 700, 1000, 1.6, "happy", t)
    day_tile(c, 1350, 520, 1.6, span(t, t0, t0 + 0.4), "7/30")
    big_text(c, "I FEEL... FINE", W / 2, 160, 76, span(t, S("day_seven", "fine", -0.2), S("day_seven", "fine", 0.2)), "cream")


def s_yawn(c, t, t0):
    explainer_bg(c, t, "deep")
    draw_kr(c, 600, 1000, 1.6, "worried", t)
    for i, w in enumerate(["second", "coffee"]):
        p = span(t, S("day_seven", "coffee", -0.6 + 0.3 * i), S("day_seven", "coffee", -0.2 + 0.3 * i))
        if p > 0:
            x = 1200 + i * 230
            c.drawRRect(rr(x - 70, 560, x + 70, 760, 18), paint("cream", p))
            c.drawPath(_mug_handle(x + 70), paint("cream", p, stroke=14))
            c.drawRect(skia.Rect(x - 60, 580, x + 60, 610), paint("#5E3B26", p))
            for k in range(3):
                yy = 520 - ((t * 60 + k * 30) % 90)
                c.drawLine(x - 30 + k * 30, yy, x - 30 + k * 30, yy - 30, paint("cream", 0.4 * p, stroke=5))
    label(c, "4 PM", 1320, 300, 90, "gold", "extrabold", span(t, t0, t0 + 0.4))


def _mug_handle(x):
    p = skia.Path(); p.moveTo(x, 600); p.cubicTo(x + 70, 600, x + 70, 720, x, 720); return p


def s_trap(c, t, t0):
    explainer_bg(c, t, "plum")
    sticky(c, W / 2, 560, 1.6, "I FEEL\nFINE", rot=-5, a=span(t, t0, t0 + 0.3))
    stamp(c, W / 2 + 40, 860, "THE TRAP", span(t, S("day_seven", "trap", 0), S("day_seven", "trap", 0.3)), "coral", -14)
    if t > S("day_seven", "fourteen", -0.3):
        pop(c, W / 2, 940, "BACK TO THIS ON DAY 14", t, S("day_seven", "fourteen", -0.3), "teal", 44)


# ---------------------------------------------------------------- DAY 10
def s_reel(c, t, t0):
    explainer_bg(c, t)
    smartphone(c, W / 2, 580, 1.25, t, "feed", scroll=t * 0.6)
    c.drawRRect(rr(W / 2 - 200, 400, W / 2 + 200, 520, 20), paint("space", 0.85))
    label(c, "5 AM =", W / 2, 448, 50, "gold", "extrabold")
    label(c, "SUCCESS", W / 2, 504, 50, "gold", "extrabold")
    big_text(c, "EVERY SUCCESSFUL PERSON...?", W / 2, 140, 60, span(t, t0, t0 + 0.4), "cream")


def s_movies(c, t, t0):
    dusk_bg(c, t, 0.3)
    jogger(c, 520 + (t - t0) * 60, 1000, 1.5, t)
    desk_lamp_student(c, 1400, 1000, 1.4, t)
    big_text(c, "IN THE MOVIES", W / 2, 150, 72, span(t, t0, t0 + 0.4), "gold")


def s_dna(c, t, t0):
    explainer_bg(c, t, "deep")
    p = span(t, S("day_ten", "found", -0.2), S("day_ten", "found", 1.6))
    dna(c, W / 2, 560, 1500, t, lit=int(24 * p))
    label(c, "~7 LAKH PEOPLE", W / 2, 230, 66, "cream", "extrabold", span(t, S("day_ten", "lakh", -0.4), S("day_ten", "lakh", 0)))
    label(c, f"{351 * ease(p):.0f} GENE SPOTS", W / 2, 880, 80, "gold", "extrabold", min(1.0, p * 3))
    label(c, "Jones et al., Nature Communications 2019", W / 2, 950, 30, "sand", "bold", 0.8)


def s_owl_lark(c, t, t0):
    explainer_bg(c, t, "plum")
    lark(c, 560, 520, 1.6, t, span(t, S("day_ten", "morning", -0.3), S("day_ten", "morning", 0.2)))
    owl(c, 1360, 540, 1.6, span(t, S("day_ten", "owl", -0.3), S("day_ten", "owl", 0.2)))
    label(c, "MORNING PERSON", 560, 820, 50, "gold", "extrabold", span(t, S("day_ten", "morning", -0.3), S("day_ten", "morning", 0.2)))
    label(c, "NIGHT OWL", 1360, 820, 50, "teal", "extrabold", span(t, S("day_ten", "owl", -0.3), S("day_ten", "owl", 0.2)))


# ---------------------------------------------------------------- DAY 14 (the big one)
def s_lab(c, t, t0):
    with Cam(c, keys(t, [(t0, 1.0), (t0 + 6, 1.1)]), W / 2, 560, t=t):
        lab_beds(c, t)
    p = span(t, S("the_big_one", "weeks", -0.6), S("the_big_one", "weeks", 0.6))
    for k in range(14):
        x = 520 + k * 68
        c.drawRRect(rr(x - 26, 150, x + 26, 210, 6), paint("cream", 0.85))
        if k < int(14 * p):
            c.drawLine(x - 18, 160, x + 18, 200, paint("coral", stroke=6)); c.drawLine(x + 18, 160, x - 18, 200, paint("coral", stroke=6))
    big_text(c, "6 HOURS IN BED · 14 DAYS", W / 2, 290, 60, span(t, S("the_big_one", "six", -0.2), S("the_big_one", "six", 0.3)), "gold")
    label(c, "University of Pennsylvania · 2003", W / 2, 1010, 34, "sand", "bold", 0.85)


def s_scale(c, t, t0):
    night(c, t)
    tilt = keys(t, [(t0, -1.0), (t0 + 1.6, 0.0)], ease_out)
    balance(c, W / 2, 330, tilt, "6 HOURS\n× 14 DAYS", "2 NIGHTS\nAWAKE")
    big_text(c, "UP TO", W / 2, 160, 60, span(t, t0 + 1.2, t0 + 1.6), "coral")


def s_reaction(c, t, t0):
    night(c, t)
    reaction_screen(c, 620, 560, t, t0, slow=1.0)


def s_lines(c, t, t0):
    night(c, t)
    x0, x1, y0 = 360, 1560, 820
    c.drawLine(x0, y0, x1, y0, paint("sand", 0.6, stroke=4)); c.drawLine(x0, y0, x0, 300, paint("sand", 0.6, stroke=4))
    p = span(t, t0 + 0.2, t0 + 2.4)
    xe = x0 + (x1 - x0) * p
    s1 = skia.Path(); s1.moveTo(x0, 600)
    s2 = skia.Path(); s2.moveTo(x0, 360)
    for k in range(1, 41):
        x = x0 + (x1 - x0) * k / 40
        if x > xe:
            break
        s1.lineTo(x, 600 - 80 * min(1, k / 6) + math.sin(k) * 4)
        s2.lineTo(x, 360 + 380 * (k / 40) ** 0.9)
    c.drawPath(s1, paint("teal", stroke=10)); c.drawPath(s2, paint("coral", stroke=10))
    label(c, "how sleepy they felt", 1500, 480, 38, "teal", "bold", min(1.0, p * 2))
    label(c, "how their brain performed", 1380, 780, 38, "coral", "bold", min(1.0, p * 2))
    big_text(c, "THEY DIDN'T FEEL IT", W / 2, 170, 72, span(t, S("the_big_one", "feel", -0.3), S("the_big_one", "feel", 0.1)), "gold")


def s_note_fall(c, t, t0):
    explainer_bg(c, t, "plum")
    p = span(t, t0 + 1.2, t0 + 3.6)
    draw_kr(c, 520, 1000, 1.5, "worried", t)
    sticky(c, 1250 + 60 * p, 520 + 380 * ease(p), 1.3, "I FEEL\nFINE", rot=-5 + 30 * p, a=1 - 0.5 * p)
    big_text(c, "DAY 7 WAS THIS", W / 2, 160, 72, span(t, S("the_big_one", "this", -0.2), S("the_big_one", "this", 0.2)), "coral")


# ---------------------------------------------------------------- DAY 21 (the fix)
def s_reveal(c, t, t0):
    zm = keys(t, [(t0 + 1.2, 1.0), (t0 + 2.6, 1.6)])
    with Cam(c, zm, 1270, 640, t=t):
        bed_scene(c, 0, 960, t, bedtime=11)
        bed_scene(c, 960, 960, t + 0.11, bedtime=10)
        c.drawLine(960, 0, 960, H, paint("cream", 0.9, stroke=6))
        mp = span(t, S("day_twenty_one", "dial", -0.2), S("day_twenty_one", "dial", 0.5))
        for cx in (810, 960 + 810):
            arc = skia.Path(); arc.addArc(skia.Rect(cx - 20 - 32, 679 - 32, cx - 20 + 32, 679 + 32), -90, 360 * mp)
            c.drawPath(arc, paint("coral", stroke=8))
    _title_strip(c, t, t0, "FOUND IT: THE BEDTIME")
    bp = span(t, S("day_twenty_one", "eleven", -0.1), S("day_twenty_one", "eleven", 0.3))
    rp = span(t, S("day_twenty_one", "ten", -0.1), S("day_twenty_one", "ten", 0.3))
    for (x, txt, colr, p) in ((420, "BED 11 PM", "coral", bp), (1500, "BED 10 PM", "teal", rp)):
        if p > 0:
            c.drawRRect(rr(x - 230, 860, x + 230, 990, 30), paint("space", 0.85 * p))
            c.drawRRect(rr(x - 230, 860, x + 230, 990, 30), dashed(colr, p, 5))
            label(c, txt, x, 950, 80, colr, "extrabold", p)


def s_lights_off(c, t, t0):
    off = span(t, S("day_twenty_one", "lights", 0), S("day_twenty_one", "lights", 0.4))
    room_bg(c, t, 1 - 0.8 * off)
    p = span(t, t0 + 0.2, t0 + 1.2)
    smartphone(c, 600 - 400 * ease(p), 600, 0.6, t, "feed", rot=-10, a=1 - 0.7 * ease(p))
    c.drawRRect(rr(80, 700, 400, 860, 30), paint(WOOD))
    moon_clock(c, 1300, 520, 1.1, t, off)
    if off <= 0:
        big_text(c, "PHONE OUT", W / 2, 160, 72, span(t, t0, t0 + 0.4), "cream")


def s_bar7(c, t, t0):
    explainer_bg(c, t)
    sleep_bar(c, W / 2, 560, 22, 5, span(t, t0 + 0.2, t0 + 1.6), color="gold", title="BED 10 PM · ALARM 5 AM")
    if t > t0 + 1.6:
        pop(c, W / 2, 860, "7 HOURS · THE MINIMUM", t, t0 + 1.6, "teal", 48)


def s_beat_alarm(c, t, t0):
    bed_scene(c, 0, W, t, made=True, ring=span(t, t0 + 1.0, t0 + 1.1))
    draw_kr(c, 520, 1000, 1.6, "happy", t)
    big_text(c, "AWAKE BEFORE 5:00", W / 2, 150, 70, span(t, t0, t0 + 0.4), "gold")


# ---------------------------------------------------------------- DAY 30 (twist)
def s_magic(c, t, t0):
    night(c, t)
    sw = span(t, S("payoff", "ten", -0.3), S("payoff", "ten", 0.6))
    alarm_clock(c, W / 2 - 520 * ease(sw), 560, 1.4, t, a=1 - 0.6 * sw)
    moon_clock(c, W / 2 + 300 * (1 - ease(sw)), 520, 1.3, t, sw)
    if sw > 0.5:
        xmark(c, W / 2 - 520, 560, 1.8, span(t, S("payoff", "ten", 0.3), S("payoff", "ten", 0.7)))
    big_text(c, "THE MAGIC WAS NEVER 5 AM", W / 2, 150, 66, span(t, t0, t0 + 0.4), "gold")


def s_depression(c, t, t0):
    explainer_bg(c, t, "plum")
    dna(c, 640, 560, 800, t, lit=24, total=14)
    p = span(t, S("payoff", "percent", -0.8), S("payoff", "percent", 0.6))
    x, y0 = 1420, 300
    c.drawRRect(rr(x - 110, y0, x + 110, y0 + 520, 24), paint("#0E0A22"))
    h = 520 * (1 - 0.23 * ease(p))
    c.drawRRect(rr(x - 90, y0 + 520 - h + 20, x + 90, y0 + 500, 18), paint("teal"))
    label(c, f"-{23 * ease(p):.0f}%", x, y0 - 40, 96, "gold", "extrabold", min(1.0, p * 3))
    label(c, "depression risk", x, y0 + 590, 40, "cream", "bold")
    label(c, "sleep set 1 hour earlier (by genes) · Daghlas et al., JAMA Psychiatry 2021", W / 2, 1010, 30, "sand", "bold", 0.8)


def s_shift(c, t, t0):
    explainer_bg(c, t)
    p = span(t, t0 + 0.3, t0 + 1.6)
    sleep_bar(c, W / 2, 420, 23 - ease(p), 6 - ease(p), 1.0, need=7, s=0.9, color="teal", title="NOT MORE SLEEP...")
    label(c, "...JUST EARLIER", W / 2, 820, 72, "gold", "extrabold", span(t, S("payoff", "earlier", -0.2), S("payoff", "earlier", 0.3)))


def s_two_you(c, t, t0):
    def left(c, t):
        explainer_bg(c, t, "deep"); draw_kr(c, 480, 1000, 1.6, "worried", t); battery(c, 760, 460, 0.6, 0.2, t)
        label(c, "5 AM ON 6 HOURS", 480, 200, 52, "coral", "extrabold")
    def right(c, t):
        dusk_bg(c, t, 1.2); draw_kr(c, 1440, 1000, 1.6, "happy", t); battery(c, 1720, 460, 0.6, 1.0, t)
        label(c, "5 AM ON 7 HOURS", 1440, 200, 52, "gold", "extrabold")
    split(left, right, wipe_at=S("payoff", "seven", -0.3))(c, t, t0)


# ---------------------------------------------------------------- DAY 31 (bonus)
def s_sunrise(c, t, t0):
    rooftop(c, t, 1.6)
    sy = 640 - 80 * ease(span(t, t0, t0 + 4))
    glow(c, 1250, sy, 460, "gold", 0.55)
    c.drawCircle(1250, sy, 90, paint("gold"))
    person(c, 760, 1000, 1.6, "teal", look_up=1.0)
    label(c, "6:47 AM", 380, 200, 80, "gold", "extrabold", span(t, t0, t0 + 0.4))


def s_callback(c, t, t0):
    bed_scene(c, 0, 960, t, bedtime=11, made=True, ring=1.0, bright=0.6)
    bed_scene(c, 960, 960, t + 0.11, bedtime=10, made=True, ring=1.0, bright=0.6)
    c.drawLine(960, 0, 960, H, paint("cream", 0.9, stroke=6))
    _title_strip(c, t, t0, "ALREADY AWAKE")


def s_tease(c, t, t0):
    dusk_bg(c, t, 0.9)
    p = span(t, t0 + 0.2, t0 + 1.2)
    for k in range(9):
        x = 160 + k * 200
        yy = -200 + (900 - 120 * (k % 2)) * ease(span(t, t0 + 0.1 * k, t0 + 0.1 * k + 0.8))
        c.drawRRect(rr(x - 70, yy - 40, x + 70, yy + 40, 10), paint("#3BB273"))
        c.drawRRect(rr(x - 70, yy - 10, x + 70, yy + 10, 4), paint("amber"))
        label(c, "₹1 Cr", x, yy + 10, 26, "ink", "extrabold")
    big_text(c, "NEXT: ₹1 CRORE FOR EVERY INDIAN?", W / 2, 180, 64, p, "gold")


# ---------------------------------------------------------------- the list: (start, shot, transition)
def SHOTS():
    return [
        (0.0, s_split_open, "cut"),
        (S("hook", "fourteen", -0.4), s_hook_battery, "whip"),
        (S("hook", "difference", -0.4), s_split_search, "fade"),
        (E("hook"), logo_sting(), "flash"),
        (E("hook") + 2.0, s_rules, "iris"),
        (S("promise", "everything", -0.3), s_same_life, "cut"),
        (S("promise", "went", -0.3), s_papers_effort, "fade"),

        (B("day_one") - 0.6, card("DAY 1", "5 AM"), "iris"),
        (S("day_one", "dark", -0.3), s_dark_delhi, "fade"),
        (S("day_one", "house", -0.3), s_silent, "fade"),
        (S("day_one", "feel", -0.3), kr_react("happy", "C.E.O. MODE", line_at=S("day_one", "feel", 0.2)), "whip"),
        (S("day_one", "photo", -1.2), s_photo, "cut"),
        (S("day_one", "used", -0.3), s_two_hours, "fade"),
        (S("day_one", "month", -0.3), counter(0, 60, "{:.0f} HOURS", until=S("day_one", "sixty", 0.3), label="FREE · IN ONE MONTH",
                                              label_at=S("day_one", "free", 0), bg=month_grid), "zoom"),

        (B("day_three") - 0.6, card("DAY 3", "11:40 PM"), "iris"),
        (S("day_three", "bed", -0.4), s_phone_bed, "fade"),
        (S("day_three", "alone", -0.3), s_india58, "whip"),
        (S("day_three", "night", -0.3), s_bar6, "fade"),
        (S("day_three", "alarm", -0.3), s_moved, "cut"),

        (B("day_seven") - 0.6, card("DAY 7", "I feel fine"), "iris"),
        (B("day_seven") + 0.4, s_fine, "fade"),
        (S("day_seven", "yawn", -0.3), s_yawn, "whip"),
        (S("day_seven", "trap", -0.6), s_trap, "cut"),
        (S("day_seven", "quick", -0.2), comment_prompt("What time does your alarm ring right now?", bg=alarm_row), "fade"),

        (S("day_seven", "already", -0.4), kr_react("curious", "WHO'S UP AT 5?", line_at=S("day_seven", "already", 0)), "cut"),

        (B("day_ten") - 0.6, card("DAY 10", "The myth"), "iris"),
        (S("day_ten", "reel", -0.4), s_reel, "fade"),
        (S("day_ten", "movies", -0.3), layer(s_movies, stamp_at("MYTH", S("day_ten", "science", -0.4))), "whip"),
        (S("day_ten", "science", -0.5), statement("HERE'S WHAT THE SCIENCE SAYS", bg=lambda c, t: explainer_bg(c, t, "deep"), color="gold"), "flash"),
        (S("day_ten", "nineteen", -0.6), s_dna, "fade"),
        (S("day_ten", "found", -0.3), zoom(s_dna, 1.0, 1.15, dur=4), "cut"),
        (S("day_ten", "morning", -0.8), s_owl_lark, "cut"),
        (S("day_ten", "torture", -0.8), kr_react("thinking", "NOT LAZINESS. GENES.", line_at=S("day_ten", "laziness", 0)), "fade"),

        (B("the_big_one") - 0.6, card("DAY 14", "The brain"), "iris"),
        (S("the_big_one", "thousand", -0.6), s_lab, "fade"),
        (S("the_big_one", "end", -0.4), s_scale, "fade"),
        (S("the_big_one", "skipped", -0.3), statement("= UP TO 2 NIGHTS WITHOUT SLEEP", bg=two_nights, color="coral"), "flash"),
        (S("the_big_one", "slower", -0.3), s_reaction, "cut"),
        (S("the_big_one", "scariest", -0.3), s_lines, "fade"),
        (S("the_big_one", "remember", -0.3), s_note_fall, "fade"),

        (B("day_twenty_one") - 0.6, card("DAY 21", "The fix"), "iris"),
        (S("day_twenty_one", "spot", -0.4), s_reveal, "fade"),
        (S("day_twenty_one", "change", -0.3), statement("CHANGE ONE NUMBER", sub="Not the alarm. The bedtime.", bg=lambda c, t: (explainer_bg(c, t, "deep"), moon_clock(c, W / 2, 830, 0.7, t)), color="gold"), "fade"),
        (S("day_twenty_one", "phone", -0.3), s_lights_off, "whip"),
        (S("day_twenty_one", "seven", -0.8), s_bar7, "fade"),
        (S("day_twenty_one", "stare", -0.4), kr_react("worried", "STARING AT THE FAN", line_at=S("day_twenty_one", "ceiling", 0)), "cut"),
        (S("day_twenty_one", "easier", -0.3), s_beat_alarm, "fade"),

        (B("payoff") - 0.6, card("DAY 30", "The twist"), "iris"),
        (S("payoff", "magic", -0.3), s_magic, "flash"),
        (S("payoff", "genetic", -0.6), s_depression, "fade"),
        (S("payoff", "whose", -0.3), zoom(s_depression, 1.0, 1.12, dur=4), "cut"),
        (S("payoff", "more", -0.3), s_shift, "fade"),
        (S("payoff", "drains", -0.8), s_two_you, "cut"),

        (S("payoff", "mornings", -0.3), zoom(s_two_you, 1.0, 1.1, dur=4), "cut"),
        (B("bonus") - 0.6, card("DAY 31", "Sunrise"), "iris"),
        (S("bonus", "roof", -0.6), s_sunrise, "fade"),
        (S("bonus", "five", -0.3), s_callback, "fade"),
        (S("bonus", "would", -0.6), comment_prompt("10 PM to 5 AM for 30 days. Would you?", bg=lambda c, t: rooftop(c, t, 1.4)), "fade"),
        (S("bonus", "next", -0.3), s_tease, "flash"),
        (S("bonus", "story", -0.3), statement("...FOR THE NEXT WHAT IF", bg=lambda c, t: dusk_bg(c, t, 0.9), color="gold"), "fade"),
        (E(LAST_BEAT) + 0.3, end_screen(), "fade"),
    ]


LAST_BEAT = BEAT_KEYS[-1]
