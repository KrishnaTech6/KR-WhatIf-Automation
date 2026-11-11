"""Shot library. A run's video/shots.py starts with `from krwi.lib import *` and gets:
  - timing: T, at, B, E, TOTAL, MODE (from the voice script / anchors.json)
  - drawing: everything in krwi.art (brand primitives, draw_kr, logo cards, big_text, india_map, Cam, rng, ...)
  - the ready-made shots below. Each one is a factory that returns fn(c, t, t0) for the shot list:
        (at("year", "proof", -0.2), india_pin("ODISHA", 84.5, 20.6, T("year", "odisha")), "fade")
Times passed to a factory are absolute seconds (use T()/at()). `bg` is any fn(c, t); default explainer_bg.
Only hero shots and topic drawings need new code in the run.
"""
import math

import skia

from .art import *  # noqa: F401,F403
from .art import W, H, explainer_bg, span, ease, ease_out, back_out, paint, font, text, text_w, glow, pill, big_text, \
    counter_text, stamp, paper, comment_card, india_map, pop, draw_kr, draw_logo, chapter_card, end_card, night_sky, finish, lin
from .timeline import T, at, B, E, TOTAL, MODE, BEAT_KEYS  # noqa: F401


def _bg(bg, c, t):
    (bg or explainer_bg)(c, t)


def _named(fn, name, kind=None):
    fn.__name__ = name
    fn.kind = kind
    return fn


# ---------------------------------------------------------------- brand shots
def card(value, name):
    """Full-screen chapter card: the time value big ('DAY 10', '+2 HOURS'), the chapter name under it. ~1.5 s."""
    def f(c, t, t0):
        chapter_card(c, W, H, value, name, span(t, t0, t0 + 1.4), t)
    f.kind = "card"
    return f


def logo_sting(bg=None):
    """The KR logo sting, right after the hook."""
    def f(c, t, t0):
        (bg or (lambda c, t: night_sky(c, W, H, t)))(c, t)
        draw_logo(c, W / 2, H / 2, 1.25, span(t, t0, t0 + 2.5), t)
    return _named(f, "logo_sting", "logo")


def end_screen():
    """End card ("See you in the next What If")."""
    def f(c, t, t0):
        end_card(c, W, H, span(t, t0, t0 + 2.0), t)
    return _named(f, "end_screen", "end")


# ---------------------------------------------------------------- numbers and text
def counter(v0, v1, fmt="{:,.0f}", until=None, label=None, label_at=None, bg=None, tint="magenta", size=104, color="gold"):
    """Animated big number counting v0 -> v1 from the shot start to `until` (default +1.5 s), optional label pill.
    fmt: a format string or fn(v) -> str."""
    f_ = fmt if callable(fmt) else (lambda v: fmt.format(v))

    def f(c, t, t0):
        _bg(bg, c, t)
        glow(c, W / 2, H / 2, 700, tint, 0.3)
        counter_text(c, v0, v1, span(t, t0, until or t0 + 1.5), f_, W / 2, 560, size, color)
        if label:
            pop(c, W / 2, 720, label, t, label_at or t0 + 0.3, "plum", 44)
    return _named(f, "counter")


def statement(line, sub=None, at_t=None, bg=None, color="cream", size=72, sub_color="sand"):
    """One big line (and an optional smaller line) rising in at `at_t` (default shot start + 0.15 s)."""
    def f(c, t, t0):
        _bg(bg, c, t)
        a = at_t if at_t is not None else t0 + 0.15
        big_text(c, line, W / 2, 520, size, span(t, a, a + 0.4), color)
        if sub:
            big_text(c, sub, W / 2, 640, int(size * 0.6), span(t, a + 0.3, a + 0.7), sub_color, "bold")
    return _named(f, "statement")


def pills(items, title=None, bg=None, x=W / 2, y0=380, gap=130, size=46):
    """A list that pops in item by item: items = [(label, time, color), ...] (color optional)."""
    def f(c, t, t0):
        _bg(bg, c, t)
        if title:
            big_text(c, title, W / 2, 200, 64, span(t, t0, t0 + 0.4))
        for i, it in enumerate(items):
            label, when = it[0], it[1]
            pop(c, x, y0 + i * gap, label, t, when, it[2] if len(it) > 2 else "teal", size)
    return _named(f, "pills")


def bars(items, title=None, at_t=None, fmt="{:,.0f}", unit="", bg=None, stagger=0.35):
    """Scale comparison: horizontal bars growing to their values. items = [(label, value, color), ...]."""
    vmax = max(v for _, v, *_ in items)
    f_ = fmt if callable(fmt) else (lambda v: fmt.format(v))

    def f(c, t, t0):
        _bg(bg, c, t)
        a0 = at_t if at_t is not None else t0 + 0.2
        if title:
            big_text(c, title, W / 2, 190, 60, span(t, t0, t0 + 0.4))
        n = len(items)
        top = H / 2 - (n - 1) * 75
        for i, it in enumerate(items):
            label, v, color = it[0], it[1], it[2] if len(it) > 2 else "teal"
            p = ease(span(t, a0 + i * stagger, a0 + i * stagger + 0.9))
            y = top + i * 150
            text(c, label, 500, y + 16, font("bold", 44), paint("cream"), align="right")
            L = 1100 * v / vmax * p
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(530, y - 38, 530 + max(L, 1), y + 38), 18, 18), paint(color))
            if p > 0.05:
                text(c, f_(v * p) + unit, 560 + L, y + 16, font("extrabold", 46), paint("gold", min(1, p * 2)), align="left")
    return _named(f, "bars")


# ---------------------------------------------------------------- maps (complete India outline from brand/india.json)
def india_pin(label, lon, lat, pin_at=None, k=28, bg=None, color="coral", cy=560):
    """India map with a pin dropping on (lon, lat) at `pin_at` and a label pill."""
    def f(c, t, t0):
        _bg(bg, c, t)
        P = india_map(c, W / 2, cy, k)
        ox, oy = P(lon, lat)
        a = pin_at if pin_at is not None else t0 + 0.3
        p = back_out(span(t, a, a + 0.4))
        if p > 0:
            c.drawCircle(ox, oy - 40 * p, 22 * p, paint(color))
            c.drawLine(ox, oy, ox, oy - 30 * p, paint(color, stroke=6))
            pill(c, ox + 180, oy - 60, 1.0, label, color, "cream", 38)
    return _named(f, "india_pin")


def india_states(states, label=None, hl_at=None, hcol="#2A2420", k=28, bg=None, label_xy=(1500, 560)):
    """India map with `states` filling in at `hl_at` (names as in brand/india.json), optional label pill."""
    def f(c, t, t0):
        _bg(bg, c, t)
        a = hl_at if hl_at is not None else t0 + 0.4
        ha = ease(span(t, a - 0.6, a + 0.4))
        india_map(c, W / 2, 560, k, highlight=states, hcol=hcol, ha=ha)
        if label and ha > 0.5:
            pop(c, label_xy[0], label_xy[1], label, t, a, "plum", 48)
    return _named(f, "india_states")


# ---------------------------------------------------------------- comparisons and people
def split(left, right, left_label=None, right_label=None, wipe_at=None):
    """Before/after (with/without) split screen. left/right: fn(c, t). The divider wipes in at `wipe_at`."""
    def f(c, t, t0):
        a = wipe_at if wipe_at is not None else t0
        x = W / 2 + (1 - ease(span(t, a, a + 0.5))) * W / 2
        c.save(); c.clipRect(skia.Rect(0, 0, x, H)); left(c, t); c.restore()
        c.save(); c.clipRect(skia.Rect(x, 0, W, H)); right(c, t); c.restore()
        c.drawLine(x, 0, x, H, paint("cream", stroke=6))
        if left_label:
            pill(c, W / 4, 110, 1.0, left_label, "teal", "cream", 40)
        if right_label and x < W * 0.6:
            pill(c, W * 3 / 4, 110, 1.0, right_label, "coral", "cream", 40)
    return _named(f, "split")


def kr_react(expr="shocked", line=None, line_at=None, bg=None, x=W / 2, scale=1.5, color="plum"):
    """KR big on screen with an expression (neutral, curious, shocked, thinking, happy, worried, pointing)."""
    def f(c, t, t0):
        _bg(bg, c, t)
        glow(c, x, 640, 520, "teal", 0.25)
        k = back_out(span(t, t0, t0 + 0.35))
        c.save(); c.translate(x, 940); c.scale(k, k); c.translate(-x, -940)
        draw_kr(c, x, 940, scale, expr, t)
        c.restore()
        if line:
            pop(c, x, 170, line, t, line_at if line_at is not None else t0 + 0.3, color, 46)
    return _named(f, "kr_react")


def papers(left, right, right_at, headline="SCIENTISTS STILL ARGUE", bg=None):
    """Two studies disagreeing: left/right = (title, sub). The second paper and the headline land at `right_at`."""
    def f(c, t, t0):
        _bg(bg, c, t)
        a1 = ease_out(span(t, t0, t0 + 0.5)); a2 = ease_out(span(t, right_at - 0.4, right_at))
        paper(c, 640, 560 + (1 - a1) * 300, 1.2, left[0], left[1], "teal", -4, a1)
        if a2 > 0:
            paper(c, 1280, 560 + (1 - a2) * 300, 1.2, right[0], right[1], "coral", 5, a2)
            sh = 8 * math.sin(t * 30) * (1 - span(t, right_at, right_at + 1))
            big_text(c, headline, W / 2 + sh, 140, 64, a2, "cream")
    return _named(f, "papers")


def comment_prompt(question, card_at=None, bg=None):
    """'Tell me in the comments' card with the script's comment question."""
    def f(c, t, t0):
        _bg(bg, c, t)
        a = card_at if card_at is not None else t0 + 0.3
        comment_card(c, W / 2, H / 2, 1.2, question, span(t, a, a + 0.6), t)
    return _named(f, "comment_prompt")


def tease(line, bg=None):
    """Next-video tease: 'NEXT: ...' over a backdrop."""
    def f(c, t, t0):
        _bg(bg, c, t)
        big_text(c, line, W / 2, 260, 64, span(t, t0 + 0.3, t0 + 0.8), "gold")
    return _named(f, "tease")


# ---------------------------------------------------------------- combinators
def layer(*fns):
    """Draw several shot fns on top of each other: layer(my_scene, stamp_at("GONE", T("hook", "gone")))."""
    def f(c, t, t0):
        for fn in fns:
            fn(c, t, t0)
    return _named(f, "+".join(getattr(x, "__name__", "fn") for x in fns), getattr(fns[0], "kind", None))


def stamp_at(label, when, color="coral", x=W / 2, y=H / 2, rot=-12):
    """Overlay: a rubber stamp slamming in at `when` (use with layer())."""
    def f(c, t, t0):
        stamp(c, x, y, label, span(t, when, when + 0.3), color, rot)
    return _named(f, "stamp")


def pop_at(label, when, x=W / 2, y=150, color="teal", size=44):
    """Overlay: a label pill popping in at `when` (use with layer())."""
    def f(c, t, t0):
        pop(c, x, y, label, t, when, color, size)
    return _named(f, "pop")


def zoom(fn, z0=1.0, z1=1.12, cx=W / 2, cy=H / 2, dur=None):
    """Slow push-in on any shot (Ken Burns) over `dur` seconds (default 6)."""
    def f(c, t, t0):
        k = z0 + (z1 - z0) * ease(span(t, t0, t0 + (dur or 6.0)))
        c.save(); c.translate(cx, cy); c.scale(k, k); c.translate(-cx, -cy); fn(c, t, t0); c.restore()
    return _named(f, getattr(fn, "__name__", "zoom"), getattr(fn, "kind", None))
