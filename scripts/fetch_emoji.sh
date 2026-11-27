#!/usr/bin/env bash
# Download a Microsoft Fluent Emoji PNG (MIT licence — free for any use) for use as an overlay.py `image` layer
# or an Editroom image clip.
#
#   fetch_emoji.sh "Fire"                 # 3D style (default) → prints the local .png path
#   fetch_emoji.sh "Thumbs up" flat       # styles: 3d | color | flat | high-contrast
#   fetch_emoji.sh "Face with tears of joy"
# Names are the emoji's English CLDR name (as in the folder names of github.com/microsoft/fluentui-emoji/assets).
set -euo pipefail
name="${1:?emoji name, e.g. \"Fire\"}"; style="${2:-3d}"
CACHE="${EDIT_GENIUS_CACHE:-$HOME/Movies/edit-genius-cache}/emoji"; mkdir -p "$CACHE"
folder=$(python3 -c 'import sys,urllib.parse;n=sys.argv[1];print(urllib.parse.quote(n[0].upper()+n[1:]))' "$name")
slug=$(printf '%s' "$name" | tr '[:upper:]' '[:lower:]' | tr ' ' '_' | tr -d "'")
case "$style" in
  3d) sub="3D"; file="${slug}_3d.png" ;;
  color) sub="Color"; file="${slug}_color.svg" ;;
  flat) sub="Flat"; file="${slug}_flat.svg" ;;
  high-contrast) sub="High%20Contrast"; file="${slug}_high_contrast.svg" ;;
  *) echo "style: 3d | color | flat | high-contrast" >&2; exit 2 ;;
esac
out="$CACHE/$file"
base="https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/$folder"
if [ ! -s "$out" ]; then
  # emoji with skin tones keep their files under Default/<style>/<slug>_<style>_default.<ext>
  curl -fsSL "$base/$sub/$file" -o "$out" 2>/dev/null \
    || curl -fsSL "$base/Default/$sub/${file%.*}_default.${file##*.}" -o "$out" 2>/dev/null \
    || { rm -f "$out"; echo "not found: '$name' ($style). Check the exact name in the fluentui-emoji assets folder." >&2; exit 1; }
fi
echo "$out"
