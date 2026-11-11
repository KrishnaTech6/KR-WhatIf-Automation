"""Word anchors for the main video. T(beat, word, n) -> global seconds.

Estimate mode (no audio yet): 150 wpm (0.4 s/word, +0.15 s after . ? ...), (beat) = 1 s,
1.2 s between beats, 2.4 s before the HARD_CUT_BEFORE beat.
Real mode: video/anchors.json (from `wi.py <slug> anchors main`) replaces the estimate; shot code doesn't change.
"""
import json
import os

from . import ctx
from .script import Beats, norm

BEATS = Beats("full")
BEAT_KEYS = BEATS.keys
HARD_CUT = BEATS.hard_cut


def _estimate():
    t, words, spans = 0.0, {}, {}
    for k, toks in zip(BEAT_KEYS, BEATS.toks()):
        if k == HARD_CUT:
            t += 1.2
        t0, lst = t, []
        for tok in toks:
            if tok == "(beat)":
                t += 1.0
                continue
            w = norm(tok)
            if w:
                lst.append((w, t))
            t += 0.4
            if tok.endswith("...") or tok.endswith("?") or tok.endswith("."):
                t += 0.15
        words[k], spans[k] = lst, (t0, t)
        t += 1.2
    return words, spans, t


_real = os.path.join(ctx.VIDEO, "anchors.json")
if os.path.exists(_real):
    _d = json.load(open(_real))
    WORDS = {k: [tuple(x) for x in v] for k, v in _d["words"].items()}
    SPANS = {k: tuple(v) for k, v in _d["spans"].items()}
    TOTAL = _d["total"]
    MODE = "real"
else:
    WORDS, SPANS, TOTAL = _estimate()
    MODE = "estimate"


def T(beat, word, n=1):
    """Start time of the n-th occurrence of `word` inside `beat`."""
    k = BEATS.key(beat)
    w = norm(word)
    hits = [t for x, t in WORDS[k] if x == w]
    if len(hits) < n:
        raise KeyError(f"T({beat!r}, {word!r}, {n}): only {len(hits)} hit(s) in {k}")
    return hits[n - 1]


def at(beat, word, off=0.0, n=1):
    """T() plus an offset: at("hook", "wings", -0.2)."""
    return T(beat, word, n) + off


def B(beat):
    return SPANS[BEATS.key(beat)][0]


def E(beat):
    return SPANS[BEATS.key(beat)][1]


FIRST, LAST = BEAT_KEYS[0], BEAT_KEYS[-1]
