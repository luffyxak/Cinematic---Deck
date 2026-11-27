---
name: cut-craft
description: Cut speech-led footage like a pro editor — voiceovers, talking heads, tutorials, reviews: fix misheard words first, remove retakes, false starts, stutters, filler and dead air on word boundaries, keep the rhythm natural, and lay visuals on phrase boundaries. Use when cleaning up narration or A-roll, tightening a cut, or deciding where cuts go.
---

# Cut craft

Combined from video-use (audio-first EDL editing), chengfeng-videocut (semantic deletion, proven on real projects)
and auto-editor (silence/motion first pass). Read it whole before cutting speech.

## Principles
1. **Audio is primary, visuals follow.** Cut candidates come from word boundaries and silences; check pictures only
   at decision points.
2. **Fix the words before judging them.** Transcripts mishear names and terms (one test: "Grok" came back as
   Clock / Glock / Gokul in the same file). Correct your reading first — a wrong name is not a reason to delete.
   Never invent words that weren't said; if you can't confirm a name, flag it.
3. **Read in playback order.** "Said twice" means adjacent *as it plays*, not as stored in the file. On an edited
   timeline, rebuild the playing order before judging repeats.
4. **Two states only:** a word is cut or kept. Don't hand the person "maybe" lists; decide, then let them review.

## The five-pass retake scan
Read the whole transcript five times, each time looking for ONE kind of problem (one criterion per pass is far
more accurate than all at once). Later passes skip what's already marked.

| Pass | Look for | Default action | Risk |
|---|---|---|---|
| 1 | Repeats: a sentence or phrase said twice | delete the **earlier**, keep the later complete one | low if fully contained; high for whole sentences |
| 2 | Fragments & restarts: a sentence abandoned and restarted differently | delete the fragment(s); a chain of fragments goes as one group | low |
| 3 | Misspoken then corrected: wrong number, name or word, then said right | delete the wrong version | high |
| 4 | Stutters on a word head / letters / syllables (incl. English words in other languages) | delete the stutter | low |
| 5 | Filler & tics (um, uh, like, you know, so…) | delete runs of 2+; keep a single natural filler unless the style is tight | subjective |

**Delete-earlier-keep-later** is the rule. Branching restarts (same opening, different ending): if both carry
different information it's not a repeat — keep both. For high-risk cuts, re-read the context and confirm the
remaining sentence reads cleanly; if you can't confirm, don't cut.

Then build two tables for the person: every cut (time · type · removed · reads-as · risk) and a repeated-sentence
table (sentence · times said · which take kept · which removed). Read the result end to end once; undo any cut
that makes it read badly.

## Where and how to cut
- Never cut inside a word. Snap every edge to a word boundary.
- Pad edges **30–200 ms** (transcript timestamps drift 50–100 ms). Worked example: 50 ms before the first kept
  word, 80 ms after the last. Fast styles (Style A) sit at the tight end.
- Silences ≥ 400 ms are the cleanest cuts; 150–400 ms usable with a check; < 150 ms is mid-phrase — avoid.
- Dead air: tight styles leave ~0.1–0.25 s between sentences (Style A had only 23 pauses ≥ 0.25 s in 5 min).
  Keep a longer pause only when it's a beat (a joke, a reveal — Style B kept one 4.3 s comedic silence).
- Preserve peaks: laughs, punchlines, reactions — extend past them; the laugh IS the beat.
- Speaker handoffs want 400–600 ms of air.
- Audio pops: Editroom crossfades nothing by default — put a 0.03 s `set_audio` fade_in/fade_out on speech clips
  at hard joins if a click is likely (cut on a non-zero sound).
- Never reason audio and picture separately: every cut must work on both.

## Laying visuals over the voice
- Change the visual on a **phrase boundary** (a comma, a breath, the start of a new idea), not mid-word.
- Land each graphic or punch-in on the **payoff word**: start a reveal `reveal_duration` before the word so it
  lands on it.
- Hold a readable line ≈ 0.5 s + 0.3 s per word; the film's last line ≥ 2 s.
- Contrast speeds: quick cuts during lists and jokes, a held 4–10 s shot when the UI or action is the point.
- J/L cuts (sound leads or trails the picture by 0.2–0.5 s) make section changes feel smooth.

## First pass on long raw footage (optional)
For hour-long raw takes, a silence pre-cut saves time: `auto-editor in.mp4 --edit audio:-30dB --margin 0.1s,0.15s
--export premiere` (or just `--preview` to see what would go). Then do the semantic passes above on what's left.
Useful auto-editor ideas even inside Editroom: speed up silent stretches instead of cutting them (`-w:0 speed:4`)
for screen recordings where something still happens on screen.

## Structures that work (pick, adapt, or invent)
- Review / app video: HOOK → what it is → "here's the rundown" → feature sections → verdict → soft CTA
- Tech launch / demo: HOOK → PROBLEM → SOLUTION → BENEFIT → EXAMPLE → CTA
- Tutorial: INTRO → SETUP → STEPS → GOTCHAS → RECAP
- Exploration / first look: cold open → headline features → discover in order → honest reactions → wrap
