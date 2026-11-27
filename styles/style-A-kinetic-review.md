# Style A — "Kinetic-type app review"

Learned from `This App Fixes MacOS_1.mp4` (5:04, 1 narrator, a macOS app review). Every number below was
measured from the video (rea-video survey of all 167 shots + frame-by-frame ffmpeg sampling), unless marked *(est.)*.

## The idea in one line
The narration is "illustrated" three ways, cutting between them every ~1.4 s: (1) a cream card that shows the phrase
being spoken, (2) a punched-in macOS screen recording proving it, (3) a short daylight desk B-roll shot for the
physical/hardware moments. There is no talking head.

## Pacing (measured)
| Metric | Value |
|---|---|
| Shots | 167 in 5:04 |
| Cuts per minute | 32.8 (range 26–50 per minute by 30 s window; busiest 1:30–2:00) |
| Shot length | mean 1.82 s · median 1.37 s · p10 0.47 s · p90 3.83 s · max 9.5 s |
| Distribution | <0.5 s: 10% · 0.5–1 s: 21% · 1–2 s: 36% · 2–4 s: 23% · >4 s: 10% |
| Transitions | hard cut 71% · punch-in zoom 9% · fade 5% · slide 5% · blur 4% · wipe 2% · dissolve 2% · whip 1% |
| Last ~4 s | changelog/website scroll then fade to the cream card; ends cleanly, no end screen |

Rule of thumb: **one visual per spoken phrase**. A new phrase on the card = a new "shot". Longer holds (4–9 s) are
reserved for screen demos where the UI is doing something.

## Layer 1 — the cream phrase card (≈45% of shots)
- Background `#ECE4DA` (exact). Text `#000000`.
- Font **Times New Roman Bold** (renders identically). Regular words size **100 px** at 1080p, the coloured keyword
  **108 px** (8% larger). One line, centred exactly at frame centre (x 0.5, y 0.5).
- **One phrase on screen at a time**, 2–6 words, the exact words being spoken right then (so it doubles as captions).
- Animation (measured at 30 fps):
  - in: opacity 0→1 over **3 frames (0.10 s)**, ease-out, with a **~6 px rise** (1080p).
  - hold until the next phrase starts.
  - out: opacity 1→0 over **2 frames (0.067 s)**, then **1 blank frame**, then the next phrase fades in.
  - A phrase can also fade up from light grey (≈40% opacity) when the narrator is mid-sentence.
- Keyword colour = meaning (one colour per phrase, usually one word):
  | Colour | Hex | Used for |
  |---|---|---|
  | Coral | `#F2604A` | the key idea / problem word ("modular", "most", "rundown", "wrong", "gripes", "presses") |
  | Green | `#2E6B33` | positive / good / the solution ("the best", "toxic"*ironic*, "3 separate apps", "file", "macOS" as praise) |
  | Blue | `#0070DD` | product / tech terms, directions ("Vorssaint", "down", "up", "move", "lightning") |
  | Crimson italic | `#C8302A` Times Bold Italic | an app/feature **name** ("*Keep Awake*") |
  | Red caps | `#F84830` | big emphasis word set larger ("This is a **BIG** one") |
- Inline icons on the card: small app/brand icons sit beside the word (PowerToys logo, Apple logo , 🇫🇷 flag,
  Windows logo, Vorssaint icon above the words). Icons pop in with the phrase. Several icons can appear one by one
  (Arch, Windows, Ubuntu, Mint logos building up across 3 beats).
- Special card moves: the phrase in a dark macOS-window chip ("with macOS" → grey highlight box → dark pill),
  i.e. the card mutates instead of cutting.

## Layer 2 — screen recordings (≈45% of shots)
- macOS desktop, Sequoia-style dune wallpaper, dark-mode UI. Recorded full screen.
- **Constant virtual camera**: almost every screen shot is punched in 1.3–2.5× on the menu-bar panel being
  discussed, often animating (slow push-in 0.5–1 s, ease-in-out) during the shot. Wide shot first, then push.
- **Focus dim**: everything except the active row/panel darkens ~50–60% while the panel stays bright
  (spotlight effect) — used on settings lists and menus.
- **Keyboard shortcut labels**: white SF text, bottom-left (x≈0.12, y≈0.86), no box: "cmd + c", "cmd + opt + v",
  "cmd + q". Appear when the keys are pressed, gone when the action completes.
- **Red rectangle** around a dock icon or UI element; **hand-drawn red scribbles** ("P", "Pen") and **green ✓**
  stamps popping in one by one to tick items off.
- Transitions inside demos: short cross-dissolve (0.3–0.5 s) between two recordings; fade-to-dark before a cut.
- Joke inserts: TV colour-bars "technical difficulties" card (≈1.5 s, hard cut in/out); a lyrics wall (rickroll
  gag) dissolving to the desktop; the creator's own YouTube channel page as a self-plug (≈3 s, twice).

## Layer 3 — desk B-roll (≈10% of shots)
- Phone/mirrorless, natural window daylight from the left, white wall, wooden desk, small plant, monitor on an arm.
- Angles: 45° high angle on laptop + mouse, overhead flat-lay of laptop keyboard, low close-up of keyboard with
  shallow depth of field, side shot of monitor turning off. Slow handheld/slider drift.
- Hands **demonstrate**: plugging a USB dongle, comparing two mice with a hand gesture, opening the lid.
- Used only when the narration talks about hardware or a physical action. 0.5–3 s each, hard cuts.

## Sound (measured)
- Voiceover only narration, integrated loudness **−19.4 LUFS** (quiet; we deliver at −14).
- Very tight VO: only 23 pauses ≥ 0.25 s in 5 min (mean 0.52 s, max 1.09 s) → breaths and gaps are cut out.
- **No music bed** (stem split: the non-voice track has no stretch of music ≥ 4 s anywhere). The film is
  carried by the voice alone, which suits the calm, minimal cream look.
- Non-voice sound is only short transients; they coincide with cuts slightly above chance (28% vs 22%), so at
  most a few light SFX on card changes — no designed whoosh-on-every-cut pattern. *(measured, not heard)*
- To reproduce: no music, or a very quiet bed only if the person wants one; optional soft pop/tick on a few
  keyword cards; keep the voice clean and tight.

## Narrative shape
Hook ("So I think I just found the best PowerToys alternative for Mac") → context/explainer ("if you don't know
what PowerToys is…") → app intro → "here's the rundown" → feature tour, one feature per section, each section =
card title ("Keep Awake", "Stats", "lightning round") → personal verdict ("Vorssaint has replaced like 3 separate
apps for me") → soft CTA ("So if you haven't tried it…") → website/changelog.

## Recipe in Editroom
1. `set_sequence` 1920×1080 @ 30. Voiceover on A1 (tighten with the cut-craft skill: gaps > 0.25 s out).
2. Phrase cards: for single-colour phrases use Editroom natively — `add_solid #ECE4DA` on V1 for the card's span,
   `add_title` on V2 per phrase (`set_title_style` font "Times New Roman", bold, size ≈100, colour `#000000`),
   `set_audio` fade_in 0.1 / fade_out 0.067 on each title. For coloured keywords, icons or the rise, render the
   phrase with `scripts/overlay.py` (`phrase` layer, background `#ECE4DA`) and place the .mov on V1/V2.
3. Screen recordings on V1; `set_transform` zoom `in` (scale 1.4–2.2, focus on the panel, zoom_seconds 0.6) on most.
   Focus-dim, shortcut labels, red boxes, ✓ stamps: `overlay.py` (`dim`, `kbd`, `box`, `image`) on V2 above.
4. B-roll only on hardware lines. Hard cuts; 2–3 short dissolves in the whole film at most.
5. Pace check: aim for 28–36 cuts/min and a median shot of 1.2–1.6 s; no visual held > 4 s unless the UI moves.
6. Export at −14 LUFS.
