"""Upload one video package to YouTube (run by the publish-youtube workflow).

  python scripts/youtube_upload.py <assets_dir>/upload.json <assets_dir> runs/<slug>/published.json
  python scripts/youtube_upload.py --check          # login test only (keepalive workflow)
  python scripts/youtube_upload.py --verify runs/<slug>/published.json
                                                    # after release time: still private = locked (verify-youtube workflow)

Credentials come from env: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN.

upload.json (written by Claude):
{
  "slug": "sun-vanished-8-minutes",
  "dry_run": false,                 # true = validate and print the plan, upload nothing
  "privacy": "public",              # or "private" / "unlisted"
  "publish_at": null,               # ISO time, e.g. "2026-11-12T12:30:00Z" (needs privacy "private")
                                    # main / each short may carry its own "privacy" and "publish_at";
                                    # an item's own value wins over the package-level one
  "synthetic": false,               # YouTube "altered or synthetic content" flag
  "language": "en",
  "main":   {"file": "MAIN.mp4", "title": "...", "description": "...", "tags": ["..."],
             "category": "27", "thumbnail": "THUMB_A.jpg", "comment": "..."},
  "shorts": [{"file": "SHORT.mp4", "title": "... #shorts", "description": "... {MAIN_URL} ...", "tags": ["..."]},
             {"file": "REEL.mp4",  "title": "... #shorts", "description": "... {MAIN_URL} ...", "tags": ["..."]}]
}
published.json is written after every finished step, so a re-run skips what is already up.
It also keeps each video's publish_at, so --verify can check later that YouTube really published it.
"""
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube.force-ssl"]
RETRY_STATUS = {500, 502, 503, 504}


def youtube():
    creds = Credentials(None, refresh_token=os.environ["YT_REFRESH_TOKEN"],
                        token_uri="https://oauth2.googleapis.com/token",
                        client_id=os.environ["YT_CLIENT_ID"],
                        client_secret=os.environ["YT_CLIENT_SECRET"], scopes=SCOPES)
    return build("youtube", "v3", credentials=creds, cache_discovery=False)


def with_retry(fn, what, tries=4):
    for n in range(tries):
        try:
            return fn()
        except HttpError as e:
            if e.resp.status not in RETRY_STATUS or n == tries - 1:
                raise
            print(f"  {what}: HTTP {e.resp.status}, retry {n + 1}", flush=True)
            time.sleep(10 * 2 ** n)


def when(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00"))


def settings_for(pkg, item):
    """(privacy, publish_at) for one video: its own values win over the package-level ones."""
    return item.get("privacy", pkg.get("privacy", "public")), item.get("publish_at", pkg.get("publish_at"))


def validate(pkg, assets):
    errors = []
    items = [("main", pkg["main"])] + [(f"shorts[{i}]", s) for i, s in enumerate(pkg.get("shorts", []))]
    for name, it in items:
        if not os.path.exists(os.path.join(assets, it["file"])):
            errors.append(f"{name}: missing file {it['file']}")
        if not 0 < len(it["title"]) <= 100:
            errors.append(f"{name}: title must be 1-100 characters")
        if len(it["description"]) > 5000:
            errors.append(f"{name}: description over 5000 characters")
        if any(c in it["title"] + it["description"] for c in "<>"):
            errors.append(f"{name}: '<' or '>' is not allowed in title/description")
        if len(",".join(it.get("tags", []))) > 500:
            errors.append(f"{name}: tags over 500 characters")
        privacy, at = settings_for(pkg, it)
        if at:
            if privacy != "private":
                errors.append(f"{name}: publish_at needs privacy 'private'")
            try:
                t = when(at)
                if t.tzinfo is None:
                    errors.append(f"{name}: publish_at needs a time zone, e.g. 2026-11-12T15:30:00Z")
                elif t < datetime.now(timezone.utc) + timedelta(minutes=15):
                    errors.append(f"{name}: publish_at {at} is under 15 min away (YouTube would publish at once)")
            except ValueError:
                errors.append(f"{name}: publish_at is not an ISO time: {at}")
    thumb = pkg["main"].get("thumbnail")
    if thumb:
        p = os.path.join(assets, thumb)
        if not os.path.exists(p):
            errors.append(f"main: missing thumbnail {thumb}")
        elif os.path.getsize(p) > 2 * 1024 * 1024:
            errors.append("main: thumbnail over 2 MB")
    return errors


def status_block(pkg, item):
    privacy, at = settings_for(pkg, item)
    st = {"privacyStatus": privacy, "selfDeclaredMadeForKids": False,
          "containsSyntheticMedia": bool(pkg.get("synthetic", False))}
    if at:
        st["publishAt"] = at
    return st


def upload(yt, path, item, pkg):
    body = {"snippet": {"title": item["title"], "description": item["description"],
                        "tags": item.get("tags", []), "categoryId": item.get("category", "27"),
                        "defaultLanguage": pkg.get("language", "en"),
                        "defaultAudioLanguage": pkg.get("language", "en")},
            "status": status_block(pkg, item)}
    media = MediaFileUpload(path, mimetype="video/mp4", chunksize=8 * 1024 * 1024, resumable=True)
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    resp, fails = None, 0
    while resp is None:
        try:
            st, resp = req.next_chunk()
            if st:
                print(f"  {item['file']}: {int(st.progress() * 100)}%", flush=True)
        except HttpError as e:
            fails += 1
            if e.resp.status not in RETRY_STATUS or fails > 5:
                raise
            time.sleep(10 * fails)
    vid = resp["id"]
    got = with_retry(lambda: yt.videos().list(part="status", id=vid).execute(), "status")["items"][0]["status"]
    asked = status_block(pkg, item)
    # Asked for public/unlisted but got private = locked now. A scheduled upload is private on purpose,
    # so its lock only shows after the release time: keep publish_at for --verify.
    rec = {"id": vid, "locked_private": asked["privacyStatus"] != "private" and got.get("privacyStatus") == "private"}
    if asked.get("publishAt"):
        rec["publish_at"] = asked["publishAt"]
        rec["schedule_kept"] = bool(got.get("publishAt"))   # hint only: YouTube doesn't document this
    return rec


def save(out, data):
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    json.dump(data, open(out, "w"), indent=1)


def verify(out):
    """Every video whose publish_at passed 15+ min ago must be public by now. Still private = locked
    (the Google project hasn't passed YouTube's API audit). Returns 3 if any video is locked
    (any other non-zero exit is an error, e.g. a broken login)."""
    done = json.load(open(out))
    recs = [("main", done.get("main"))] + [(s.get("file", "short"), s) for s in done.get("shorts", [])]
    now = datetime.now(timezone.utc)
    due = [(n, r) for n, r in recs if r and r.get("publish_at") and "verified" not in r
           and when(r["publish_at"]) + timedelta(minutes=15) <= now]
    if not due:
        print("  nothing due")
        return 0
    yt = youtube()
    ids = ",".join(r["id"] for _, r in due)
    got = {v["id"]: v["status"] for v in
           with_retry(lambda: yt.videos().list(part="status", id=ids).execute(), "status")["items"]}
    bad = 0
    for n, r in due:
        st = got.get(r["id"])
        if st is None:
            r["verified"] = "missing"
            print(f"  {n}: {r['id']} not found (deleted?)")
            continue
        r["verified"] = st["privacyStatus"]
        r["locked_private"] = st["privacyStatus"] == "private"
        bad += r["locked_private"]
        print(f"  {n}: {st['privacyStatus']}" + ("  <- LOCKED: API audit not passed" if r["locked_private"] else ""))
    save(out, done)
    return 3 if bad else 0


def main():
    if sys.argv[1:] == ["--check"]:
        yt = youtube()
        me = yt.channels().list(part="snippet,contentDetails", mine=True).execute()["items"][0]
        print("login OK:", me["snippet"]["title"])
        # also list scheduled uploads, so their publish times can be mirrored on Instagram
        up = me["contentDetails"]["relatedPlaylists"]["uploads"]
        ids = [i["contentDetails"]["videoId"] for i in
               yt.playlistItems().list(part="contentDetails", playlistId=up, maxResults=20).execute()["items"]]
        for v in yt.videos().list(part="snippet,status", id=",".join(ids)).execute()["items"] if ids else []:
            if v["status"].get("publishAt"):
                print(f"scheduled: {v['status']['publishAt']}  https://youtu.be/{v['id']}  {v['snippet']['title']}")
        return
    if sys.argv[1:2] == ["--verify"]:
        sys.exit(verify(sys.argv[2]))
    pkg_path, assets, out = sys.argv[1:4]
    pkg = json.load(open(pkg_path))
    errors = validate(pkg, assets)
    if errors:
        sys.exit("upload.json problems:\n- " + "\n- ".join(errors))
    if pkg.get("dry_run"):
        print("DRY RUN, nothing uploaded. Plan:")
        for it in [pkg["main"]] + pkg.get("shorts", []):
            print(f"  {it['file']} -> {it['title']}")
        save(out, {"dry_run": True})
        return

    done = json.load(open(out)) if os.path.exists(out) else {}
    yt = youtube()
    if "main" not in done:
        rec = upload(yt, os.path.join(assets, pkg["main"]["file"]), pkg["main"], pkg)
        done["main"] = dict(rec, url=f"https://youtu.be/{rec['id']}")
        save(out, done)
        print("main:", done["main"]["url"], "(LOCKED PRIVATE: API audit not passed)" if rec["locked_private"] else "", flush=True)
    vid = done["main"]["id"]
    if pkg["main"].get("thumbnail") and not done.get("thumbnail"):
        with_retry(lambda: yt.thumbnails().set(
            videoId=vid, media_body=MediaFileUpload(os.path.join(assets, pkg["main"]["thumbnail"]))).execute(), "thumbnail")
        done["thumbnail"] = True
        save(out, done)
    if pkg["main"].get("comment") and not done.get("comment"):
        try:
            with_retry(lambda: yt.commentThreads().insert(part="snippet", body={"snippet": {
                "videoId": vid, "topLevelComment": {"snippet": {"textOriginal": pkg["main"]["comment"]}}}}).execute(),
                "comment")
            done["comment"] = True
        except HttpError as e:   # comments can be blocked while a video is private; not worth failing the run
            done["comment"] = f"failed: HTTP {e.resp.status}"
        save(out, done)
    done.setdefault("shorts", [])
    for i, s in enumerate(pkg.get("shorts", [])):
        if i < len(done["shorts"]):
            continue
        item = dict(s, description=s["description"].replace("{MAIN_URL}", done["main"]["url"]))
        rec = upload(yt, os.path.join(assets, s["file"]), item, pkg)
        done["shorts"].append(dict(rec, file=s["file"], url=f"https://youtube.com/shorts/{rec['id']}"))
        save(out, done)
        print(f"{s['file']}: {done['shorts'][-1]['url']}", flush=True)
    print("ALL UPLOADED")


if __name__ == "__main__":
    main()
