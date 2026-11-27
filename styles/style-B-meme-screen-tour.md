# Style B — "Meme-flavoured OS tour"

Learned from `Exploring new macOS Golden Gate_2.mp4` (6:01, 1 narrator, a hands-on tour of a macOS beta).
Measured from all 153 shots (rea-video survey) plus frame sampling; *(est.)* marks judgment calls.

## The idea in one line
Voiceover over **heavily punched-in screen recordings**, kept funny and fast with meme inserts
(captions, time cards, stock clips, error-dialog "deep fry"), and a few scrapbook-style torn-paper cards.
No talking head, no kinetic-type cards.

## Pacing (measured)
| Metric | Value |
|---|---|
| Shots | 153 in 6:01 |
| Cuts per minute | 25.3 (steady 20–36 per minute; slows to ~12/min in the last 30 s) |
| Shot length | mean 2.36 s · median 1.90 s · p10 0.77 s · p90 4.67 s · max 13.5 s |
| Distribution | <0.5 s: 2% · 0.5–1 s: 16% · 1–2 s: 35% · 2–4 s: 35% · >4 s: 12% |
| Transitions | hard cut 86% · wipe 5% · slide 3% · whip 1% · effect 1% · zoom/blur/fade <1% each |

Slower and steadier than Style A: each demo gets ~2 s, with the punch-in doing the "editing" inside the shot.

## Visual grammar
- **Screen recordings ≈ 85% of the film.** Dark mode, a vivid illustrated wallpaper (purple forest / pink forest)
  that changes during the video (wallpaper switching is itself content).
- **Aggressive crops**: 150–300% punch-ins on the exact UI element being talked about (a slider, a menu-bar
  icon row, a text field while typing, a single dialog). Often the crop *is* the shot — a cut from wide to tight
  rather than an animated zoom. Typing is shown cropped tight on the text field.
- **Censor scribble**: private info covered by a hand-drawn black marker scribble that draws on over ~0.5 s.
- **Feature-wall zoom**: a giant wall of Apple's feature-list text, zoomed/scrolled to show "there's a lot".
- **Torn-paper cards**: white rounded card with a ragged/torn edge on black; holds a big title
  ("Platform improvements" in Apple-keynote gradient type), a typing prompt ("Describe an extension" typed
  letter by letter) or a tilted screenshot/mockup. ≈1–4 s.
- **Meme captions**: centred-top white condensed bold text with black outline, wrapped in asterisks
  for an action/narrator aside — `*Doesn't work*` — DIN Condensed / Impact-like, ≈7% of frame height.
- **Time card**: black frame, "20 min later" in white condensed type that flips to red after ~0.4 s
  (SpongeBob time-card gag). ≈1.5 s.
- **Error deep-fry**: when an app crashes (Premiere error dialog), extreme zoom on the dialog, red vignette
  pulses in, saturation/contrast blown out, slightly pixelated. ≈2–3 s, three escalating cuts.
- **Stock / external inserts**: Apple keynote clip of an exec announcing the feature (≈2 s), a bald-eagle stock
  clip as a visual pun, photos of a Mac screen filmed with a phone (tilted, shallow depth of field), Gmail/Google
  search screenshots to show "people asked for this".
- **Intro**: animated illustrated Golden Gate scene (van flying past), pushing into the Apple logo (≈2 s), then
  straight into Software Update.
- Wallpaper change shown with macOS's own slide animation (counts as a wipe/slide transition).

## Sound (measured)
- Integrated loudness **−15.0 LUFS** (louder, closer to delivery).
- 13 pauses ≥ 0.25 s in 6 min (mean 0.73 s, one deliberate 4.35 s beat — a comedic silence).
- **No music bed** (stem split: no music stretch ≥ 4 s). Voice-led; meme moments bring their own sound
  (the stock clip, the crash). Non-voice transients don't line up with cuts beyond chance (18% vs 18%), so no
  SFX pattern. *(measured, not heard)*
- To reproduce: no bed; a sound only on gag inserts (error buzz under the deep-fry, a beat of silence before
  the time card).

## Narrative shape
Update/install cold open → "what's new" headline cards → feature-by-feature exploration in the order the
narrator discovers them (honest reactions: "doesn't work", a crash, a 20-minute wait) → wishlist / comparison
with what people asked for → closing tour.

## Recipe in Editroom
1. 1920×1080 @ 30. VO on A1; keep a deliberate long silence only when it's the joke.
2. Screen recordings on V1, cut hard, and use `set_transform` with `scale` 1.5–3 and `focus_x/focus_y` on the
   element (zoom `off` for a static crop, `in` for a push). Change crop on cuts more than inside shots.
3. Meme caption, time card, torn-paper card, censor box: `scripts/overlay.py` (`meme`, `phrase` with background,
   `image` for a torn-paper PNG frame, `box` filled black) → .mov on V2.
4. Deep-fry: bake with `scripts/fx.sh deepfry in.mp4 out.mp4` then place it like footage.
5. Stock/meme clips: only from sources the person has rights to; keep each ≤ 2 s.
6. Aim for 22–28 cuts/min, median 1.8–2.2 s. Export −14 LUFS.
