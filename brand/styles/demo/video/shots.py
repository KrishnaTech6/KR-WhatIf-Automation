"""Style demo: the same few shots in every style (render: python3 brand/render_styles.py).
Shows how topic art is drawn per style: branch on STYLE and use the style helpers."""
import math
from krwi.lib import *  # noqa: F401,F403

SX, SY, EX, EY = 960, 400, 960, 860


def s_sun(c, t, t0):
    vanish = t0 + 1.2
    k = 1 - ease(span(t, vanish, vanish + 0.35))
    if STYLE == "cinematic":
        cinematic_bg(c, t)
        light_stream(c, SX, SY, EX, EY - 60, t, 0.55 * ease_out(span(t, vanish + 0.3, t0 + 6)) if t > vanish + 0.3 else 0)
        if k > 0.01:
            bloom(c, SX, SY, 120 * k)
        shock_ring(c, SX, SY, span(t, vanish + 0.3, vanish + 1.8))
        c.drawCircle(EX, EY, 64, paint("#123E73"))
        glow(c, EX, EY, 110, "#5FA8FF", 0.35)
        countdown(c, 500 - max(0, t - vanish), 1550, 900, 64)
    elif STYLE == "collage":
        collage_bg(c, t)
        dx, dy, r = jit("sun", t)
        if k > 0.5:
            def sun(k):
                p = paper_circle(SX + dx, SY + dy, 150, 3)
                k.drawPath(p, paint("#F6A21E")); halftone(k, p, "#D9480F", 0.7)
            cutout(c, sun)
            tape(c, SX - 120 + dx, SY - 130 + dy, 140, 44, -35)
        else:
            c.drawPath(paper_circle(SX + dx, SY + dy, 160, 4, 0.06), paint("#101014"))
            marker_circle(c, SX, SY, 200, 190, span(t, vanish + 0.4, vanish + 0.9))
            stamp(c, SX, SY, "MISSING", span(t, vanish + 0.6, vanish + 0.9), rot=-12)
        ex, ey, er = jit("earth", t)
        def earth(k):
            p = paper_circle(EX + ex, EY + ey, 90, 8)
            k.drawPath(p, paint("#2B6CB0")); halftone(k, p, "#000022", 0.3)
        cutout(c, earth)
        red_string(c, [(SX + 120, SY + 110), (EX + 70, EY - 60)], span(t, vanish + 1.0, vanish + 1.6))
    else:
        night_sky(c, W, H, t)
        if k > 0.01:
            glow(c, SX, SY, 420 * k, "amber", 0.6); c.drawCircle(SX, SY, 120 * k, paint("gold"))
        c.drawCircle(EX, EY, 70, paint("teal"))
    big_text(c, "THE SUN JUST VANISHED.", W / 2, 120, 64, span(t, vanish + 0.3, vanish + 0.8))


def SHOTS():
    return [
        (0.0, s_sun, "cut"),
        (6.0, statement("8 MIN 20 SEC", sub="Light from the Sun is already old", size=110, color="gold"), "fade"),
        (9.0, card("+8 MIN", "The lights go out"), "flash"),
        (11.0, pills([("No sunlight", 11.3), ("No photosynthesis", 11.7, "coral"), ("Freezing nights", 12.1, "plum")],
                     title="WHAT STOPS FIRST"), "fade"),
        (14.0, kr_react("shocked", "WAIT, WHAT?!"), "zoom"),
        (17.0, comment_prompt("What would you do in those 8 minutes?"), "fade"),
    ]
