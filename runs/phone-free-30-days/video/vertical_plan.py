"""Short + Reel plans for 'What If You Didn't Use Your Phone for 30 Days?' (engine: krwi.vertical).
Each scene: scene(start_in_vertical, main_video_time, cx, zoom). vt.T("word") = time of that word in the Short/Reel.
Whole frame always (Krishna, 13 Nov: never crop the verticals)."""
from krwi.vertical import scene
from krwi.timeline import T as MT, B as MB, E as ME  # noqa: F401  main-video times

HOOK = {"short": "30 DAYS. NO PHONE.", "reel": "+150 HOURS OF YOUR LIFE"}
SUB = {"short": "DAY 2: LOST IN YOUR CITY", "reel": "30 DAYS WITHOUT YOUR PHONE"}
FIX = {"thirty": "30", "two": "2", "nine": "9", "ten": "10", "eighty-nine": "89", "percent": "%",
       "fourteen": "14", "six": "6", "seven": "7", "k": "KR'S", "r's": ""}
FULL = 1080 / 1920
CAPTIONS = "standard"   # UPI (last video) used bold; never two in a row


def plan_short(vt):
    w = vt.T
    return [
        scene(0.0, 0.4, cx=960, zoom=FULL),                                        # frame 0: rooftop, no phone
        scene(w("no"), MT("day_two", "maps") - 0.4, cx=960, zoom=FULL),           # lost on the street
        scene(w("train"), MT("day_two", "nine") - 0.3, cx=960, zoom=FULL),        # 9 in 10 tickets online
        scene(w("never"), MT("day_two", "never") - 0.2, cx=960, zoom=FULL),
        scene(w("wallet"), MT("day_two", "wallet") + 0.3, cx=960, zoom=FULL),
        scene(w("cash"), MT("day_two", "cash") - 0.1, cx=960, zoom=FULL),
        scene(w("brain"), MT("hour_one", "nothing") - 0.2, cx=960, zoom=FULL),    # empty pocket
        scene(w("leg"), MT("hour_one", "buzzes") - 0.3, cx=960, zoom=FULL),
        scene(w("phantom"), MT("hour_one", "study") - 0.2, cx=960, zoom=FULL),    # 89%
        scene(w("trained"), MT("hour_one", "making") - 0.8, cx=960, zoom=FULL),
        scene(w("fourteen"), MT("day_fourteen", "strange") - 0.4, cx=960, zoom=FULL),
        scene(w("full"), MT("hook", "inside") - 0.3, cx=960, zoom=FULL),
        scene(w("think"), 0.2, cx=960, zoom=FULL),                                # loop back to frame 0
    ]


def plan_reel(vt):
    w = vt.T
    return [
        scene(0.0, 0.5, cx=960, zoom=FULL),                                        # frame 0: +150 HOURS
        scene(w("six"), MT("hook", "six") - 0.3, cx=960, zoom=FULL),              # 6 day tiles
        scene(w("first"), MT("day_seven", "metro") - 0.2, cx=960, zoom=FULL),
        scene(w("shampoo") - 0.4, MT("day_seven", "shampoo") - 0.4, cx=960, zoom=FULL),
        scene(w("somewhere"), MT("day_seven", "look") - 0.5, cx=960, zoom=FULL),
        scene(w("call"), MT("day_seven", "conversation") - 0.4, cx=960, zoom=FULL),
        scene(w("fourteen"), MT("day_fourteen", "strange") - 0.4, cx=960, zoom=FULL),
        scene(w("full", 2), MT("day_thirty", "six") + 0.2, cx=960, zoom=FULL),    # 6 days handed back
    ]
