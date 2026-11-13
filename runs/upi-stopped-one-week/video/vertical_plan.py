"""Short + Reel plans for 'What If UPI Stopped Working for One Week?' (engine: krwi.vertical).
Each scene: scene(start_in_vertical, main_video_time, cx, zoom). vt.T("word") = time of that word in the Short/Reel."""
from krwi.vertical import scene
from krwi.timeline import T as MT, B as MB, E as ME  # noqa: F401  main-video times

HOOK = {"short": "7 DAYS. NO UPI.", "reel": "DAY 3 WITHOUT UPI"}
SUB = {"short": "NOT EVEN A ₹10 CHAI", "reel": "YOUR SABZIWALA IS BROKE"}
FIX = {"u": "UPI", "p": "", "i": "", "q": "QR", "r": "", "k": "KR'S", "r's": "",
       "seven": "7", "three": "3", "ten": "₹10", "rupee": "", "eighty-two": "82", "twenty": "20", "fifty": "50"}
FULL = 1080 / 1920   # Krishna (13 Nov): show the whole frame in the verticals, never crop
CAPTIONS = "bold"     # Short/Reel are number-led this time; the last video used standard captions


def plan_short(vt):
    w = vt.T
    return [
        scene(0.0, 0.4, cx=960, zoom=FULL),                                        # frame 0: PAYMENT FAILED
        scene(w("eighty-two"), MT("hook", "not") + 0.4, cx=960, zoom=FULL),
        scene(w("you", 2), MT("minute_one", "switch") + 0.4, cx=960, zoom=FULL),
        scene(w("because"), MT("minute_one", "behind") + 0.6, cx=960, zoom=FULL),
        scene(w("and", 2), MT("minute_one", "change") + 0.2, cx=960, zoom=FULL),
        scene(w("so"), MT("hour_three", "twenty") - 0.6, cx=960, zoom=FULL),
        scene(w("by"), MT("hour_three", "temporarily") - 0.3, cx=960, zoom=FULL),
        scene(w("your"), MT("night_one", "upi") + 0.8, cx=960, zoom=FULL),
        scene(w("but"), MT("night_one", "no") + 0.4, cx=960, zoom=FULL),
        scene(w("by", 2), MT("day_three", "sorry") + 0.2, cx=960, zoom=FULL),
        scene(w("and", 4), MT("day_three", "sabziwala") + 0.4, cx=960, zoom=FULL),
        scene(w("full"), MT("hook", "person") + 0.2, cx=960, zoom=FULL),
        scene(w("because", 2), 0.2, cx=960, zoom=FULL),                             # loop back to frame 0
    ]


def plan_reel(vt):
    w = vt.T
    return [
        scene(0.0, MT("day_three", "today") + 1.2, cx=960, zoom=FULL),
        scene(w("he"), MT("day_three", "sabziwala") + 0.3, cx=960, zoom=FULL),
        scene(w("but"), MT("day_three", "his") + 0.5, cx=960, zoom=FULL),
        scene(w("so"), MT("day_three", "today") + 2.2, cx=960, zoom=FULL),
        scene(w("delivery"), MT("day_five", "delivery") + 0.3, cx=960, zoom=FULL),
        scene(w("cook"), MT("day_five", "cook") + 0.3, cx=960, zoom=FULL),
        scene(w("thats"), MT("day_five", "this") + 0.3, cx=960, zoom=FULL),
        scene(w("so", 2), MB("day_seven") - 0.4, cx=960, zoom=FULL),
        scene(w("full"), ME("payoff") + 0.8, cx=960, zoom=FULL),
    ]
