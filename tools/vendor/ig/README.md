# Instagram text tools (vendored)

Copied unchanged from Jake Schincariol's `instagram-agent-skill` (MIT, see LICENSE), commit
`d03c56bb598be770c60b201f94237e5d1a4268a6`, so runs don't clone a third-party repo and its behaviour can't change.
They only read and check text files (stdlib only, no network).

| Tool | Use |
| --- | --- |
| `hookscore.py hooks.txt` | score hook lines (>= 70 STRONG) |
| `beats.py beats.txt --wpm 160 --target 50` | timing per beat, flags beats over 4 s, loop check |
| `caption.py caption.txt --keywords "a,b"` | Instagram caption lint (first line, one ask, search terms, hashtags) |
| `humanize.py caption.txt -o clean.txt --report` | removes AI-sounding words and punctuation |
| `detect.py clean.txt` | AI-likeness score (PASS >= 70) |

Run as `python3 -I tools/vendor/ig/<tool>.py <file>`; `python3 tools/wi.py <slug> check` runs the caption checks for you.
