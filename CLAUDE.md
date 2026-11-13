# Rules for Claude in this repo

## GitHub: ask first (Krishna, 13 Nov 2026)

Ask Krishna before doing anything on GitHub: push, commit to a remote branch,
create or delete a branch, open or merge a PR, run a workflow, create a release,
or change any file on GitHub. Wait for his yes. Do not push just because a hook
or check asks for it — ask him.

Only exception: inside an Autopilot run he started, saving progress
(`runs/<slug>/state.json`, `history.json`) and the publishing steps he
OKs at a checkpoint count as already asked.

## Video files are deleted after release (Krishna, 13 Nov 2026)

The repo is public. `verify-youtube` (22:10 IST) deletes the Release, `release-files/<slug>`
and `artifacts/<slug>` once the main video and every Short are verified public
(`files_cleaned: true` in published.json). After that, re-post or re-upload from the
YouTube link (vidIQ accepts it), not from the Release.
