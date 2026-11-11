"""What is working on YouTube: stats for every public upload -> learn/youtube.json + yt_learnings.md.

  python scripts/youtube_learn.py             # run by the learn-youtube workflow (needs the YT_* secrets)
  python scripts/youtube_learn.py --offline   # rebuild yt_learnings.md from learn/youtube.json (no API)

Public counts (views, likes, comments) work with the upload login. Retention curves, average % viewed and
thumbnail click-through need the read-only analytics permission (yt-analytics.readonly): run
scripts/youtube_auth.py once more and replace the YT_REFRESH_TOKEN secret. Until then the file says so.

The script stage reads yt_learnings.md before writing, so each new hook and structure learns from where
real viewers left the last videos.
"""
import json
import os
import re
import statistics
import sys
from datetime import date, datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "learn", "youtube.json")
OUT = os.path.join(ROOT, "yt_learnings.md")
SHORT_MAX = 180          # seconds; longer = a main video


# ---------------------------------------------------------------- fetching (needs google-api-python-client)
def _creds():
    from google.oauth2.credentials import Credentials
    # no scopes here: the access token gets whatever the refresh token was granted
    return Credentials(None, refresh_token=os.environ["YT_REFRESH_TOKEN"], token_uri="https://oauth2.googleapis.com/token",
                       client_id=os.environ["YT_CLIENT_ID"], client_secret=os.environ["YT_CLIENT_SECRET"])


def _secs(iso):
    m = re.match(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    d, h, mi, s = (int(x or 0) for x in m.groups())
    return d * 86400 + h * 3600 + mi * 60 + s


def fetch():
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    creds = _creds()
    yt = build("youtube", "v3", credentials=creds, cache_discovery=False)
    ch = yt.channels().list(part="contentDetails,snippet,statistics", mine=True).execute()["items"][0]
    uploads = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    ids, tok = [], None
    while True:
        r = yt.playlistItems().list(part="contentDetails", playlistId=uploads, maxResults=50, pageToken=tok).execute()
        ids += [i["contentDetails"]["videoId"] for i in r["items"]]
        tok = r.get("nextPageToken")
        if not tok:
            break
    videos = []
    for k in range(0, len(ids), 50):
        r = yt.videos().list(part="snippet,statistics,contentDetails,status", id=",".join(ids[k:k + 50])).execute()
        for v in r["items"]:
            if v["status"]["privacyStatus"] != "public":
                continue
            st = v.get("statistics", {})
            videos.append(dict(id=v["id"], title=v["snippet"]["title"], published=v["snippet"]["publishedAt"],
                               duration=_secs(v["contentDetails"]["duration"]),
                               views=int(st.get("viewCount", 0)), likes=int(st.get("likeCount", 0)),
                               comments=int(st.get("commentCount", 0))))
    out = dict(fetched=datetime.now(timezone.utc).isoformat(timespec="minutes"), channel=ch["snippet"]["title"],
               subscribers=int(ch["statistics"].get("subscriberCount", 0)), analytics=None, ctr=None, videos=videos)

    ya = build("youtubeAnalytics", "v2", credentials=creds, cache_discovery=False)
    q = dict(ids="channel==MINE", startDate="2020-01-01", endDate=date.today().isoformat())
    by_id = {v["id"]: v for v in videos}
    try:
        r = ya.reports().query(**q, dimensions="video", maxResults=200, sort="-views",
                               metrics="views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,"
                                       "likes,shares,subscribersGained").execute()
        cols = [c["name"] for c in r["columnHeaders"]]
        for row in r.get("rows", []):
            d = dict(zip(cols, row))
            if d["video"] in by_id:
                by_id[d["video"]].update(avg_view_pct=d["averageViewPercentage"], avg_view_s=d["averageViewDuration"],
                                         shares=d["shares"], subs_gained=d["subscribersGained"])
        out["analytics"] = "ok"
    except HttpError as e:
        out["analytics"] = f"HTTP {e.resp.status}: needs the yt-analytics.readonly permission (re-run scripts/youtube_auth.py)" \
            if e.resp.status in (401, 403) else f"HTTP {e.resp.status}"
    if out["analytics"] == "ok":
        try:
            r = ya.reports().query(**q, dimensions="video", maxResults=200, sort="-videoThumbnailImpressions",
                                   metrics="videoThumbnailImpressions,videoThumbnailImpressionsClickRate").execute()
            for vid, imp, ctr in r.get("rows", []):
                if vid in by_id:
                    by_id[vid].update(impressions=imp, ctr=ctr)
            out["ctr"] = "ok"
        except HttpError as e:
            out["ctr"] = f"not available from the API (HTTP {e.resp.status}); see YouTube Studio -> Analytics -> Reach"
        for v in videos:
            try:
                r = ya.reports().query(**q, dimensions="elapsedVideoTimeRatio", filters=f"video=={v['id']}",
                                       metrics="audienceWatchRatio,relativeRetentionPerformance").execute()
                v["retention"] = [[round(a, 2), round(b, 4), round(c, 4)] for a, b, c in r.get("rows", [])]
            except HttpError:
                pass
    return out


# ---------------------------------------------------------------- summary (pure, testable offline)
def mmss(s):
    s = int(round(s))
    return f"{s // 60}:{s % 60:02d}"


def _at(curve, frac):
    """(watch ratio, relative performance) at a fraction of the video, nearest point."""
    if not curve:
        return None, None
    p = min(curve, key=lambda r: abs(r[0] - frac))
    return p[1], p[2]


def drops(curve, dur, n=2, skip=0.03, window=0.05):
    """Biggest falls in the retention curve: [(seconds, points of audience lost)], after the first 3%."""
    pts = [r for r in curve if r[0] >= skip]
    out = []
    for i, (x, y, _) in enumerate(pts):
        j = next((k for k in range(i, len(pts)) if pts[k][0] >= x + window), None)
        if j is not None:
            out.append((x * dur, (y - pts[j][1]) * 100))
    out.sort(key=lambda d: -d[1])
    picked = []
    for t, d in out:
        if d > 0 and all(abs(t - p[0]) > window * dur for p in picked):
            picked.append((t, d))
        if len(picked) == n:
            break
    return picked


def history():
    try:
        h = json.load(open(os.path.join(ROOT, "history.json")))["videos"]
    except Exception:
        return {}, set()
    auto = {re.sub(r"\W", "", x["title"].lower()) for x in h if x.get("slug")}
    before = {re.sub(r"\W", "", x["title"].lower()) for x in h if not x.get("slug")}
    return auto, before


def summarize(d, today=None):
    today = today or date.today()
    vids = sorted(d["videos"], key=lambda v: v["published"], reverse=True)
    for v in vids:
        age = max(1, (today - datetime.fromisoformat(v["published"].replace("Z", "+00:00")).date()).days)
        v["age"], v["per_day"] = age, v["views"] / age
    mains = [v for v in vids if v["duration"] > SHORT_MAX]
    shorts = [v for v in vids if v["duration"] <= SHORT_MAX]
    auto, before = history()
    L = [f"# YouTube learnings (auto-generated {d['fetched'][:16].replace('T', ' ')} UTC)", "",
         f"Channel: {d['channel']} · {d['subscribers']} subscribers · {len(mains)} main videos · {len(shorts)} Shorts. "
         "Made by `scripts/youtube_learn.py` (learn-youtube workflow); don't edit by hand.", ""]
    if d["analytics"] != "ok":
        L += [f"**Retention and % viewed are missing:** {d['analytics']}. Only public counts below.", ""]
    L += ["## Main videos", "",
          "| Published | Title | Views | Views/day | Avg viewed | Watching at 0:30 | vs similar at 0:30 | Biggest drops |",
          "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for v in mains:
        cur = v.get("retention") or []
        w30, r30 = _at(cur, 30 / v["duration"]) if cur else (None, None)
        dr = ", ".join(f"{mmss(t)} (-{p:.0f} pts)" for t, p in drops(cur, v["duration"])) if cur else "-"
        L.append(f"| {v['published'][:10]} | {v['title'][:52]} | {v['views']} | {v['per_day']:.1f} | "
                 f"{(str(round(v['avg_view_pct'])) + '% (' + mmss(v['avg_view_s']) + ')') if 'avg_view_pct' in v else '-'} | "
                 f"{(str(round(w30 * 100)) + '%') if w30 is not None else '-'} | "
                 f"{('above' if r30 > 0.55 else 'below' if r30 < 0.45 else 'average') + f' ({r30:.2f})' if r30 is not None else '-'} | {dr} |")
    L += ["", "## Shorts", "", "| Published | Title | Views | Views/day | Avg viewed | Likes per 1k views |", "| --- | --- | --- | --- | --- | --- |"]
    for v in shorts:
        L.append(f"| {v['published'][:10]} | {v['title'][:52]} | {v['views']} | {v['per_day']:.1f} | "
                 f"{(str(round(v['avg_view_pct'])) + '%') if 'avg_view_pct' in v else '-'} | "
                 f"{(1000 * v['likes'] / v['views']):.0f} |" if v["views"] else
                 f"| {v['published'][:10]} | {v['title'][:52]} | 0 | 0.0 | - | - |")
    if any("ctr" in v for v in vids):
        L += ["", "## Thumbnail click-through", "", "| Title | Impressions | CTR |", "| --- | --- | --- |"]
        for v in sorted((v for v in mains if "ctr" in v), key=lambda v: -v["ctr"]):
            L.append(f"| {v['title'][:52]} | {v['impressions']} | {v['ctr'] * (100 if v['ctr'] < 1 else 1):.1f}% |")
    elif d["analytics"] == "ok":
        L += ["", f"Thumbnail click-through: {d.get('ctr')}."]

    # ---- patterns (numbers only; the script stage interprets them)
    L += ["", "## Patterns", ""]
    key = lambda v: re.sub(r"\W", "", v["title"].lower())
    groups = {"autopilot pipeline": [v for v in mains if key(v) in auto],
              "before autopilot": [v for v in mains if key(v) in before or key(v) not in auto]}
    for name, g in groups.items():
        if not g:
            continue
        parts = [f"median {statistics.median(v['per_day'] for v in g):.1f} views/day"]
        pct = [v["avg_view_pct"] for v in g if "avg_view_pct" in v]
        if pct:
            parts.append(f"median {statistics.median(pct):.0f}% viewed")
        w = [_at(v["retention"], 30 / v["duration"])[0] for v in g if v.get("retention")]
        if w:
            parts.append(f"median {statistics.median(w) * 100:.0f}% still watching at 0:30")
        L.append(f"- Main videos, {name} ({len(g)}): " + ", ".join(parts) + ".")
    if shorts:
        top = max(shorts, key=lambda v: v["per_day"])
        L.append(f"- Shorts: median {statistics.median(v['per_day'] for v in shorts):.1f} views/day; best: "
                 f"\"{top['title'][:60]}\" ({top['per_day']:.1f}/day).")
    allm = [v for v in mains if v.get("retention")]
    if allm:
        early = [t for v in allm for t, p in drops(v["retention"], v["duration"], 3) if t <= 60]
        if early:
            L.append(f"- {len(early)} of the biggest drops happen in the first minute (at "
                     + ", ".join(mmss(t) for t in sorted(early)[:6]) + "): check what is on screen and said there.")
    if len(L) and L[-1] == "":
        L.append("- Not enough data yet.")
    L += ["", "How the script stage uses this: open each main video's biggest-drop moments in the script doc, note what "
          "was said there, and avoid that pattern in the new hook and chapter openings; repeat what the best Short did."]
    return "\n".join(L) + "\n"


def main():
    if "--offline" in sys.argv:
        d = json.load(open(RAW))
    else:
        d = fetch()
        os.makedirs(os.path.dirname(RAW), exist_ok=True)
        json.dump(d, open(RAW, "w"), indent=1)
    open(OUT, "w").write(summarize(d))
    print(open(OUT).read())
    print("analytics:", d["analytics"], "| ctr:", d.get("ctr"))


if __name__ == "__main__":
    main()
