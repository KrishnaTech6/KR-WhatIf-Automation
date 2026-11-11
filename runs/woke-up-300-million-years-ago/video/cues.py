"""Music, SFX and ambience cue sheet for the main video (style: a sound on every motion,
ambience bed per scene, riser -> impact into every chapter card, silence before the fire)."""
import numpy as np
from krwi import sfx as X, music as Mu
from krwi.sfx import SR
from krwi.timeline import T, B, E, TOTAL
import shots as S


def BUILD():
    tot = TOTAL + 6
    mus, fx, amb = Mu.Track(tot), Mu.Track(tot), Mu.Track(tot)
    L = S.SHOTS()
    starts = {fn.__name__ if fn.__name__ != "f" else f"card{i}": st for i, (st, fn, tr) in enumerate(L)}
    cards = [st for st, fn, tr in L if fn.__name__ == "f"]
    endt = E("payoff") + 0.3

    # ---------------- ambience beds (scene based)
    def bed(kind, a, b, g):
        x = getattr(X, "amb_" + kind)(b - a + 1.0)
        fade = int(0.8 * SR); x[:fade] *= np.linspace(0, 1, fade); x[-fade:] *= np.linspace(1, 0, fade)
        amb.add(a, x, g)
    bed("swamp", 0, E("hook"), 0.5)
    bed("swamp", B("minute"), B("night") - 1.5, 0.45)
    bed("rain", T("night", "clouds") - 0.5, T("night", "now"), 0.5)
    bed("fire", T("night", "lightning") + 0.3, E("night") + 0.5, 0.6)
    bed("wind", B("year"), E("year"), 0.45)
    bed("swamp", B("twist"), T("twist", "fall") + 2, 0.35)
    bed("room", T("payoff", "so", 1), E("payoff"), 0.6)

    # ---------------- transitions: soft whoosh on every non-cut shot change (not on cards: they get riser+impact)
    for i, (st, fn, tr) in enumerate(L):
        if fn.__name__ == "f" or tr == "cut" or i == 0:
            continue
        fx.add(st - 0.15, X.whoosh(0.55, i), 0.35 if tr in ("whip", "zoom") else 0.22)

    # ---------------- chapter cards: riser into an impact (not before Night 1: hard silence instead)
    for c in cards:
        if abs(c - (B("night") - 0.3)) < 0.01:
            continue
        fx.add(c - 1.6, X.riser(1.6, int(c)), 0.35)
        fx.add(c, X.impact(int(c), 0.6), 0.45)

    # ---------------- specific hits (every visible motion gets a sound)
    hits = [
        (0.15, X.buzz(1.8), 0.5),                       # wings on your chest
        (T("hook", "wings"), X.chime(990), 0.35),
        (T("hook", "spark"), X.click(), 0.6),
        (T("hook", "fire") - 0.1, X.impact(1, 0.7), 0.6),
        (T("hook", "scariest"), X.heartbeat(), 0.6), (T("hook", "scariest") + 0.9, X.heartbeat(), 0.6),
        (E("hook") + 0.1, X.impact(2, 1.0), 0.7),        # logo hit
        (T("promise", "nobody") + 0.3, X.pop(700), 0.5),
        (T("promise", "pretend"), X.glitch(), 0.4),
        (T("promise", "three"), X.riser(1.2, 9), 0.3),
        (T("promise", "dinosaurs"), X.stamp_hit(), 0.6),
        (T("minute", "today") + 0.5, X.pop(800), 0.45), (T("minute", "here") + 0.5, X.pop(1000), 0.5),
        (T("minute", "dont") + 0.3, X.pop(900), 0.45),
        (T("minute", "strike"), X.click(), 0.5),
        (T("minute", "whoosh") - 0.05, X.match_flare(), 0.8),
        (T("hour1", "spot"), X.chime(1320), 0.3),
        (T("hour1", "flowers"), X.pop(800), 0.45), (T("hour1", "flowers") + 0.3, X.stamp_hit(), 0.35),
        (T("hour1", "grass"), X.pop(900), 0.45), (T("hour1", "grass") + 0.3, X.stamp_hit(), 0.35),
        (T("hour1", "birds"), X.pop(1000), 0.45), (T("hour1", "birds") + 0.3, X.stamp_hit(), 0.35),
        (T("hour1", "scaly"), X.pop(700), 0.4),
        (T("hour1", "tall"), X.riser(0.8, 12), 0.25),
        (T("hour1", "dinosaurs") - 0.2, X.whoosh(0.5, 30), 0.4), (T("hour1", "early"), X.stamp_hit(), 0.7),
        (T("hour1", "seventy"), X.riser(1.0, 13), 0.3),
        (T("hour3", "something"), X.skitter(2.5, 1), 0.45),
        (T("hour3", "bed"), X.impact(14, 0.4), 0.4),
        (T("hour3", "good") + 0.3, X.pop(850), 0.45),
        (T("hour3", "above") - 0.2, X.buzz(1.6, 3), 0.55),
        (T("hour3", "hunter"), X.pop(600), 0.5),
        (T("hour3", "heres"), X.pop(1100), 0.4),
        (T("hour3", "more"), X.riser(1.5, 15), 0.25),
        (T("hour3", "fighting") - 0.4, X.stamp_hit(), 0.5),
        (T("hour3", "comments") - 0.6, X.chime(1180), 0.4),
        (T("night", "clouds"), X.thunder(31), 0.35),
        (T("night", "lightning") - 0.05, X.thunder(32), 0.95),
        (T("night", "lightning"), X.impact(33, 1.0), 0.6),
        (T("night", "now"), X.heartbeat(), 0.7), (T("night", "now") + 0.8, X.heartbeat(), 0.7),
        (T("night", "here"), X.match_flare(), 0.6),
        (T("night", "runs"), X.impact(34, 0.8), 0.6),
        (T("night", "burnt") - 0.3, X.whoosh(0.5, 35), 0.4),
        (T("night", "air"), X.impact(36, 1.0), 0.6),
        (T("year", "crashing"), X.riser(1.2, 40), 0.3), (T("year", "piece"), X.impact(41, 0.8), 0.55),
        (T("year", "ice"), X.chime(660), 0.4),
        (T("year", "odisha"), X.pop(700), 0.5),
        (T("year", "boulders"), X.stamp_hit(), 0.4),
        (T("year", "frozen"), X.chime(1760), 0.35),
        (T("twist", "die"), X.whoosh(1.2, 42), 0.4), (T("twist", "die") + 1.4, X.impact(43, 0.5), 0.45),
        (T("twist", "rot"), X.stamp_hit(), 0.5),
        (T("twist", "squeezed"), X.impact(44, 0.6), 0.4),
        (T("twist", "maybe", 1), X.pop(800), 0.45), (T("twist", "maybe", 2), X.pop(950), 0.45),
        (T("twist", "either"), X.riser(2.0, 45), 0.3),
        (T("payoff", "coal"), X.pop(700), 0.5),
        (T("payoff", "three"), X.click(), 0.5), (T("payoff", "three") + 0.25, X.click(), 0.5), (T("payoff", "three") + 0.5, X.click(), 0.5),
        (T("payoff", "switch"), X.click(), 0.9), (T("payoff", "switch") + 0.05, X.chime(880), 0.4),
        (T("payoff", "happening"), X.pop(600), 0.45),
        (T("payoff", "if"), X.chime(1180), 0.35),
        (T("payoff", "next"), X.impact(50, 0.7), 0.5),
        (endt, X.impact(51, 1.0), 0.6),
    ]
    for t, x, g in hits:
        fx.add(t, x, g)

    # ---------------- music (sections)
    hk = E("hook")
    for i in range(int(hk / 1.0)):                                     # hook: ticking clock + motif + warm pad
        fx.add(i * 1.0, X.tick(), 0.25)
    Mu.pad(mus, 0, hk, ["Dm", "Bb"], "pad_2_warm", 0.35, 4)
    Mu.motif(mus, 0.6, "music_box", 0.55); Mu.motif(mus, 6.5, "music_box", 0.5)
    for n in Mu.CH["Dm"]:                                             # logo chord + sparkle
        mus.add(hk + 0.1, Mu.note("string_ensemble_1", n, 3.0, 0.6), 0.6)
        mus.add(hk + 0.1, Mu.note("choir_aahs", n, 3.0, 0.5), 0.4)
    Mu.motif(mus, hk + 0.3, "celesta", 0.45, 0.25, ["D6", "F6", "A6", "G6"])
    Mu.pad(mus, B("promise") + 2.5, E("promise"), ["F", "C"], "pad_2_warm", 0.3, 4)
    # minute 1: light explainer groove
    Mu.pad(mus, B("minute"), E("minute"), ["F", "C", "Dm", "Bb"], "string_ensemble_1", 0.22, 4)
    Mu.arp(mus, B("minute") + 1.5, E("minute"), ["F", "C", "Dm", "Bb"], "pizzicato_strings", 104, 0.35)
    Mu.arp(mus, T("minute", "fire"), E("minute"), ["F", "C"], "marimba", 104, 0.2, 1)
    # hour 1: wonder
    Mu.pad(mus, B("hour1"), E("hour1"), ["F", "Dm", "Bb", "C"], "choir_aahs", 0.3, 4)
    Mu.pad(mus, B("hour1"), E("hour1"), ["F", "Dm", "Bb", "C"], "string_ensemble_1", 0.25, 4)
    Mu.arp(mus, B("hour1"), T("hour1", "dinosaurs"), ["F", "Dm", "Bb", "C"], "orchestral_harp", 80, 0.3)
    Mu.arp(mus, T("hour1", "dinosaurs"), E("hour1"), ["F", "C"], "pizzicato_strings", 104, 0.3)
    # hour 3: tension
    Mu.pulse(mus, B("hour3"), T("hour3", "so", 1), "D2", "contrabass", 100, 0.5)
    Mu.pad(mus, B("hour3"), E("hour3"), ["Dm", "Bb", "Gm", "A"], "string_ensemble_1", 0.22, 4)
    Mu.arp(mus, T("hour3", "so", 1), E("hour3"), ["Dm", "Bb", "Gm", "A"], "marimba", 100, 0.28)
    for k in range(4):
        mus.add(B("hour3") + k * 4.8, Mu.note("timpani", "D2", 1.5, 0.6), 0.4)
    # night 1: hard silence before, then drone + cello + accelerating heartbeat
    Mu.pad(mus, B("night") + 0.6, E("night"), ["Dm", "Dm", "Gm", "A"], "cello", 0.45, 4)
    Mu.pad(mus, B("night") + 0.6, E("night"), ["Dm"], "contrabass", 0.4, 6)
    Mu.pulse(mus, T("night", "fire"), E("night"), "D2", "timpani", 90, 0.35, accel=0.6)
    hb = T("night", "fire"); k = 0
    while hb < E("night"):
        fx.add(hb, X.heartbeat(), 0.4); hb += max(0.45, 0.9 - k * 0.03); k += 1
    # year 1: cold
    Mu.pad(mus, B("year"), E("year"), ["Dm", "Bb", "F", "C"], "synth_strings_1", 0.28, 4)
    Mu.arp(mus, B("year") + 2, E("year"), ["Dm", "Bb", "F", "C"], "celesta", 70, 0.25, 1)
    # twist: hopeful build
    Mu.pad(mus, B("twist"), E("twist"), ["Bb", "F", "C", "Dm"], "string_ensemble_1", 0.3, 4)
    Mu.arp(mus, B("twist"), E("twist"), ["Bb", "F", "C", "Dm"], "orchestral_harp", 96, 0.3)
    for n in ["F3", "C4", "F4", "A4"]:
        mus.add(T("twist", "either"), Mu.note("french_horn", n, 4.0, 0.5), 0.35)
    # payoff: soft piano + motif callback
    Mu.pad(mus, B("payoff"), T("payoff", "next"), ["F", "C", "Dm", "Bb"], "pad_2_warm", 0.25, 4)
    t = B("payoff") + 1.0
    while t < T("payoff", "next") - 1:
        for k, n in enumerate(Mu.CH[["F", "C", "Dm", "Bb"][int((t - B("payoff")) / 4) % 4]][1:]):
            mus.add(t + k * 0.5, Mu.note("acoustic_grand_piano", n, 1.5, 0.5), 0.45)
        t += 2.0
    Mu.motif(mus, T("payoff", "wake"), "acoustic_grand_piano", 0.6, 0.6)
    for n in ["D2", "A2"]:                                            # ominous rumble on the tease
        mus.add(T("payoff", "next"), Mu.note("contrabass", n, 4.0, 0.7), 0.6)
    Mu.motif(mus, endt + 0.3, "celesta", 0.4, 0.3, ["D6", "F6", "A6", "G6"])
    # hard silence before Night 1: cut the music bed 1.3 s before the card
    a, b = int((B("night") - 1.5) * SR), int((B("night") + 0.5) * SR)
    for tr in (mus, amb):
        tr.buf[a:b] *= np.concatenate([np.linspace(1, 0, int(0.15 * SR)), np.zeros(b - a - int(0.15 * SR))])
    return mus.buf, fx.buf, amb.buf


def SECTIONS(total):
    return [(0, E("hook"), -31), (E("hook"), E("hook") + 3.5, -24), (E("hook") + 3.5, B("minute"), -31),
            (B("minute"), B("night") - 1.5, -31), (B("night") - 1.5, B("night") + 0.3, None),
            (B("night") + 0.3, E("night"), -28), (E("night"), B("payoff"), -31), (B("payoff"), E("payoff"), -32),
            (E("payoff"), total, -25)]
