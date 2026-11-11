"""Voice processing + music/sfx/ambience levelling, ducking, -14 LUFS master."""
import numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy.signal import butter, sosfilt, fftconvolve
from .sfx import SR

meter = pyln.Meter(SR)


def db(x): return 10 ** (x / 20)


def peq(x, f, gain_db, q=1.0):
    from scipy.signal import iirpeak
    b, a = iirpeak(f, q, fs=SR)
    from scipy.signal import lfilter
    return x + (db(gain_db) - 1) * lfilter(b, a, x)


def voice_chain(v):
    v = sosfilt(butter(2, 80, 'high', fs=SR, output='sos'), v)
    v = peq(v, 250, -2, 1.0); v = peq(v, 3200, 2.5, 1.2); v = peq(v, 120, 1.5, 1.0)
    # de-ess: compress 5.5-9 kHz band
    s = sosfilt(butter(2, [5500, 9000], 'band', fs=SR, output='sos'), v)
    env = np.convolve(np.abs(s), np.ones(480) / 480, 'same')
    g = np.minimum(1, 0.05 / np.maximum(env, 1e-6)) ** 0.5
    v = v - s + s * g
    # gentle compression
    env = np.convolve(np.abs(v), np.ones(960) / 960, 'same')
    thr = np.percentile(env, 90) * 0.7
    gain = np.where(env > thr, (thr / np.maximum(env, 1e-9)) ** 0.4, 1.0)
    v = v * gain
    return v * db(-16 - meter.integrated_loudness(v))


def reverb(x, sec=3.0, wet=0.18):
    n = int(sec * SR); t = np.arange(n) / SR
    ir = np.random.default_rng(1).standard_normal(n) * np.exp(-t * 6.9 / sec)
    ir /= np.sqrt(np.sum(ir ** 2))
    return x * (1 - wet) + fftconvolve(x, ir)[:len(x)] * wet


def level_sections(m, sections, voice_env):
    """sections: [(t0, t1, target_lufs_or_None)]; per-section gain to target, smoothed."""
    g = np.ones(len(m))
    for a, b, tgt in sections:
        i, j = int(a * SR), min(len(m), int(b * SR))
        if j - i < SR // 2:
            continue
        seg = m[i:j]
        if tgt is None:
            g[i:j] = 0; continue
        try:
            L = meter.integrated_loudness(seg) if j - i > SR * 0.5 else -70
        except Exception:
            L = -70
        if L > -70:
            g[i:j] = db(tgt - L)
    k = int(0.6 * SR)
    g = np.convolve(g, np.ones(k) / k, 'same')
    return m * g


def duck(m, v, depth_db=6.0):
    env = np.convolve(np.abs(v), np.ones(int(0.05 * SR)) / int(0.05 * SR), 'same')
    on = (env > np.percentile(env, 60) * 0.3).astype(float)
    k = int(0.25 * SR); on = np.convolve(on, np.ones(k) / k, 'same')
    g = 1 - (1 - db(-depth_db)) * on
    # carve 0.9-4 kHz while talking
    band = sosfilt(butter(2, [900, 4000], 'band', fs=SR, output='sos'), m)
    return m * g - band * on * 0.4


def limiter(x, ceil_db=-1.2):
    c = db(ceil_db)
    env = np.maximum.accumulate(np.abs(x)[::-1])[::-1]  # placeholder not used
    peak = np.abs(x)
    k = int(0.005 * SR)
    pk = np.convolve(peak, np.ones(k), 'same') / k * 0 + peak
    g = np.minimum(1, c / np.maximum(pk, 1e-9))
    rel = int(0.08 * SR)
    g = np.minimum.accumulate(g) if False else g
    # smooth gain (fast attack, slow release)
    out = np.empty_like(g); cur = 1.0; a = np.exp(-1 / rel)
    for i in range(len(g)):
        cur = g[i] if g[i] < cur else a * cur + (1 - a) * g[i]
        out[i] = cur
    return x * out


def master(voice, mus, fx, amb, sections, total, fade=1.8):
    n = int(total * SR)
    def fit(x):
        y = np.zeros(n); y[:min(n, len(x))] = x[:n]; return y
    v, m, f, a = fit(voice), fit(mus), fit(fx), fit(amb)
    m = reverb(m, 3.0, 0.22)
    m = level_sections(m, sections, v)
    m = duck(m, v, 6.0)
    f = f * db(-27 - meter.integrated_loudness(f + 1e-9)) if np.any(f) else f
    a = a * db(-32 - meter.integrated_loudness(a + 1e-9)) if np.any(a) else a
    mix = v + m + f + a
    mix *= db(-14 - meter.integrated_loudness(mix))
    # simple soft-knee limiter via vectorised envelope (chunked for speed)
    c = db(-1.2)
    pk = np.abs(mix)
    k = int(0.004 * SR)
    from scipy.ndimage import maximum_filter1d
    pk = maximum_filter1d(pk, k)
    g = np.minimum(1, c / np.maximum(pk, 1e-9))
    g = np.convolve(g, np.ones(int(0.02 * SR)) / int(0.02 * SR), 'same')
    g = np.minimum(g, np.minimum(1, c / np.maximum(pk, 1e-9)) + 0.0)
    mix = mix * g
    c2 = db(-2.0)                                   # final soft ceiling (AAC adds ~1 dB of overs)
    from scipy.signal import resample_poly           # true-peak control: soften and lowpass the hot spots
    mix = sosfilt(butter(4, 16000, 'low', fs=SR, output='sos'), mix)
    for _ in range(3):
        tp = np.abs(resample_poly(mix, 4, 1))
        tpk = maximum_filter1d(tp.reshape(-1, 4).max(1)[:len(mix)], int(0.01 * SR))
        g2 = np.minimum(1, db(-2.2) / np.maximum(tpk, 1e-9))
        g2 = np.convolve(g2, np.ones(int(0.01 * SR)) / int(0.01 * SR), 'same')
        mix = mix * np.minimum(g2, 1)
    mix = np.where(np.abs(mix) > c2 * 0.7, np.sign(mix) * (c2 * 0.7 + c2 * 0.3 * np.tanh((np.abs(mix) - c2 * 0.7) / (c2 * 0.3))), mix)
    fl = int(fade * SR); mix[-fl:] *= np.linspace(1, 0, fl)
    return mix.astype(np.float32), dict(v=v, m=m, f=f, a=a)
