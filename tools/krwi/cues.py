"""Music, SFX and ambience for the main video, built from the shot list + the voice script's beat moods.

Automatic (no per-video code needed):
  - a soft whoosh on every non-cut transition, riser -> impact into every chapter card
  - logo hit, end-card hit, hard silence before the HARD_CUT_BEFORE beat (no riser into that card)
  - a score in the channel family, chosen per beat from its [Beat | mood] tag (see score())
Per video, video/cues.py may add (all optional):
  HITS()      -> [(time, sound, gain), ...]   sounds from krwi.sfx (pop, click, impact(seed, big), thunder, ...)
  AMB()       -> [(kind, t0, t1, gain), ...]  kind in swamp, rain, fire, wind, room (sfx.amb_<kind>)
  SCORE(mus, fx, amb)                          replace the automatic score
  SECTIONS(total) -> [(t0, t1, target_lufs or None), ...]   music levelling targets for the mix
  BUILD()     -> (mus, fx, amb) arrays         replace everything (old runs)
"""
import numpy as np

from . import ctx, sfx as X, music as Mu
from .sfx import SR
from .timeline import T, B, E, TOTAL, BEAT_KEYS, HARD_CUT, WORDS, BEATS, FIRST, LAST


def bed(amb, kind, a, b, g):
    x = getattr(X, "amb_" + kind)(b - a + 1.0)
    fade = int(0.8 * SR); x[:fade] *= np.linspace(0, 1, fade); x[-fade:] *= np.linspace(1, 0, fade)
    amb.add(a, x, g)


def auto_fx(L, fx):
    hc_start = B(HARD_CUT) if HARD_CUT else None
    for i, (st, fn, tr) in enumerate(L):
        kind = getattr(fn, "kind", None)
        if kind == "card":
            if hc_start is not None and hc_start - 1.0 <= st <= hc_start + 0.2:
                continue                                   # hard silence instead of a riser before the big escalation
            fx.add(st - 1.6, X.riser(1.6, int(st)), 0.35)
            fx.add(st, X.impact(int(st), 0.6), 0.45)
        elif kind == "logo":
            fx.add(st, X.impact(2, 1.0), 0.7)
        elif kind == "end":
            fx.add(st, X.impact(51, 1.0), 0.6)
        elif tr != "cut" and i > 0:
            fx.add(st - 0.15, X.whoosh(0.55, i), 0.35 if tr in ("whip", "zoom") else 0.22)


def _span(i):
    k = BEAT_KEYS[i]
    return B(k), (B(BEAT_KEYS[i + 1]) if i + 1 < len(BEAT_KEYS) else E(k))


def score(mus, fx):
    """Channel score by beat mood (D minor / F major family, 4-note motif D F A G)."""
    for i, k in enumerate(BEAT_KEYS):
        a, b = _span(i)
        mood = BEATS.moods[k]
        if i == 0:                                         # hook: ticking clock + warm pad + music-box motif
            for s in range(int(E(k))):
                fx.add(s * 1.0, X.tick(), 0.25)
            Mu.pad(mus, 0, E(k), ["Dm", "Bb"], "pad_2_warm", 0.35, 4)
            Mu.motif(mus, 0.6, "music_box", 0.55)
            if E(k) > 8:
                Mu.motif(mus, 6.5, "music_box", 0.5)
            hk = E(k)                                      # logo chord + sparkle
            for n in Mu.CH["Dm"]:
                mus.add(hk + 0.1, Mu.note("string_ensemble_1", n, 3.0, 0.6), 0.6)
                mus.add(hk + 0.1, Mu.note("choir_aahs", n, 3.0, 0.5), 0.4)
            Mu.motif(mus, hk + 0.3, "celesta", 0.45, 0.25, ["D6", "F6", "A6", "G6"])
        elif i == 1:                                       # channel promise after the logo
            Mu.pad(mus, a + 2.5, b, ["F", "C"], "pad_2_warm", 0.3, 4)
        elif k == HARD_CUT:                                # biggest escalation: drone + cello + accelerating heartbeat
            Mu.pad(mus, a + 0.6, b, ["Dm", "Dm", "Gm", "A"], "cello", 0.45, 4)
            Mu.pad(mus, a + 0.6, b, ["Dm"], "contrabass", 0.4, 6)
            h0 = a + 0.6 + (b - a) * 0.25
            Mu.pulse(mus, h0, b, "D2", "timpani", 90, 0.35, accel=0.6)
            hb, n = h0, 0
            while hb < b:
                fx.add(hb, X.heartbeat(), 0.4); hb += max(0.45, 0.9 - n * 0.03); n += 1
        elif i == len(BEAT_KEYS) - 1:                      # payoff: soft piano, motif callback, rumble on the tease
            nxt = [t for w, t in WORDS[k] if w == "next"]
            tease = nxt[-1] if nxt else b - 3.0
            Mu.pad(mus, a, tease, ["F", "C", "Dm", "Bb"], "pad_2_warm", 0.25, 4)
            t = a + 1.0
            while t < tease - 1:
                for j, n in enumerate(Mu.CH[["F", "C", "Dm", "Bb"][int((t - a) / 4) % 4]][1:]):
                    mus.add(t + j * 0.5, Mu.note("acoustic_grand_piano", n, 1.5, 0.5), 0.45)
                t += 2.0
            Mu.motif(mus, max(a, tease - 4.0), "acoustic_grand_piano", 0.6, 0.6)
            for n in ["D2", "A2"]:
                mus.add(tease, Mu.note("contrabass", n, 4.0, 0.7), 0.6)
            Mu.motif(mus, b + 0.6, "celesta", 0.4, 0.3, ["D6", "F6", "A6", "G6"])
        elif mood in ("wonder", "excited"):
            Mu.pad(mus, a, b, ["F", "Dm", "Bb", "C"], "choir_aahs", 0.3, 4)
            Mu.pad(mus, a, b, ["F", "Dm", "Bb", "C"], "string_ensemble_1", 0.25, 4)
            Mu.arp(mus, a, b, ["F", "Dm", "Bb", "C"], "orchestral_harp", 80, 0.3)
        elif mood in ("tense", "dramatic", "serious", "mysterious", "deep"):
            Mu.pulse(mus, a, b, "D2", "contrabass", 100, 0.5)
            Mu.pad(mus, a, b, ["Dm", "Bb", "Gm", "A"], "string_ensemble_1", 0.22, 4)
            for j in range(int((b - a) / 4.8)):
                mus.add(a + j * 4.8, Mu.note("timpani", "D2", 1.5, 0.6), 0.4)
        elif mood in ("soft", "sad", "warm", "whispers"):
            Mu.pad(mus, a, b, ["Dm", "Bb", "F", "C"], "synth_strings_1", 0.28, 4)
            Mu.arp(mus, a + 1.0, b, ["Dm", "Bb", "F", "C"], "celesta", 70, 0.25, 1)
        else:                                              # neutral / playful / curious / confident / deadpan
            Mu.pad(mus, a, b, ["F", "C", "Dm", "Bb"], "string_ensemble_1", 0.22, 4)
            Mu.arp(mus, a + 1.5, b, ["F", "C", "Dm", "Bb"], "pizzicato_strings", 104, 0.35)


def hard_silence(*tracks):
    if not HARD_CUT:
        return
    a, b = int((B(HARD_CUT) - 1.5) * SR), int((B(HARD_CUT) + 0.5) * SR)
    env = np.concatenate([np.linspace(1, 0, int(0.15 * SR)), np.zeros(b - a - int(0.15 * SR))])
    for tr in tracks:
        seg = tr.buf[a:b]
        seg *= env[:len(seg)]


def build(L):
    run = ctx.run_module("cues")
    if run and hasattr(run, "BUILD"):
        return run.BUILD()
    tot = TOTAL + 6
    mus, fx, amb = Mu.Track(tot), Mu.Track(tot), Mu.Track(tot)
    auto_fx(L, fx)
    if run and hasattr(run, "SCORE"):
        run.SCORE(mus, fx, amb)
    else:
        score(mus, fx)
    for kind, a, b, g in (run.AMB() if run and hasattr(run, "AMB") else []):
        bed(amb, kind, a, b, g)
    for t, x, g in (run.HITS() if run and hasattr(run, "HITS") else []):
        fx.add(t, x, g)
    hard_silence(mus, amb)
    return mus.buf, fx.buf, amb.buf


def sections(total):
    """Music levelling targets (LUFS, before ducking; voice at -16). None = silence."""
    run = ctx.run_module("cues")
    if run and hasattr(run, "SECTIONS"):
        return run.SECTIONS(total)
    hk, last = E(FIRST), LAST
    out = [(0, hk, -31), (hk, hk + 3.5, -24)]
    if HARD_CUT:
        hc = HARD_CUT
        out += [(hk + 3.5, B(hc) - 1.5, -31), (B(hc) - 1.5, B(hc) + 0.3, None), (B(hc) + 0.3, E(hc), -28), (E(hc), B(last), -31)]
    else:
        out += [(hk + 3.5, B(last), -31)]
    return out + [(B(last), E(last), -32), (E(last), total, -25)]
