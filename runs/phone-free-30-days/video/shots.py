"""Shot list: What If You Didn't Use Your Phone for 30 Days? (atlas style).
Threads: (1) the wooden drawer opens the video and opens again on Day 31; (2) a dashed outline = the missing phone;
(3) the keypad phone (calls + SMS) appears on Day 2 and becomes the twist on Day 30."""
import math
import skia
from krwi.lib import *  # noqa: F401,F403
from art import *  # noqa: F401,F403


def S(beat, word, off=0.0, n=1):
    return at(beat, word, off, n)


# ---------------------------------------------------------------- HOOK
def s_hook_drawer(c, t, t0):
    th = T("hook", "hundred")
    room_bg(c, t)
    with Cam(c, keys(t, [(t0, 1.12), (t0 + 5, 1.0)]), W / 2, 640, t=t):
        # phone drops into the open drawer, the drawer slams shut, then six DAY tiles fly out of it
        op = keys(t, [(t0, 1.0), (t0 + 0.9, 1.0), (t0 + 1.4, 0.0)])
        drawer(c, W / 2, 760, 1.0, t, open_p=op, phone=True, screen="feed")
        if t < t0 + 1.0:
            py = keys(t, [(t0, 260), (t0 + 0.9, 560)], ease_out)
            smartphone(c, W / 2, py, 0.5, t, "feed", rot=-8, scroll=t)
    for i in range(6):
        p = span(t, th + 0.15 * i, th + 0.15 * i + 0.7)
        if p > 0:
            ang = math.radians(200 + i * 28)
            r = 520 * ease_out(p)
            day_tile(c, W / 2 + math.cos(ang) * r * 1.4, 620 + math.sin(ang) * r * 0.75, 0.9, p, f"DAY {i + 1}")
    big_text(c, "30 DAYS · NO PHONE", W / 2, 130, 76, span(t, t0, t0 + 0.3), "cream")
    if t > th:
        pop(c, W / 2, 990, "+150 HOURS = 6 FULL DAYS", t, th + 0.4, "coral", 52)


def s_hook_locked(c, t, t0):
    explainer_bg(c, t)
    for i, k in enumerate(["WALLET", "TICKETS", "MAPS", "BANK"]):
        icon_tile(c, 420 + i * 360, 560, 1.1, k, span(t, t0 + 0.1 * i, t0 + 0.1 * i + 0.4))
    lk = span(t, S("hook", "locked", -0.1), S("hook", "locked", 0.35))
    for i in range(4):
        padlock(c, 420 + i * 360, 520, 0.8, lk)
    big_text(c, "DAY 2: LOCKED OUT", W / 2, 180, 72, span(t, S("hook", "locked", -0.1), S("hook", "locked", 0.3)), "coral")


def s_hook_head(c, t, t0):
    explainer_bg(c, t, "plum")
    head_profile(c, W / 2 - 60, 600, 1.35, t, light=span(t, S("hook", "inside", -0.2), S("hook", "inside", 0.6)))
    big_text(c, "INSIDE YOUR HEAD", W / 2, 160, 64, span(t, S("hook", "inside", 0.0), S("hook", "inside", 0.4)), "gold")


# ---------------------------------------------------------------- PROMISE
def s_rules_drawer(c, t, t0):
    room_bg(c, t)
    tl = T("promise", "locked")
    drawer(c, W / 2, 700, 1.05, t, open_p=keys(t, [(t0, 0.6), (tl - 0.3, 0.0)]), screen="dark", lock=span(t, tl, tl + 0.4))
    day_tile(c, 1560, 380, 1.3, span(t, S("promise", "thirty", -0.1), S("promise", "thirty", 0.4)), "30")
    big_text(c, "THE RULES", W / 2, 150, 70, span(t, t0, t0 + 0.4), "cream")


def s_rules(c, t, t0):
    explainer_bg(c, t)
    phone_outline(c, 480, 560, 1.15, span(t, t0, t0 + 0.6))
    xmark(c, 480, 560, 2.2, span(t, S("promise", "internet", -0.2), S("promise", "internet", 0.3)))
    for i, (w, word) in enumerate([("NO SCROLLING", "scrolling"), ("NO APPS", "apps"), ("NO INTERNET", "internet")]):
        pop(c, 1240, 380 + i * 170, w, t, S("promise", word, -0.1), ["coral", "plum", "magenta"][i], 56)


# ---------------------------------------------------------------- HOUR 1
def s_pocket_pat(c, t, t0):
    explainer_bg(c, t, "deep")
    jeans_pocket(c, W / 2, 640, 0.95, t)
    ta = T("hour_one", "again")
    for i, tt in enumerate([t0 + 0.2, ta]):
        p = span(t, tt, tt + 0.5) - span(t, tt + 0.9, tt + 1.4)
        if p > 0:
            hand(c, W / 2 + 40, 640 + 380 * (1 - ease(p)), 1.1, rot=-8)
    if t > ta:
        pop(c, 1500, 260, "AGAIN.", t, ta, "coral", 60)
    big_text(c, "NOTHING THERE", W / 2, 110, 60, span(t, S("hour_one", "nothing", 0), S("hour_one", "nothing", 0.4)), "sand")


def s_queue(c, t, t0):
    dusk_bg(c, t, 0.8)
    for i, x in enumerate([260, 520, 1400, 1660]):
        person(c, x, 1010, 1.15, ["#3D5A80", "#8A2A5C", "#7A4E2D", "#4A3F8C"][i], phone=True, female=i % 2 == 0)
    person(c, 960, 1010, 1.3, "teal")
    # your thumb swiping thin air (close-up inset)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(1200, 120, 1760, 560), 30, 30), paint("deep", 0.9))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(1200, 120, 1760, 560), 30, 30), paint("gold", 0.6, stroke=5))
    sw = (t * 1.6) % 1.0
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect(1200, 120, 1760, 560), 30, 30))
    phone_outline(c, 1480, 330, 0.55, 0.7)
    hand(c, 1480 + 60 * math.sin(t * 9), 600 - 120 * ease(sw), 0.75, rot=-10, point=True)
    c.restore()
    big_text(c, "SCROLLING... AIR", W / 2, 120, 60, span(t, S("hour_one", "air", -0.3), S("hour_one", "air", 0.2)), "gold")


def s_buzz(c, t, t0):
    explainer_bg(c, t, "deep")
    tb = T("hour_one", "buzzes")
    jeans_pocket(c, W / 2 - 300, 620, 0.9, t, buzz=span(t, tb - 0.1, tb + 0.2) - span(t, tb + 1.6, tb + 2.2))
    drawer(c, 1460, 760, 0.55, t, open_p=0.0, lock=1.0)
    label(c, "your phone: at home", 1460, 520, 40, "sand", "bold", span(t, S("hour_one", "home", -0.2), S("hour_one", "home", 0.3)))
    big_text(c, "BZZZ?", W / 2 - 300, 160, 90, span(t, tb, tb + 0.3), "gold")


def s_phantom_count(c, t, t0):
    explainer_bg(c, t)
    p = span(t, t0 + 0.2, t0 + 1.8)
    people_icons(c, W / 2, 760, 10, 9, 1.0, gap=150, s=1.0, colr="gold", dim_a=0.25)
    counter_text(c, 0, 89, p, lambda v: f"{v:.0f}%", W / 2, 460, 150, "gold")
    big_text(c, "PHANTOM VIBRATION", W / 2, 160, 66, span(t, t0, t0 + 0.4), "cream")
    label(c, "of students felt it (Drouin et al., 2012)", W / 2, 960, 40, "sand", "bold", span(t, t0 + 1.2, t0 + 1.7))


def s_fake_notifs(c, t, t0):
    explainer_bg(c, t, "plum")
    head_profile(c, 760, 620, 1.2, t, pings=span(t, t0 + 0.2, t0 + 2.6))
    big_text(c, "IT'S MAKING UP NOTIFICATIONS", W / 2, 140, 60, span(t, S("hour_one", "making", -0.2), S("hour_one", "making", 0.3)), "gold")


# ---------------------------------------------------------------- DAY 2
def s_pay(c, t, t0):
    explainer_bg(c, t)
    icon_tile(c, 620, 560, 1.4, "WALLET", span(t, t0, t0 + 0.4), cross=span(t, S("day_two", "drawer", -0.2), S("day_two", "drawer", 0.3)))
    drawer(c, 1380, 760, 0.6, t, open_p=0.0, lock=1.0)
    big_text(c, "UPI APP: IN THE DRAWER", W / 2, 160, 64, span(t, S("day_two", "drawer", -0.1), S("day_two", "drawer", 0.3)), "coral")
    big_text(c, "NOBODY WARNS YOU", W / 2, 160, 64, span(t, t0, t0 + 0.3) - span(t, S("day_two", "pay", -0.4), S("day_two", "pay", -0.1)), "sand")


def s_tickets(c, t, t0):
    explainer_bg(c, t, "deep")
    c.save(); c.translate(W / 2, 560); c.scale(1.22, 1.22); c.translate(-W / 2, -560)
    ticket_row(c, W / 2, 560, t, span(t, S("day_two", "nine", -0.3), S("day_two", "nine", 1.2)))
    c.restore()
    big_text(c, "~9 IN 10 TRAIN TICKETS", W / 2, 230, 74, span(t, S("day_two", "nine", 0), S("day_two", "nine", 0.4)), "gold")
    label(c, "booked online (Indian Railways, 2025-26)", W / 2, 860, 46, "cream", "bold", span(t, S("day_two", "online", 0), S("day_two", "online", 0.4)))


def s_lost(c, t, t0):
    explainer_bg(c, t)
    city_map(c, W / 2, 600, 1300, 760, t, lost=span(t, t0 + 0.6, t0 + 1.4))
    big_text(c, "NO MAPS", W / 2, 120, 72, span(t, S("day_two", "maps", -0.1), S("day_two", "maps", 0.3)), "coral")


def s_otp(c, t, t0):
    room_bg(c, t, 0.6)
    tb = T("day_two", "bank")
    drawer(c, 700, 740, 1.0, t, open_p=0.0, lock=1.0)
    glow(c, 700, 600, 260, "teal", 0.35 * (0.5 + 0.5 * math.sin(t * 8)) * span(t, tb, tb + 0.4))
    bubble(c, 700, 420, 1.3, span(t, tb + 0.2, tb + 0.6), "teal")
    label(c, "OTP: 4 8 2 1", 700, 360, 40, "gold", "extrabold", span(t, tb + 0.2, tb + 0.6))
    kr_x = 1450
    draw_kr(c, kr_x, 960, 1.15, "worried", t)
    big_text(c, "...TO A PHONE YOU CAN'T TOUCH", W / 2, 130, 58, span(t, S("day_two", "touch", -0.6), S("day_two", "touch", -0.2)), "coral")


def s_shop(c, t, t0):
    c.drawRect(skia.Rect(0, 0, W, H), paint("#1E1438"))
    glow(c, W / 2, 380, 520, "gold", 0.35)
    for k in range(5):  # shelves of boxes
        for j in range(8):
            c.drawRect(skia.Rect(120 + j * 220, 120 + k * 120, 300 + j * 220, 210 + k * 120), paint(["#2C2350", "#352A5E"][(j + k) % 2]))
    c.drawRect(skia.Rect(0, 760, W, H), paint("#5E3B26"))
    c.drawRect(skia.Rect(0, 760, W, 790), paint("#B07A52"))
    keypad_phone(c, W / 2, 420, 1.2 * back_out(span(t, t0 + 0.3, t0 + 0.8)), t, "CALLS  SMS", lit=span(t, S("day_two", "keypad", -0.3), S("day_two", "keypad", 0.2)))
    big_text(c, "THE ONE PHONE THAT CAN'T SCROLL", W / 2, 950, 58, span(t, S("day_two", "scroll", -0.2), S("day_two", "scroll", 0.3)), "gold")


def s_four(c, t, t0):
    explainer_bg(c, t)
    p = span(t, S("day_two", "wallet", -0.3), S("day_two", "wallet", 0.6))
    phone_outline(c, W / 2, 560, 1.1, 1 - p)
    for i, (k, word) in enumerate([("WALLET", "wallet"), ("TICKETS", "ticket"), ("MAPS", "map"), ("BANK", "bank")]):
        tw = S("day_two", word, -0.1)
        q = ease_out(span(t, tw, tw + 0.5))
        x = W / 2 + (-540 + i * 360) * q
        icon_tile(c, x, 560, 1.1, k, span(t, tw, tw + 0.4))
    big_text(c, "NEVER JUST A PHONE", W / 2, 150, 66, span(t, S("day_two", "never", 0), S("day_two", "never", 0.4)), "cream")


def s_2005(c, t, t0):
    dusk_bg(c, t, 0.7)
    c.drawRect(skia.Rect(0, 0, W, H), paint("#704214", 0.28))
    person(c, 760, 1010, 1.35, "teal")
    person(c, 1160, 1010, 1.35, "#7A4E2D", female=True)
    for k in range(5):
        c.drawCircle(600 + k * 26, 640, 22, paint("gold")); c.drawCircle(600 + k * 26, 640, 22, paint("#B8862E", stroke=4))
    big_text(c, "LIKE IT'S 2005", W / 2, 160, 84, span(t, S("day_two", "like", -0.1), S("day_two", "like", 0.3)), "gold")


# ---------------------------------------------------------------- DAY 7
def s_clock(c, t, t0):
    explainer_bg(c, t)
    clock_ring(c, 700, 580, 300, 5, span(t, t0 + 0.2, t0 + 1.6), t)
    big_text(c, "5 HRS", 700, 600, 96, span(t, t0 + 1.0, t0 + 1.4), "coral")
    label(c, "a day, on a phone", 1350, 520, 54, "cream", "bold", span(t, t0 + 0.4, t0 + 0.9))
    label(c, "average Indian (EY, 2025)", 1350, 600, 38, "sand", "bold", span(t, t0 + 0.8, t0 + 1.2))
    label(c, "≈ 1/3 of your waking hours", 1350, 680, 44, "coral", "bold", span(t, t0 + 1.6, t0 + 2.0))
    big_text(c, "EVERY. SINGLE. DAY.", 1350, 760, 56, span(t, S("day_seven", "single", -0.3), S("day_seven", "single", 0.2)), "gold")


def s_metro(c, t, t0):
    with Cam(c, keys(t, [(t0, 1.0), (t0 + 6, 1.1)]), W / 2, 600, t=t):
        metro(c, t)
    for i, w in enumerate(["metro", "lift", "bathroom"]):
        pop(c, 380 + i * 580, 120, ["LONGER", "LONGER", "EVEN LONGER"][i], t, S("day_seven", w, 0.2), "plum", 44)


def s_shampoo(c, t, t0):
    room_bg(c, t)
    draw_kr(c, 820, 980, 1.6, "thinking", t, look=(1, 0))
    shampoo(c, 1180, 560, 1.1, rot=-12 + 4 * math.sin(t * 2))
    pop(c, 1180, 200, "INGREDIENTS... ALL OF THEM", t, t0 + 0.3, "teal", 40)


def s_look_up(c, t, t0):
    dusk_bg(c, t, 1.3)
    person(c, 760, 1010, 1.4, "teal", phone=False)
    person(c, 1080, 1010, 1.4, "#8A2A5C", female=True)
    glow(c, 920, 600, 400, "amber", 0.18)
    big_text(c, "YOU LOOK UP", W / 2, 160, 70, span(t, S("day_seven", "look", -0.1), S("day_seven", "look", 0.3)), "gold")
    label(c, "a whole conversation. no checking.", W / 2, 250, 42, "cream", "bold", span(t, S("day_seven", "conversation", -0.2), S("day_seven", "conversation", 0.3)))


# ---------------------------------------------------------------- DAY 10
def s_lake(c, t, t0):
    p = span(t, t0 + 0.3, S("day_ten", "perfect", 0.2))
    lake_scene(c, t, p)
    label(c, "IN MOVIES", 240, 110, 46, "sand", "extrabold")


def s_study(c, t, t0):
    explainer_bg(c, t)
    paper(c, W / 2, 560, 1.25, "PNAS Nexus · 2025", "467 people, 2 weeks", "teal", -2, span(t, t0, t0 + 0.5))
    label(c, "IN REAL LIFE", W / 2, 140, 54, "sand", "extrabold", span(t, t0, t0 + 0.3))


def s_quarter(c, t, t0):
    explainer_bg(c, t)
    people_icons(c, W / 2, 640, 4, 1, span(t, t0 + 0.3, t0 + 1.4), gap=300, s=1.8, colr="gold")
    big_text(c, "~1 IN 4", W / 2, 200, 110, span(t, t0, t0 + 0.4), "gold")
    label(c, "kept it up for even 10 of the 14 days", W / 2, 960, 46, "cream", "bold", span(t, t0 + 0.6, t0 + 1.0))


def s_pings(c, t, t0):
    explainer_bg(c, t, "magenta")
    head_profile(c, 760, 620, 1.2, t, pings=span(t, t0, S("day_ten", "pain", 0)))
    big_text(c, "JUST ONE LITTLE HIT...", 1300, 200, 50, span(t, S("day_ten", "hits", -0.4), S("day_ten", "hits", 0.1)), "gold")


# ---------------------------------------------------------------- DAY 14
def s_dark_head(c, t, t0):
    c.drawRect(skia.Rect(0, 0, W, H), paint("#07051A"))
    head_profile(c, W / 2, 600, 1.4, t, light=0.25 + 0.15 * math.sin(t * 2))
    big_text(c, "THIS IS WHERE IT GETS STRANGE", W / 2, 140, 54, span(t, t0 + 0.2, t0 + 0.7), "sand")


def s_focus(c, t, t0):
    explainer_bg(c, t, "deep")
    focus_test(c, W / 2, 600, t, calm=span(t, S("day_fourteen", "drift", 0.3), S("day_fourteen", "drift", 2.5)))
    big_text(c, "STAY ON THE DOT", W / 2, 150, 60, span(t, S("day_fourteen", "stay", -0.1), S("day_fourteen", "stay", 0.3)), "gold")


def s_age(c, t, t0):
    explainer_bg(c, t, "plum")
    ty = T("day_fourteen", "younger")
    age_dial(c, 760, 720, 360, span(t, ty - 0.8, ty + 0.6), t)
    draw_kr(c, 1500, 980, 1.3, "shocked" if t > ty else "curious", t)
    label(c, "after 2 weeks without mobile internet", 760, 900, 38, "sand", "bold", span(t, t0, t0 + 0.4))


def s_nine(c, t, t0):
    explainer_bg(c, t)
    people_icons(c, W / 2, 640, 10, 9, span(t, t0 + 0.3, t0 + 1.2), gap=165, s=1.05, colr="teal")
    big_text(c, "9 IN 10 IMPROVED", W / 2, 220, 90, span(t, t0, t0 + 0.4), "gold")
    for i, (w, word) in enumerate([("MOOD", "mood"), ("FOCUS", "focus"), ("LIFE", "life")]):
        pop(c, 560 + i * 400, 930, w, t, S("day_fourteen", word, -0.1, 2 if word == "focus" else 1), ["coral", "teal", "plum"][i], 48)


# ---------------------------------------------------------------- DAY 30
def s_count(c, t, t0):
    explainer_bg(c, t)
    th = T("day_thirty", "hundred")
    counter_text(c, 0, 150, span(t, t0 + 0.4, th + 0.6), lambda v: f"{v:.0f} HOURS", 720, 420, 120, "gold")
    for i in range(6):
        day_tile(c, 330 + i * 160, 760, 0.75, span(t, S("day_thirty", "six", -0.2) + i * 0.12, S("day_thirty", "six", 0.2) + i * 0.12), f"DAY {i + 1}")
    draw_kr(c, 1600, 1000, 1.25, "pointing" if t > th else "thinking", t)
    label(c, "5 hrs × 30 days", 720, 270, 44, "sand", "bold", span(t, t0, t0 + 0.4))


def s_twist(c, t, t0):
    explainer_bg(c, t, "magenta")
    keypad_phone(c, 560, 560, 1.0, t, "CALLS  SMS")
    smartphone(c, 1360, 560, 0.85, t, "lock", glow_a=0.4)
    tc, tx, ti = T("day_thirty", "calls"), T("day_thirty", "texts"), T("day_thirty", "internet")
    pop(c, 1360, 160, "CALLS: WORKED", t, tc, "teal", 46)
    pop(c, 1360, 250, "TEXTS: WORKED", t, tx, "teal", 46)
    pop(c, 1360, 960, "INTERNET: GONE", t, ti, "coral", 50)
    if t < tc:
        big_text(c, "THEY NEVER GAVE UP THEIR PHONES", W / 2, 150, 54, span(t, S("day_thirty", "never", -0.1), S("day_thirty", "never", 0.3)), "gold")


def s_scroll(c, t, t0):
    explainer_bg(c, t)
    ts = T("day_thirty", "scroll")
    scroll_feed(c, W / 2, 560, t, speed=2.5, snap=span(t, ts + 0.2, ts + 0.7))
    big_text(c, "THE PROBLEM: THE ENDLESS SCROLL", W / 2, 1000, 56, span(t, ts, ts + 0.4), "gold")


def s_fb(c, t, t0):
    explainer_bg(c, t)
    paper(c, 640, 540, 1.1, "Allcott et al. · AER 2020", "4 weeks off Facebook", "plum", -3, span(t, t0, t0 + 0.5))
    tb = T("day_thirty", "less")
    for i, (lab, v) in enumerate([("NEVER QUIT", 1.0), ("QUIT FOR 4 WEEKS", 0.62)]):
        w = 560 * (v if i == 0 else 1 - (1 - v) * ease(span(t, tb, tb + 0.8)))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(1120, 420 + i * 200, 1120 + w, 520 + i * 200), 20, 20), paint(["sand", "teal"][i]))
        label(c, lab, 1120, 400 + i * 200, 36, "cream", "bold", 1.0, "left")
    label(c, "Facebook use, weeks later", 1400, 860, 44, "cream", "bold", span(t, tb, tb + 0.4))
    big_text(c, "IT BREAKS THE HABIT", W / 2, 150, 68, span(t, S("day_thirty", "habit", -0.3), S("day_thirty", "habit", 0.1)), "gold")


# ---------------------------------------------------------------- PAYOFF
def s_drawer_back(c, t, t0):
    room_bg(c, t)
    to = T("payoff", "open")
    tn = T("payoff", "hundreds")
    with Cam(c, keys(t, [(t0, 1.0), (tn, 1.0), (tn + 1.5, 1.45)]), W / 2, 600, t=t):
        drawer(c, W / 2, 760, 1.0, t, open_p=span(t, to - 0.1, to + 0.8), phone=False)
        rise = ease_out(span(t, to + 0.5, to + 1.4))
        if rise > 0:
            smartphone(c, W / 2, 640 - 140 * rise, 0.62, t, "notifs" if t > tn else "lock", notifs=int(120 * span(t, tn, tn + 1.5)), a=rise)
    if t > tn:
        for k in range(int(14 * span(t, tn, tn + 1.5))):
            bubble(c, 300 + rng(k, 3) * 1300, 160 + rng(k, 4) * 300, 0.7, 1.0, i=k)


def s_wait(c, t, t0):
    explainer_bg(c, t, "deep")
    jeans_pocket(c, W / 2, 700, 0.85, t, outline=0.5)
    hand(c, W / 2 + 60, 470 + 14 * math.sin(t * 1.5), 1.0, rot=-6)
    big_text(c, "...IT WAITS.", W / 2, 140, 76, span(t, S("payoff", "waits", -0.1), S("payoff", "waits", 0.4)), "gold")


def s_tease(c, t, t0):
    explainer_bg(c, t, "plum")
    glow(c, W / 2 - 200, 700, 420, "amber", 0.35)
    piggy(c, W / 2 - 200, 700, 1.2, t, coin_p=(t - t0) % 1.4 / 1.4)
    for i in range(5):
        coin_stack(c, 1180 + i * 130, 900, int(4 + i * 5 * span(t, t0 + 0.5, t0 + 3)), 1.0)
    label(c, "OVER 20 YEARS...", 1440, 980, 40, "sand", "bold")
    big_text(c, "NEXT: ₹100 A DAY FOR 20 YEARS?", W / 2, 150, 64, span(t, t0 + 0.2, t0 + 0.7), "gold")


# ---------------------------------------------------------------- round 2 (quality gate): hero scenes + pacing
def s_hook_roof(c, t, t0):
    rooftop(c, t)
    with Cam(c, keys(t, [(t0, 1.08), (t0 + 6, 1.0)]), 480, 700, t=t):
        person(c, 420, 1000, 1.7, "teal", phone=False, look_up=1.0)
        phone_outline(c, 640, 560, 0.42, 0.9 + 0.1 * math.sin(t * 5), rot=12, color="gold")
        xmark(c, 640, 560, 1.2, span(t, t0 + 0.4, t0 + 0.9))
    big_text(c, "30 DAYS.", 1350, 330, 150, span(t, t0, t0 + 0.25), "gold")
    big_text(c, "NO PHONE.", 1350, 500, 150, span(t, t0 + 0.2, t0 + 0.45), "cream")


def s_hook_tiles(c, t, t0):
    room_bg(c, t)
    th = t0 + 0.3
    counter_text(c, 0, 150, span(t, t0, t0 + 1.2), lambda v: f"{v:.0f} HOURS", W / 2, 260, 150, "gold")
    big_text(c, "= 6 FULL DAYS BACK", W / 2, 400, 80, span(t, S("hook", "six", -0.1), S("hook", "six", 0.3)), "coral")
    for i in range(6):
        p = span(t, S("hook", "six", -0.2) + 0.12 * i, S("hook", "six", 0.3) + 0.12 * i)
        day_tile(c, 360 + i * 240, 760 - 120 * (1 - ease_out(p)), 1.2, p, f"DAY {i + 1}")


def s_wall(c, t, t0):
    dusk_bg(c, t, 0.9)
    person(c, 420, 1010, 1.4, "teal")
    for r in range(4):
        for k in range(6):
            x = 760 + k * 190 + (95 if r % 2 else 0)
            c.drawRect(skia.Rect(x, 300 + r * 150, x + 180, 440 + r * 150), paint("#7A3B2E"))
            c.drawRect(skia.Rect(x, 300 + r * 150, x + 180, 440 + r * 150), paint("#4E2219", stroke=6))
    c.drawLine(760, 300, 1900, 300, paint("amber", 0.6, stroke=6))
    big_text(c, "THE PROBLEM NOBODY WARNS YOU ABOUT", W / 2, 160, 54, span(t, S("day_two", "nobody", -0.2), S("day_two", "nobody", 0.2)), "gold")


def s_street_lost(c, t, t0):
    dusk_bg(c, t, 1.0)
    c.drawRect(skia.Rect(0, 900, W, H), paint("#2A2438"))
    for k in range(12):
        c.drawRect(skia.Rect(k * 180, 980, k * 180 + 90, 992), paint("sand", 0.6))
    auto_rickshaw(c, 1650 - (t - t0) * 90, 960, 1.0)
    signpost(c, 330, 960, 1.0, [("ANDHERI ?", 1), ("BANDRA ?", -1), ("???", 1)])
    person(c, 960, 1000, 1.45, "teal")
    big_text(c, "?", 1060, 450, 160, span(t, t0 + 0.4, t0 + 0.8), "gold")
    big_text(c, "NO MAPS. NO IDEA WHERE YOU ARE.", W / 2, 150, 58, span(t, S("day_two", "maps", -0.1), S("day_two", "maps", 0.3)), "coral")


def s_keypad_close(c, t, t0):
    explainer_bg(c, t, "magenta")
    keypad_phone(c, 620, 560, 1.5, t, "CALLS  SMS", rot=-6 + 2 * math.sin(t * 2))
    pop(c, 1320, 420, "CALLS", t, S("day_two", "calls", -0.1), "teal", 70)
    pop(c, 1320, 560, "SMS", t, S("day_two", "calls", 0.4), "teal", 70)
    pop(c, 1320, 700, "THAT'S IT.", t, S("day_two", "calls", 1.0), "coral", 60)


def s_never(c, t, t0):
    rooftop(c, t, 0.9)
    smartphone(c, W / 2, 560, 1.15, t, "lock", glow_a=0.8)
    phone_outline(c, W / 2, 560, 1.32 + 0.04 * math.sin(t * 3), 0.7, color="gold")
    big_text(c, "NEVER JUST A PHONE", W / 2, 150, 72, span(t, S("day_two", "never", 0), S("day_two", "never", 0.4)), "gold")


def s_fill(c, t, t0):
    explainer_bg(c, t)
    for i in range(5):
        p = span(t, t0 + 0.2 + 0.25 * i, t0 + 0.6 + 0.25 * i)
        x = 360 + i * 300
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 120, 420, x + 120, 700), 26, 26), dashed("sand", p, 6))
        label(c, f"HOUR {i + 1}", x, 580, 40, "sand", "bold", p)
    big_text(c, "5 EMPTY HOURS. EVERY DAY.", W / 2, 220, 76, span(t, t0, t0 + 0.4), "gold")
    label(c, "almost 1/3 of your waking day", W / 2, 840, 46, "cream", "bold", span(t, t0 + 1.2, t0 + 1.6))


def s_talk(c, t, t0):
    rooftop(c, t, 1.2)
    person(c, 760, 1000, 1.55, "teal")
    person(c, 1160, 1000, 1.55, "#8A2A5C", female=True)
    for i, (x, w) in enumerate([(820, "So then..."), (1100, "Haha, sach mein?")]):
        if t > t0 + 0.3 + i * 0.9:
            pill(c, x, 380 + i * 90, 1.0, w, ["teal", "magenta"][i], "cream", 40)
    big_text(c, "A WHOLE CONVERSATION. NO CHECKING.", W / 2, 150, 56, span(t, t0, t0 + 0.4), "gold")


def s_real(c, t, t0):
    dusk_bg(c, t, 0.7)
    for i, x in enumerate([420, 760, 1160, 1500]):
        a = 1.0 if i == 1 else 1 - 0.75 * span(t, t0 + 0.6 + 0.2 * i, t0 + 1.2 + 0.2 * i)
        person(c, x, 1000, 1.3, ["#3D5A80", "teal", "#8A2A5C", "#7A4E2D"][i], phone=i != 1)
        if a < 1:
            c.drawRect(skia.Rect(x - 120, 500, x + 120, 1010), paint("#140A26", 1 - a))
    big_text(c, "IN REAL LIFE...", W / 2, 170, 80, span(t, t0, t0 + 0.4), "gold")


def s_boredom(c, t, t0):
    room_bg(c, t, 0.5)
    clock_ring(c, 1300, 520, 230, 1, 1.0, t)
    c.save(); c.rotate((t - t0) * 6, 1300, 520); c.drawLine(1300, 520, 1300, 340, paint("cream", stroke=10)); c.restore()
    draw_kr(c, 640, 980, 1.5, "worried", t)
    big_text(c, "BOREDOM... FEELS LIKE PAIN", W / 2, 140, 62, span(t, S("day_ten", "boredom", 0), S("day_ten", "boredom", 0.4)), "coral")


def s_six(c, t, t0):
    rooftop(c, t, 1.5)
    person(c, 380, 1000, 1.4, "teal", look_up=1.0)
    for i in range(6):
        p = span(t, t0 + 0.15 * i, t0 + 0.5 + 0.15 * i)
        day_tile(c, 760 + i * 190, 520 + 30 * math.sin(t * 2 + i), 1.0, p, f"DAY {i + 1}")
    big_text(c, "6 FULL DAYS. HANDED BACK.", W / 2, 180, 76, span(t, t0, t0 + 0.4), "gold")
    label(c, "almost a full week of holidays", W / 2, 820, 46, "cream", "bold", span(t, S("day_thirty", "holidays", -0.8), S("day_thirty", "holidays", -0.4)))


def s_twist_head(c, t, t0):
    c.drawRect(skia.Rect(0, 0, W, H), paint("#07051A"))
    glow(c, W / 2, 560, 520, "magenta", 0.35)
    smartphone(c, W / 2, 600, 1.0, t, "lock", glow_a=0.9)
    big_text(c, "THEY NEVER GAVE UP THEIR PHONES", W / 2, 150, 62, span(t, S("day_thirty", "never", -0.1), S("day_thirty", "never", 0.3)), "gold")


def s_habit(c, t, t0):
    rooftop(c, t, 1.4)
    person(c, 760, 1000, 1.6, "teal", look_up=1.0)
    p = span(t, t0 + 0.3, t0 + 1.4)
    for k in range(5):  # a chain of notification links snapping apart
        x = 1250 + k * 110 + (k - 2) * 80 * ease(p)
        y = 560 + (k - 2) ** 2 * 18 * ease(p)
        c.drawOval(skia.Rect(x - 60, y - 34, x + 60, y + 34), paint("#9AA3BF", stroke=14))
    big_text(c, "IT BREAKS THE HABIT", W / 2, 160, 84, span(t, S("day_thirty", "habit", -0.3), S("day_thirty", "habit", 0.1)), "gold")


def s_calm(c, t, t0):
    rooftop(c, t, 1.5)
    person(c, 760, 1000, 1.7, "teal", look_up=1.0)
    smartphone(c, 1240, 840, 0.28, t, "notifs", rot=-80, glow_a=0.5 * (0.5 + 0.5 * math.sin(t * 6)), notifs=120)
    big_text(c, "YOU DON'T RUSH TO CHECK", W / 2, 160, 70, span(t, S("payoff", "rush", -0.2), S("payoff", "rush", 0.2)), "gold")


# ---------------------------------------------------------------- the list: (start, shot, transition)
def SHOTS():
    return [
        (0.0, s_hook_roof, "cut"),
        (S("hook", "hundred", -0.4), s_hook_tiles, "zoom"),
        (S("hook", "day", -0.25), s_hook_locked, "whip"),
        (S("hook", "biggest", -0.2), s_hook_head, "fade"),
        (E("hook") + 0.1, logo_sting(), "flash"),
        (S("promise", "deal", -0.5), s_rules_drawer, "iris"),
        (S("promise", "scrolling", -0.3), s_rules, "cut"),

        (B("hour_one") - 0.6, card("HOUR 1", "The reflex"), "iris"),
        (S("hour_one", "hand", -0.3), s_pocket_pat, "fade"),
        (S("hour_one", "queue", -0.3), s_queue, "whip"),
        (S("hour_one", "leg", -0.3), s_buzz, "cut"),
        (S("hour_one", "study", -0.4), s_phantom_count, "zoom"),
        (S("hour_one", "brain", -0.2), s_fake_notifs, "fade"),
        (S("hour_one", "says", -1.2), kr_react("worried", "IT'S BEEN 1 HOUR", line_at=S("hour_one", "been", 0)), "cut"),

        (B("day_two") - 0.6, card("DAY 2", "The wall"), "iris"),
        (B("day_two") + 0.9, s_wall, "fade"),
        (S("day_two", "pay", -0.4), s_pay, "whip"),
        (S("day_two", "train", -0.4), s_tickets, "whip"),
        (S("day_two", "new", -0.4), s_street_lost, "whip"),
        (S("day_two", "bank", -0.4), s_otp, "cut"),
        (S("day_two", "walk", -0.4), s_shop, "fade"),
        (S("day_two", "calls", -0.3), s_keypad_close, "cut"),
        (S("day_two", "now", -0.3, 2), s_never, "fade"),
        (S("day_two", "wallet", -0.4), s_four, "zoom"),
        (S("day_two", "cash", -0.4), s_2005, "fade"),

        (B("day_seven") - 0.6, card("DAY 7", "Boredom"), "iris"),
        (S("day_seven", "average", -0.3), s_clock, "fade"),
        (S("day_seven", "fill", -1.6), s_fill, "cut"),
        (S("day_seven", "metro", -0.3), s_metro, "whip"),
        (S("day_seven", "shampoo", -0.6), s_shampoo, "cut"),
        (S("day_seven", "slowly", -0.4), s_look_up, "fade"),
        (S("day_seven", "conversation", -1.6), s_talk, "cut"),
        (S("day_seven", "quick", -0.2), comment_prompt("What would you do with 5 free hours a day?", bg=lambda c, t: rooftop(c, t, 1.0)), "fade"),

        (B("day_ten") - 0.6, card("DAY 10", "The myth"), "iris"),
        (S("day_ten", "movies", -0.4), layer(s_lake, stamp_at("MYTH", S("day_ten", "perfect", 0.3))), "fade"),
        (S("day_ten", "real", -0.3), s_real, "whip"),
        (S("day_ten", "study", -0.4), s_study, "cut"),
        (S("day_ten", "quarter", -0.3), s_quarter, "cut"),
        (S("day_ten", "first", -0.3), s_pings, "fade"),
        (S("day_ten", "boredom", -0.4), s_boredom, "cut"),
        (S("day_ten", "rare", -1.6), kr_react("happy", "ALREADY RARE", line_at=S("day_ten", "rare", 0)), "cut"),

        (B("day_fourteen") - 0.6, card("DAY 14", "The brain"), "iris"),
        (S("day_fourteen", "this", -0.2), s_dark_head, "fade"),
        (S("day_fourteen", "same", -0.3), s_focus, "fade"),
        (S("day_fourteen", "after", -0.3), s_age, "zoom"),
        (S("day_fourteen", "pill", -1.0), statement("NO PILL. NO APP.", sub="Just... less scrolling.", at_t=S("day_fourteen", "pill", -0.6), bg=lambda c, t: (explainer_bg(c, t, "plum"), head_profile(c, W / 2, 820, 0.8, t, light=1.0))), "cut"),
        (S("day_fourteen", "nine", -0.3), s_nine, "fade"),

        (B("day_thirty") - 0.6, card("DAY 30", "The twist"), "iris"),
        (S("day_thirty", "five", -0.3), s_count, "fade"),
        (S("day_thirty", "six", -0.3), s_six, "fade"),
        (S("day_thirty", "twist", -0.3), s_twist_head, "flash"),
        (S("day_thirty", "calls", -0.5), s_twist, "cut"),
        (S("day_thirty", "problem", -0.8), s_scroll, "cut"),
        (S("day_thirty", "stanford", -1.0), s_fb, "whip"),
        (S("day_thirty", "month", -0.4), s_habit, "fade"),

        (B("payoff") - 0.6, card("DAY 31", "Back"), "iris"),
        (S("payoff", "open", -0.6), s_drawer_back, "fade"),
        (S("payoff", "first", -0.6), s_calm, "fade"),
        (S("payoff", "hand", -0.3), s_wait, "fade"),
        (S("payoff", "tell", -0.4), comment_prompt("Could you last 30 days? Or even 3?", bg=lambda c, t: room_bg(c, t)), "fade"),
        (S("payoff", "next", -0.3), s_tease, "flash"),
        (E(LAST_BEAT) + 0.3, end_screen(), "fade"),
    ]


LAST_BEAT = BEAT_KEYS[-1]
