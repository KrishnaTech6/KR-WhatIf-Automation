"""Short + Reel plans for 'What If India's Population Started Shrinking?' (engine: krwi.vertical).
Each scene: scene(start_in_vertical, main_video_time, cx, zoom). vt.T("word") = time of that word in the Short/Reel."""
from krwi.vertical import scene
from krwi.timeline import T as MT, at as MAT, B as MB, E as ME  # noqa: F401  main-video times

HOOK = {"short": "-20 CRORE INDIANS", "reel": "6 KIDS. NOW 1."}
SUB = {"short": "NO WAR. JUST FEWER BABIES", "reel": "YOUR FAMILY PHOTO IS SHRINKING"}
FIX = {"k": "KR'S", "r's": "", "twenty-one": "2100", "hundred": "", "six": "6", "two": "2", "five": "5",
       "twenty": "", "crore": "20 CRORE", "sixties": "2060s"}
FULL = 1080 / 1920   # Krishna (13 Nov): show the whole frame in the verticals, never crop
CAPTIONS = "standard"  # the last video used bold; these verticals are story-led

SIX, CLS = "sixties", "classroom"


def plan_short(vt):
    w = vt.T
    f0 = MT(SIX, "twenty", 2) + 0.5                                              # -20 CRORE stamp, people peel away
    return [
        scene(0.0, f0, cx=960, zoom=FULL),
        scene(w("a"), MT("today", "indias") + 0.8, cx=960, zoom=FULL),            # India 1.9 falls below the line
        scene(w("you"), MT("today", "replace") + 0.3, cx=960, zoom=FULL),         # mum + dad -> 2 kids
        scene(w("were"), MT("today", "below") + 0.2, cx=960, zoom=FULL),
        scene(w("so"), MT("today", "heres") + 0.6, cx=960, zoom=FULL),            # myth card
        scene(w("because"), MT("today", "think") + 0.4, cx=960, zoom=FULL),       # the long train
        scene(w("but"), MT(SIX, "india") + 0.8, cx=960, zoom=FULL),               # peak graph
        scene(w("then"), MT(SIX, "next") + 0.2, cx=960, zoom=FULL),               # fewer, then fewer
        scene(w("no", 3), MT("hook", "keep") + 0.6, cx=960, zoom=FULL),           # India shrinking
        scene(w("and", 2), MT(CLS, "not") + 0.1, cx=960, zoom=FULL),                 # hospital x, classroom circled
        scene(w("full"), MT(CLS, "the", 2) + 0.4, cx=960, zoom=FULL),             # the bell, nobody left
        scene(w("because", 2), f0 - 0.6, cx=960, zoom=FULL),                      # loop back to frame 0
    ]


def plan_reel(vt):
    w = vt.T
    return [
        scene(0.0, MT("hook", "six") + 0.4, cx=960, zoom=FULL),                   # nani's photo, 6 kids
        scene(w("in", 2), MT("hook", "yours") + 0.7, cx=960, zoom=FULL),             # both photos
        scene(w("fewer"), MT(CLS, "and") + 0.6, cx=960, zoom=FULL),               # desks emptying
        scene(w("japan"), MT(CLS, "japan") + 0.2, cx=960, zoom=FULL),
        scene(w("some"), MT(CLS, "some") + 0.1, cx=960, zoom=FULL),               # the last two students
        scene(w("the", 2), MT(CLS, "the", 2) + 0.1, cx=960, zoom=FULL),           # the bell
        scene(w("india"), MT("hook", "keep") + 0.5, cx=960, zoom=FULL),           # India shrinking
        scene(w("but"), MT("twist", "shrinking") + 0.6, cx=960, zoom=FULL),       # cities pinned, not named
        scene(w("full"), ME("payoff") + 0.8, cx=960, zoom=FULL),
    ]
