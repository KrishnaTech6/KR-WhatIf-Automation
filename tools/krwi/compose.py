"""Shot list -> frame. A shot list is [(start_seconds, fn(c, t, t0), transition), ...] sorted by start.
The compositor draws the previous shot under the new one during the transition, then the film finish
(grain + vignette). Everything is a pure function of t, so frames render in any order."""
import skia

from .art import W, H, span, ease, paint, finish

TRANS = {"cut": 0.0, "fade": 0.35, "iris": 0.5, "zoom": 0.4, "whip": 0.3, "flash": 0.25}


def render_frame(c, t, shots):
    idx = max(i for i, s in enumerate(shots) if s[0] <= t or i == 0)
    st, fn, tr = shots[idx]
    d = TRANS[tr]
    p = span(t, st, st + d) if d else 1.0
    if p < 1 and idx > 0:
        pst, pfn, _ = shots[idx - 1]
        pfn(c, t, pst)
        if tr == "iris":
            c.save(); clip = skia.Path(); clip.addCircle(W / 2, H / 2, ease(p) * 1150); c.clipPath(clip, doAntiAlias=True)
            fn(c, t, st); c.restore()
        elif tr == "flash":
            fn(c, t, st); c.drawRect(skia.Rect(0, 0, W, H), paint("cream", 1 - p))
        elif tr == "whip":
            c.saveLayerAlpha(None, int(255 * ease(p))); c.translate((1 - ease(p)) * 300, 0); fn(c, t, st); c.restore()
        elif tr == "zoom":
            c.saveLayerAlpha(None, int(255 * ease(p))); k = 1.25 - 0.25 * ease(p)
            c.translate(W / 2, H / 2); c.scale(k, k); c.translate(-W / 2, -H / 2); fn(c, t, st); c.restore()
        else:
            c.saveLayerAlpha(None, int(255 * ease(p))); fn(c, t, st); c.restore()
    else:
        fn(c, t, st)
    finish(c, W, H, t)
    return shots[idx]


def check(shots):
    """Shot list sanity: sorted starts, known transitions. Returns a list of problems (empty = OK)."""
    bad = []
    for i, (st, fn, tr) in enumerate(shots):
        if tr not in TRANS:
            bad.append(f"shot {i} ({getattr(fn, '__name__', fn)}): unknown transition {tr!r}")
        if i and st < shots[i - 1][0]:
            bad.append(f"shot {i} ({getattr(fn, '__name__', fn)}) starts at {st:.2f} s, before shot {i - 1} ({shots[i - 1][0]:.2f} s)")
    return bad
