"""Sound for this video. The engine already adds: whooshes on transitions, riser + impact into chapter cards,
logo and end hits, hard silence before the HARD_CUT_BEFORE beat, and a score chosen from each beat's mood.
Add only what's specific to this story: a sound on every visible hit, and ambience beds per scene."""
from krwi import sfx as X  # pop(pitch), tick(), whoosh(d, seed), riser(d, seed), impact(seed, big), thunder(seed),
from krwi.timeline import T, at, B, E  # noqa: F401   match_flare(), heartbeat(), buzz(d), skitter(d), stamp_hit(),
                                       #               click(), chime(freq), glitch()


def _ring(d=1.6):
    """Old twin-bell alarm: fast chime trills."""
    import numpy as np
    sr = 48000
    out = np.zeros(int(d * sr), np.float32)
    for k in range(int(d * 14)):
        c = X.chime(1760 if k % 2 else 1980)
        s = int(k / 14 * sr)
        n = min(len(c), len(out) - s)
        if n > 0:
            out[s:s + n] += c[:n] * 0.5
    return out


def HITS():
    return [
        (0.05, _ring(1.8), 0.45),                                   # both alarms ringing on frame 0
        (at("hook", "fourteen", 0.0), X.impact(1, 0.6), 0.5),
        (at("hook", "difference", 0.0), X.chime(1320), 0.5),
        (at("promise", "alarm", 0.0), _ring(0.8), 0.35),
        (at("promise", "snooze", 0.0), X.stamp_hit(), 0.5),
        (at("promise", "went", 0.2), X.click(), 0.5),
        (at("day_one", "photo", 0.0), X.click(), 0.7),
        (at("day_one", "sixty", 0.0), X.pop(900), 0.5),
        (at("day_three", "percent", 0.0), X.pop(700), 0.5),
        (at("day_three", "bedtime", 0.0), X.impact(2, 0.4), 0.4),
        (at("day_seven", "trap", 0.0), X.stamp_hit(), 0.6),
        (at("day_ten", "science", -0.4), X.stamp_hit(), 0.6),
        (at("day_ten", "found", 0.0), X.skitter(1.2), 0.3),
        (at("the_big_one", "skipped", 0.0), X.impact(3, 1.0), 0.6),
        (at("the_big_one", "slower", 0.0), X.glitch(), 0.4),
        (at("the_big_one", "scariest", 0.0), X.heartbeat(), 0.5),
        (at("day_twenty_one", "dial", 0.0), X.chime(1568), 0.6),
        (at("day_twenty_one", "lights", 0.0), X.click(), 0.6),
        (at("payoff", "magic", 0.0), X.impact(5, 0.7), 0.5),
        (at("payoff", "percent", 0.0), X.pop(1000), 0.5),
        (at("bonus", "five", 0.0), _ring(1.0), 0.35),
    ]


def AMB():
    return [
        ("room", 0.0, B("promise"), 0.35),
        ("wind", B("bonus"), at("bonus", "would", -0.5), 0.3),
    ]
