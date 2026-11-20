"""Short + Reel plans for 'What If You Woke Up at 5 AM for 30 Days?' (engine: krwi.vertical).
Each scene: scene(start_in_vertical, main_video_time, cx, zoom). vt.T("word") = time of that word in the Short/Reel.
Whole frame always (Krishna, 13 Nov: never crop the verticals). anchors_*.json: 'A M' merged into 'AM' for captions."""
from krwi.vertical import scene
from krwi.timeline import T as MT, B as MB, E as ME  # noqa: F401  main-video times

HOOK = {"short": "6 HOURS × 2 WEEKS", "reel": "5 AM. TOTAL SILENCE."}
SUB = {"short": "= 2 NIGHTS NO SLEEP?", "reel": "30 DAYS OF 5 AM"}
FIX = {"six": "6", "two": "2", "five": "5", "eleven": "11", "k": "", "r's": "KR's"}
FULL = 1080 / 1920
CAPTIONS = "bold"   # fact-led Short; last two videos used standard


def plan_short(vt):
    w = vt.T
    return [
        scene(0.0, MT("hook", "fourteen") + 1.6, cx=960, zoom=FULL),               # 15% vs 100% batteries
        scene(w("scientists"), MT("the_big_one", "thousand") + 0.4, cx=960, zoom=FULL),  # sleep lab
        scene(w("reactions"), MT("the_big_one", "slower") + 0.4, cx=960, zoom=FULL),     # reaction test
        scene(w("creepy"), MT("the_big_one", "scariest") + 1.6, cx=960, zoom=FULL),      # felt vs performed
        scene(w("look"), MT("promise", "alarm") + 0.4, cx=960, zoom=FULL),               # the 5:00 clock
        scene(w("phone"), MT("day_three", "bed") + 0.2, cx=960, zoom=FULL),              # phone in bed 11:40
        scene(w("hours", 3), MT("day_three", "night") + 1.6, cx=960, zoom=FULL),         # 6-hour bar
        scene(w("everyone"), MT("day_seven", "trap") - 0.2, cx=960, zoom=FULL),          # I FEEL FINE
        scene(w("fix"), MT("hook", "difference") + 0.6, cx=960, zoom=FULL),              # one difference
        scene(w("because"), MT("day_three", "alarm") + 0.6, cx=960, zoom=FULL),          # 5:00 AM vs 11:00 PM -> loop
    ]


def plan_reel(vt):
    w = vt.T
    return [
        scene(0.0, MT("day_one", "house") + 0.6, cx=960, zoom=FULL),                     # silent room, 5:00 AM
        scene(w("delhi"), MT("day_one", "dark") + 1.2, cx=960, zoom=FULL),               # dark Delhi, sunrise 6:47
        scene(w("week"), MT("day_seven", "fine") + 0.4, cx=960, zoom=FULL),              # 7/30, feeling fine
        scene(w("one", 2), MT("day_three", "night") + 1.6, cx=960, zoom=FULL),           # the missing hour
        scene(w("sharper"), MT("payoff", "drains") + 0.4, cx=960, zoom=FULL),            # drained vs sharp
        scene(w("alarm"), MT("hook", "difference") + 0.6, cx=960, zoom=FULL),            # spot the difference
        scene(w("full"), MT("bonus", "five") + 0.6, cx=960, zoom=FULL),                  # both rooms, already awake
    ]
