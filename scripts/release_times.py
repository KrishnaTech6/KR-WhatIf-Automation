"""Release times for one video, from settings.json "release_schedule".

  python scripts/release_times.py <slug> [--now 2026-11-13T10:00:00Z]

Prints JSON: each video's publish_at in UTC (for upload.json) and in IST (for upload_text.txt).

Rule (Krishna, 13 Nov 2026): main first, so the Short and Reel can point viewers to it.
  D1 = first day whose main slot is at least 1 h away and where neither D1 nor D2
       already has another video's release (runs/*/published.json), so no day gets two.
  D2 = the day after D1.
Each slot then moves a few minutes past its hour (settings "release_jitter_minutes", e.g. 9:03,
6:11), so uploads don't land on round times (Krishna, 14 Nov 2026). The minute comes from the
slug, so re-running for the same video gives the same times.
"""
import hashlib
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

IST = timezone(timedelta(hours=5, minutes=30))
ROOT = Path(__file__).resolve().parent.parent


def parse(at):
    return datetime.fromisoformat(at.replace("Z", "+00:00"))


def busy_days(slug):
    """IST dates that already carry a release of another video."""
    days = set()
    for f in ROOT.glob("runs/*/published.json"):
        if f.parent.name == slug:
            continue
        pub = json.loads(f.read_text())
        for rec in [pub.get("main")] + pub.get("shorts", []):
            if rec and rec.get("publish_at"):
                days.add(parse(rec["publish_at"]).astimezone(IST).date())
    return days


def slot(day, spec):
    """'D2 09:00' on D1 = day -> aware IST datetime."""
    d, hm = spec.split()
    h, m = map(int, hm.split(":"))
    return datetime(day.year, day.month, day.day, h, m, tzinfo=IST) + timedelta(days=int(d[1:]) - 1)


def jitter(slug, name, lo, hi):
    """Stable minute offset in [lo, hi] for this video's slot."""
    h = int(hashlib.sha256(f"{slug}:{name}".encode()).hexdigest(), 16)
    return timedelta(minutes=lo + h % (hi - lo + 1))


def release_times(slug, now):
    settings = json.loads((ROOT / "settings.json").read_text())
    sched = settings["release_schedule"]
    lo, hi = settings.get("release_jitter_minutes", [0, 0])
    busy = busy_days(slug)
    day = now.astimezone(IST).date()
    for _ in range(30):
        main = slot(day, sched["main"])
        if main >= now + timedelta(hours=1) and not {day, day + timedelta(days=1)} & busy:
            return {name: slot(day, spec) + jitter(slug, name, lo, hi) for name, spec in sched.items()}
        day += timedelta(days=1)
    sys.exit("no free release days in the next 30 days")


if __name__ == "__main__":
    args = sys.argv[1:]
    now = parse(args[args.index("--now") + 1]) if "--now" in args else datetime.now(timezone.utc)
    times = release_times(args[0], now)
    print(json.dumps({
        "utc": {k: v.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") for k, v in times.items()},
        "ist": {k: v.strftime("%a %d %b, %I:%M %p IST") for k, v in times.items()},
    }, indent=1))
