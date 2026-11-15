"""Sound for this video. The engine already adds: whooshes on transitions, riser + impact into chapter cards,
logo and end hits, hard silence before the HARD_CUT_BEFORE beat, and a score chosen from each beat's mood.
Add only what's specific to this story: a sound on every visible hit, and ambience beds per scene."""
from krwi import sfx as X  # pop(pitch), tick(), whoosh(d, seed), riser(d, seed), impact(seed, big), thunder(seed),
from krwi.timeline import T, at, B, E  # noqa: F401   match_flare(), heartbeat(), buzz(d), skitter(d), stamp_hit(),
                                       #               click(), chime(freq), glitch()


def HITS():
    return [
        # (T("hook", "gone"), X.impact(1, 0.8), 0.6),
        # (at("hook", "scariest", 0.0), X.heartbeat(), 0.6),
    ]


def AMB():
    return [
        # (kind in swamp | rain | fire | wind | room, start, end, gain)
        # ("room", B("payoff"), E("payoff"), 0.5),
    ]
