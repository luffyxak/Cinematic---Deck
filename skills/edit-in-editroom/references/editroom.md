# Editroom: what it does, what it doesn't, and the workaround

Learned from Editroom's source (v1.0.9) and tested live. Endpoint: `http://127.0.0.1:47920/mcp`.

## Model
- Times in seconds. Video tracks V1, V2, … (higher covers lower); audio A1, A2, …. `add_track` adds one on top.
- A video with sound is a linked pair; `detach_audio` to treat picture and sound separately.
- Placing/moving onto an occupied stretch of a track **overwrites** what's there. Plan track use:
  V1 spine/visuals, V2 graphics & cards, V3+ extra overlays; A1 voice, A2 music, A3 SFX.
- Every tool call is one undo step (`history undo`).

## Native and good
| Need | Tool |
|---|---|
| Cut / trim / ripple | `split_clip`, `trim_clip`, `delete_clips ripple:true`, `move_clip` |
| Punch-in, reframe, animated zoom | `set_transform` (`scale`, `focus_x/y`, `zoom` in/in_out/out/off, `zoom_seconds`, `zoom_start`) |
| Speed, ramps, freeze, reverse | `set_speed`, `set_speed_ramp`, `freeze_frame`, `reverse_clip` |
| Fades | `set_audio fade_in/fade_out` — on a sound clip it fades sound; on video/photo/title/solid it fades the **picture's opacity** (true transparency, so titles fade over footage) |
| Transitions | `set_transition` dissolve / dipToBlack / wipe (0.5 s default) |
| Text | `add_title` + `set_title_style` (font installed on the Mac, size in pt for a 1080-high frame, colour, bold, x/y centre) — one font/colour/size per title |
| Captions from speech | `set_captions` (word highlight, position, size; `edit` fixes words) |
| Solid colour cards | `add_solid`, `set_solid_color` |
| Colour | `set_grade` (exposure, contrast, saturation, temperature, tint, look, .cube LUT) |
| Levels | `set_audio gain_db`, `set_track gain_db/mute/solo` |
| Find shots | `search_media shows/said`, `get_transcript`, `analyze_media` (best moments; song tempo/beats/bars) |
| Music from the web | `download_media` — **audio files only**, https direct link, licence noted |
| Export | `export` (h264/hevc, height, loudness LUFS, shape vertical/square/portrait + reframe point, range only, wav) |

## Gaps → workaround
| Gap | Workaround (tested) |
|---|---|
| Multi-colour phrase, inline icons, text that rises, per-word animation | Render with `scripts/overlay.py` → ProRes 4444 `.mov`; `import_media`; put it on V2+. **Transparency is kept** (tested: red box over a blue solid composited correctly). |
| Images/stickers/emoji over video | PNG with alpha imports directly as an image clip; or `fx.sh alpha` to a .mov; position with `set_transform` |
| Blur, vignette, deep-fry, glow, dim-except-panel | Bake with `scripts/fx.sh` (deepfry, redpulse, blurbg) or `overlay.py` `dim` layer with a hole |
| Keyframed movement of overlays | Bake the motion into the overlay render; or use `set_transform zoom` on the overlay clip |
| SFX / music outside `download_media` | `scripts/fetch_audio.sh` (CC0 library) → `import_media` the printed path |
| Text via ffmpeg | This Mac's ffmpeg has no `drawtext`; use `overlay.py` |
| Long first-pass silence cut of raw footage | Transcript-based cutting (cut-craft); optional `auto-editor --edit audio:-30dB --export premiere` for very long raw takes |

## Gotchas (learned on real edits)
- **Frame snapping**: every start and duration snaps to a frame (1/30 s). Compute all placements frame-rounded
  from ONE master timeline (`round(t*fps)/fps`), never by repeatedly rounding up the previous end: rounding up
  per clip drifted a 6-minute voiceover 0.9 s late versus the planned visuals.
- **Speed ripple**: `set_speed` moves only the clips *butted* against it (a clip 6 s away did not move). To build
  a sequence of speed-changed shots safely, alternate shots between V1 and V2 (gaps on each track), add each clip
  with its full source length, then `set_speed` it before placing anything that would overlap it.
- After speed changes, ends can land 1 frame short of the next shot → a 1-frame black flash. Fix with
  `trim_clip end=<next start>`, and verify on the export: `ffmpeg -i out.mp4 -vf blackdetect=d=0.03:pic_th=0.98 -an -f null -`.
- **Export loudness**: `export loudness:-14` produced -25 LUFS on one 6-min export. Always measure the file and
  master with `scripts/master_loudness.sh in.mp4 out.mp4 -14` (two-pass loudnorm + true-peak limiter).
- `export wait:true` times out on long videos; poll `export_status` instead.
- A screen recording made with an auto-zoom recorder (Screen Studio etc.) already contains zooms: build a gridded
  framing sheet (frames at key moments with a 10% grid) before choosing punch-ins, or you zoom on a zoom.
- A screen recording's own (silent) audio still lands on an audio track when placed: strip it first
  (`ffmpeg -i in.mp4 -an -c:v copy silent.mp4`) and use the silent copy.
- 16:10 Mac recordings (1728×1080) pillarbox in 1920×1080: `set_transform scale 1.112` fills the frame.
- `import_media` can time out on big files while the Mac is busy but still finish: `list_media` before retrying.
- Clip `gain_db -60` on a split-out word did not silence it in an audio export (vowel still at full level):
  censor in the voice stem with `scripts/voice_polish.sh` mute ranges, and measure the export.
- `export format: audio` + `set_track muted` gives clean stems (voice / everything else) for processing.
- Hidden tracks don't export; locked tracks refuse edits.
- `set_title_style` x/y are the text centre (0–1); Style A cards are x 0.5, y 0.5.
- Editroom's own Magic popover runs Claude through the Claude chat app; this plugin's knowledge applies when
  Editroom is driven from Claude Code.
