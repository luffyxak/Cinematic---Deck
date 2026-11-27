#!/usr/bin/env python3
"""Pacing numbers for a style playbook, from a rea-video survey timeline, plus loudness and pause stats.

    python3 style_stats.py out/ref/survey/timeline.json [--video ref.mp4]

Prints shot count, cuts/min overall and per 30 s window, shot-length mean/median/p10/p90/max and buckets,
transition mix, and (with --video) integrated loudness and how many pauses ≥ 0.25 s the voice leaves.
"""
import argparse
import collections
import json
import re
import statistics as st
import subprocess


def pct(xs, q):
    s = sorted(xs)
    return s[min(len(s) - 1, int(q * len(s)))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("timeline")
    ap.add_argument("--video")
    a = ap.parse_args()
    t = json.load(open(a.timeline))
    L = t["rhythm"]["shot_lengths"]
    cuts = t["cuts"]
    dur = sum(L)
    n = len(L)
    print(f"shots {n} in {dur/60:.0f}:{dur%60:04.1f} · cuts/min {60*(n-1)/dur:.1f}")
    print(f"shot length mean {st.mean(L):.2f}s median {st.median(L):.2f}s p10 {pct(L,.1):.2f} p90 {pct(L,.9):.2f} max {max(L):.2f}")
    b = [(0, .5), (.5, 1), (1, 2), (2, 4), (4, 1e9)]
    print("buckets " + " · ".join(f"{lo}-{hi if hi<1e9 else '∞'}s {100*sum(lo<=x<hi for x in L)/n:.0f}%" for lo, hi in b))
    k = collections.Counter(c["kind"] for c in cuts)
    print("transitions " + " · ".join(f"{name} {100*v/len(cuts):.0f}%" for name, v in k.most_common()))
    ts = [c["t"] for c in cuts]
    print("cuts per 30s " + str([sum(s <= x < s + 30 for x in ts) for s in range(0, int(dur) + 1, 30)]))
    if a.video:
        out = subprocess.run(["ffmpeg", "-nostats", "-i", a.video, "-af", "ebur128", "-f", "null", "-"],
                             capture_output=True, text=True).stderr
        m = re.findall(r"I:\s+(-?[\d.]+) LUFS", out)
        print(f"integrated loudness {m[-1] if m else '?'} LUFS")
        out = subprocess.run(["ffmpeg", "-nostats", "-i", a.video, "-af", "silencedetect=n=-40dB:d=0.25", "-f", "null", "-"],
                             capture_output=True, text=True).stderr
        d = [float(x) for x in re.findall(r"silence_duration: ([\d.]+)", out)]
        if d:
            print(f"pauses ≥0.25s: {len(d)} · mean {st.mean(d):.2f}s · max {max(d):.2f}s")
        else:
            print("pauses ≥0.25s: 0 (continuous bed or very tight cut)")


if __name__ == "__main__":
    main()
