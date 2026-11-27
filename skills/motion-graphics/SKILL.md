---
name: motion-graphics
description: Design and render motion graphics for an Editroom edit — kinetic text cards, keyword highlights, meme captions, time cards, keyboard-shortcut labels, highlight boxes, focus-dim spotlights, censor boxes, stickers/emoji and title animations — with professional timing, then layer them in Editroom with transparency. Use whenever a video needs on-screen text, annotations or animated overlays.
---

# Motion graphics

Timing rules measured by HyperFrames from professional launch films, annotation rules from chengfeng-videocut's
real projects, and the renderer in `../../scripts/overlay.py` (PIL → ProRes 4444; transparency verified in Editroom).

## Decide: native title, rendered overlay, or nothing
1. **Nothing** — when the screen is already telling the story (a live demo, a page changing, proof on screen),
   adding graphics subtracts. In one study 4 of 13 segments were best left alone.
2. **Native Editroom title** (`add_title` + `set_title_style` + `set_audio` fades) — a single-colour phrase,
   chapter label, simple lower third. Stays editable on the timeline. Prefer it when it's enough.
3. **Rendered overlay** (`overlay.py`) — multi-colour keywords, inline icons/emoji, rise/pop/blur entrances,
   meme outlines, highlight boxes, focus dim, shortcut labels. Render, `import_media`, place on V2+.
4. **HyperFrames** (`npx hyperframes`, Node 22+, needs headless Chrome — heavy on an 8 GB Mac) — only for complex
   animation (charts, morphs, 3D type, UI mockups). Render `--format mov` for ProRes 4444 alpha.

## Using overlay.py
```bash
uv run --script ../../scripts/overlay.py spec.json -o card.mov                 # transparent ProRes 4444
uv run --script ../../scripts/overlay.py spec.json -o x.mov --still 0.5 --png check.png   # look at one frame first
```
Layers: `phrase` (runs of differently coloured/sized text), `meme` (outlined text), `kbd` (shortcut label),
`box` (outline/fill rectangle), `dim` (darken all but a hole), `image` (PNG/emoji/icon). Every layer takes
`start`, `end`, `x`, `y` (centre, 0–1) and `in: {fade, rise, pop, blur}`, `out: {fade}`. Spec details are in the
script's header. Make one overlay file per beat (easy to retime), named by beat, kept in a `graphics/` folder
next to the project. Always render a `--still` at the landing moment and look at it before rendering the clip.

Fonts available by key: times-bold, times-bold-italic, georgia-bold, impact, din-condensed, din-bold,
arial-black, helvetica, sf, menlo — or any absolute .ttf/.otf path.

## Timing (measured defaults)
- **Arrive slow, leave clean.** Arrivals ease out on a long tail; exits are 40–50% shorter than entrances.
- Entrances worth rotating (don't use one for everything): per-word fade from light grey to ink 0.07–0.1 s apart;
  per-word blur 6 px→0 + fade in 0.13 s, 0.067 s apart; whole line blurring in 8 px→0 in 0.13–0.2 s;
  fast fade 0.1 s + 6 px rise (Style A); pop with slight overshoot for badges/icons (0.18 s).
- A landed title is **dead still** — no floating, breathing, creeping scale.
- Hold ≈ 0.5 s + 0.3 s per word; a one-word chapter can hold 0.4 s; last line ≥ 2 s.
- Exit: fade/blur-out 0.07–0.25 s, then a hard kill. One phrase on screen at a time.
- Stagger: letters a frame apart, words 60–120 ms, list items 40–80 ms. The next element starts when the previous
  is 30–50% done — never all at once, never strictly one-after-another.
- Size: titles 4–9% of frame height (Style A card text ≈ 100 px on 1080); quiet lines 2.5–4%; one highlighted word
  in the accent colour, and the colour must mean something.
- Land the graphic on the spoken word: reveal start = word start − reveal duration.
- Keep text inside the 80% title-safe box; content inside 90% action-safe.

## Annotations on screen recordings (what to circle, when)
- **Truth priority: what the screen shows beats what the words sound like.** Before adding a box or arrow,
  look at the frames for the whole span: the page may scroll or change mid-sentence.
- Circle/box **the evidence itself** (that line, that button, that number) when the keyword is spoken; if the page
  is still scrolling, wait until it settles.
- On a long static stretch (8+ frames unchanged), bring the annotation in early — it becomes the only motion.
- Exit **0.2 s before** the screen is operated again; a box hovering over moving content is the worst tell.
- White pages: outline only, never dim (dimming greys the whole page). Dark UIs: focus-dim works (`dim` layer with
  a hole, 0.5–0.6 opacity).
- Skip the label if the punch-in already makes the text readable.
- Keyboard shortcuts: show the keys while they're pressed (Style A: white SF, bottom-left, no box).

## Transitions with a cause
Use 3–5 kinds per film, each caused by something on screen; hard cuts for most seams inside a section.
Zoom through a button into the next screen · object grows into the next scene · whip (0.13–0.3 s smear) ·
dip (darken ~40% for 3 frames, then cut) · blur swap on one background. In Editroom: `set_transform zoom` +
cut on the fastest frame, `set_transition dissolve/dipToBlack/wipe`, or bake a whip in the overlay.

## Style recipes (from the learned styles)
- **Style A phrase card**: background `#ECE4DA`, times-bold 100 px black, keyword 108 px in coral `#F2604A` /
  green `#2E6B33` / blue `#0070DD`, app names times-bold-italic crimson `#C8302A`; in fade 0.1 + rise 6, out fade
  0.067, 1 blank frame between phrases. Template: `../../templates/style-a-card.json`.
- **Style A shortcut**: `kbd` "cmd + c", sf 44 px white, x 0.08 left-anchored, y 0.86.
- **Style B meme caption**: `meme` "*Doesn't work*", din-condensed ≈ 76 px white, black stroke 5, y ≈ 0.2.
  Template: `../../templates/style-b-meme.json`.
- **Style B time card**: black background, din-condensed white "20 min later" then the same in `#E8261E` from 0.4 s.
  Template: `../../templates/style-b-timecard.json`.
- **Censor**: filled black `box` (or a scribble PNG) over private info, in 0.3 s.

Emoji: `../../scripts/fetch_emoji.sh "Fire"` downloads a Microsoft Fluent Emoji 3D PNG (MIT licence, 256 px
with transparency) and prints its path — use it as an `image` layer (`in: {pop: 0.18}`) or import it straight
into Editroom. Icons and logos: use the real mark (the app's own icon or the brand's official logo), never draw
one by hand. Memes/stock images: only from sources the person has rights to.
