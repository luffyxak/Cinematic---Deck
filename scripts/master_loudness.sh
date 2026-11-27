#!/usr/bin/env bash
# Master an exported video to a delivery loudness with a true-peak ceiling (video stream copied untouched).
#   master_loudness.sh "in.mp4" "out.mp4" [target_lufs=-14] [true_peak=-1.5]
# Two-pass loudnorm (measure, then apply) + an oversampled limiter, then prints the measured result.
# Use it after every Editroom export: its `loudness` option has been seen not to apply (export came out at -25 LUFS).
set -euo pipefail
in="${1:?input}"; out="${2:?output}"; I="${3:--14}"; TP="${4:--1.5}"
J=$(ffmpeg -nostats -i "$in" -af "loudnorm=I=${I}:TP=${TP}:LRA=11:print_format=json" -f null - 2>&1 | sed -n '/^{/,/^}/p')
g() { printf '%s' "$J" | python3 -c "import sys,json;print(json.load(sys.stdin)['$1'])"; }
MI=$(g input_i); MTP=$(g input_tp); MLRA=$(g input_lra); MTH=$(g input_thresh); OFF=$(g target_offset)
LIM=$(python3 -c "print(round(10**((${TP}-0.6)/20),3))")   # limiter a little under the ceiling (AAC overshoot)
ffmpeg -v error -y -i "$in" -c:v copy -af "aresample=192000,loudnorm=I=${I}:TP=${TP}:LRA=11:measured_I=${MI}:measured_TP=${MTP}:measured_LRA=${MLRA}:measured_thresh=${MTH}:offset=${OFF},alimiter=limit=${LIM}:attack=2:release=60:level=disabled,aresample=48000" -c:a aac -b:a 256k "$out"
echo "input: ${MI} LUFS, true peak ${MTP} dBTP"
ffmpeg -nostats -i "$out" -af ebur128=peak=true -f null - 2>&1 | grep -A14 Summary | grep -E "I:|Peak:" | sed 's/^ */output: /'
