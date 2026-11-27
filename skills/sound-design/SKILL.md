---
name: sound-design
description: Add music and sound effects to an Editroom edit like a sound designer — pick a licensed bed that fits the style, duck it under speech, place few, exact SFX on visible events (cuts, pops, clicks, text landing), and master to a delivery loudness. Use when an edit needs music, SFX, audio levels or loudness fixes.
---

# Sound design

Rules from video-use and HyperFrames (both shipped launch films), the free CC0 library from OpenFilm,
and Editroom's mixer. You can measure audio but not hear it — always say levels were measured, not listened to.

## Sources, in order
1. The person's own music/SFX (what they shot or paid for).
2. **OpenFilm CC0 library** — 1,222 music tracks, 5,436 SFX (foley, UI, stings, transitions, tech, impacts,
   ambience, nature, cartoon…). No credit needed.
   ```bash
   ../../scripts/fetch_audio.sh music "calm lo-fi bed for a tech review, 90 bpm"
   ../../scripts/fetch_audio.sh sfx "soft whoosh for a fast cut"
   ../../scripts/fetch_audio.sh take openfilm/audio/sfx/<id>.mp3     # → local path; then import_media it
   ```
   Search with the *feel and tempo*, not the subject. Read 3–5 results (duration, energy) before choosing.
3. Editroom `download_media` for a royalty-free track found on the web whose licence explicitly allows use
   without credit (CC0 or a site licence saying so) — direct audio-file link, plus source page and licence text.
4. Never take music from a source that doesn't clearly allow it.

## Music
- A film over ~15 s that tells something gets a bed unless the person wants silence or the style has none.
- Enter at the track's strongest bar, not its quiet intro; end on a bar line, fading out over the last ~2 s
  (`set_audio fade_out 2`). `analyze_media` on the track gives tempo, beats and bar starts — cut section
  changes on bars, quick cuts on beats when there's no voice leading.
- **Duck under speech**: the bed sits ~12–15 dB under its music-only level while someone talks — in Editroom
  around `gain_db -20` to `-24` on the music track (A2) relative to voice at 0. Bring it up 6–8 dB in gaps
  without voice (intro, outro, montage), using split music clips with their own gain and short fades.
- A bed with nearly all its energy under 150 Hz disappears on phone speakers — prefer beds with mids.
- Let music act out the story: hold it back until the payoff, drop it for a joke beat or a dramatic pause.

## Sound effects — few and exact
| Sound | Only on |
|---|---|
| whoosh | a scene/section cut, a big card or zoom moving fast |
| pop | a badge, icon, emoji or number landing |
| click | a real cursor click / keypress on screen |
| soft key tick | text arriving letter by letter |
| riser → impact | the payoff, once per film |
| record scratch / error buzz | a fail moment (Style B crash gag) |
- Every effect has a visible cause. ~8 designed hits in 18 s reads designed; ~20 reads generic.
- **Hit on the frame**: put the effect's peak 1 frame after the picture event (light before sound). Most files
  peak after their start: find the peak (`ffmpeg -i sfx.mp3 -af astats -f null -` or look at the waveform) and
  start the clip that much earlier.
- Rotate 2–3 takes of a repeated sound; the same whoosh on every cut is the most common tell.
- Effects sit 3–6 dB over the bed and under the voice. Put all SFX on their own track (A3).
- No synthesised beeps or chimes; over strong music a typing-heavy film can drop the clicks.

## Levels and master
- Voice is king: voice clips around 0 dB gain; if clips differ in level, even them out first.
- Nothing clips; true peak ≤ −1 dBTP.
- Deliver with `export loudness: -14` (YouTube/social), `-16` podcast, `-23` broadcast.
- Measure the export: `ffmpeg -i out.mp4 -af ebur128=peak=true -f null -` (integrated LUFS, true peak) and check
  music-only sections vs dialogue — an end card 15 dB under the dialogue, or SFX louder than speech, is a bug.

## Voice polish and censoring (Editroom has no audio EQ/compressor)
- For a crisp voice: export two stems with `export format: audio` — voice only (mute the other audio tracks with
  `set_track muted`), then everything but the voice — unmute all tracks afterwards. Then
  `../../scripts/voice_polish.sh video.mp4 voice.wav fx.wav final.mp4 "<mute ranges>"`: high-pass 80 Hz, −2.5 dB
  at 250 Hz, 3:1 compression, +3 dB at 3.5 kHz, air shelf, de-ess, remix, master to −14 LUFS.
- Bleeping a word: find the word's real edges in the waveform (transcript word times can be off by ~0.1 s; the
  "f" fricative starts before the vowel), cover onset → end of the final consonant. Generate the tone
  (`ffmpeg -f lavfi -i "sine=frequency=1000:duration=0.3" -af "volume=0.3,afade=t=in:d=0.006,afade=t=out:st=0.294:d=0.006"`),
  place it on its own audio track (don't overwrite a pop on A3), and silence the word in the voice stem via
  `voice_polish.sh`'s mute ranges — Editroom clip gain −60 did not silence it in the export.
- A bed the person called "too loud" at −24 sat right at −33 dB clip gain (voice −25 LUFS raw, bed ~18 LU under).

## Learned styles
- Style A: voice only, no music bed (verified by stem split), −19 LUFS original → deliver −14; VO tightly
  trimmed. At most a few soft SFX on keyword cards.
- Style B: voice only, no bed, −15 LUFS original; silence used as a comedic beat; gag inserts carry their own sound.
- So "music on every film over 15 s" is a default, not a law: when the learned style has none, don't add one
  unless the person asks.
