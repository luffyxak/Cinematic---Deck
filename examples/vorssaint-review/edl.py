"""Edit decision list for the Vorssaint review, Style A. Times are VO-source seconds unless named R (recording)."""
import json, re, bisect

W = json.load(open('vo_transcript.json'))['words']           # [start, end, text]
SEG = json.load(open('vo_segments.json'))
F = 1 / 30

def norm(s): return re.sub(r"[^a-z0-9]", "", s.lower())

def wt(phrase, near):
    """start time of `phrase` (first words) in the VO nearest to `near`."""
    toks = [norm(t) for t in phrase.split()]
    best = None
    for i in range(len(W) - len(toks) + 1):
        if all(norm(W[i + k][2]).startswith(toks[k]) for k in range(len(toks))):
            d = abs(W[i][0] - near)
            if best is None or d < best[0]: best = (d, W[i][0])
    if best is None or best[0] > 8: raise SystemExit(f"not found: {phrase} @ {near}")
    return best[1]

def out(t):
    """VO source time → timeline time (snapped to frame)."""
    for s in SEG:
        if t < s['src_start']:
            v = s['out_start']; break
        if t <= s['src_end']:
            v = s['out_start'] + (t - s['src_start']); break
    else:
        v = SEG[-1]['out_end']
    return round(round(v / F) * F, 3)

FILL = (1.112, 0.5, 0.5)
# ---- V1 visual track: ("rec", src_t, R0, R1, (scale, fx, fy)) or ("card", src_t, [runs...])
C = lambda *runs: [r if isinstance(r, dict) else {"text": r} for r in runs]
BLUE, GREEN, CORAL, CRIM = "#0070DD", "#2E6B33", "#F2604A", "#C8302A"
def k(text, color, italic=False, size=108):
    d = {"text": text, "color": color, "size": size}
    if italic: d["font"] = "times-bold-italic"
    return d

V = [
 # HOOK
 ("card", wt("One free Mac app", 0.8), C("One ", k("free", GREEN), " Mac app")),
 ("rec",  wt("that replaces", 2.2), 6.0, 9.2, FILL),                    # 6 app icons → arrow
 ("card", wt("you might not", 4.7), C("you might not need ", k("anymore", CORAL))),
 ("rec",  wt("volume mixer", 6.6), 85.0, 88.0, (1.35, 0.6, 0.38)),
 ("rec",  wt("system monitor", 8.1), 97.0, 100.0, (1.15, 0.6, 0.45)),
 ("rec",  wt("screenshot editor", 9.1), 136.0, 139.0, FILL),
 ("rec",  wt("cleaner", 10.6), 179.0, 182.0, (1.112, 0.6, 0.5)),
 ("rec",  wt("clipboard manager", 11.3), 189.0, 192.0, (1.5, 0.6, 0.35)),
 ("rec",  wt("Windows manager", 12.4), 223.0, 226.0, (1.2, 0.72, 0.45)),
 ("rec",  wt("all inside one", 13.4), 9.2, 13.0, FILL),                  # icons merge into the logo
 ("card", wt("cold war sent", 15.4), C(k("Vorssaint", BLUE, size=120))),
 ("card", wt("Not corset", 17.7), C("not ", k("croissant", CORAL))),
 ("card", wt("It's worsened", 18.9), C("It's ", k("Vorssaint", BLUE))),
 ("card", wt("So if you want", 20.6), C("So if you want a ", k("faster", GREEN), " workflow")),
 ("card", wt("without paying", 23.5), C("without paying for ", k("extra apps", CORAL))),
 ("card", wt("This video is", 26.4), C("this video is for ", k("you", BLUE))),
 ("card", wt("So let's get", 28.4), C("So let's get ", k("started", GREEN))),
 # INSTALL
 ("rec",  wt("Now open Firefox", 30.7), 21.0, 30.0, FILL),
 ("rec",  wt("open the 1st", 35.5), 30.0, 33.5, FILL),
 ("rec",  wt("and click on", 37.3), 37.0, 48.0, (1.9, 0.9, 0.28)),        # download button, right side
 ("rec",  wt("It's downloading", 42.5), 43.0, 48.0, FILL),
 ("rec",  wt("Now open the file", 44.0), 48.0, 54.0, (1.8, 0.37, 0.45)),    # drag into Applications
 ("rec",  wt("and launch it", 49.0), 54.0, 56.0, FILL),
 ("card", wt("And by the way", 52.8), C("it needs an ", k("Apple silicon", BLUE), " Mac")),
 ("card", wt("with macOS", 56.5), C("with ", k("macOS 14", BLUE), " or newer")),
 ("card", wt("So check that", 58.9), C("so check that ", k("first", CORAL))),
 # DYNAMIC ISLAND TEASE
 ("rec",  wt("Okay, now see", 61.7), 56.0, 61.0, (3.0, 0.5, 0.02)),
 ("card", wt("It's one of the best", 65.6), C("one of the ", k("best parts", GREEN))),
 ("card", wt("I will show you", 68.4), C("I'll show you why ", k("later", BLUE))),
 # MENU
 ("rec",  wt("Now, 1st up", 74.0), 60.0, 66.0, (1.5, 0.6, 0.3)),
 # KEEP AWAKE
 ("card", wt("First, keep awake", 83.4), C(k("Keep Awake", CRIM, italic=True))),
 ("rec",  wt("it stop your", 84.6), 66.0, 78.0, (1.5, 0.6, 0.3)),
 ("card", wt("It's like caffeine", 91.7), C("like ", k("caffeinate", BLUE))),
 ("card", wt("but without opening", 93.5), C("without opening ", k("Terminal", CORAL))),
 ("rec",  wt("and it's good", 96.0), 78.0, 82.0, (1.5, 0.6, 0.3)),
 # VOLUME MIXER
 ("rec",  wt("Next, and I love", 99.1), 82.0, 85.0, (1.35, 0.6, 0.38)),
 ("card", wt("the volume mixer", 101.3), C("the ", k("volume mixer", CRIM, italic=True))),
 ("rec",  wt("you can control", 102.4), 85.0, 96.0, (1.35, 0.6, 0.38)),
 ("card", wt("and Apple never", 109.5), C("Apple never gave us this ", k("natively", CORAL))),
 ("card", wt("So, Apple", 116.7), C("So, ", k("Apple", CORAL), "…")),
 # MONITOR
 ("rec",  wt("So here is the system", 120.3), 96.0, 102.0, (1.15, 0.6, 0.45)),
 ("rec",  wt("And another one", 127.1), 102.0, 113.0, (1.45, 0.6, 0.35)),
 ("rec",  wt("And this one is", 133.1), 113.0, 118.0, (1.12, 0.6, 0.5)),
 ("card", wt("Oh my god", 141.3), C(k("Oh my god", CORAL, italic=True))),
 ("card", wt("31 terabytes", 144.4), C(k("31 TB", CORAL), " read")),
 ("card", wt("87 terabyte", 146.9), C(k("87 TB", CORAL), " written")),
 ("card", wt("Interesting", 150.4), C(k("Interesting", CORAL, italic=True))),
 ("rec",  wt("And for the battery", 152.3), 120.0, 127.0, (1.45, 0.6, 0.35)),
 ("card", wt("And now, it is", 159.3), C("now, a very ", k("interesting", CORAL), " section")),
 # SCREENSHOT
 ("rec",  wt("1st of all", 162.5), 129.0, 134.0, (2.2, 0.5, 0.1)),
 ("rec",  wt("Take a screenshot", 166.9), 134.0, 150.0, FILL),
 ("rec",  wt("And his like", 176.4), 150.0, 168.0, FILL),
 # CLEANER
 ("card", wt("Then there is the cleaner", 188.1), C("the ", k("Cleaner", CRIM, italic=True))),
 ("rec",  wt("hit scan", 189.5), 168.0, 186.0, (1.112, 0.6, 0.5)),
 # CLIPBOARD
 ("card", wt("Next is clipboard", 205.4), C(k("Clipboard history", CRIM, italic=True))),
 ("rec",  wt("super useful on", 207.6), 186.0, 195.0, (1.5, 0.6, 0.35)),
 ("rec",  wt("Let me show", 215.3), 195.0, 222.0, FILL),
 # WINDOW LAYOUT
 ("rec",  wt("Then there is a window", 228.4), 222.0, 228.0, (1.2, 0.72, 0.45)),
 ("rec",  wt("If you got", 235.0), 345.0, 351.0, (1.3, 0.48, 0.5)),
 # COLOR PICKER / ISLAND
 ("card", wt("And the color picker", 241.4), C("the ", k("colour picker", CRIM, italic=True))),
 ("rec",  wt("I use this feature", 242.9), 226.5, 232.0, FILL),
 ("rec",  wt("You can also grab", 251.7), 232.0, 238.0, FILL),
 ("card", wt("And here is my favorite", 256.3), C("my ", k("favourite trick", GREEN))),
 ("rec",  wt("I will create a new folder", 259.9), 238.0, 247.0, FILL),
 ("card", wt("It works like", 267.0), C("like ", k("temporary storage", BLUE))),
 ("rec",  wt("if you are editing", 269.5), 247.0, 256.0, FILL),
 ("card", wt("It's super useful", 277.2), C("super ", k("useful", GREEN))),
 ("rec",  wt("Like, that's why", 280.6), 375.0, 386.0, (1.6, 0.47, 0.2)),
 # CUSTOMISE / QUICK PANEL
 ("rec",  wt("And you can customize", 290.0), 258.0, 267.0, FILL),
 ("card", wt("You already seen", 296.5), C(k("Quick panel", CRIM, italic=True))),
 ("rec",  wt("It keeps your favorite", 302.0), 267.0, 276.0, FILL),
 ("card", wt("Like cleaning mode", 308.3), C(k("Cleaning mode", CRIM, italic=True))),
 ("rec",  wt("when you are wiping", 309.6), 276.0, 282.0, FILL),
 ("card", wt("It's very useful", 315.5), C("very ", k("useful", GREEN))),
 # RADIAL MENU
 ("card", wt("Then the radical menu", 320.9), C("the ", k("radial menu", CRIM, italic=True))),
 ("rec",  wt("I really use", 323.9), 282.0, 286.0, FILL),
 ("card", wt("It's a wheel", 327.1), C("a wheel of your own ", k("shortcuts", BLUE))),
 ("rec",  wt("To add something", 333.5), 286.0, 300.0, FILL),
 ("rec",  wt("Now I open the menu", 341.0), 300.0, 320.0, FILL),
 # KEEP AWAKE LID CLOSED
 ("card", wt("Remember, keep awake", 351.5), C("remember ", k("Keep Awake", CRIM, italic=True), "?")),
 ("rec",  wt("It can also keep", 353.4), 321.0, 336.0, (1.3, 0.5, 0.5)),
 ("card", wt("Super useful feature", 365.0), C("super ", k("useful", GREEN))),
 # CUT & PASTE
 ("rec",  wt("If you miscut", 367.3), 351.0, 366.0, (1.3, 0.5, 0.5)),
 # SHELF / UNINSTALLER
 ("rec",  wt("No, this one", 377.9), 378.0, 386.0, (1.6, 0.47, 0.2)),
 ("rec",  wt("there's an Stoller", 384.3), 366.0, 375.0, (1.3, 0.48, 0.5)),
 ("rec",  wt("You can also set up", 394.6), 336.0, 345.0, (1.3, 0.48, 0.5)),
 # OUTRO
 ("card", wt("So that's worsened", 418.3), C("So that's ", k("Vorssaint", BLUE))),
 ("card", wt("free open source", 420.0), C(k("free", GREEN), " and ", k("open source", GREEN))),
 ("card", wt("and packed with", 421.6), C("packed with tools you usually ", k("pay for", CORAL))),
 ("card", wt("Try it yourself", 426.0), C(k("Try it", GREEN), " yourself")),
 ("card", wt("tell me in", 427.2), C("which feature do you use ", k("most", CORAL), "?")),
 ("card", wt("If this helped", 431.2), C("like & ", k("subscribe", CORAL))),
]
END_SRC = 436.6  # VO end

# ---- V2 overlays on top: (src_t, kind, payload, seconds)
EM = "~/Desktop/Ai-Auto-editor/asset-cache/emoji/"
O = [
 (wt("Not corset", 17.7) + 0.25, "emoji", EM + "croissant_3d.png", 0.9),
 (wt("fuck you", 117.4) , "emoji", EM + "middle_finger_3d.png", 0.6),
 (wt("Oh my god", 141.3), "emoji", EM + "exploding_head_3d.png", 1.0),
 (wt("command, C", 222.4), "kbd", "cmd + C", 0.5),
 (wt("command V", 223.5), "kbd", "cmd + V", 1.4),
 (wt("press command X", 370.5), "kbd", "cmd + X", 0.9),
 (wt("command V and", 371.9), "kbd", "cmd + V", 1.4),
 (wt("If this helped", 431.2) + 1.0, "emoji", EM + "thumbs_up_3d.png", 2.0),
]

if __name__ == "__main__":
    items = []
    for i, it in enumerate(V):
        s0 = it[1]
        s1 = V[i + 1][1] if i + 1 < len(V) else END_SRC
        t0, t1 = out(s0), out(s1)
        if i == 0: t0 = 0.0
        items.append({"kind": it[0], "t0": t0, "t1": t1, "dur": round(t1 - t0, 3), **(
            {"R0": it[2], "R1": it[3], "scale": it[4][0], "fx": it[4][1], "fy": it[4][2]} if it[0] == "rec" else {"runs": it[2]})})
    over = [{"t": out(s), "kind": k_, "payload": p, "dur": d} for s, k_, p, d in O]
    json.dump({"v1": items, "v2": over}, open("edl.json", "w"), indent=1)
    for x in items:
        extra = f"R {x['R0']}-{x['R1']} speed {(x['R1']-x['R0'])/x['dur']:.2f}" if x['kind'] == 'rec' else ''.join(r['text'] for r in x['runs'])
        print(f"{x['t0']:7.2f} {x['dur']:5.2f} {x['kind']:4} {extra}")
    print("overlays:", [(o['t'], o['kind']) for o in over])
