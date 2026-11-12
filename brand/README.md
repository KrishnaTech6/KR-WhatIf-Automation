# Brand lock

Everything here is reused as-is in every video. Never redraw it per video.

| File | What it is |
|---|---|
| `kr.py` | KR, the cartoon host: `draw_kr(c, x, y, s, expr, t, look, flip)`. Expressions: neutral, curious, shocked, thinking, happy, worried, pointing. New poses are built from these parts and added here. |
| `logo.py` | Logo and logo sting (`draw_logo`, p = 0→1 over ~2.5 s after the hook), chapter card, end card. Only the background behind the logo may change. |
| `primitives.py` | Palette, fonts, easing, night sky, glow, pills, vignette and film grain. |
| `render_reference.py` | Renders `reference/*.png`; `--check` fails if the code drifted from them (> 2% mean difference). |
| `reference/` | The approved look: `kr_sheet.png`, `logo.png`, `logo_sting.png`, `chapter_card.png`, `end_card.png`. |
| `fonts/` | Poppins and DM Serif Display (OFL), plus Special Elite (Apache 2.0, collage typewriter) and Anton (OFL, Style 2 captions). Licences included. |
| `styles/` | The video styles (atlas default, cinematic, collage, bold captions for some verticals): **`styles/README.md` has the topic → style rule and the quality bar.** Reference sheets `styles/*.jpg`, re-rendered by `render_styles.py`. |

Default look (style `atlas`): "Cinematic Night Atlas". Palette: space #0A0716, deep #170E33, purple #2A1450, plum #4E1C5E, magenta #8A2A5C, sunset #D9573D, teal #2A9D8F, sand #E9D8A6, cream #F4F1E8, amber #F2B44C, gold #FFD27A; coral #E76F51 only when something goes wrong. KR wears the teal hoodie with the KR badge.

Other styles (`cinematic`, `collage`) change the backgrounds, text, pills, stamps, chapter cards and frame finish
(`tools/krwi/style.py`), never KR's design, the logo sting, the end card, the music or the thumbnail look.

Every run starts with `python3 brand/render_reference.py --check`. It must print `BRAND OK`. If it doesn't, fix the code, never the reference. The reference changes only when Krishna approves a new look.
