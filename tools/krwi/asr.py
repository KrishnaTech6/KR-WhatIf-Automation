"""Transcribe a voice file (sherpa-onnx parakeet, word timestamps) and align it to the voice script.
main  -> video/anchors.json        (beat spans + word times; timeline.py switches to real mode)
short -> video/anchors_short.json  (script words as written + heard start times; used by vertical.py)
"""
import difflib
import json
import os

import numpy as np
import soundfile as sf

from . import ctx
from .assets import asr_dir
from .script import Beats, norm, vertical_lines


def transcribe(path):
    import sherpa_onnx
    A = asr_dir()
    rec = sherpa_onnx.OfflineRecognizer.from_transducer(
        encoder=f"{A}/encoder.int8.onnx", decoder=f"{A}/decoder.int8.onnx", joiner=f"{A}/joiner.int8.onnx",
        tokens=f"{A}/tokens.txt", model_type="nemo_transducer", num_threads=4)
    x, sr = sf.read(path, dtype="float32")
    if x.ndim > 1:
        x = x.mean(1)
    if sr != 16000:
        import scipy.signal as ss
        x = ss.resample_poly(x, 16000, sr).astype(np.float32); sr = 16000
    hop = int(0.01 * sr)
    e = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2)) for i in range(0, len(x) - hop, hop)])
    cuts, pos = [0], 0
    while pos + 25 * sr < len(x):                      # ~25 s chunks, cut at the quietest 10 ms
        lo, hi = (pos + 20 * sr) // hop, min(len(e), (pos + 28 * sr) // hop)
        k = lo + int(np.argmin(e[lo:hi])); pos = k * hop; cuts.append(pos)
    cuts.append(len(x))
    words = []
    for a, b in zip(cuts, cuts[1:]):
        s = rec.create_stream(); s.accept_waveform(sr, x[a:b]); rec.decode_stream(s)
        r, cur = s.result, None
        for tok, ts in zip(r.tokens, r.timestamps):
            if tok.startswith(" ") or cur is None:
                if cur:
                    words.append(cur)
                cur = [a / sr + ts, tok.strip()]
            else:
                cur[1] += tok
        if cur:
            words.append(cur)
    return words, len(x) / sr


def _match(script_words, words, step):
    """difflib-align normalized script words to heard words; interpolate the unmatched ones."""
    heard = [norm(w) for _, w in words]
    sm = difflib.SequenceMatcher(None, script_words, heard, autojunk=False)
    times = [None] * len(script_words)
    for blk in sm.get_matching_blocks():
        for i in range(blk.size):
            times[blk.a + i] = words[blk.b + i][0]
    idx = [i for i, t in enumerate(times) if t is not None]
    for i in range(len(times)):
        if times[i] is None:
            p = max([j for j in idx if j < i], default=None); n = min([j for j in idx if j > i], default=None)
            if p is None:
                times[i] = times[n] - step * (n - i)
            elif n is None:
                times[i] = times[p] + step * (i - p)
            else:
                times[i] = times[p] + (times[n] - times[p]) * (i - p) / (n - p)
    return times, len(idx) / max(1, len(script_words))


def align_main(words, total):
    bt = Beats("full")
    script = [(k, norm(tok)) for k, toks in zip(bt.keys, bt.toks()) for tok in toks if tok != "(beat)" and norm(tok)]
    times, match = _match([w for _, w in script], words, 0.4)
    W, S = {}, {}
    for (k, w), t in zip(script, times):
        W.setdefault(k, []).append((w, round(t, 3)))
    for k in bt.keys:
        S[k] = (W[k][0][1], W[k][-1][1] + 0.45)
    return {"words": W, "spans": S, "total": total, "match": round(match, 4)}


def align_vertical(job, words, total):
    toks = [t for l in vertical_lines(job) for t in l.split() if t != "(beat)"]
    times, match = _match([norm(t) for t in toks], words, 0.35)
    return {"words": [[round(t, 3), w] for t, w in zip(times, toks)], "total": total, "match": round(match, 3)}


def run(job):
    wav = ctx.voice_wav(job)
    words, total = transcribe(wav)
    json.dump({"words": words}, open(os.path.join(ctx.VIDEO, f"transcript_{job}.json"), "w"))
    if job == "main":
        d = align_main(words, total)
        json.dump(d, open(os.path.join(ctx.VIDEO, "anchors.json"), "w"))
        for k, sp in d["spans"].items():
            print(f"  {k:12s} {sp[0]:7.2f} - {sp[1]:7.2f}")
    else:
        d = align_vertical(job, words, total)
        json.dump(d, open(os.path.join(ctx.VIDEO, f"anchors_{job}.json"), "w"))
    print(f"{job}: {os.path.basename(wav)}  words {len(words)}  match {d['match']:.1%}  total {total:.1f} s")
    return d
