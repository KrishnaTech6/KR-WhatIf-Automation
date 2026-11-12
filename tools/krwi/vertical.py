"""9:16 Short + Reel: reframes the main video's frames, hook text from frame 0, word-by-word captions (current word gold).

Per video, video/vertical_plan.py provides:
  HOOK = {"short": "DON'T MOVE.", "reel": "..."}   frame-0 hook text (<= 6 words)
  SUB  = {"short": "300 MILLION YEARS AGO", ...}    smaller line under it
  FIX  = {"three": "300", "hundred": ""}            caption display fixes (word -> shown text, "" hides it)
  CAPTIONS = "standard"                             or "bold" (Style 2: Anton, white + yellow, black outline, pop)
                                                    use "bold" only sometimes, never on every Reel (Krishna, Nov 2026)
  def plan_short(vt): return [scene(0.0, main_time, cx, zoom, rate), scene(vt.T("its"), ...), ...]
  def plan_reel(vt):  ...
  AUDIO(job, vt, total, mus, fx)                    optional: replace the default vertical score
scene(start, main_t, cx=960, zoom=1.15, rate=1.0): from `start` (vertical seconds) show the main video from main_t on,
centred on x=cx, zoomed. A plan entry can also be the raw tuple (start, fn(d) -> main time, cx, zoom).
"""
import json
import os
import subprocess
import sys

import numpy as np
import skia
import soundfile as sf

from . import ctx
from .art import font, text, paint, back_out, finish, grain, text_w, span
from .script import norm, vertical_lines

VW, VH = ctx.VW, ctx.VH
FIX = {"k": "", "r's": "KR's"}


def estimate(job):
    t, words = 0.0, []
    for l in vertical_lines(job):
        for tok in l.split():
            if tok == "(beat)":
                t += 1.0; continue
            words.append([t, tok]); t += 60 / 160
            if tok[-1] in ".?":
                t += 0.2
    return words, t + 0.5


class VT:
    """Vertical timing: vt.T("word", n) -> seconds in the Short/Reel."""
    def __init__(self, job):
        self.job = job
        p = os.path.join(ctx.VIDEO, f"anchors_{job}.json")
        if os.path.exists(p):
            d = json.load(open(p)); self.words, self.total, self.mode = d["words"], d["total"], "real"
        else:
            (self.words, self.total), self.mode = estimate(job), "estimate"

    def T(self, w, n=1):
        hits = [t for t, x in self.words if norm(x) == norm(w)]
        if len(hits) < n:
            raise KeyError((self.job, w, n))
        return hits[n - 1]

    def has(self, w):
        return any(norm(x) == norm(w) for _, x in self.words)


def scene(start, main_t, cx=960, zoom=1.15, rate=1.0):
    return (start, lambda d: main_t + d * rate, cx, zoom)


def plan_module():
    P = ctx.run_module("vertical_plan")
    if P is None:
        raise SystemExit("video/vertical_plan.py missing (copy tools/templates/vertical_plan.py)")
    return P


_surf, _main = None, None


def main_shots():
    global _main
    if _main is None:
        import shots as S
        _main = S.SHOTS()
    return _main


_held = [None, None]


def main_frame(tm):
    global _surf
    from .compose import render_frame, frame_key
    key = frame_key(tm, main_shots())
    if key is not None and key == _held[0]:   # collage stop-motion: same drawing as the last frame
        return _held[1]
    if _surf is None:
        _surf = skia.Surface(ctx.W, ctx.H)
    c = _surf.getCanvas(); c.clear(skia.Color(0, 0, 0))
    render_frame(c, tm, main_shots())
    img = _surf.makeImageSnapshot()
    _held[0], _held[1] = key, img
    return img


def reframe(c, img, cx, cy=540, zoom=1.25, top=150):
    """background: same frame, cover-scaled, blurred, darkened; foreground: zoomed crop centred on (cx, cy)."""
    sc = VH / 1080
    c.save(); c.translate(VW / 2, VH / 2); c.scale(sc, sc); c.translate(-cx, -540)
    p = skia.Paint(); p.setImageFilter(skia.ImageFilters.Blur(10, 10))
    c.drawImage(img, 0, 0, skia.SamplingOptions(), p); c.restore()
    c.drawRect(skia.Rect(0, 0, VW, VH), paint("space", 0.55))
    fh, y0 = 1100, top
    k = fh / 1080 * zoom
    c.save(); c.clipRect(skia.Rect(0, y0, VW, y0 + fh))
    c.translate(VW / 2, y0 + fh / 2); c.scale(k, k); c.translate(-cx, -cy)
    c.drawImage(img, 0, 0, skia.SamplingOptions(skia.FilterMode.kLinear))
    c.restore()
    c.drawLine(0, y0 + fh, VW, y0 + fh, paint("gold", 0.25, stroke=3))


def hook_text(c, s, p, y=120, size=78, color="cream"):
    if p <= 0:
        return
    f = font("extrabold", size)
    k = back_out(p)
    c.save(); c.translate(VW / 2, y); c.scale(k, k)
    w = text_w(s, f) + 50
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-w / 2, -size * 0.95, w / 2, size * 0.4), 18, 18), paint("space", 0.75))
    text(c, s, 0, 0, f, paint(color))
    c.restore()


def fix(w, extra):
    base = w.strip(".,?!")
    lw = base.lower()
    m = dict(FIX, **extra)
    return m[lw] if lw in m else base.upper()


def captions(c, vt, t, extra=None, y=1360):
    """word-by-word, groups of 2-3, current word gold, Poppins ExtraBold with dark outline, shrink to fit."""
    ws = vt.words
    groups, cur = [], []
    for i, (wt, w) in enumerate(ws):
        cur.append(i)
        if len(cur) == 3 or w[-1] in ".?!," or (len(cur) == 2 and len(w) > 7):
            groups.append(cur); cur = []
    if cur:
        groups.append(cur)
    g = None
    for gr in groups:
        if ws[gr[0]][0] - 0.05 <= t:
            g = gr
    if g is None or t > ws[g[-1]][0] + 1.2:
        return
    disp = [fix(ws[i][1], extra or {}) for i in g]
    size = 92
    while True:
        f = font("extrabold", size)
        total = sum(text_w(d, f) for d in disp) + 26 * (len(disp) - 1)
        if total <= VW - 120 or size <= 56:
            break
        size -= 4
    x = VW / 2 - total / 2
    for i, d in zip(g, disp):
        on = ws[i][0] <= t
        c.drawString(d, x, y, f, paint("space", 1, stroke=16))
        c.drawString(d, x, y, f, paint("gold" if on and (i == g[-1] or ws[i + 1][0] > t) else "cream"))
        x += text_w(d, f) + 26


def captions_bold(c, vt, t, extra=None, y=1330):
    """Style 2 captions: groups of 2-3 words in Anton, white with a thick black outline, the spoken word yellow,
    each group pops in."""
    from .style import bold_words
    ws = vt.words
    groups, cur = [], []
    for i, (wt, w) in enumerate(ws):
        cur.append(i)
        if len(cur) == 3 or w[-1] in ".?!," or (len(cur) == 2 and len(w) > 7):
            groups.append(cur); cur = []
    if cur:
        groups.append(cur)
    g = None
    for gr in groups:
        if ws[gr[0]][0] - 0.05 <= t:
            g = gr
    if g is None or t > ws[g[-1]][0] + 1.2:
        return
    shown = [(i, fix(ws[i][1], extra or {})) for i in g]
    shown = [(i, d) for i, d in shown if d]
    if not shown:
        return
    spoken = [k for k, (i, _) in enumerate(shown) if ws[i][0] <= t]
    hl = {spoken[-1]} if spoken else set()
    bold_words(c, [d for _, d in shown], VW / 2, y, 124, hl, span(t, ws[g[0]][0] - 0.05, ws[g[0]][0] + 0.15), VW - 110)


def cut_marks(c, t, marks):
    for m in marks:
        if 0 <= t - m < 0.12:
            c.drawRect(skia.Rect(0, 0, VW, VH), paint("cream", 0.25 * (1 - (t - m) / 0.12)))


def plan_for(job, vt):
    return getattr(plan_module(), f"plan_{job}")(vt)


def frame(c, job, vt, plan, t):
    P = plan_module()
    L = main_shots()
    idx = max(i for i, p in enumerate(plan) if p[0] <= t or i == 0)
    st, fn, cx, z = plan[idx]
    tm0 = max(0.0, fn(0.0))
    starts = [x[0] for x in L] + [1e9]
    k = max(i for i in range(len(L)) if starts[i] <= tm0 + 1e-6) if tm0 >= starts[0] else 0
    lo, hi = starts[k], starts[k + 1] - 0.05             # stay inside the main shot the plan points at
    reframe(c, main_frame(min(max(fn(t - st), lo), hi)), cx, 540, z)
    hook_end = plan[1][0] - 0.25 if len(plan) > 1 else 2.5
    bold = getattr(P, "CAPTIONS", "standard") == "bold"
    if t < hook_end:                                      # hook text from frame 0, then a small channel label
        if bold:
            from .style import bold_words
            bold_words(c, P.HOOK[job].split(), VW / 2, 120, 110, set(range(1, 99)), 1.0, VW - 100, 0)
        else:
            hook_text(c, P.HOOK[job], 1.0, 130, 80, "gold")
        text(c, P.SUB[job], VW / 2, 215, font("bold", 40), paint("cream", 0.9))
    else:
        text(c, "KR's What If Explained", VW / 2, 110, font("semibold", 34), paint("sand", 0.75))
    (captions_bold if bold else captions)(c, vt, t, getattr(P, "FIX", {}))
    cut_marks(c, t, [p[0] for p in plan[1:]])
    grain(c, VW, VH, t)


def frames(job, a, b, out):
    from .render import _ffmpeg_pipe
    vt = VT(job); plan = plan_for(job, vt)
    p = _ffmpeg_pipe(VW, VH, out)
    s = skia.Surface(VW, VH)
    for i in range(a, b):
        c = s.getCanvas(); c.clear(skia.Color(0, 0, 0))
        frame(c, job, vt, plan, i / ctx.FPS)
        p.stdin.write(s.makeImageSnapshot().toarray(colorType=skia.kBGRA_8888_ColorType).tobytes())
    p.stdin.close(); p.wait()
    os.rename(out + ".part.mp4", out)


def default_audio(job, vt, total, plan, mus, fx):
    from . import sfx as X, music as Mu
    if job == "short":                                    # shock: tension bed, riser lands on the loop point
        Mu.pulse(mus, 0, total - 0.3, "D2", "contrabass", 104, 0.55)
        Mu.pad(mus, 0, total, ["Dm", "Bb", "Gm", "A"], "string_ensemble_1", 0.3, 4)
        Mu.arp(mus, 0, total - 0.3, ["Dm", "Bb", "Gm", "A"], "pizzicato_strings", 104, 0.4)
        for k in range(int(total / 4.6)):
            mus.add(k * 4.6, Mu.note("timpani", "D2", 1.2, 0.6), 0.35)
        fx.add(0.0, X.impact(60, 0.8), 0.5)
    else:                                                 # feeling: wonder bed
        Mu.pad(mus, 0, total, ["Dm", "Bb", "F", "C"], "synth_strings_1", 0.35, 4)
        Mu.arp(mus, 0, total - 0.3, ["Dm", "Bb", "F", "C"], "celesta", 84, 0.35, 1)
        fx.add(0.0, X.impact(60, 0.7), 0.5)
    fx.add(total - 2.0, X.riser(2.0, 70), 0.42)


def audio(job, total):
    from . import sfx as X, music as Mu
    vt = VT(job); plan = plan_for(job, vt)
    mus, fx = Mu.Track(total + 2), Mu.Track(total + 2)
    P = plan_module()
    if hasattr(P, "AUDIO"):
        P.AUDIO(job, vt, total, mus, fx)
    else:
        default_audio(job, vt, total, plan, mus, fx)
    for st, *_ in plan[1:]:
        fx.add(st - 0.12, X.whoosh(0.4, int(st * 10)), 0.25)
    return mus.buf, fx.buf


def render(job, workers=None):
    from . import mix as MX
    from .sfx import SR
    from .render import spawn, voice, concat
    vt = VT(job)
    assert vt.mode == "real", f"anchors_{job}.json missing: run `wi.py <slug> anchors {job}` first"
    total = vt.total
    os.makedirs(ctx.OUT, exist_ok=True)
    n = int(total * ctx.FPS)
    K = workers or int(os.environ.get("KR_WORKERS", os.cpu_count() or 2))
    parts = [f"{ctx.OUT}/{job}_{k}.mp4" for k in range(K)]
    procs = [spawn(["krwi.vertical", "chunk", job, str(n * k // K), str(n * (k + 1) // K), parts[k]]) for k in range(K)]
    m, f = audio(job, total)
    master, _ = MX.master(voice(job), m, f, np.zeros(10), [(0, total + 2, -29.0)], total, fade=0.05 if job == "short" else 1.0)
    sf.write(f"{ctx.OUT}/{job}.wav", master, SR)
    for p in procs:
        p.wait()
    if any(p.returncode for p in procs):
        raise SystemExit("a frame worker failed")
    out = f"{ctx.OUT}/{job.upper()}.mp4"
    concat(parts, f"{ctx.OUT}/{job}.wav", out)
    for p in parts:
        os.remove(p)
    print("done", out, round(total, 1), "s")
    from .qa import check as qa
    qa(out, total)


def part(job, i, n, workers=None):
    """Render part i of n of a vertical's frames into out/<job>_part_<i>of<n>.mp4 (one Bash call each), then join(job)."""
    from .render import spawn
    vt = VT(job)
    assert vt.mode == "real", f"anchors_{job}.json missing: run `wi.py <slug> anchors {job}` first"
    os.makedirs(ctx.OUT, exist_ok=True)
    nf = int(vt.total * ctx.FPS)
    a0, a1 = nf * (i - 1) // n, nf * i // n
    K = workers or int(os.environ.get("KR_WORKERS", os.cpu_count() or 2))
    subs = [f"{ctx.OUT}/{job}_part_{i}of{n}_{k}.mp4" for k in range(K)]
    procs = [spawn(["krwi.vertical", "chunk", job, str(a0 + (a1 - a0) * k // K), str(a0 + (a1 - a0) * (k + 1) // K), subs[k]])
             for k in range(K)]
    for p in procs:
        p.wait()
    if any(p.returncode for p in procs):
        raise SystemExit("a frame worker failed")
    lst = f"{ctx.OUT}/{job}_part_{i}of{n}.txt"
    open(lst, "w").write("".join(f"file '{os.path.abspath(x)}'\n" for x in subs))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
                    f"{ctx.OUT}/{job}_part_{i}of{n}.mp4"], check=True)
    for x in subs + [lst]:
        os.remove(x)
    print(f"{job} part {i}/{n}: frames {a0}-{a1}")


def join(job):
    """Mix the vertical's audio and mux its parts into out/<JOB>.mp4, then QA."""
    import glob
    import re
    from . import mix as MX
    from .sfx import SR
    from .render import voice, concat
    parts = glob.glob(f"{ctx.OUT}/{job}_part_*of*.mp4")
    ns = {int(re.search(r"of(\d+)", x).group(1)) for x in parts}
    if len(ns) != 1:
        raise SystemExit(f"need parts from one split, found {sorted(ns) or 'none'}")
    n = ns.pop()
    have = sorted(int(re.search(r"part_(\d+)of", x).group(1)) for x in parts)
    if have != list(range(1, n + 1)):
        raise SystemExit(f"missing parts: {sorted(set(range(1, n + 1)) - set(have))}")
    total = VT(job).total
    m, f = audio(job, total)
    master, _ = MX.master(voice(job), m, f, np.zeros(10), [(0, total + 2, -29.0)], total, fade=0.05 if job == "short" else 1.0)
    sf.write(f"{ctx.OUT}/{job}.wav", master, SR)
    out = f"{ctx.OUT}/{job.upper()}.mp4"
    concat([f"{ctx.OUT}/{job}_part_{i}of{n}.mp4" for i in range(1, n + 1)], f"{ctx.OUT}/{job}.wav", out)
    for i in range(1, n + 1):
        os.remove(f"{ctx.OUT}/{job}_part_{i}of{n}.mp4")
    print("done", out, round(total, 1), "s")
    from .qa import check as qa
    qa(out, total)


if __name__ == "__main__":
    if sys.argv[1] == "chunk":
        frames(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5])
