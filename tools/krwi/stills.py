"""Stills and 3-up contact sheets for Checkpoint 2 (main) and vertical checks. Output: video/sheets/."""
import os

import skia

from . import ctx
from .art import font, text, paint

OUT = os.path.join(ctx.VIDEO, "sheets")


def _shots():
    import shots as S
    return S.SHOTS()


def still(t, shots=None):
    from .compose import render_frame
    s = skia.Surface(ctx.W, ctx.H)
    sh = render_frame(s.getCanvas(), t, shots or _shots())
    fn = sh[1]
    return s.makeImageSnapshot(), ("card" if getattr(fn, "kind", None) == "card" else getattr(fn, "__name__", "?"))


def vstill(job, t, vt=None, plan=None):
    from . import vertical as V
    vt = vt or V.VT(job); plan = plan or V.plan_for(job, vt)
    s = skia.Surface(ctx.VW, ctx.VH)
    V.frame(s.getCanvas(), job, vt, plan, t)
    return s.makeImageSnapshot()


def sheet(name, times, labels=None, job=None):
    """Tile stills 3-up (main) or 4-up (vertical) with a label under each: time + shot name."""
    os.makedirs(OUT, exist_ok=True)
    vert = job is not None
    if vert:
        from . import vertical as V
        vt = V.VT(job); plan = V.plan_for(job, vt)
        cols, tw, th = 4, 360, 640
    else:
        shots = _shots()
        cols, tw, th = 3, 640, 360
    pad = 12
    rows = (len(times) + cols - 1) // cols
    S = skia.Surface(cols * tw + (cols + 1) * pad, rows * (th + 46) + pad)
    c = S.getCanvas(); c.clear(skia.Color(20, 16, 30))
    for i, t in enumerate(times):
        if vert:
            img, fn = vstill(job, t, vt, plan), job
        else:
            img, fn = still(t, shots)
        x = pad + (i % cols) * (tw + pad); y = pad + (i // cols) * (th + 46)
        c.drawImageRect(img, skia.Rect(x, y, x + tw, y + th), skia.SamplingOptions(skia.FilterMode.kLinear))
        lab = (labels[i] + "  " if labels else "") + f"t={t:.1f}s  {fn}"
        text(c, lab, x + 6, y + th + 32, font("semibold", 22), paint("cream"), align="left")
    path = os.path.join(OUT, name + ".png")
    S.makeImageSnapshot().save(path, skia.kPNG)
    print("wrote", path)
    return path


def auto(per_sheet=9):
    """One still per shot, 80% of the way through it (max 6 s in) so animations have landed; 9 per sheet."""
    L = _shots()
    times, labels = [], []
    for i, (st, fn, tr) in enumerate(L):
        nxt = L[i + 1][0] if i + 1 < len(L) else st + 3.0
        times.append(st + min(0.8 * (nxt - st), 6.0)); labels.append(f"#{i}")
    paths = []
    for k in range(0, len(times), per_sheet):
        paths.append(sheet(f"shots_{k // per_sheet + 1}", times[k:k + per_sheet], labels[k:k + per_sheet]))
    return paths
