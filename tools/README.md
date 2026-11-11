# Video engine (`tools/`)

Everything that is the same in every video lives here, written once: timing from the voice script, the shot
library, the compositor, the score and SFX, the mix, transcription and alignment, the main and vertical renders,
contact sheets, thumbnails and QA. A video folder only holds what is new for that topic.

```
python3 tools/wi.py setup                    # once per machine: libraries + ASR model + orchestra samples (~2 min)
python3 tools/wi.py <slug> new               # creates runs/<slug>/video/{shots,cues,vertical_plan}.py from templates/
python3 tools/wi.py <slug> timeline          # beat keys, aliases, spans, mood, hard cut
python3 tools/wi.py <slug> sheets            # Checkpoint 2: one still per shot, 9 per sheet (video/sheets/)
python3 tools/wi.py <slug> anchors all       # after the voiceover: real word timing for main, Short, Reel
python3 tools/wi.py <slug> render 1/3        # ... 2/3, 3/3 (each < 10 min on 2 CPUs), then:
python3 tools/wi.py <slug> render join       # mix + mux -> video/out/MAIN.mp4, then QA
python3 tools/wi.py <slug> vertical short 1/2   # ... 2/2, then `vertical short join` -> SHORT.mp4 (+ QA)
python3 tools/wi.py <slug> vertical reel     # a ~40 s Reel fits in one call
python3 tools/wi.py <slug> preview 40 55     # quick look at 40-55 s with the voice
python3 tools/wi.py <slug> remix             # audio fix only: rebuild the mix, re-mux MAIN.mp4
python3 tools/wi.py <slug> qa FILE [seconds] # -14 LUFS +-1, true peak <= -1 dB, no black > 0.5 s, length
```

## What a video folder contains

| File | What you write |
| --- | --- |
| `video/shots.py` | `SHOTS()`: the shot list `(start, shot, transition)`, built mostly from library shots, plus hero shots |
| `video/art.py` (optional) | topic drawings (a dragonfly, a coal seam); `from krwi.art import *` for the rest |
| `video/cues.py` | `HITS()` (a sound on every visible hit) and `AMB()` (ambience beds); everything else is automatic |
| `video/vertical_plan.py` | `HOOK`, `SUB`, `FIX`, `plan_short(vt)`, `plan_reel(vt)` built from `scene(...)` |
| `video/run.json` (optional) | `{"beats": [...]}` to name beats yourself; default keys come from the beat names |
| `video/thumbs.py` | the thumbnail drawing, using `krwi.thumb.canvas()`, `save()`, `compare()` |

## Timing

`T("beat", "word", n)` is the start of the n-th `word` in that beat; `at("beat", "word", -0.2)` adds an offset;
`B(beat)` / `E(beat)` are its start and end. Before the voiceover exists these come from an estimate
(150 wpm, `(beat)` = 1 s, 1.2 s between beats, 2.4 s before the `HARD_CUT_BEFORE` beat). After
`wi.py <slug> anchors main` they come from the real audio, and no shot code changes.

Beat keys: the beat name before ` - `, lowercased (`[Night one - the fire | deep]` -> `night_one`). Any word of a beat
name used by only one beat is an alias (`fire`, `night`). `wi.py <slug> timeline` prints them.

## Shot library (`krwi.lib`)

| Shot | Use it for |
| --- | --- |
| `card(value, name)` | chapter card ("DAY 10", "The flood") |
| `logo_sting()`, `end_screen()` | brand moments (right after the hook; the end) |
| `counter(v0, v1, fmt, until=, label=)` | an animated big number |
| `statement(line, sub=)` | one big line |
| `pills([(label, time, color)], title=)` | a list popping in word by word |
| `bars([(label, value, color)], title=, unit=)` | scale comparison |
| `india_pin(label, lon, lat, pin_at)` / `india_states(states, label, hl_at)` | the complete India map (brand rule) |
| `split(left_fn, right_fn, "TODAY", "THEN")` | before/after, with/without |
| `kr_react(expr, line)` | KR reaction (neutral, curious, shocked, thinking, happy, worried, pointing) |
| `papers((title, sub), (title, sub), right_at)` | scientists disagree |
| `comment_prompt(question, card_at)` | the comment question |
| `tease("NEXT: ...")` | next-video tease |
| `layer(a, b, ...)`, `stamp_at(label, t)`, `pop_at(label, t)`, `zoom(shot)` | overlays and push-ins on any shot |

Every factory returns `fn(c, t, t0)`; times are absolute seconds; `bg=` takes any `fn(c, t)` background.

## Sound (automatic)

Whoosh on every non-cut transition, riser -> impact into every chapter card, logo and end hits, hard silence before
the `HARD_CUT_BEFORE` beat, and a score in the channel family chosen from each beat's mood tag: hook = ticking clock +
music-box motif, wonder = choir + harp, tense = contrabass pulse + timpani, the hard-cut beat = drone + cello +
accelerating heartbeat, last beat = soft piano + motif callback + rumble on "next". `SCORE()`, `SECTIONS()` or
`BUILD()` in the run's `cues.py` replace parts of it.

## Speed (2-CPU workspace)

Main video ~0.13 s per frame (5 min ~ 20 min: render in 3 parts). Verticals ~0.3 s per frame (58 s Short ~ 9 min:
2 parts). `KR_WORKERS` sets the number of processes. Caches live in `~/.cache/kr-whatif` (`KR_CACHE`).

## Checked

`runs/woke-up-300-million-years-ago` was moved onto this engine and re-rendered: 26 main frames and 12 vertical
frames are pixel-identical to the original code, and the main, Short and Reel mixes are sample-identical.
