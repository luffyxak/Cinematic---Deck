#!/usr/bin/env bash
# Crisp voice + remix + master, from two Editroom stems (Editroom has no EQ/compressor on audio).
#   voice_polish.sh video.mp4 voice.wav fx.wav out.mp4 [mute_ranges] [lufs=-14]
# voice.wav: export format:audio with only the voice track unmuted. fx.wav: the same with voice muted
# (music, SFX, bleep tones). video.mp4: any export of the same cut (its picture is copied untouched).
# mute_ranges: "95.133-95.433,120.5-120.8" — timeline seconds silenced in the voice (censoring). Do the
# muting here: Editroom clip gain -60 did NOT silence a word in an audio export (vowel came through).
set -euo pipefail
v="${1:?video}"; vo="${2:?voice stem}"; fx="${3:?fx stem}"; out="${4:?out}"; M="${5:-}"; I="${6:--14}"
T=$(mktemp -d); here="$(cd "$(dirname "$0")" && pwd)"
mute=""
if [ -n "$M" ]; then
  expr=$(python3 -c "import sys;r=[x.split('-') for x in sys.argv[1].split(',')];print('+'.join(f'between(t,{float(a)-0.005:.3f},{float(b)+0.005:.3f})' for a,b in r))" "$M")
  mute="volume=volume='if(${expr},0,1)':eval=frame,"
fi
# high-pass rumble, cut mud, gentle 3:1 compression, presence + air, de-ess
ffmpeg -v error -y -i "$vo" -af "${mute}highpass=f=80:poles=2,equalizer=f=250:t=q:w=1.0:g=-2.5,acompressor=threshold=-22dB:ratio=3:attack=5:release=90:makeup=2:knee=4,equalizer=f=3500:t=q:w=0.9:g=3,highshelf=f=9500:g=2,deesser=i=0.35:m=0.5:f=0.5:s=o" -c:a pcm_s24le "$T/voice.wav"
ffmpeg -v error -y -i "$T/voice.wav" -i "$fx" -filter_complex "[0:a][1:a]amix=inputs=2:duration=first:normalize=0[a]" -map "[a]" -c:a pcm_s24le "$T/mix.wav"
ffmpeg -v error -y -i "$v" -i "$T/mix.wav" -map 0:v -map 1:a -c:v copy -c:a pcm_s24le -shortest "$T/remix.mov"
# -2.5 dBTP ceiling: at -1.5 the AAC encode overshot to +0.2 dBTP on a mix with a sine bleep
bash "$here/master_loudness.sh" "$T/remix.mov" "$out" "$I" -2.5
rm -rf "$T"
