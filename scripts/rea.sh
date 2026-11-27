#!/usr/bin/env bash
# Run rea-video (video reverse-engineering CLI, github.com/JuneYaooo/rea-video), installing it on first use.
#   rea.sh survey ref.mp4 -o out/ref
#   rea.sh --lang en decompose ref.mp4 -o out/ref --lang en --ocr-lang en --no-speakers
# Needs ffmpeg and a Python 3.10–3.14 (onnxruntime has no wheels for newer). On an 8 GB Mac run ONE decompose
# at a time — two in parallel get killed for memory (exit 137).
set -euo pipefail
for c in "${REA_VIDEO_BIN:-}" "$(command -v rea-video || true)" \
         "$HOME/Desktop/Ai-Auto-editor/tools/rea-video/.venv/bin/rea-video" \
         "$HOME/.local/share/edit-genius/rea-video/.venv/bin/rea-video"; do
  if [ -n "$c" ] && [ -x "$c" ]; then exec "$c" "$@"; fi
done
DIR="$HOME/.local/share/edit-genius/rea-video"
PY=""
for p in python3.12 python3.13 python3.11 python3.14 python3.10; do command -v "$p" >/dev/null && { PY="$p"; break; }; done
[ -n "$PY" ] || { echo "rea-video needs Python 3.10–3.14 (brew install python@3.12)" >&2; exit 1; }
echo "Installing rea-video into $DIR (first use)…" >&2
mkdir -p "$(dirname "$DIR")"
[ -d "$DIR" ] || git clone -q --depth 1 https://github.com/JuneYaooo/rea-video.git "$DIR"
"$PY" -m venv "$DIR/.venv"
"$DIR/.venv/bin/python" -m pip install -q --upgrade pip
"$DIR/.venv/bin/python" -m pip install -q -e "$DIR[ocr,asr]"
if "$DIR/.venv/bin/python" -m pip show opencv-python >/dev/null 2>&1; then
  "$DIR/.venv/bin/python" -m pip uninstall -y -q opencv-python
  "$DIR/.venv/bin/python" -m pip install -q --force-reinstall --no-deps "opencv-python-headless>=4.8,<5"
fi
exec "$DIR/.venv/bin/rea-video" "$@"
