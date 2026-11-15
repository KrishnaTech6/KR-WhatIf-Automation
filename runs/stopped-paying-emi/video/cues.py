"""Sound for this video. The engine already adds: whooshes on transitions, riser + impact into chapter cards,
logo and end hits, hard silence before the HARD_CUT_BEFORE beat, and a score chosen from each beat's mood.
Add only what's specific to this story: a sound on every visible hit, and ambience beds per scene."""
from krwi import sfx as X  # pop(pitch), tick(), whoosh(d, seed), riser(d, seed), impact(seed, big), thunder(seed),
from krwi.timeline import T, at, B, E  # noqa: F401   match_flare(), heartbeat(), buzz(d), skitter(d), stamp_hit(),
                                       #               click(), chime(freq), glitch()


def HITS():
    return [
        (0.2, X.buzz(0.9), 0.4),
        (T("hook", "defaulter"), X.stamp_hit(), 0.7),
        (T("hook", "court"), X.click(), 0.6),
        (T("hook", "paper"), X.heartbeat(), 0.5),
        (T("promise", "fourteen"), X.pop(900), 0.5),
        (T("day_one", "empty"), X.stamp_hit(), 0.6),
        (T("day_one", "overdue"), X.stamp_hit(), 0.6),
        (T("day_one", "bounced") - 0.1, X.buzz(0.5), 0.4),
        (T("day_one", "fine") - 0.1, X.buzz(0.5), 0.4),
        (T("day_one", "cant"), X.click(), 0.6),
        (T("day_thirty", "lights"), X.buzz(1.0), 0.4),
        (T("day_thirty", "again"), X.buzz(0.8), 0.4),
        (T("day_thirty", "again", 2), X.buzz(0.8), 0.4),
        (T("day_thirty", "threats"), X.stamp_hit(), 0.5),
        (T("day_thirty", "shouting"), X.stamp_hit(), 0.5),
        (T("day_thirty", "shaming"), X.stamp_hit(), 0.5),
        (T("day_thirty", "oh") - 0.2, X.buzz(0.8), 0.4),
        (T("day_thirty_one", "s"), X.stamp_hit(), 0.6),
        (T("day_thirty_one", "fall"), X.glitch(), 0.4),
        (T("day_thirty_one", "rejected"), X.stamp_hit(), 0.7),
        (T("day_thirty_one", "rejected", 2), X.stamp_hit(), 0.7),
        (T("day_thirty_one", "breathe") - 0.2, X.chime(660), 0.45),
        (T("day_sixty", "rings") - 0.1, X.chime(1200), 0.35),
        (T("day_sixty", "guarantor"), X.click(), 0.6),
        (T("day_ninety_one", "n"), X.stamp_hit(), 0.8),
        (T("day_ninety_one", "judge"), X.stamp_hit(), 0.6),
        (T("month_four", "drawer"), X.click(), 0.6),
        (T("month_six", "possession"), X.stamp_hit(), 0.7),
        (T("month_six", "auction"), X.impact(2, 0.8), 0.6),
        (T("twist", "crime"), X.stamp_hit(), 0.6),
        (T("twist", "bounced"), X.stamp_hit(), 0.7),
        (T("twist", "rare"), X.stamp_hit(), 0.5),
        (T("twist", "real"), X.stamp_hit(), 0.6),
        (T("payoff", "money") - 0.2, X.chime(880), 0.4),
        (T("payoff", "life") - 0.2, X.chime(660), 0.45),
    ]


def AMB():
    return [
        # (kind in swamp | rain | fire | wind | room, start, end, gain)
        ("room", B("day_thirty"), E("day_thirty"), 0.35),
        ("wind", B("month_six"), E("month_six"), 0.3),
    ]
