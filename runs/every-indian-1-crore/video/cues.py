"""Sound for this video. The engine already adds: whooshes on transitions, riser + impact into chapter cards,
logo and end hits, hard silence before the HARD_CUT_BEFORE beat, and a score chosen from each beat's mood.
Add only what's specific to this story: a sound on every visible hit, and ambience beds per scene."""
from krwi import sfx as X  # pop(pitch), tick(), whoosh(d, seed), riser(d, seed), impact(seed, big), thunder(seed),
from krwi.timeline import T, at, B, E  # noqa: F401   match_flare(), heartbeat(), buzz(d), skitter(d), stamp_hit(),
                                       #               click(), chime(freq), glitch()


def HITS():
    h = [
        # HOOK: the phone buzzes on frame 0, the stamp slams, phones light up across India, the red circle
        (0.05, X.buzz(1.6), 0.55),
        (T("hook", "credited"), X.stamp_hit(), 0.8),
        (at("hook", "credited", 0.4), X.heartbeat(), 0.45),
        (T("hook", "all"), X.impact(1, 0.6), 0.55),
        (T("hook", "loses"), X.skitter(0.5), 0.35),
        (T("hook", "sitting"), X.pop(500), 0.5),
        # PROMISE: rules typed, baby pops, reports slap down
        (T("promise", "baby"), X.pop(1100), 0.45),
        # HOUR 1: three refresh taps, IT'S REAL stamp, wedding card, the "?" on whose
        (T("hour_one", "check"), X.click(), 0.5),
        (at("hour_one", "check", 0.5), X.click(), 0.5),
        (at("hour_one", "check", 1.0), X.click(), 0.5),
        (T("hour_one", "real"), X.stamp_hit(), 0.7),
        (T("hour_one", "fifty"), X.impact(2, 0.5), 0.5),
        (T("hour_one", "wedding"), X.chime(1180), 0.35),
        (T("hour_one", "whose"), X.pop(700), 0.5),
        # HOUR 6: tag torn off, new tag, SOLD OUT, the "≠"
        (T("hour_six", "changes"), X.skitter(0.35), 0.5),
        (at("hour_six", "changes", 0.35), X.pop(600), 0.5),
        (at("hour_six", "changes", 0.8), X.stamp_hit(), 0.75),
        (T("hour_six", "not"), X.impact(3, 0.5), 0.5),
        # DAY 3: the doorbell that never rings, riders blinking out, GONE, EMPTY
        (at("day_three", "doorbell", 0.6), X.click(), 0.45),
        (T("day_three", "seventyseven"), X.pop(900), 0.45),
        (T("day_three", "log"), X.glitch(), 0.4),
        (T("day_three", "gone"), X.stamp_hit(), 0.75),
        (at("day_three", "milk", -0.2), X.stamp_hit(), 0.7),
        (T("day_three", "promise"), X.chime(990), 0.35),
        # WEEK 2: ×47, the tomato price racing, the reveal
        (T("week_two", "fortyseven"), X.impact(4, 0.8), 0.6),
        (T("week_two", "prices"), X.riser(1.8, 6), 0.35),
        (T("week_two", "two", 2), X.impact(5, 1.0), 0.7),
        # MONTH 2: NO NOTES, the press, prices doubling day by day, WORTHLESS
        (at("month_two", "notes", 0.2), X.stamp_hit(), 0.7),
        (T("month_two", "gold"), X.chime(1320), 0.3),
        (T("month_two", "zimbabwe"), X.impact(6, 0.7), 0.5),
        (at("month_two", "stopped", -0.2), X.stamp_hit(), 0.8),
        # MONTH 3: the red circle lands on her, the FD melts, MELTED
        (T("month_three", "grandmother"), X.impact(7, 0.5), 0.45),
        (T("month_three", "twenty"), X.heartbeat(), 0.4),
        (at("month_three", "melted", -0.2), X.stamp_hit(), 0.7),
        # PAYOFF: 4% card, prices ×2
        (T("payoff", "four"), X.impact(8, 0.5), 0.5),
        (T("payoff", "eighteen"), X.stamp_hit(), 0.7),
        # BONUS: PRICELESS, the phone buzzes again (KYC)
        (at("bonus", "printed", 0.3), X.stamp_hit(), 0.7),
        (T("bonus", "eight"), X.buzz(1.2), 0.5),
        (T("bonus", "update"), X.pop(450), 0.5),
    ]
    # prices doubling MON..SAT: one tick per day card
    td = T("month_two", "doubled")
    h += [(td - 0.3 + i * 0.3, X.tick(), 0.45) for i in range(6)]
    return h


def AMB():
    return [
        ("room", B("hook"), E("hook"), 0.35),
        ("room", B("day_three"), E("day_three"), 0.4),
        ("wind", B("month_two"), E("month_two"), 0.5),
        ("room", B("month_three"), E("month_three"), 0.35),
        ("room", B("bonus"), E("bonus"), 0.3),
    ]
