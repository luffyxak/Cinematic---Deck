#!/usr/bin/env bash
# Search or fetch free CC0 music / sound effects from OpenFilm's library (5,436 SFX, 1,222 music tracks).
#
#   fetch_audio.sh sfx   "fast whoosh for a cut"        # search: prints numbered matches with ids
#   fetch_audio.sh music "calm lo-fi bed for a tech review, 90 bpm"
#   fetch_audio.sh take  openfilm/audio/sfx/quick-reverse-whoosh-c500c9.mp3   # download → prints the local path
#
# Files land in $EDIT_GENIUS_CACHE/openfilm/assets (default ~/Movies/edit-genius-cache). Import that path into
# Editroom with import_media. Licence: CC0 1.0 (no credit needed) — see OpenFilm library/LICENSE.md.
set -euo pipefail
CACHE="${EDIT_GENIUS_CACHE:-$HOME/Movies/edit-genius-cache}/openfilm"
mkdir -p "$CACHE"
cd "$CACHE"
[ -f film.html ] || printf '<!doctype html><html><head><meta name="viewport" content="width=1920, height=1080"></head><body></body></html>\n' > film.html
mode="${1:-}"; shift || true
case "$mode" in
  sfx)   npx -y openfilm@latest get sfx-search --prompt "$*" ;;
  music) npx -y openfilm@latest get music-search --prompt "$*" ;;
  take)
    id="$1"
    if [[ "$id" == openfilm/audio/music/* ]]; then verb=music-search; else verb=sfx-search; fi
    out=$(npx -y openfilm@latest get "$verb" --take "$id" 2>&1)
    rel=$(printf '%s\n' "$out" | awk 'NR==1{print $1}')
    if [ -f "$CACHE/$rel" ]; then echo "$CACHE/$rel"; else printf '%s\n' "$out" >&2; exit 1; fi
    ;;
  *) sed -n '2,9p' "$0"; exit 2 ;;
esac
