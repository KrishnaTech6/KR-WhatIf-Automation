"""Sampled orchestra (FluidR3_GM, MIT licence) for the channel score: notes, chords, pads, arps, pulses, the D-F-A-G motif.
Samples download once into the cache (assets.soundfont)."""
import numpy as np
from .sfx import SR, lp
from .assets import soundfont
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
_cache = {}
SUSTAIN = {"string_ensemble_1", "choir_aahs", "pad_2_warm", "cello", "contrabass", "french_horn", "synth_strings_1"}


def sample(inst, midi):
    if inst not in _cache:
        _cache[inst] = dict(np.load(soundfont(inst)))
    name = NAMES[midi % 12] + str(midi // 12 - 1)
    return _cache[inst][name].astype(np.float64)


def M(n):
    """'D4' -> midi"""
    for i, nm in sorted(enumerate(NAMES), key=lambda x: -len(x[1])):
        if n.startswith(nm):
            return 12 * (int(n[len(nm):]) + 1) + i
    raise ValueError(n)


def note(inst, n, dur, vel=0.7):
    x = sample(inst, M(n) if isinstance(n, str) else n)
    L = int(dur * SR)
    if inst in SUSTAIN and L > len(x) - int(0.4 * SR):
        a, b, xf = int(0.7 * SR), int(2.7 * SR), int(0.3 * SR)
        body = x[a:b]
        out = list(x[:b])
        out = np.array(out)
        while len(out) < L + int(0.5 * SR):
            fade = np.linspace(0, 1, xf)
            seg = body.copy()
            out[-xf:] = out[-xf:] * (1 - fade) + seg[:xf] * fade
            out = np.concatenate([out, seg[xf:]])
        x = out
    x = x[:L + int(0.6 * SR)].copy()
    r = int(0.5 * SR)
    if len(x) > L:
        tail = x[L:]; tail *= np.linspace(1, 0, len(tail)) ** 2; x[L:] = tail
    # attack smoothing for pads
    if inst in SUSTAIN:
        a = min(len(x), int(0.25 * SR)); x[:a] *= np.linspace(0, 1, a)
    return x * vel


class Track:
    def __init__(self, total):
        self.buf = np.zeros(int((total + 6) * SR))

    def add(self, t, x, g=1.0):
        i = int(t * SR)
        if i < 0 or i >= len(self.buf):
            return
        n = min(len(x), len(self.buf) - i)
        self.buf[i:i + n] += x[:n] * g


CH = {  # chords (D minor / F major family)
    "Dm": ["D3", "A3", "D4", "F4"], "Bb": ["Bb2", "F3", "Bb3", "D4"], "F": ["F3", "C4", "F4", "A4"],
    "C": ["C3", "G3", "C4", "E4"], "Gm": ["G2", "D3", "G3", "Bb3"], "A": ["A2", "E3", "A3", "Db4"],
}
MOTIF = ["D5", "F5", "A5", "G5"]


def pad(tr, t0, t1, prog, inst="string_ensemble_1", g=0.5, bar=4.0):
    t = t0; i = 0
    while t < t1:
        d = min(bar, t1 - t)
        for n in CH[prog[i % len(prog)]]:
            tr.add(t, note(inst, n, d + 0.3, 0.5), g)
        t += bar; i += 1


def arp(tr, t0, t1, prog, inst="pizzicato_strings", bpm=104, g=0.5, octave=0):
    step = 60 / bpm / 2; t = t0; k = 0
    while t < t1:
        ch = CH[prog[int((t - t0) / (step * 16)) % len(prog)]]
        n = ch[[1, 2, 3, 2][k % 4]]
        m = M(n) + 12 * octave
        tr.add(t, note(inst, m, step * 1.5, 0.6 if k % 4 == 0 else 0.45), g)
        t += step; k += 1


def pulse(tr, t0, t1, n="D2", inst="contrabass", bpm=100, g=0.6, accel=0.0):
    t = t0
    while t < t1:
        step = 60 / (bpm * (1 + accel * (t - t0) / max(1, t1 - t0))) / 2
        tr.add(t, note(inst, n, step * 0.9, 0.6), g)
        t += step


def motif(tr, t0, inst="music_box", g=0.6, step=0.55, notes=MOTIF):
    for i, n in enumerate(notes):
        tr.add(t0 + i * step, note(inst, n, step * 1.6, 0.7), g)
