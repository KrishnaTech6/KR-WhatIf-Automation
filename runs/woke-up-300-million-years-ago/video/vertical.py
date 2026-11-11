"""9:16 Short + Reel: reframes the main video's illustrations, adds hook text and word-by-word captions.
Timing: anchors_<job>.json (from vertical_anchors()) or a 160 wpm estimate."""
import json, os, re, sys, math
import skia
import shots as S
from timeline import norm, HERE, RUN
from art import font, text, paint, span, ease, ease_out, back_out, keys, col, finish, grain, vignette, text_w
from timeline import T as MT

VW, VH = 1080, 1920


def parse_lines(job):
    body = open(os.path.join(RUN, "script", f"voice-{job}.txt")).read().split("\n\n", 1)[1]
    lines = []
    for l in body.splitlines():
        if not l.strip() or l.startswith("["):
            continue
        l = re.sub(r"\{\w+\}", "", l).strip()
        lines.append(l)
    return lines


def estimate(job):
    t, words = 0.0, []
    for l in parse_lines(job):
        for tok in l.split():
            if tok == "(beat)":
                t += 1.0; continue
            words.append([t, tok]); t += 60 / 160
            if tok[-1] in ".?": t += 0.2
    return words, t + 0.5


def load(job):
    p = os.path.join(HERE, f"anchors_{job}.json")
    if os.path.exists(p):
        d = json.load(open(p)); return d["words"], d["total"]
    return estimate(job)


class VT:
    def __init__(self, job):
        self.job = job
        self.words, self.total = load(job)

    def T(self, w, n=1):
        hits = [t for t, x in self.words if norm(x) == norm(w)]
        if len(hits) < n:
            raise KeyError((self.job, w, n))
        return hits[n - 1]


# ---------------------------------------------------------------- main-frame cache
_surf = skia.Surface(1920, 1080)
_main_shots = S.SHOTS()


def main_frame(tm):
    c = _surf.getCanvas(); c.clear(skia.Color(0, 0, 0))
    S.render_frame(c, tm, _main_shots)
    return _surf.makeImageSnapshot()


def reframe(c, img, cx, cy=540, zoom=1.25, top=150):
    """background: same frame, cover-scaled and darkened; foreground: zoomed crop centred on (cx, cy)."""
    sc = VH / 1080
    c.save(); c.translate(VW / 2, VH / 2); c.scale(sc, sc); c.translate(-cx, -540)
    p = skia.Paint(); p.setImageFilter(skia.ImageFilters.Blur(10, 10))
    c.drawImage(img, 0, 0, skia.SamplingOptions(), p); c.restore()
    c.drawRect(skia.Rect(0, 0, VW, VH), paint("space", 0.55))
    fh = 1100
    y0 = top
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


def captions(c, vt, t, y=1360):
    """word-by-word, groups of 2-3, current word gold, Poppins ExtraBold with dark outline."""
    ws = vt.words
    groups, cur = [], []
    for i, (wt, w) in enumerate(ws):
        cur.append(i)
        if len(cur) == 3 or w[-1] in ".?!," or (len(cur) == 2 and len(w) > 7):
            groups.append(cur); cur = []
    if cur: groups.append(cur)
    g = None
    for gr in groups:
        if ws[gr[0]][0] - 0.05 <= t:
            g = gr
    if g is None or t > ws[g[-1]][0] + 1.2:
        return
    f = font("extrabold", 92)
    disp = [fix(ws[i][1]) for i in g]
    total = sum(text_w(d, f) for d in disp) + 26 * (len(disp) - 1)
    x = VW / 2 - total / 2
    for i, d in zip(g, disp):
        on = ws[i][0] <= t
        out = paint("space", 1, stroke=16)
        c.drawString(d, x, y, f, out)
        c.drawString(d, x, y, f, paint("gold" if on and (i == g[-1] or ws[i + 1][0] > t) else "cream"))
        x += text_w(d, f) + 26


FIX = {"seventy": "70", "centimetre": "cm", "three": "300", "hundred": "", "million": "MILLION", "kr's": "KR's",
       "k": "", "r's": "KR's"}


def fix(w):
    base = w.strip(".,?!")
    lw = base.lower()
    if lw in ("hundred",):
        return ""
    if lw == "three":
        return "300"
    if lw == "seventy":
        return "70"
    if lw == "centimetre":
        return "cm"
    if lw == "k":
        return "KR's" if False else ""
    if lw == "r's":
        return "KR's"
    return base.upper()


def cut_marks(c, t, marks):
    for m in marks:
        if 0 <= t - m < 0.12:
            c.drawRect(skia.Rect(0, 0, VW, VH), paint("cream", 0.25 * (1 - (t - m) / 0.12)))


# ---------------------------------------------------------------- shot plans: (start_word, main_time_fn, cx, zoom, hook text)
def plan_short(vt):
    w = vt.T
    return [
        (0.0, lambda d: 3.2 + d, 960, 1.25),
        (w("its"), lambda d: MT("hook", "wings") + 1.0 + d, 1160, 1.15),
        (w("you", 1), lambda d: MT("promise", "three") + 0.6 + d * 1.5, 960, 1.0),
        (w("no"), lambda d: MT("hour1", "dinosaurs") + 0.6 + d, 1000, 1.2),
        (w("look"), lambda d: MT("hour3", "millipede") + 0.6 + d * 1.4, 900, 1.1),
        (w("it", 1), lambda d: MT("hour3", "good") + 0.8 + d, 900, 1.15),
        (w("so", 1), lambda d: MT("hour3", "so", 1) + 0.6 + d, 960, 1.15),
        (w("has"), lambda d: MT("minute", "today") + d * 1.3, 960, 1.1),
        (w("bugs"), lambda d: MT("hour3", "bugs") + 0.8 + d, 1060, 1.1),
        (w("more", 2), lambda d: MT("hour3", "more") + d * 1.2, 1060, 1.1),
        (w("but", 1), lambda d: MT("night", "lightning") - 0.4 + d, 1000, 1.25),
        (w("one"), lambda d: MT("night", "fire") + d * 1.3, 960, 1.2),
        (w("and", 1), lambda d: MT("night", "coal") + 1.0 + d, 1100, 1.1),
        (w("scariest"), lambda d: MT("payoff", "so", 1) + 0.2 + d * 0.5, 1000, 1.15),
        (w("full"), lambda d: MT("payoff", "wake") + 0.4 + d, 960, 1.15),
        (w("so", 3) if len([1 for t, x in vt.words if norm(x) == "so"]) >= 3 else w("if"), lambda d: max(0.0, d - 1.0) + 0.2, 960, 1.25),
    ]


def plan_reel(vt):
    w = vt.T
    return [
        (0.0, lambda d: MT("year", "frozen") + 0.6 + d, 1440, 1.25),
        (w("three"), lambda d: MT("promise", "three") + 0.6 + d * 1.5, 960, 1.0),
        (w("all"), lambda d: MT("year", "crashing") - 0.3 + d * 1.2, 960, 1.05),
        (w("and", 1), lambda d: MT("year", "india", 3) + d, 960, 1.05),
        (w("proof"), lambda d: MT("year", "odisha") - 0.5 + d, 1000, 1.1),
        (w("big"), lambda d: MT("year", "boulders") + 0.2 + d, 960, 1.15),
        (w("meanwhile"), lambda d: MT("hour1", "tall") + d, 1000, 1.15),
        (w("dragonflies"), lambda d: MT("hook", "wings") + 1.0 + d, 1160, 1.15),
        (w("later"), lambda d: MT("hour1", "spot") + d, 960, 1.2),
        (w("probably"), lambda d: MT("payoff", "so", 1) + 0.2 + d * 0.4, 1000, 1.15),
        (w("full"), lambda d: E_END + 0.8 + d, 960, 1.0),
        (w("because"), lambda d: MT("year", "frozen") + 0.4 + d * 0.3, 1440, 1.25),
    ]


from timeline import E as ME
E_END = ME("payoff") + 0.3

HOOK = {"short": "DON'T MOVE.", "reel": "INDIA WAS FROZEN."}
SUB = {"short": "300 MILLION YEARS AGO", "reel": "300 MILLION YEARS AGO"}


def frame(c, job, vt, plan, t):
    idx = max(i for i, p in enumerate(plan) if p[0] <= t or i == 0)
    st, fn, cx, z = plan[idx]
    img = main_frame(max(0.0, fn(t - st)))
    reframe(c, img, cx, 540, z)
    # top text: hook from frame 0, then a small persistent label
    if t < plan[1][0]:
        hook_text(c, HOOK[job], 1.0 if t < 0.05 else span(t, 0, 0.25) * 0 + 1.0, 130, 80, "gold")
        text(c, SUB[job], VW / 2, 215, font("bold", 40), paint("cream", 0.9))
    else:
        text(c, "KR's What If Explained", VW / 2, 110, font("semibold", 34), paint("sand", 0.75))
    captions(c, vt, t)
    cut_marks(c, t, [p[0] for p in plan[1:]])
    grain(c, VW, VH, t)
