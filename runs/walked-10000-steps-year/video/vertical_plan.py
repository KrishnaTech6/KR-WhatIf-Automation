"""Short + Reel plans for 'What If You Walked 10,000 Steps Every Day for a Year?' (engine: krwi.vertical).
Each scene: scene(start_in_vertical, main_video_time, cx, zoom). vt.T("word") = time of that word in the Short/Reel.
Whole frame always (never crop the verticals). The Short loops: its last frame is its first frame.
Short = shock (the scale barely moves + the 10,000 myth); Reel = feeling (11:50 PM pacing, the quiet change).
Neither reveals the brain twist."""
from krwi.vertical import scene
from krwi.timeline import T as MT, B as MB, E as ME  # noqa: F401  main-video times

HOOK = {"short": "WALK MORE, LOSE MORE?", "reel": "9,990 STEPS. 11:50 PM."}
SUB = {"short": "1 YEAR OF WALKING", "reel": "10,000 A DAY FOR A YEAR"}
FIX = {"two": "2", "k": "KR'S", "r's": ""}
FULL = 1080 / 1920
CAPTIONS = "bold"   # fact-led Short; the last video (Maggi) used standard captions


def plan_short(vt):
    w = vt.T
    F = dict(cx=960, zoom=FULL)
    return [
        scene(0.0, MT("hook", "barely") - 0.2, **F),                           # frame 0: the scale under the sneakers
        scene(w("walk") - 0.2, MT("day_one", "hour") - 0.4, **F),              # the clock: 1.5-2 hours
        scene(w("every") - 0.3, MT("day_one", "walking", 1) - 1.5, **F),       # 25 full days a year
        scene(w("on") - 0.2, MT("year_one", "almost") - 1.6, **F),             # on paper: ~10 kg
        scene(w("in") - 0.2, MT("year_one", "roughly") + 0.3, **F),            # the scale: -2.5 kg
        scene(w("because") - 0.2, MT("year_one", "hadza") - 0.2, **F),         # the Hadza at sunset
        scene(w("they") - 0.2, MT("year_one", "same") - 0.6, **F),             # same calories
        scene(w("and") - 0.2, MT("week_one", "why") - 0.2, **F),               # WHY 10,000?
        scene(w("pedometer") - 0.8, MT("week_one", "manpokei") - 0.2, **F),    # the Manpo-kei box
        scene(w("but") - 0.2, MT("hook", "grew") - 0.6, **F),                  # the head glows (no reveal)
        scene(w("full") - 0.2, MT("week_one", "advert") - 0.5, **F),           # the meme beat
        scene(w("exactly") - 0.2, MT("hook", "barely") - 0.6, rate=0.5, **F),  # loop -> frame 0
    ]


def plan_reel(vt):
    w = vt.T
    F = dict(cx=960, zoom=FULL)
    return [
        scene(0.0, MT("day_one", "nine") + 0.2, **F),                          # frame 0: 9,990 on the phone
        scene(w("your") - 0.2, MT("day_one", "eleven") + 0.6, **F),            # pacing the bedroom
        scene(w("because") - 0.2, MT("promise", "ten") + 0.2, **F),            # the 10,000 goal
        scene(w("month") - 0.2, MT("month_one", "few") + 0.3, **F),            # the scale, -0.3 kg
        scene(w("friend") - 0.3, MT("month_one", "walking") - 0.2, **F),       # friend laughs
        scene(w("but") - 0.2, MT("month_one", "dinner") - 0.5, **F),           # walking after dinner
        scene(w("calls") - 0.3, MT("month_three", "calls") - 0.2, **F),        # calls while walking, no lift
        scene(w("and", 2) - 0.2, MT("month_three", "less") - 0.6, **F),           # the cloud shrinks
        scene(w("by") - 0.2, MT("hook", "grew") - 0.8, **F),                   # something grew (no reveal)
        scene(w("full") - 0.2, MT("bonus", "happens") + 0.4, **F),             # out for a walk at dusk
    ]
