"""Sound for this video. The engine already adds: whooshes on transitions, riser + impact into chapter cards,
logo and end hits, hard silence before the HARD_CUT_BEFORE beat, and a score chosen from each beat's mood.
Add only what's specific to this story: a sound on every visible hit, and ambience beds per scene."""
from krwi import sfx as X  # pop(pitch), tick(), whoosh(d, seed), riser(d, seed), impact(seed, big), thunder(seed),
from krwi.timeline import T, at, B, E  # noqa: F401   match_flare(), heartbeat(), buzz(d), skitter(d), stamp_hit(),
                                       #               click(), chime(freq), glitch()


def HITS():
    return [
        (T("hook", "six") - 0.1, X.pop(900), 0.5),
        (T("hook", "yours") - 0.2, X.click(), 0.6),
        (T("hook", "one") + 0.2, X.pop(700), 0.5),
        (T("hook", "first"), X.stamp_hit(), 0.6),
        (T("promise", "fantasy"), X.stamp_hit(), 0.6),
        (T("promise", "born"), X.stamp_hit(), 0.6),
        (T("today", "two") - 0.1, X.pop(1000), 0.5),
        (T("today", "one", 2) - 0.1, X.pop(800), 0.5),
        (T("today", "below"), X.stamp_hit(), 0.6),
        (T("today", "its", 1), X.stamp_hit(), 0.6),
        (T("today", "brakes"), X.buzz(0.8), 0.35),
        (T("kerala", "sixty") - 0.1, X.pop(800), 0.5),
        (T("kerala", "three"), X.click(), 0.6),
        (T("kerala", "locked"), X.click(), 0.6),
        (T("kerala", "rings") - 0.2, X.chime(880), 0.4),
        (T("kerala", "family"), X.stamp_hit(), 0.6),
        (T("classroom", "hospital"), X.stamp_hit(), 0.5),
        (T("classroom", "fifteen"), X.impact(2, 0.5), 0.5),
        (T("classroom", "close"), X.stamp_hit(), 0.6),
        (T("classroom", "works") - 0.3, X.chime(660), 0.5),
        (T("fifty", "sixty") - 0.2, X.pop(800), 0.5),
        (T("fifty", "you"), X.stamp_hit(), 0.7),
        (T("sixties", "first"), X.stamp_hit(), 0.6),
        (T("sixties", "empty") - 0.2, X.heartbeat(), 0.5),
        (T("sixties", "twenty", 2), X.stamp_hit(), 0.6),
        (T("twist", "same"), X.stamp_hit(), 0.6),
        (T("payoff", "now"), X.stamp_hit(), 0.6),
    ]


def AMB():
    return [
        # (kind in swamp | rain | fire | wind | room, start, end, gain)
        ("room", B("kerala"), E("kerala"), 0.4),
        ("wind", B("sixties"), E("sixties"), 0.35),
    ]
