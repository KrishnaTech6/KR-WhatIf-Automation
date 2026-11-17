"""Sound for 'What If You Walked 10,000 Steps Every Day for a Year?'. The engine already adds whooshes, risers into
chapter cards, logo/end hits, the hard silence before Day 365 and the mood score. Here: a sound on every visible hit
(pops, stamps, counters, ticks) and ambience beds."""
from krwi import sfx as X  # pop(pitch), tick(), whoosh(d, seed), riser(d, seed), impact(seed, big), thunder(seed),
from krwi.timeline import T, at, B, E  # noqa: F401   match_flare(), heartbeat(), buzz(d), skitter(d), stamp_hit(),
                                       #               click(), chime(freq), glitch()


def HITS():
    return [
        # HOOK: year counter, the London-Moscow line, scale needle, the glow
        (0.05, X.chime(1320), 0.35),
        (at("hook", "london", -0.1), X.pop(800), 0.4),
        (at("hook", "moscow", 0.0), X.pop(1100), 0.45),
        (at("hook", "barely", -0.05), X.tick(), 0.6),
        (at("hook", "moved", 0.0), X.stamp_hit(), 0.45),
        (at("hook", "grew", 0.0), X.chime(990), 0.4),
        # PROMISE: papers flip in, phone counter, world average, goal, NO EXCUSES stamp
        (at("promise", "nine", 0.0), X.impact(4, 0.4), 0.4),
        (at("promise", "january", -0.1), X.pop(900), 0.4),
        (at("promise", "five", 0.0), X.click(), 0.5),
        (at("promise", "average", 0.0), X.pop(1000), 0.4),
        (at("promise", "ten", 0.3), X.chime(1320), 0.4),
        (at("promise", "excuses", -0.1), X.stamp_hit(), 0.55),
        # DAY 1
        (at("day_one", "two", -0.1), X.click(), 0.5),
        (at("day_one", "grocery", -0.1), X.pop(850), 0.4),
        (at("day_one", "long", -0.2), X.pop(950), 0.4),
        (at("day_one", "laps", -0.1), X.tick(), 0.5),
        (at("day_one", "hidden", -0.1), X.impact(3, 0.4), 0.4),
        (at("day_one", "hour", 0.0), X.pop(1000), 0.45),
        (at("day_one", "twentyfive", 0.0), X.stamp_hit(), 0.45),
        (at("day_one", "nine", 0.0), X.tick(), 0.5),
        (at("day_one", "done", -0.05), X.chime(1480), 0.55),
        # WEEK 1: ouch, the question, NOT SCIENCE stamp, pedometer, kanji morph, meme, AN ADVERT stamp
        (at("week_one", "hurt", -0.1), X.pop(600), 0.45),
        (at("week_one", "sleeping", -0.1), X.chime(880), 0.3),
        (at("week_one", "why", -0.05), X.impact(5, 0.4), 0.45),
        (at("week_one", "doctor", 0.3), X.stamp_hit(), 0.55),
        (at("week_one", "nineteen", -0.1), X.pop(800), 0.4),
        (at("week_one", "manpokei", -0.05), X.chime(1180), 0.45),
        (at("week_one", "walking", 0.0), X.pop(1200), 0.45),
        (at("week_one", "advert", -0.05), X.stamp_hit(), 0.6),
        # MONTH 1: scale, meme wipe, friend laughs, sugar curves
        (at("month_one", "three", -0.1), X.pop(800), 0.4),
        (at("month_one", "few", -0.1), X.tick(), 0.55),
        (at("month_one", "laughs", 0.0), X.pop(500), 0.45),
        (at("month_one", "dinner", -0.1), X.pop(900), 0.35),
        (at("month_one", "ireland", -0.1), X.pop(1000), 0.4),
        (at("month_one", "softens", 0.0), X.chime(990), 0.4),
        (at("month_one", "looking", 0.0), X.click(), 0.5),
        # MONTH 3
        (at("month_three", "lift", -0.1), X.click(), 0.5),
        (at("month_three", "calls", -0.1), X.pop(900), 0.4),
        (at("month_three", "less", 0.0), X.chime(1180), 0.35),
        (at("month_three", "studies", 0.0), X.impact(4, 0.4), 0.45),
        (at("month_three", "fifth", 0.0), X.pop(1100), 0.5),
        (at("month_three", "honest", 0.0), X.pop(700), 0.45),
        # MONTH 6
        (at("month_six", "rome", 0.0), X.pop(1100), 0.45),
        (at("month_six", "one", 0.0), X.pop(800), 0.4),
        (at("month_six", "not", 0.0), X.chime(1320), 0.45),
        # DAY 365
        (at("year_one", "almost", 0.0), X.click(), 0.55),
        (at("year_one", "roughly", 0.0), X.impact(2, 0.9), 0.7),
        (at("year_one", "hadza", 0.0), X.pop(700), 0.35),
        (at("year_one", "same", 0.0), X.pop(1000), 0.45),
        (at("year_one", "total", 0.0), X.tick(), 0.5),
        (at("year_one", "matters", 0.0), X.stamp_hit(), 0.5),
        # PAYOFF
        (at("payoff", "never", 0.0), X.chime(880), 0.35),
        (at("payoff", "scanned", 0.0), X.buzz(0.8), 0.25),
        (at("payoff", "grown", 0.0), X.chime(1480), 0.5),
        (at("payoff", "two", 0.0), X.pop(1200), 0.5),
        (at("payoff", "shrank", 0.0), X.pop(400), 0.45),
        (at("payoff", "turned", 0.0), X.chime(1320), 0.45),
        # BONUS + OUTRO
        (at("bonus", "seven", 0.3), X.chime(1480), 0.45),
        (at("bonus", "happens", 0.0), X.chime(1180), 0.35),
        (at("sign_off", "five", 0.0), X.tick(), 0.6),
    ]


def AMB():
    return [
        ("wind", B("hook"), E("hook"), 0.2),
        ("room", B("day_one"), E("day_one"), 0.3),
        ("room", B("week_one"), at("week_one", "and", 0.0), 0.3),
        ("room", B("month_one"), at("month_one", "researchers", 0.0), 0.3),
        ("wind", at("year_one", "why", 0.0), at("year_one", "they", 0.0), 0.35),
        ("room", at("bonus", "remember", 0.0), E("bonus"), 0.3),
    ]
