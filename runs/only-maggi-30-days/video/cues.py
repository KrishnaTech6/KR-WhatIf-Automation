"""Sound for this video. The engine already adds: whooshes on transitions, riser + impact into chapter cards,
logo and end hits, hard silence before the HARD_CUT_BEFORE beat, and a score chosen from each beat's mood.
Here: a sound on every visible hit (our own synthesized SFX only), and ambience beds per scene."""
from krwi import sfx as X
from krwi.timeline import T, at, B, E  # noqa: F401


def HITS():
    h = [
        # HOOK: PACKET #210 lands, pages tear, three meals, 3x salt, missing foods
        (0.05, X.stamp_hit(), 0.5),
        (T("hook", "breakfast") - 0.1, X.pop(900), 0.5),
        (T("hook", "lunch") - 0.1, X.pop(1000), 0.5),
        (T("hook", "dinner") - 0.1, X.pop(1100), 0.5),
        (T("hook", "three"), X.stamp_hit(), 0.6),
        (T("hook", "real"), X.chime(990), 0.3),
        # PROMISE
        (at("promise", "bet", -0.1), X.pop(700), 0.45),
        (at("promise", "five", -0.1), X.chime(1320), 0.4),
        (at("promise", "skipping", -0.1), X.stamp_hit(), 0.55),
        (at("promise", "seven", -0.3), X.pop(800), 0.45),
        (at("promise", "every", -0.05), X.pop(900), 0.45),
        (at("promise", "single", -0.05), X.pop(1000), 0.45),
        (at("promise", "day", -0.05, 2), X.pop(1100), 0.45),
        (T("promise", "shook"), X.impact(4, 0.5), 0.45),
        # DAY 1: seven packets onto the shelf, the Maggi beat (three packet-tear pops)
        *[(at("day_one", "line", -0.1 + 0.32 * i), X.pop(700 + 60 * i), 0.35) for i in range(7)],
        (at("day_one", "group", -0.3), X.click(), 0.5),
        (at("day_one", "six", -0.2), X.chime(1180), 0.35),
        (at("day_one", "cheaper", -0.2), X.pop(800), 0.45),
        (T("day_one", "maggi", 2), X.pop(1200), 0.6), (T("day_one", "maggi", 2) + 0.05, X.click(), 0.5),
        (T("day_one", "maggi", 3), X.pop(1200), 0.6), (T("day_one", "maggi", 3) + 0.05, X.click(), 0.5),
        (T("day_one", "maggi", 4), X.pop(1200), 0.6), (T("day_one", "maggi", 4) + 0.05, X.click(), 0.5),
        # DAY 3: salt
        (at("day_three", "puffy", -0.1), X.pop(600), 0.45),
        (at("day_three", "wont", -0.1), X.stamp_hit(), 0.5),
        (at("day_three", "third", -0.2), X.pop(900), 0.5),
        (at("day_three", "seven", 0.6), X.impact(5, 0.6), 0.5),
        (at("day_three", "work", -0.2), X.heartbeat(), 0.5),
        # WEEK 1: mom's call, WAX!!, FALSE
        (at("week_one", "then", 0.0), X.buzz(1.6), 0.35),
        (at("week_one", "wax", -0.2), X.pop(600), 0.55),
        (at("week_one", "no", -0.05), X.stamp_hit(), 0.7),
        (at("week_one", "wrong", 0.0), X.glitch(), 0.3),
        (at("week_one", "right", 0.0), X.chime(1320), 0.35),
        # DAY 10
        (at("day_ten", "london", -0.3), X.pop(800), 0.45),
        (at("day_ten", "forty", -0.2), X.impact(6, 0.5), 0.45),
        # DAY 20
        (at("day_twenty", "biryani", -0.2), X.click(), 0.5),
        (at("day_twenty", "forty", -0.2), X.pop(900), 0.45),
        (at("day_twenty", "fiftyfour", -0.2), X.pop(1100), 0.45),
        (at("day_twenty", "full", -0.3), X.stamp_hit(), 0.5),
        (at("day_twenty", "belly", -0.3), X.pop(800), 0.45),
        (at("day_twenty", "sugar", -0.3), X.pop(900), 0.45),
        (at("day_twenty", "pressure", -0.3), X.pop(1000), 0.45),
        # DAY 30: the same three Maggi pops, slowed and dim; money; LOST; gums
        (T("day_thirty", "maggi", 1), X.pop(500), 0.35),
        (T("day_thirty", "maggi", 2), X.pop(450), 0.3),
        (T("day_thirty", "maggi", 3), X.pop(400), 0.25),
        (at("day_thirty", "hands", 0.0), X.whoosh(0.6, 7), 0.35),
        (at("day_thirty", "won", -0.1), X.stamp_hit(), 0.6),
        (at("day_thirty", "lost", -0.1), X.impact(8, 0.7), 0.55),
        (at("day_thirty", "zero", -0.3), X.heartbeat(), 0.45),
        (at("day_thirty", "bleed", 0.0), X.pop(400), 0.4),
        # TWIST
        (at("twist", "scurvy", -0.1), X.impact(9, 1.0), 0.65),
        (at("twist", "sydney", -0.3), X.pop(800), 0.45),
        (at("twist", "twelve", -0.2), X.skitter(0.8), 0.3),
        # PAYOFF: peas, egg, lemon drop in
        (at("payoff", "peas", -0.1), X.pop(1000), 0.5),
        (at("payoff", "egg", -0.1), X.pop(1100), 0.5),
        (at("payoff", "lemon", -0.1), X.chime(1480), 0.45),
    ]
    return h


def AMB():
    return [
        ("room", B("day_one"), E("day_one"), 0.35),
        ("room", B("week_one"), E("week_one"), 0.3),
        ("room", B("day_twenty"), at("day_twenty", "but", 0.0), 0.35),
        ("wind", B("twist"), at("twist", "with", 0.0), 0.35),
        ("room", B("payoff"), E("payoff"), 0.3),
    ]
