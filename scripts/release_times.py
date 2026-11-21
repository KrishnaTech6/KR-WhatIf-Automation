"""Release times for one video: main every 2nd day, one Short/Reel every day, random test times (Krishna, 21 Nov 2026).

  python3 scripts/release_times.py <slug> [--now 2026-11-27T10:00:00Z]          # preview, changes nothing
  python3 scripts/release_times.py <slug> --save                                 # book the times (do this at publish)

Prints JSON with five times, in UTC (for upload.json / run_once_at) and IST (for upload_text.txt and messages):
  main      YouTube main video
  short_yt  the Short on YouTube Shorts      short_ig  the Short on Instagram
  reel_yt   the Reel on YouTube Shorts       reel_ig   the Reel on Instagram

Days (settings "release_plan"):
  D1 (main) = the later of today and the last booked main + main_every_days (2), on a day with no other main.
  Short = D1 + short_day (1), Reel = D1 + reel_day (2); a day that already has a Short/Reel moves it to the
  next free day, so exactly one vertical goes out per day and it always comes after its main video.
Times (settings "time_test"): each post gets a random minute inside one of the active-hour windows (IST),
picked per track (YouTube main, YouTube Shorts, Instagram), so YouTube and Instagram get separate times.
  Exploring: the window with the fewest booked posts on that track (ties at random).
  Once every window has min_tests measured posts: exploit_share of posts go to the best window, the rest test others.
Booked times live on the time-test branch (scripts/time_test.py), so every session sees one calendar.
Once booked, re-running for the same slug prints the same times.
"""
import json
import random
import sys
from datetime import datetime, timedelta, timezone

from time_test import IST, best_window, cfg, load, parse, settings, update, window_of, window_stats, windows

NAMES = {("main", "yt_main"): "main", ("short", "yt_short"): "short_yt", ("short", "ig"): "short_ig",
         ("reel", "yt_short"): "reel_yt", ("reel", "ig"): "reel_ig"}


def pick_window(data, track, rng, not_before_min=0):
    """A window with at least 20 usable minutes after not_before_min (IST minute of the day), or None."""
    cand = [w for w, a, b in windows() if b - max(a, not_before_min) >= 20]
    if not cand:
        return None
    best = best_window(data, track)
    if best in cand and rng.random() < cfg()["exploit_share"]:
        return best
    pool = [w for w in cand if w != best] or cand
    st = window_stats(data, track)
    least = min(st[w]["planned"] for w in pool)
    return rng.choice([w for w in pool if st[w]["planned"] == least])


def random_time(day, w, rng, not_before_min=0):
    a, b = next((a, b) for n, a, b in windows() if n == w)
    mins = [m for m in range(max(a, not_before_min), b) if m % 30]      # never exactly :00 or :30
    m = rng.choice(mins)
    return datetime(day.year, day.month, day.day, m // 60, m % 60, tzinfo=IST)


def book(data, slug, kind, track, at):
    data["plan"].append({"slug": slug, "kind": kind, "track": track,
                         "at": at.isoformat(timespec="minutes"), "window": window_of(at)})


def plan_video(slug, now, data):
    mine = [p for p in data["plan"] if p["slug"] == slug]
    if mine:
        return mine
    rp = settings()["release_plan"]
    rng = random.Random(slug)
    today = now.astimezone(IST).date()
    lead = now + timedelta(minutes=rp["lead_minutes"])
    days = lambda tracks: {parse(p["at"]).astimezone(IST).date() for p in data["plan"] if p["track"] in tracks}
    mains = days({"yt_main"})
    day = max([today] + [d + timedelta(days=rp["main_every_days"]) for d in mains])
    for _ in range(60):
        nb = lead.astimezone(IST).hour * 60 + lead.astimezone(IST).minute + 1 if day == lead.astimezone(IST).date() else 0
        w = None if (day in mains or day < lead.astimezone(IST).date()) else pick_window(data, "yt_main", rng, nb)
        if w:
            book(data, slug, "main", "yt_main", random_time(day, w, rng, nb))
            break
        day += timedelta(days=1)
    else:
        sys.exit("no free main day in the next 60 days")
    d1, last = day, day
    for kind, offset in (("short", rp["short_day"]), ("reel", rp["reel_day"])):
        d = max(d1 + timedelta(days=offset), last + timedelta(days=1))
        while d in days({"yt_short", "ig"}):
            d += timedelta(days=1)
        for track in ("yt_short", "ig"):
            book(data, slug, kind, track, random_time(d, pick_window(data, track, rng), rng))
        last = d
    return [p for p in data["plan"] if p["slug"] == slug]


def show(posts):
    t = {NAMES[(p["kind"], p["track"])]: parse(p["at"]) for p in posts}
    order = ["main", "short_yt", "short_ig", "reel_yt", "reel_ig"]
    return {"utc": {k: t[k].astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") for k in order if k in t},
            "ist": {k: t[k].astimezone(IST).strftime("%a %d %b, %I:%M %p IST") for k in order if k in t},
            "window": {k: window_of(t[k]) for k in order if k in t}}


if __name__ == "__main__":
    args = sys.argv[1:]
    slug = args[0]
    now = parse(args[args.index("--now") + 1]) if "--now" in args else datetime.now(timezone.utc)
    if "--save" in args:
        saved = update(lambda d: plan_video(slug, now, d), f"time-test: book {slug}")
        posts = [p for p in saved["plan"] if p["slug"] == slug]
    else:
        posts = plan_video(slug, now, load())
    print(json.dumps(show(posts), indent=1))
