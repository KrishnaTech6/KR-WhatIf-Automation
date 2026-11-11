"""Synthesized SFX + ambience (numpy). 48 kHz mono float32. Deterministic."""
import numpy as np
SR = 48000
_rng = np.random.default_rng(7)


def t_(d):
    return np.arange(int(d * SR)) / SR


def env(n, a=0.005, r=0.2, shape=4.0):
    e = np.ones(n)
    na = max(1, int(a * SR)); e[:na] = np.linspace(0, 1, na)
    tt = np.arange(n) / SR
    e *= np.exp(-tt * shape / max(r, 1e-3))
    return e


def noise(d, seed=0):
    return np.random.default_rng(seed).standard_normal(int(d * SR))


def lp(x, fc):
    from scipy.signal import butter, sosfilt
    return sosfilt(butter(2, fc, 'low', fs=SR, output='sos'), x)


def hp(x, fc):
    from scipy.signal import butter, sosfilt
    return sosfilt(butter(2, fc, 'high', fs=SR, output='sos'), x)


def bp(x, lo, hi):
    from scipy.signal import butter, sosfilt
    return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)


def norm(x, peak=0.9):
    m = np.max(np.abs(x)) or 1
    return (x / m * peak).astype(np.float32)


def pop(pitch=900):
    tt = t_(0.12); f = pitch * (1 + 2 * np.exp(-tt * 60))
    return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(tt), 0.002, 0.05), 0.6)


def tick():
    return norm(bp(noise(0.03, 1), 2000, 6000) * env(int(0.03 * SR), 0.001, 0.01), 0.5)


def whoosh(d=0.6, seed=2):
    n = noise(d, seed); tt = t_(d)
    sweep = np.sin(np.pi * tt / d) ** 2
    out = np.zeros_like(n)
    for k, fc in enumerate(np.linspace(400, 3000, 8)):
        seg = slice(int(k * len(n) / 8), int((k + 1) * len(n) / 8))
        out[seg] = bp(n, fc * 0.6, fc * 1.4)[seg]
    return norm(out * sweep, 0.5)


def riser(d=2.0, seed=3):
    tt = t_(d)
    n = hp(noise(d, seed), 800) * (tt / d) ** 2
    f = 120 + 900 * (tt / d) ** 2
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * (tt / d) ** 3 * 0.4
    return norm(n * 0.6 + tone, 0.6)


def impact(seed=4, big=1.0):
    d = 2.5; tt = t_(d)
    sub = np.sin(2 * np.pi * (45 + 60 * np.exp(-tt * 18)) * tt) * np.exp(-tt * 2.2)
    crack = hp(noise(d, seed), 1500) * np.exp(-tt * 30)
    tail = lp(noise(d, seed + 1), 400) * np.exp(-tt * 1.6) * 0.5
    return norm(sub * big + crack * 0.5 + tail, 0.95)


def thunder(seed=5):
    d = 4.0; tt = t_(d)
    crack = hp(noise(d, seed), 1200) * np.exp(-tt * 12)
    roll = lp(noise(d, seed + 1), 200) * (np.exp(-tt * 0.9) * (1 + 0.6 * np.sin(tt * 9)))
    return norm(crack * 0.7 + roll * 1.4, 0.95)


def match_flare():
    d = 1.2; tt = t_(d)
    scratch = bp(noise(0.15, 6), 1500, 7000) * env(int(0.15 * SR), 0.001, 0.08)
    roar = lp(noise(d, 7), 900) * np.minimum(1, tt * 8) * np.exp(-tt * 1.5)
    out = roar.copy(); out[:len(scratch)] += scratch * 1.5
    return norm(out, 0.8)


def heartbeat():
    d = 0.9; tt = t_(d); out = np.zeros(len(tt))
    for off, a in ((0.0, 1.0), (0.22, 0.7)):
        i = int(off * SR); seg = tt[: len(tt) - i]
        out[i:] += a * np.sin(2 * np.pi * 50 * seg) * np.exp(-seg * 22)
    return norm(out, 0.9)


def buzz(d=1.5, seed=8):
    tt = t_(d)
    f = 70 + 8 * np.sin(tt * 30)
    saw = 2 * ((np.cumsum(f) / SR) % 1) - 1
    return norm(bp(saw, 100, 1800) * np.sin(np.pi * tt / d), 0.5)


def skitter(d=1.5, seed=9):
    out = np.zeros(int(d * SR))
    r = np.random.default_rng(seed)
    for k in range(int(d * 28)):
        i = int(r.uniform(0, d - 0.03) * SR)
        out[i:i + int(0.02 * SR)] += bp(noise(0.02, k + seed), 2500, 7000) * np.hanning(int(0.02 * SR)) * r.uniform(0.3, 1)
    return norm(out, 0.5)


def stamp_hit():
    tt = t_(0.4)
    return norm(lp(noise(0.4, 10), 600) * np.exp(-tt * 18) + np.sin(2 * np.pi * 90 * tt) * np.exp(-tt * 14), 0.8)


def click():
    tt = t_(0.05)
    return norm(hp(noise(0.05, 11), 1000) * np.exp(-tt * 120) + np.sin(2 * np.pi * 1800 * tt) * np.exp(-tt * 90) * 0.4, 0.6)


def chime(f=1320):
    tt = t_(1.5)
    return norm(sum(np.sin(2 * np.pi * f * k * tt) * np.exp(-tt * (3 + k)) / k for k in (1, 2, 3)), 0.5)


def glitch():
    tt = t_(0.35)
    sq = np.sign(np.sin(2 * np.pi * (300 + 900 * (tt * 7 % 1)) * tt))
    return norm(sq * (np.sin(tt * 90) > 0) * np.exp(-tt * 6), 0.4)


# ---------------------------------------------------------------- ambience beds (looped, long)
def amb_swamp(d):
    tt = t_(d)
    hum = sum(np.sin(2 * np.pi * f * tt + k) for k, f in enumerate((220, 233, 247))) * 0.05 * (1 + 0.3 * np.sin(tt * 0.7))
    air = lp(noise(d, 20), 500) * 0.25
    out = hum + air
    r = np.random.default_rng(21)
    for k in range(int(d / 1.3)):                # water drips
        i = int(r.uniform(0, d - 0.2) * SR); seg = t_(0.15)
        out[i:i + len(seg)] += np.sin(2 * np.pi * r.uniform(900, 1600) * seg * (1 + seg * 3)) * np.exp(-seg * 40) * 0.25
    return norm(out, 0.5)


def amb_rain(d):
    return norm(hp(noise(d, 22), 1500) * 0.6 + lp(noise(d, 23), 300) * 0.4, 0.5)


def amb_fire(d):
    tt = t_(d)
    roar = lp(noise(d, 24), 600) * (1 + 0.3 * np.sin(tt * 1.3))
    out = roar * 0.6
    r = np.random.default_rng(25)
    for k in range(int(d * 12)):
        i = int(r.uniform(0, d - 0.02) * SR)
        out[i:i + int(0.01 * SR)] += hp(noise(0.01, k), 2000) * r.uniform(0.3, 1.0)
    return norm(out, 0.5)


def amb_wind(d):
    tt = t_(d)
    return norm(bp(noise(d, 26), 200, 900) * (0.6 + 0.4 * np.sin(tt * 0.4)), 0.5)


def amb_room(d):
    tt = t_(d)
    return norm(lp(noise(d, 27), 250) * 0.4 + np.sin(2 * np.pi * 100 * tt) * 0.03, 0.3)
