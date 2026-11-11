"""Short + Reel plans for 'What If You Woke Up 300 Million Years Ago?' (engine: krwi.vertical)."""
from krwi.script import norm
from krwi.timeline import T as MT
from krwi import sfx as X, music as Mu

FIX = {"hundred": "", "three": "300", "seventy": "70", "centimetre": "cm"}


# ---------------------------------------------------------------- shot plans: (start_word, main_time_fn, cx, zoom, hook text)
def plan_short(vt):
    w = vt.T
    return [
        (0.0, lambda d: 3.2 + d, 960, 1.25),
        (w("its"), lambda d: MT("hook", "wings") + 1.0 + d, 1060, 0.9),
        (w("you", 1), lambda d: MT("promise", "three") + 0.6 + d * 1.5, 960, 0.75),
        (w("no"), lambda d: MT("hour1", "dinosaurs") + 0.6 + d, 1000, 1.2),
        (w("look"), lambda d: MT("hour3", "millipede") + 0.6 + d * 1.4, 900, 1.1),
        (w("it", 1), lambda d: MT("hour3", "good") + 0.8 + d, 900, 1.15),
        (w("so", 1), lambda d: MT("hour3", "so", 1) + 0.6 + d, 950, 0.85),
        (w("has"), lambda d: MT("minute", "today") + d * 1.3, 960, 1.1),
        (w("bugs"), lambda d: MT("hour3", "bugs") + 0.8 + d, 1060, 1.1),
        (w("more", 2), lambda d: MT("hour3", "more") + d * 1.2, 1060, 1.1),
        (w("but", 1), lambda d: MT("night", "lightning") - 0.4 + d, 1000, 1.25),
        (w("one"), lambda d: MT("night", "fire") + d * 1.3, 960, 1.2),
        (w("scariest"), lambda d: MT("payoff", "so", 1) + 0.2 + d * 0.5, 1000, 1.15),
        (w("full"), lambda d: MT("payoff", "wake") + 0.4 + d, 960, 1.15),
        (w("so", 3) if len([1 for t, x in vt.words if norm(x) == "so"]) >= 3 else w("if"), lambda d: max(0.0, d - 1.0) + 0.2, 960, 1.25),
    ]


def plan_reel(vt):
    w = vt.T
    return [
        (0.0, lambda d: MT("year", "frozen") + 0.6 + d, 1440, 1.25),
        (w("three"), lambda d: MT("promise", "three") + 0.6 + d * 1.5, 960, 0.75),
        (w("all"), lambda d: MT("year", "crashing") - 0.3 + d * 1.2, 960, 1.05),
        (w("and", 1), lambda d: MT("year", "india", 3) + d, 960, 1.05),
        (w("proof"), lambda d: MT("year", "odisha") - 0.5 + d, 1000, 1.1),
        (w("big"), lambda d: MT("year", "boulders") + 0.2 + d, 960, 1.15),
        (w("meanwhile"), lambda d: MT("hour1", "tall") + d, 1000, 1.15),
        (w("dragonflies"), lambda d: MT("hook", "wings") + 1.0 + d, 1060, 0.9),
        (w("later"), lambda d: MT("hour1", "spot") + d, 960, 0.95),
        (w("probably"), lambda d: MT("payoff", "so", 1) + 0.2 + d * 0.4, 1000, 1.15),
        (w("full"), lambda d: E_END + 0.8 + d, 960, 1.0),
        (w("because"), lambda d: MT("year", "frozen") + 0.4 + d * 0.3, 1440, 1.25),
    ]


from krwi.timeline import E as ME
E_END = ME("payoff") + 0.3

HOOK = {"short": "DON'T MOVE.", "reel": "INDIA WAS FROZEN."}
SUB = {"short": "300 MILLION YEARS AGO", "reel": "300 MILLION YEARS AGO"}


def AUDIO(job, vt, total, mus, fx):
    if job == "short":
        Mu.pulse(mus, 0, total - 0.3, "D2", "contrabass", 104, 0.55)
        Mu.pad(mus, 0, total, ["Dm", "Bb", "Gm", "A"], "string_ensemble_1", 0.3, 4)
        Mu.arp(mus, 0, total - 0.3, ["Dm", "Bb", "Gm", "A"], "pizzicato_strings", 104, 0.4)
        for k in range(int(total / 4.6)):
            mus.add(k * 4.6, Mu.note("timpani", "D2", 1.2, 0.6), 0.35)
        fx.add(0.0, X.buzz(1.5), 0.6)
        fx.add(vt.T("strike") - 0.05, X.thunder(32), 0.9)
        fx.add(vt.T("one") , X.impact(33, 0.9), 0.6)
        fx.add(vt.T("bed"), X.impact(14, 0.4), 0.5)
        fx.add(vt.T("look"), X.skitter(2.0, 1), 0.5)
        fx.add(total - 2.0, X.riser(2.0, 70), 0.45)             # riser lands on the loop point (frame 0)
    else:
        Mu.pad(mus, 0, total, ["Dm", "Bb", "F", "C"], "synth_strings_1", 0.35, 4)
        Mu.arp(mus, 0, total - 0.3, ["Dm", "Bb", "F", "C"], "celesta", 84, 0.35, 1)
        Mu.pad(mus, vt.T("meanwhile"), vt.T("later"), ["F", "C"], "choir_aahs", 0.3, 4)
        fx.add(0.0, X.impact(60, 0.7), 0.5)
        fx.add(vt.T("crashing") if any(w.lower().startswith("crashing") for _, w in vt.words) else 5, X.impact(61, 0.8), 0.5)
        fx.add(vt.T("odisha") if any("odisha" in w.lower() for _, w in vt.words) else 13, X.pop(700), 0.5)
        fx.add(total - 2.0, X.riser(2.0, 71), 0.4)
