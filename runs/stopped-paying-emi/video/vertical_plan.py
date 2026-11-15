"""Short + Reel plans for 'What If You Stopped Paying Your EMI?' (engine: krwi.vertical).
Each scene: scene(start_in_vertical, main_video_time, cx, zoom). vt.T("word") = time of that word in the Short/Reel."""
from krwi.vertical import scene
from krwi.timeline import T as MT, at as MAT, B as MB, E as ME  # noqa: F401  main-video times

HOOK = {"short": "NO EMI = 91 DAYS", "reel": "HE NEVER BORROWED ₹1"}
SUB = {"short": "DAY BY DAY, BY RBI RULES", "reel": "BUT THE BANK CALLS HIM"}
FIX = {"k": "KR'S", "r's": "", "e": "", "m": "", "i": "EMI", "r": "", "b": "", "ninety-one": "91", "thirty-one": "31",
       "thirty": "30", "one": "1", "eight": "8", "seven": "7", "ninety": "90"}
FULL = 1080 / 1920   # Krishna (13 Nov): show the whole frame in the verticals, never crop
CAPTIONS = {"short": "bold", "reel": "standard"}   # Short is a fact-led day-by-day list; the Reel is a story


def plan_short(vt):
    w = vt.T
    f0 = 1.0
    return [
        scene(0.0, f0, cx=960, zoom=FULL),                                              # house + AUCTION?
        scene(w("in"), MT("hook", "in") + 0.6, cx=960, zoom=FULL),                      # Day 91 calendar
        scene(w("day"), MT("day_one", "computer") + 0.3, cx=960, zoom=FULL),           # OVERDUE
        scene(w("day", 2), MT("day_thirty", "lights") + 0.5, cx=960, zoom=FULL),       # missed calls pile up
        scene(w("but"), MT("day_thirty", "eight") + 0.3, cx=960, zoom=FULL),           # 8 AM - 7 PM clock
        scene(w("day", 3), MT("day_thirty_one", "s") + 0.3, cx=960, zoom=FULL),        # SMA-1
        scene(w("and"), MT("day_thirty_one", "seven") + 0.2, cx=960, zoom=FULL),       # 7 years
        scene(w("day", 4), MT("day_ninety_one", "n") + 0.3, cx=960, zoom=FULL),        # NPA stamp
        scene(w("then"), MT("month_four", "sixty") + 0.2, cx=960, zoom=FULL),          # the letter
        scene(w("then", 2), MT("month_six", "bank") + 0.5, cx=960, zoom=FULL),         # officers at the door
        scene(w("then", 3), MT("month_six", "newspapers") + 0.3, cx=960, zoom=FULL),   # name in the paper
        scene(w("and", 2), MT("hook", "paper") + 0.2, cx=960, zoom=FULL),              # the circled signature
        scene(w("and", 3), f0 - 0.6, cx=960, zoom=FULL),                                # loop back to frame 0
    ]


def plan_reel(vt):
    w = vt.T
    return [
        scene(0.0, MT("day_sixty", "rings") + 0.3, cx=960, zoom=FULL),                 # dad's phone ringing
        scene(w("years"), MT("day_sixty", "guarantor") + 0.2, cx=960, zoom=FULL),     # GUARANTOR signature
        scene(w("now"), 1.0, cx=960, zoom=FULL),                                        # the house, EMI stopped
        scene(w("and"), MT("day_sixty", "owes") - 0.3, cx=960, zoom=FULL),             # bank -> both gauges
        scene(w("his"), MT("day_sixty", "never") + 0.3, cx=960, zoom=FULL),            # BORROWED 0 / OWES ALL
        scene(w("and", 2), MT("hook", "paper") + 0.4, cx=960, zoom=FULL),              # the scariest paper
        scene(w("full"), ME("payoff") + 0.8, cx=960, zoom=FULL),
    ]
