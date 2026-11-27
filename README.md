# edit-genius

An expert-editor plugin for Claude Code that edits inside the **Editroom** Mac app. It learns a creator's editing
style from reference videos and applies it: cutting, pacing, punch-ins, kinetic text, meme inserts, captions,
sound design and loudness-correct export.

## What's inside
| Part | What it holds |
|---|---|
| `skills/edit-in-editroom` | The end-to-end workflow, plus `references/editroom.md`: every Editroom tool, its gaps and the tested workaround |
| `skills/cut-craft` | Speech cutting: fix names first, five-pass retake scan, delete-earlier-keep-later, padding and pause rules, visuals on phrase boundaries (video-use + chengfeng-videocut + auto-editor) |
| `skills/motion-graphics` | When to add graphics, measured timing rules, annotation rules, transitions, and the overlay renderer (HyperFrames motion research + chengfeng visual judgment) |
| `skills/sound-design` | Music/SFX sourcing (5,436 CC0 SFX + 1,222 CC0 tracks from OpenFilm), ducking, hit-on-the-frame, loudness |
| `skills/learn-style` | Reverse-engineer a new reference video into a measured playbook (rea-video + frame measurement) |
| `styles/` | Style A (kinetic-type review) and Style B (meme screen tour), measured from the practice videos |
| `templates/` | Overlay specs for the signature graphics of each style |
| `scripts/` | `overlay.py` (graphics → ProRes 4444 with transparency), `fx.sh` (deep-fry, red pulse, blur), `fetch_audio.sh`, `fetch_emoji.sh`, `rea.sh`, `style_stats.py` |
| `commands/` | `/edit-like`, `/learn-style`, `/review-cut` |
| `agents/cut-critic` | A ruthless reviewer for finished cuts |
| `preferences.md` | Template for `~/.edit-genius/preferences.md`, your lasting preferences (read first on every edit). Styles you teach it later go to `~/.edit-genius/styles/`, so plugin updates never erase them |

## Requirements
macOS, Editroom (connected to Claude Code in Editroom › Settings › Magic), ffmpeg, `uv` (for overlay.py),
Node/npx (for the CC0 library), yt-dlp (optional, for reference links), Python 3.10–3.14 (rea-video, auto-installed).

## Install
```bash
claude plugin marketplace add luffyxak/Cinematic---Deck   # from GitHub (private: needs your git login)
# or, from a local copy:
# claude plugin marketplace add ~/Desktop/Ai-Auto-editor/edit-genius
claude plugin install edit-genius@edit-genius-local
```
Asset downloads are cached in `~/Movies/edit-genius-cache` (set `EDIT_GENIUS_CACHE` to change).
