"""Word anchors. T(beat, word, n) -> global seconds.
Estimate mode (no audio yet): 150 wpm, (beat)=1 s, 1.2 s between beats, 2.4 s before the hard-cut beat.
Real mode: anchors.json (from the transcript of final/main.wav) replaces the estimate; shot code is unchanged.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.dirname(HERE)
BEAT_KEYS = ["hook", "promise", "minute", "hour1", "hour3", "night", "year", "twist", "payoff"]


def norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def _parse(path):
    body = open(path).read().split("\n\n", 1)[1]
    blocks = re.split(r"\n(?=\[)", body.strip())
    out = []
    for b in blocks:
        lines = b.splitlines()[1:]
        toks = []
        for l in lines:
            l = re.sub(r"\{\w+\}", "", l)
            for tok in re.findall(r"\(beat\)|[^\s]+", l):
                toks.append(tok)
        out.append(toks)
    return out


def _estimate():
    beats = _parse(os.path.join(RUN, "script", "voice-full.txt"))
    t, words, spans = 0.0, {}, {}
    for i, toks in enumerate(beats):
        k = BEAT_KEYS[i]
        if k == "night":
            t += 1.2
        t0 = t
        lst = []
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
        words[k] = lst
        spans[k] = (t0, t)
        t += 1.2
    return words, spans, t


_real = os.path.join(HERE, "anchors.json")
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
    w = norm(word)
    hits = [t for x, t in WORDS[beat] if x == w]
    if len(hits) < n:
        raise KeyError(f"T({beat!r}, {word!r}, {n}): only {len(hits)} hit(s)")
    return hits[n - 1]


def B(beat):
    return SPANS[beat][0]


def E(beat):
    return SPANS[beat][1]


if __name__ == "__main__":
    print(MODE, round(TOTAL, 1))
    for k in BEAT_KEYS:
        print(k, [round(x, 1) for x in SPANS[k]])
