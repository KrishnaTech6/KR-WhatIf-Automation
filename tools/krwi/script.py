"""Read the voice scripts (voice-full.txt, voice-short.txt, voice-reel.txt).

Beat keys: what T("key", "word") uses to name a beat.
- If video/run.json has {"beats": [...]}, those keys are used (one per beat, in order).
- Otherwise a beat's key is its name before " - ", lowercased, spaces -> "_" ("Night one - the fire" -> "night_one").
Every word of a beat name that appears in only one beat name also works as an alias ("fire", "night").
HARD_CUT_BEFORE / KEY_BEATS words are resolved the same way.
"""
import json
import os
import re

from . import ctx

STOP = {"the", "a", "an", "of", "and", "to", "in", "on", "is", "it", "your", "you", "what", "if", "why", "how"}


def norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def read(job="full"):
    """-> (headers dict, beats list of {name, mood, lines})."""
    txt = open(os.path.join(ctx.SCRIPT, f"voice-{job}.txt")).read()
    head, body = txt.split("\n\n", 1)
    headers = {}
    for l in head.splitlines():
        if ":" in l:
            k, v = l.split(":", 1)
            headers[k.strip().upper()] = v.strip()
    beats = []
    for b in re.split(r"\n(?=\[)", body.strip()):
        first, *lines = b.splitlines()
        m = re.match(r"\[(.+?)(?:\|\s*(\w+))?\s*\]", first.strip())
        beats.append({"name": m.group(1).strip(), "mood": (m.group(2) or "neutral").lower(),
                      "lines": [l for l in lines if l.strip()]})
    return headers, beats


def tokens(beat):
    """Spoken tokens of a beat, with "(beat)" kept as a 1 s pause marker; mood tags and (pause x) removed."""
    toks = []
    for l in beat["lines"]:
        l = re.sub(r"\{\w+\}", "", l)
        l = re.sub(r"\(pause\s+[\d.]+\)", "", l)
        toks += re.findall(r"\(beat\)|[^\s]+", l)
    return toks


def _auto_key(name):
    return re.sub(r"[^a-z0-9]+", "_", name.split(" - ")[0].lower()).strip("_")


class Beats:
    def __init__(self, job="full"):
        self.headers, self.beats = read(job)
        cfg = os.path.join(ctx.VIDEO, "run.json")
        keys = json.load(open(cfg)).get("beats") if os.path.exists(cfg) else None
        if keys and len(keys) != len(self.beats):
            raise ValueError(f"run.json has {len(keys)} beat keys, voice-{job}.txt has {len(self.beats)} beats")
        self.keys = keys or [_auto_key(b["name"]) for b in self.beats]
        self.alias = {k: k for k in self.keys}
        seen = {}
        for k, b in zip(self.keys, self.beats):
            for w in set(re.findall(r"[a-z0-9]+", b["name"].lower())) - STOP:
                seen.setdefault(w, set()).add(k)
        for w, ks in seen.items():
            if len(ks) == 1 and w not in self.alias:
                self.alias[w] = next(iter(ks))
        hc = self.headers.get("HARD_CUT_BEFORE", "").split(",")[0].strip().lower()
        self.hard_cut = self.alias.get(hc) if hc else None
        self.moods = {k: b["mood"] for k, b in zip(self.keys, self.beats)}

    def key(self, x):
        try:
            return self.alias[x.lower()]
        except KeyError:
            raise KeyError(f"no beat {x!r}; beats are {self.keys}") from None

    def toks(self):
        return [tokens(b) for b in self.beats]


def vertical_lines(job):
    """Spoken lines of a Short/Reel script (no headers, beat lines, mood tags or pause marks)."""
    _, beats = read(job)
    out = []
    for b in beats:
        for l in b["lines"]:
            l = re.sub(r"\{\w+\}|\(pause\s+[\d.]+\)", "", l).strip()
            if l:
                out.append(l)
    return out
