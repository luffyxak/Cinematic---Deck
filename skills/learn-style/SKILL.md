---
name: learn-style
description: Reverse-engineer a reference video's editing style shot by shot and save it as a reusable, measured style playbook (pacing, layers, text design and animation timing, colours, fonts, transitions, graphics, B-roll, sound) that the edit-in-editroom skill can apply. Use when the user gives a reference video or YouTube link and says "learn this style", "edit like this", "copy this editing", or wants a new style added.
---

# Learn a style

Goal: a file in `~/.edit-genius/styles/style-<letter>-<name>.md` (create the folder; never write into the
plugin folder, it is replaced on updates — letters A and B are taken by the bundled styles in `../../styles/`) with **numbers**, not adjectives — so a future edit can
reproduce the look. Follow the two existing playbooks as the format. Paths are relative to this skill's folder.

## 1. Get the video
- A local file, or a link: `yt-dlp -f "bv*[height<=1080]+ba/b" --merge-output-format mp4 -o "<dir>/%(title)s.%(ext)s" <url>`
  (only videos the person may use for study). Prefer 1080p — at 360p fonts and fine detail are guesses.
- Optional: the transcript/metadata of a YouTube link through the Supadata connector if it's connected.

## 2. Shot-by-shot survey (you are the vision model)
```bash
../../scripts/rea.sh survey ref.mp4 -o <work>/ref
```
It prints images and waiting answer files. Look at every image, answer in the JSON format the task describes,
run the same command again; repeat until `status: done`. How to answer well:
- Overview: accept the tool's red-line cuts unless you see otherwise; text that swaps on the same background is a
  cut; push-ins and UI changes on the same screen are `busy`; mark real doubt `unsure` so it zooms in.
- Zoom rounds: name the scenes per block, then mark the gaps (dissolves span several gaps with one kind).
- Keyframe sheets: set `look` per sheet (screen_capture / live_action / code_render for MG & text cards /
  film_footage for inserted clips / anim_2d …) and override per shot. Accept candidate frames unless wrong.
Write down what you notice as you go — the sheets are where the style is learned.

## 3. Full decompose (stems, transcript, OCR, packaging)
```bash
../../scripts/rea.sh --lang en decompose ref.mp4 -o <work>/ref --lang en --ocr-lang en --no-speakers
../../scripts/rea.sh --lang en summary <work>/ref/breakdown.json
```
Run in the background, **one at a time** (8 GB Macs kill parallel runs). Read `VIDEO.md` and `video/*.md`
layer by layer; never read `breakdown.json` raw. Listen-proxies: `stems/music.wav` vs `stems/vocals.wav` levels
tell you if there is a music bed.

## 4. Measure what makes it recognisable
- Pacing: `python3 ../../scripts/style_stats.py <work>/ref/survey/timeline.json --video ref.mp4`.
- Text animation, frame by frame: `../../scripts/rea.sh tiles ref.mp4 --start A --end B --every 0.0333 -o t.jpg`
  around an entrance and an exit; count frames for fade in, hold, fade out, gaps; note rise/scale/blur.
- Colours: grab a frame with ffmpeg and read the exact background and accent hexes (most common pixels;
  saturated-pixel clusters for accents).
- Font: compare against system fonts by rendering the same words with `overlay.py --still` and stacking it on
  the original frame; then calibrate size by measuring ink width (see Style A: Times New Roman Bold 100/108 px).
- Camera: punch-in scale range and whether zooms animate or cut; B-roll angles, light, lens.
- Graphics inventory: every recurring overlay (labels, boxes, captions, stickers, memes) with position, size,
  timing, colour — each becomes an `overlay.py` template in `../../templates/`.
- Sound: integrated LUFS, pause count, music bed (stems), SFX moments (what visible event each one sits on).
- Narrative: the section order and how the hook works (from the transcript).

## 5. Write the playbook
Sections, as in the existing styles: the idea in one line · pacing table · each visual layer with exact values ·
sound · narrative shape · **recipe in Editroom** (which tools, which tracks, which templates, target numbers).
Mark anything estimated *(est.)*. Add new templates to `~/.edit-genius/templates/` and test-render each one with `--still` before saving.
Then tell the person what's distinctive about the style in 3–5 lines and offer to apply it.

## Rules
- Every claim has evidence (a frame, a number, a timestamp); write "unsure" rather than invent.
- Learn the grammar (timing, layout, palette roles, rhythm), never copy the content, footage, logos or music.
