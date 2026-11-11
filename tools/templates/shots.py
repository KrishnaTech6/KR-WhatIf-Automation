"""Shot list for this video. Engine: tools/krwi (python3 tools/wi.py <slug> sheets | preview | render).

Rules (pipeline A4): new shot every 2-4 s, something changes at least every 3 s, every number as a comparison,
minimal text, cold open = the hook's consequence on frame 0, logo sting right after the hook.
Library shots (krwi.lib): card, logo_sting, end_screen, counter, statement, pills, bars, india_pin, india_states,
split, kr_react, papers, comment_prompt, tease, layer + stamp_at / pop_at overlays, zoom.
Write new code only for hero shots and topic drawings (put reusable topic drawings in art.py).
Beat keys: `python3 tools/wi.py <slug> timeline` lists them and their aliases.
"""
from krwi.lib import *  # noqa: F401,F403


# ---------------------------------------------------------------- hero shots (topic-specific)
def s_cold_open(c, t, t0):
    """Frame 0 must already show the hook's consequence."""
    explainer_bg(c, t)
    big_text(c, "REPLACE ME", W / 2, H / 2, 96, span(t, t0, t0 + 0.4), "gold")


# ---------------------------------------------------------------- the list: (start, shot, transition)
# transitions: cut, fade, iris, zoom, whip, flash.  at("beat", "word", offset) = word time + offset.
def SHOTS():
    return [
        (0.0, s_cold_open, "cut"),
        (E("hook") + 0.1, logo_sting(), "flash"),
        # (B("minute_one") - 0.6, card("MINUTE 1", "The air"), "iris"),
        # (at("minute_one", "today", -0.3), counter(0, 35, "{:.0f}%", until=at("minute_one", "percent")), "fade"),
        (E(LAST_BEAT) + 0.3, end_screen(), "fade"),
    ]


LAST_BEAT = BEAT_KEYS[-1]
