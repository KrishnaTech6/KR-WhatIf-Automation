# KR's What If Explained — autopilot

Makes one video every second day and publishes it to YouTube and Instagram.
Claude does the creative work; this repo holds the free parts.

| Path | What |
|---|---|
| `queue.txt` | Topics you want next (optional). |
| `settings.json` | Switches: dry runs, manual/API YouTube upload, publish time, language. |
| `history.json` | Every topic already made, so nothing repeats. |
| `lexicon.json` | Pronunciation fixes for the voice; grows by itself. |
| `brand/` | KR, logo, cards, music: the parts that never change. |
| `runs/<slug>/` | Per-video state, voice scripts, and published links. |
| `kaggle/` | Chatterbox voiceover that runs on Kaggle's free GPU. |
| `scripts/` | YouTube login (one time, on your computer) and the uploader. |
| `.github/workflows/` | `voiceover` (Kaggle), `publish-youtube`, `verify-youtube` (nightly: did the scheduled videos really go public?), `keepalive` (weekly login check). |
| `docs/` | Home page and privacy policy (GitHub Pages) for the Google OAuth app. |

Pause everything: create a file named `PAUSE` in the repo root. Delete it to resume.

## Secrets and variables (Settings → Secrets and variables → Actions)

| Name | Kind | From |
|---|---|---|
| `KAGGLE_USERNAME` | variable | your Kaggle username |
| `KAGGLE_API_TOKEN` | secret | Kaggle → Settings → API → Create New Token (or `KAGGLE_KEY` from an older kaggle.json) |
| `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN` | secrets | `python scripts/youtube_auth.py client_secret.json` |
