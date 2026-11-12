# Video styles (approved by Krishna, 12 Nov 2026)

Four looks, one channel. The **topic picks the style** of the main video; the Short and Reel follow the main video.
Reference sheets (same demo shots in every style): `atlas.jpg`, `cinematic.jpg`, `collage.jpg`, `bold_captions.jpg`
(re-render with `python3 brand/render_styles.py`; demo code in `demo/video/shots.py`).

## The rule

| Style | `run.json` | Use it when the topic is about... | Examples |
| --- | --- | --- | --- |
| Default: Cinematic Night Atlas | `atlas` | **how something works**: technology, inventions, machines, the human body, everyday science | Electric motor never invented, UPI stops working, no phone for 30 days |
| Style 1: Cinematic | `cinematic` | **danger, a countdown, a crisis or huge scale**: blackouts, disasters, survival, "X hours left"; space only when Krishna asks for a space topic | Sun vanished for 8 minutes, India with no electricity for a week |
| Style 4: Paper Collage | `collage` | **India, money, society, cities, people, news-like "what happens to us"** | Delhi smog never lifts, every Indian gets ₹1 crore, 4-day work week, Himalayas gone |
| Style 2: Bold Captions | `CAPTIONS = "bold"` in `vertical_plan.py` | **sometimes, on a Short/Reel only** (see below). Never a main video. | |

Two styles fit? Pick by the main feeling: "this is scary / huge / a countdown" → cinematic; "what happens to us,
our money, our cities" → collage; "how does this actually work" → atlas. Don't use the same style more than 3 videos
in a row if another style also fits (variety keeps the channel interesting); say which style and why at ✅1, where
Krishna can change it.

Set it once per run: `python3 tools/wi.py <slug> style collage` (writes `video/run.json`). `wi.py <slug> check shots`
warns if it is missing.

## Short and Reel

- They reframe the main video, so they are automatically in the main video's style. Keep it that way: the Reel is the
  trailer for the main video, so a viewer who liked the Reel recognises the full video.
- Style 2 bold captions (Anton, white with a thick black outline, the spoken word yellow, each group pops) replace the
  standard captions **only sometimes**: when the Short/Reel is fact- or list-led and the words carry it (roughly 1 in 3
  or 4 verticals, never on every one, never two videos in a row). Default is the standard gold captions.

## Never changes (brand)

KR's design (in collage he becomes a paper cut-out of the same KR, `kr_cutout`), the logo sting and end card (always
Night Atlas, smooth, not stop-motion), the background-music family and the thumbnail look (`brand/thumbnail_rules.md`).

## What each style must have (signature moments)

Every main video shows its style's signature at least once per chapter, so the look is unmistakable, not a palette swap.

**atlas**: illustrated scenes with people and Indian places, rim light, sunset sky, iris transitions, dashed
"missing" ring.

**cinematic** (`cinematic_bg`, `bloom`, `light_stream`, `shock_ring`, `countdown`, `starfield`): near-black frames, ONE
light source per shot, slow push-ins, thin wide-spaced type, a running countdown or clock for time pressure, very little
colour (warm light vs cold dark), silence before big reveals. Don't: busy scenes, many colours, cartoon props.

**collage** (`collage_bg`, `cutout`, `paper_circle`, `halftone`, `tape`, `torn_strip`, `type_text`, `index_card`,
`marker_circle`, `marker_line`, `red_string`, `pin`, `stamp_at`, `jit`): every object is a paper cut-out (wrap topic art
in `cutout(c, lambda k: ...)`), halftone shading, tape, typewriter labels and headlines on torn strips, red marker
circles and underlines, rubber stamps ("MISSING", "BANNED", "SOLD OUT"), red string linking cause and effect,
newspaper-style headline strips. Motion is 12 fps stop-motion (automatic); give each loose piece `jit(key, t)`.
Don't: glows, gradients, smooth tweens on paper pieces.

## Quality bar (non-negotiable, every style)

Before ✅2, and again on the final render, every contact sheet must pass all of these. A fail is fixed, never shipped.
1. **Stops the scroll**: frame 0 is the hook's consequence, big and clear, readable as a phone thumbnail.
2. **Never boring**: a new shot every 2–4 s, something moves or changes at least every 3 s.
3. **Looks premium in its style**: the style's signature moments above are there; nothing looks like a default
   template, stock clip art or a placeholder; one focal point per frame; text never cut off or overlapping.
4. **Stands out**: at least one moment per chapter a viewer would screenshot or share.
5. **Clear**: every number is a comparison (counter, scale, map, before/after); every idea has a picture.
6. **Brand intact**: `render_reference.py --check` prints BRAND OK; KR, logo, music family, thumbnail look unchanged.

Speed: atlas and cinematic ~0.13–0.2 s per frame; collage draws ~0.25 s per drawing but holds each drawing for 1/12 s,
so ~0.1 s per frame overall.
