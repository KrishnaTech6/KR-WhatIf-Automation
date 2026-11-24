"""Short + Reel plans for 'What If Every Indian Got Rs 1 Crore Tomorrow?' (engine: krwi.vertical).
Each scene: scene(start_in_vertical, main_video_time, cx, zoom). vt.T("word") = time of that word in the Short/Reel."""
from krwi.vertical import scene
from krwi.timeline import T as MT, B as MB, E as ME  # noqa: F401  main-video times

HOOK = {"short": "₹1 CRORE → ₹2 LAKH", "reel": "₹1 CRORE. NO MILK."}
SUB = {"short": "AND NOBODY STOLE IT", "reel": "EVERY INDIAN GOT ONE"}
FIX = {"k": "", "r's": "KR's", "one": "1", "two": "2", "eight": "8", "m": "", "r": "", "b": "", "i": "",
       "rbi": "RBI"}
FULL = 1080 / 1920   # Krishna (13 Nov): show the whole frame in the verticals, never crop
CAPTIONS = "standard"  # bold was used on the last two videos


def plan_short(vt):
    w = vt.T
    reveal = MT("week_two", "two", 2) + 0.5            # "≈ ₹2 LAKH" on screen
    return [
        scene(0.0, reveal, cx=960, zoom=FULL),                                     # frame 0: ₹1 CRORE ≈ ₹2 LAKH
        scene(w("every"), MT("hook", "not") + 0.8, cx=960, zoom=FULL),            # phones light up across India
        scene(w("your", 2), 0.6, cx=960, zoom=FULL),                              # the phone buzzing, CREDITED
        scene(w("your", 3), MT("hook", "all") + 0.4, cx=960, zoom=FULL),          # 146 CRORE
        scene(w("by"), MT("hour_six", "crowd") + 0.3, cx=960, zoom=FULL),         # showroom crowd
        scene(w("manager"), MT("hour_six", "changes") - 0.3, cx=960, zoom=FULL),  # the price tag swap
        scene(w("because"), MT("week_two", "fortyseven") - 0.2, cx=960, zoom=FULL),  # money ×47
        scene(w("but"), MT("week_two", "same") - 0.1, cx=960, zoom=FULL),         # the scale tips
        scene(w("so", 2), MT("week_two", "prices") - 0.1, cx=960, zoom=FULL),     # tomato tag racing up
        scene(w("thats"), MT("week_two", "why") + 0.4, cx=960, zoom=FULL),        # the notebook question
        scene(w("and", 2), MT("hook", "loses") - 0.1, cx=960, zoom=FULL),         # paper house + red question mark
        scene(w("because", 2), reveal - 0.3, cx=960, zoom=FULL),                  # loop back into frame 0
    ]


def plan_reel(vt):
    w = vt.T
    return [
        scene(0.0, MT("day_three", "milk") + 0.3, cx=960, zoom=FULL),              # frame 0: dry bread, EMPTY milk
        scene(w("every"), MT("hook", "not") + 0.8, cx=960, zoom=FULL),
        scene(w("you"), MT("hour_one", "call") + 0.2, cx=960, zoom=FULL),          # the phone call split
        scene(w("planning"), MT("hour_one", "wedding") + 0.2, cx=960, zoom=FULL),  # blank wedding card
        scene(w("day"), MT("day_three", "doorbell") - 0.2, cx=960, zoom=FULL),     # empty doorstep
        scene(w("didi"), MT("day_three", "she") + 0.2, cx=960, zoom=FULL),
        scene(w("no"), MT("day_three", "delivery") + 1.4, cx=960, zoom=FULL),      # rider dots blink out
        scene(w("no", 2), MT("day_three", "gone") + 0.1, cx=960, zoom=FULL),       # sabzi cart GONE
        scene(w("youre"), MT("day_three", "youre") + 0.4, cx=960, zoom=FULL),      # crorepati breakfast
        scene(w("because"), MT("day_three", "promise") - 0.2, cx=960, zoom=FULL),  # note tied to hands
        scene(w("and"), MT("hook", "loses") - 0.1, cx=960, zoom=FULL),             # who loses most?
    ]
