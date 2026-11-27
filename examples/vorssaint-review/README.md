# Worked example: "Vorssaint review" (Style A, kinetic review)

The build files from a real 5:52 edit made in Editroom with this plugin. Footage, renders and the final video
are not included (only the plan and the scripts that produced it).

| File | What it is |
|---|---|
| `vo_phrases.txt`, `vo_segments.json` | voiceover cleaned into phrases (retakes and gaps removed) |
| `edl.py` → `edl.json` | edit decision list: which screen moment or text card illustrates each phrase |
| `build.py` → `ops.json` | renders the text cards/overlays with `scripts/overlay.py` and emits Editroom operations |
| `plan.json`, `batches.txt` | frame-rounded placement plan (V1/V2 alternation for speed changes) |

Audio finish: bed at −33 dB clip gain, voice stems processed with `scripts/voice_polish.sh` (EQ, compression,
de-ess, one bleeped word), mastered to −14.5 LUFS / −1.6 dBTP.
