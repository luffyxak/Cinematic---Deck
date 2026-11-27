#!/usr/bin/env bash
# Bake effects Editroom has no tool for. Output is a normal clip to import_media and place on the timeline.
#
#   fx.sh deepfry  in.mp4 out.mp4 [zoom=2.2] [cx=0.5] [cy=0.5]   # meme "error" look: punch-in, crushed contrast,
#                                                                #   oversaturation, red vignette, low-res crunch
#   fx.sh redpulse in.mp4 out.mp4                                # red vignette only, pulsing twice a second
#   fx.sh blurbg   in.mp4 out.mp4 [sigma=18]                     # blurred, darkened backdrop (put a crop on top)
#   fx.sh still    in.mp4 out.png  <time>                        # grab a frame (for a freeze or a torn-paper card)
#   fx.sh alpha    in.png out.mov <seconds>                      # PNG (with transparency) → ProRes 4444 clip
# Note: this ffmpeg build has no drawtext — text goes through overlay.py.
set -euo pipefail
cmd="${1:-}"; in="${2:-}"; out="${3:-}"
case "$cmd" in
  deepfry)
    z="${4:-2.2}"; cx="${5:-0.5}"; cy="${6:-0.5}"
    IFS=x read -r W H < <(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0:s=x "$in")
    ffmpeg -v error -y -i "$in" -vf "crop=iw/$z:ih/$z:(iw-iw/$z)*$cx:(ih-ih/$z)*$cy,\
scale=trunc($W/6)*2:trunc($H/6)*2,scale=$W:$H:flags=neighbor,eq=contrast=1.6:saturation=2.4:brightness=-0.03,\
unsharp=7:7:2.5,vignette=angle=PI/3.2,colorchannelmixer=rr=1.25:gg=0.85:bb=0.8,format=yuv420p" \
      -c:v libx264 -crf 16 -c:a copy "$out" ;;
  redpulse)
    ffmpeg -v error -y -i "$in" -vf "vignette=angle='PI/3.5+0.25*sin(2*PI*2*t)':eval=frame,colorchannelmixer=rr=1.15:gg=0.9:bb=0.9,format=yuv420p" \
      -c:v libx264 -crf 16 -c:a copy "$out" ;;
  blurbg)
    s="${4:-18}"
    ffmpeg -v error -y -i "$in" -vf "gblur=sigma=$s,eq=brightness=-0.12,format=yuv420p" -c:v libx264 -crf 18 -an "$out" ;;
  still)
    ffmpeg -v error -y -ss "${4:?time}" -i "$in" -frames:v 1 "$out" ;;
  alpha)
    ffmpeg -v error -y -loop 1 -t "${4:?seconds}" -r 30 -i "$in" -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le "$out" ;;
  *) sed -n '2,11p' "$0"; exit 2 ;;
esac
echo "$out"
