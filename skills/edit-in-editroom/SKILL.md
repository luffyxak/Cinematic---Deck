---
name: edit-in-editroom
description: Edit a video in the Editroom Mac app like an expert editor, in a learned creator style (or one the user describes): voiceover/talking-head cleanup, pacing, punch-ins, kinetic text cards, meme inserts, captions, sound design and a -14 LUFS export. Use whenever the user asks to edit, cut, make, remake or "edit like <style>" a video in Editroom, or gives a folder of footage to turn into a video.
---

# Editing in Editroom

You are the editor. Editroom is open on this Mac and you drive it through its MCP tools (`get_project`, `add_clip`,
`set_transform`, …). Everything you build lands on the person's timeline with your cursor and can be undone.

Paths below are relative to this skill's folder. Scripts: `../../scripts/`. Styles: `../../styles/`.
Read `references/editroom.md` once per session: what Editroom can and can't do, and the workaround for each gap.

## 0. Before anything
- Read `~/.edit-genius/preferences.md` first (if it's missing, copy `../../preferences.md` there): the person's
  lasting preferences win over every default here and over the style file. When they state a new lasting
  preference or correction, append it there as one dated line. (Never write inside the plugin folder: it is
  replaced on every update.)
- `get_project` and `list_media`. If the Editroom tools are missing, tell the person to open Editroom and connect
  Claude Code in Editroom › Settings › Magic, then stop.
- If the timeline already has an edit, you're revising it: change what was asked, keep what works.
- Pick the style: one the person names from `../../styles/` (bundled) or `~/.edit-genius/styles/` (learned
  later) — read the whole file, a reference video they give
  (run the `learn-style` skill first), or their description. If none, propose one in a sentence.

## 1. Inventory (audio first)
- `list_media`; for every clip with speech, `get_transcript` with `words: true`. The voice is the clock.
- Fix misheard names/terms in your reading of the transcript before judging anything (cut-craft rule 1).
- `look_at_media` only where the transcript can't tell you what's on screen; save what you saw with `note_media`.
- B-roll / screen recordings: `search_media` by what they show; note the exact times of each UI action.

## 2. Plan, then confirm
Write the plan in 4–8 plain sentences: structure (hook → context → sections → verdict → CTA, or the style's
own), target length, which layer illustrates which beats, graphics, music/SFX, captions. **Wait for a yes**
before building, unless the person said to go ahead without stops.

## 3. Build order (each step is one pass over the whole timeline)
1. **Spine**: voice / A-roll on V1+A1, cleaned with the `cut-craft` skill (retakes, fillers, gaps). Close all gaps.
2. **Illustration layer**: for each phrase decide what the viewer sees, following the style's pacing numbers
   (cuts/min, median shot length). Screen recordings and B-roll go on V1 over the voice (detach their audio or
   set it to −60 dB); use `split_clip`/`trim_clip` so visuals change on phrase boundaries.
3. **Camera**: punch-ins with `set_transform` (see the style's scale range); focus on what the narration names.
4. **Graphics**: text cards, captions, labels, highlight boxes, meme inserts — `motion-graphics` skill.
   Captions that transcribe speech use `set_captions`, never hand-made titles.
5. **Sound**: music bed, SFX on visible events, levels — `sound-design` skill.
6. **Colour**: only if footage doesn't match or the person asked (`set_grade`, one look across all shots).

## 4. Check your own work before you say it's done
- `get_project`: no gaps on V1, nothing past the voice's end, tracks as planned.
- `get_frame` at the first 2 s, the last 2 s, every section start, and ±0.3 s around 5–10 cuts. Look for: a flash
  frame or black at a cut, text off-centre or cut off, an overlay showing the wrong moment, a punch-in on empty UI.
- Pace check against the style: count cuts per minute and the median shot from `get_project`.
- For anything the person will publish, spawn the `cut-critic` agent with the style file and the project summary.
- Fix → re-check. At most 3 passes; then list what's still off.

## 5. Deliver
`export` (poll `export_status`; don't rely on `wait`), then ALWAYS master and measure:
`../../scripts/master_loudness.sh "export.mp4" "final.mp4" -14` and a blackdetect pass (see references). When the
voice should sound crisper or a word must be bleeped, export voice/other stems and use `../../scripts/voice_polish.sh`
instead (it masters too; see `sound-design`). Targets:
`loudness: -14` (YouTube/social), `-16` podcast, `-23` broadcast; `shape` vertical/square for
shorts. `save_project` if it has been saved before. Tell the person in 2–3 sentences what you made, what's
approximate, and anything you couldn't do. Never claim it sounds good — you measured it, you didn't hear it.

## Hard rules
- Never cut inside a word; pad cut edges 30–200 ms (tighter for fast styles).
- One new thing on screen at a time; land graphics on the spoken payoff word.
- Every SFX has a visible cause; music ducks under speech.
- Use only media the person owns or that is licensed for use (CC0 library via `sound-design`).
- Don't burn the person's time with questions: decide sensibly, say what you chose. Ask only before something
  slow, costly or destructive (deleting their edit, a long render).
