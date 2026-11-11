"""Transcribe final/main.wav (sherpa-onnx parakeet) and align words to the voice-script beats -> anchors.json."""
import json, os, re, sys, difflib
import numpy as np, soundfile as sf
from timeline import BEAT_KEYS, norm, _parse, RUN, HERE

ASR = "/tmp/claude-0/-home-user-KR-WhatIf-Automation/78e4e397-8cb2-57f1-8382-3ff9493a7fb3/scratchpad/asr/sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8"


def transcribe(path):
    import sherpa_onnx
    rec = sherpa_onnx.OfflineRecognizer.from_transducer(
        encoder=f"{ASR}/encoder.int8.onnx", decoder=f"{ASR}/decoder.int8.onnx", joiner=f"{ASR}/joiner.int8.onnx",
        tokens=f"{ASR}/tokens.txt", model_type="nemo_transducer", num_threads=4)
    x, sr = sf.read(path, dtype="float32")
    if x.ndim > 1: x = x.mean(1)
    if sr != 16000:
        import scipy.signal as ss
        x = ss.resample_poly(x, 16000, sr).astype(np.float32); sr = 16000
    # split at quiet points ~25 s
    hop = int(0.01 * sr); e = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2)) for i in range(0, len(x) - hop, hop)])
    cuts = [0]; pos = 0
    while pos + 25 * sr < len(x):
        lo, hi = (pos + 20 * sr) // hop, min(len(e), (pos + 28 * sr) // hop)
        k = lo + int(np.argmin(e[lo:hi])); pos = k * hop; cuts.append(pos)
    cuts.append(len(x))
    words = []
    for a, b in zip(cuts, cuts[1:]):
        s = rec.create_stream(); s.accept_waveform(sr, x[a:b]); rec.decode_stream(s)
        r = s.result; cur = None
        for tok, ts in zip(r.tokens, r.timestamps):
            if tok.startswith(" ") or cur is None:
                if cur: words.append(cur)
                cur = [a / sr + ts, tok.strip()]
            else:
                cur[1] += tok
        if cur: words.append(cur)
    return words, len(x) / sr


def align(words, total):
    beats = _parse(os.path.join(RUN, "script", "voice-full.txt"))
    script = []
    for k, toks in zip(BEAT_KEYS, beats):
        for tok in toks:
            if tok != "(beat)" and norm(tok):
                script.append((k, norm(tok)))
    heard = [norm(w) for _, w in words]
    sm = difflib.SequenceMatcher(None, [w for _, w in script], heard, autojunk=False)
    times = [None] * len(script)
    for blk in sm.get_matching_blocks():
        for i in range(blk.size):
            times[blk.a + i] = words[blk.b + i][0]
    # interpolate unmatched
    idx = [i for i, t in enumerate(times) if t is not None]
    for i in range(len(times)):
        if times[i] is None:
            prev = max([j for j in idx if j < i], default=None); nxt = min([j for j in idx if j > i], default=None)
            if prev is None: times[i] = times[nxt] - 0.4 * (nxt - i)
            elif nxt is None: times[i] = times[prev] + 0.4 * (i - prev)
            else: times[i] = times[prev] + (times[nxt] - times[prev]) * (i - prev) / (nxt - prev)
    W, S = {}, {}
    for (k, w), t in zip(script, times):
        W.setdefault(k, []).append((w, round(t, 3)))
    for k in BEAT_KEYS:
        S[k] = (W[k][0][1], W[k][-1][1] + 0.45)
    match = sum(1 for t in [None] if t) or len(idx) / len(script)
    return {"words": W, "spans": S, "total": total, "match": round(match, 4)}


if __name__ == "__main__":
    wav = sys.argv[1]
    words, total = transcribe(wav)
    json.dump({"words": words}, open(os.path.join(HERE, "transcript.json"), "w"))
    d = align(words, total)
    json.dump(d, open(os.path.join(HERE, "anchors.json"), "w"))
    print("words", len(words), "match", d["match"], "total", round(total, 1))
    for k in BEAT_KEYS: print(k, d["spans"][k])


def vertical(job):
    """anchors_<job>.json: script words (as written) with heard start times."""
    import vertical as V
    wav = os.path.join(RUN, "audio", "final", f"{job}_edit.wav")
    if not os.path.exists(wav):
        wav = os.path.join(RUN, "audio", "final", f"{job}.wav")
    words, total = transcribe(wav)
    toks = [t for l in V.parse_lines(job) for t in l.split() if t != "(beat)"]
    heard = [norm(w) for _, w in words]
    sm = difflib.SequenceMatcher(None, [norm(t) for t in toks], heard, autojunk=False)
    times = [None] * len(toks)
    for b in sm.get_matching_blocks():
        for i in range(b.size):
            times[b.a + i] = words[b.b + i][0]
    idx = [i for i, t in enumerate(times) if t is not None]
    for i in range(len(times)):
        if times[i] is None:
            p = max([j for j in idx if j < i], default=None); n = min([j for j in idx if j > i], default=None)
            times[i] = (times[n] - 0.35 * (n - i)) if p is None else (times[p] + 0.35 * (i - p)) if n is None else times[p] + (times[n] - times[p]) * (i - p) / (n - p)
    out = {"words": [[round(t, 3), w] for t, w in zip(times, toks)], "total": total, "match": round(len(idx) / len(toks), 3)}
    json.dump(out, open(os.path.join(HERE, f"anchors_{job}.json"), "w"))
    return out
