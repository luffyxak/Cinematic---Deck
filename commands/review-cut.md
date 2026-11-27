---
description: Critique the current Editroom timeline against a style, then offer fixes
argument-hint: [style name] [focus, e.g. "pacing" or "sound"]
---
Review the edit that is open in Editroom. Arguments: $ARGUMENTS

Spawn the cut-critic agent with: the style file (if named), the output of get_project, and the transcript of the main
speech clip. When it reports, show the person its verdict and top 5 fixes, and offer to apply them — don't change the
timeline until they say so.
