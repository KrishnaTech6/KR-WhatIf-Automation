"""Cap long silences inside a voice file (quietest-frame cuts, 25 ms fades)."""
import numpy as np, soundfile as sf, sys


def cap_silences(x, sr, max_gap=0.7, keep=0.55, thr_db=-45, protect=()):
    hop = int(0.01 * sr)
    e = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2) + 1e-12) for i in range(0, len(x) - hop, hop)])
    quiet = 20 * np.log10(e) < thr_db
    runs, i = [], 0
    while i < len(quiet):
        if quiet[i]:
            j = i
            while j < len(quiet) and quiet[j]: j += 1
            runs.append((i * hop, j * hop)); i = j
        else:
            i += 1
    out, pos, cuts = [], 0, []
    f = int(0.025 * sr)
    for a, b in runs:
        if a == 0 or b >= len(x) - hop:
            continue
        if (b - a) / sr <= max_gap or any(a / sr <= p <= b / sr for p in protect):
            continue
        k = int(keep * sr)
        ca, cb = a + k // 2, b - k // 2
        seg = x[pos:ca].copy(); seg[-f:] *= np.linspace(1, 0, f)
        out.append(seg); pos = cb
        cuts.append((round(ca / sr, 2), round((cb - ca) / sr, 2)))
    tail = x[pos:].copy(); tail[:f] *= np.linspace(0, 1, f); out.append(tail)
    return np.concatenate(out), cuts


if __name__ == "__main__":
    src, dst, mg, kp = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
    x, sr = sf.read(src, dtype="float32")
    if x.ndim > 1: x = x.mean(1)
    y, cuts = cap_silences(x, sr, mg, kp)
    sf.write(dst, y, sr)
    print(round(len(x) / sr, 2), "->", round(len(y) / sr, 2), cuts)
