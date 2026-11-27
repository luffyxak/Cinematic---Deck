#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pillow>=10"]
# ///
"""Render a motion-graphics overlay from a JSON spec to ProRes 4444 (keeps transparency in Editroom).

    uv run overlay.py spec.json -o out.mov          # transparent overlay (default)
    uv run overlay.py spec.json -o out.mov --still 0.5 --png frame.png   # check one frame

Spec (all times in seconds from the overlay's own start; x/y are 0..1 of the frame, the element's centre):
{
  "width": 1920, "height": 1080, "fps": 30, "duration": 2.0,
  "background": null,                 # or "#ECE4DA" for an opaque card
  "layers": [
    {"type": "phrase", "start": 0, "end": 1.2, "x": 0.5, "y": 0.5, "size": 66, "font": "times-bold",
     "runs": [{"text": "is that it's "}, {"text": "modular", "color": "#F2604A"}],
     "color": "#000000", "in": {"fade": 0.1, "rise": 6}, "out": {"fade": 0.067}},
    {"type": "meme", "text": "*Doesn't work*", "start": 0, "end": 2, "x": 0.62, "y": 0.2, "size": 70,
     "font": "din-condensed", "color": "#FFFFFF", "stroke": "#000000", "stroke_width": 5},
    {"type": "kbd", "text": "cmd + c", "start": 0, "end": 2, "x": 0.12, "y": 0.86, "size": 44},
    {"type": "box", "start": 0, "end": 2, "x": 0.5, "y": 0.5, "w": 0.3, "h": 0.1, "stroke": "#FF2D2D",
     "stroke_width": 6, "fill": null, "radius": 10},
    {"type": "dim", "start": 0, "end": 2, "opacity": 0.55, "hole": {"x": 0.5, "y": 0.5, "w": 0.3, "h": 0.1, "radius": 12}},
    {"type": "image", "path": "/abs/icon.png", "start": 0, "end": 2, "x": 0.5, "y": 0.4, "height": 0.12, "in": {"pop": 0.18}}
  ]
}
Every layer also takes "in": {"fade": s, "rise": px, "pop": s, "blur": px} and "out": {"fade": s}.
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONTS = {
    "times-bold": "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
    "times-bold-italic": "/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf",
    "times": "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
    "georgia-bold": "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
    "impact": "/System/Library/Fonts/Supplemental/Impact.ttf",
    "din-condensed": "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf",
    "din-bold": "/System/Library/Fonts/Supplemental/DIN Alternate Bold.ttf",
    "arial-black": "/System/Library/Fonts/Supplemental/Arial Black.ttf",
    "helvetica": "/System/Library/Fonts/Helvetica.ttc",
    "sf": "/System/Library/Fonts/SFNS.ttf",
    "menlo": "/System/Library/Fonts/Menlo.ttc",
}


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    path = FONTS.get(name, name)
    if not Path(path).exists():
        sys.exit(f"font not found: {name} ({path}) — pass a key of FONTS or an absolute .ttf/.otf path")
    return ImageFont.truetype(path, size)


def rgba(c, alpha: float = 1.0):
    if c is None:
        return None
    c = c.lstrip("#")
    if len(c) == 6:
        c += "ff"
    r, g, b, a = (int(c[i:i + 2], 16) for i in (0, 2, 4, 6))
    return (r, g, b, int(a * max(0.0, min(1.0, alpha))))


def ease_out_cubic(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def ease_out_back(t: float, s: float = 1.6) -> float:
    t = max(0.0, min(1.0, t)) - 1
    return t * t * ((s + 1) * t + s) + 1


def envelope(layer: dict, t: float):
    """Returns (opacity, dy_px, scale, blur_px) for a layer at time t, or None when it is not on screen."""
    start, end = layer.get("start", 0.0), layer.get("end", 1e9)
    if t < start or t >= end:
        return None
    lin, lout = layer.get("in", {}), layer.get("out", {})
    op, dy, sc, bl = 1.0, 0.0, 1.0, 0.0
    if lin.get("fade"):
        k = ease_out_cubic((t - start) / lin["fade"])
        op *= k
        dy = lin.get("rise", 0) * (1 - k)
        bl = lin.get("blur", 0) * (1 - k)
    if lin.get("pop"):
        k = (t - start) / lin["pop"]
        sc = ease_out_back(k) if k < 1 else 1.0
        op *= min(1.0, k * 3)
    if lout.get("fade"):
        k = (end - t) / lout["fade"]
        if k < 1:
            op *= max(0.0, k)
    return op, dy, sc, bl


def text_runs_image(layer: dict, alpha: float, _scale: float = 1.0) -> Image.Image:
    """Renders the runs; with "max_width" (px) a too-long line is shrunk uniformly to fit (title-safe)."""
    if _scale == 1.0 and layer.get("max_width"):
        probe = text_runs_image({**layer, "max_width": None}, alpha)
        mw = float(layer["max_width"])
        if probe.width > mw:
            return text_runs_image({**layer, "max_width": None}, alpha, mw / probe.width)
        return probe
    size = int(layer.get("size", 64) * _scale)
    if _scale != 1.0:
        layer = {**layer, "runs": [{**r, "size": int(r["size"] * _scale)} if "size" in r else r
                                   for r in (layer.get("runs") or [{"text": layer.get("text", "")}])]}
    base_font = layer.get("font", "times-bold")
    default_color = layer.get("color", "#000000")
    runs = layer.get("runs") or [{"text": layer.get("text", "")}]
    pieces = []
    for r in runs:
        f = font(r.get("font", base_font), int(r.get("size", size)))
        bbox = f.getbbox(r["text"])
        adv = f.getlength(r["text"])
        pieces.append((r, f, adv, bbox))
    asc = max(p[1].getmetrics()[0] for p in pieces)
    desc = max(p[1].getmetrics()[1] for p in pieces)
    stroke = int(layer.get("stroke_width", 0)) if layer.get("stroke") else 0
    pad = stroke + 8
    w = int(sum(p[2] for p in pieces)) + 2 * pad
    h = asc + desc + 2 * pad
    img = Image.new("RGBA", (max(w, 1), max(h, 1)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x = pad
    for r, f, adv, _ in pieces:
        fill = rgba(r.get("color", default_color), alpha)
        kw = {}
        if stroke:
            kw = {"stroke_width": stroke, "stroke_fill": rgba(layer["stroke"], alpha)}
        d.text((x, pad + asc), r["text"], font=f, fill=fill, anchor="ls", **kw)
        x += adv
    return img


def kbd_image(layer: dict, alpha: float) -> Image.Image:
    size = int(layer.get("size", 44))
    f = font(layer.get("font", "sf"), size)
    tw = int(f.getlength(layer["text"]))
    padx, pady = int(size * 0.5), int(size * 0.3)
    img = Image.new("RGBA", (tw + 2 * padx, size + 2 * pady), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    bg = layer.get("bg")
    if bg:
        d.rounded_rectangle([0, 0, img.width - 1, img.height - 1], radius=int(size * 0.3), fill=rgba(bg, alpha))
    d.text((padx, img.height / 2), layer["text"], font=f, fill=rgba(layer.get("color", "#FFFFFF"), alpha), anchor="lm",
           stroke_width=int(layer.get("stroke_width", 0)), stroke_fill=rgba(layer.get("stroke", "#000000"), alpha))
    return img


_image_cache: dict[str, Image.Image] = {}


def picture(layer: dict, H: int) -> Image.Image:
    p = layer["path"]
    if p not in _image_cache:
        _image_cache[p] = Image.open(p).convert("RGBA")
    im = _image_cache[p]
    target_h = int(layer.get("height", 0.12) * H)
    return im.resize((max(1, int(im.width * target_h / im.height)), target_h), Image.LANCZOS)


def paste_centered(frame: Image.Image, el: Image.Image, cx: float, cy: float, scale: float, blur: float, opacity: float):
    if scale != 1.0:
        el = el.resize((max(1, int(el.width * scale)), max(1, int(el.height * scale))), Image.LANCZOS)
    if blur > 0.3:
        el = el.filter(ImageFilter.GaussianBlur(blur))
    if opacity < 0.999:
        a = el.getchannel("A").point(lambda v: int(v * opacity))
        el.putalpha(a)
    frame.alpha_composite(el, (int(cx - el.width / 2), int(cy - el.height / 2)))


def draw_frame(spec: dict, t: float) -> Image.Image:
    W, H = spec.get("width", 1920), spec.get("height", 1080)
    bg = rgba(spec.get("background")) if spec.get("background") else (0, 0, 0, 0)
    frame = Image.new("RGBA", (W, H), bg)
    for layer in spec["layers"]:
        env = envelope(layer, t)
        if env is None:
            continue
        op, dy, sc, bl = env
        if op <= 0.002:
            continue
        kind = layer["type"]
        cx, cy = layer.get("x", 0.5) * W, layer.get("y", 0.5) * H + dy
        if kind in ("phrase", "meme", "text"):
            paste_centered(frame, text_runs_image(layer, 1.0), cx, cy, sc, bl, op)
        elif kind == "kbd":
            el = kbd_image(layer, 1.0)
            ax = layer.get("anchor", "left")
            if ax == "left":
                cx += el.width / 2
            paste_centered(frame, el, cx, cy, sc, bl, op)
        elif kind == "image":
            paste_centered(frame, picture(layer, H), cx, cy, sc, bl, op)
        elif kind in ("box", "dim"):
            el = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            d = ImageDraw.Draw(el)
            if kind == "dim":
                d.rectangle([0, 0, W, H], fill=(0, 0, 0, int(255 * layer.get("opacity", 0.55))))
                hole = layer.get("hole")
                if hole:
                    hx, hy, hw, hh = hole["x"] * W, hole["y"] * H, hole["w"] * W, hole["h"] * H
                    d.rounded_rectangle([hx - hw / 2, hy - hh / 2, hx + hw / 2, hy + hh / 2],
                                        radius=int(hole.get("radius", 12)), fill=(0, 0, 0, 0))
            else:
                bw, bh = layer["w"] * W, layer["h"] * H
                d.rounded_rectangle([cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2],
                                    radius=int(layer.get("radius", 10)), fill=rgba(layer.get("fill")),
                                    outline=rgba(layer.get("stroke", "#FF2D2D")), width=int(layer.get("stroke_width", 6)))
            if op < 0.999:
                el.putalpha(el.getchannel("A").point(lambda v: int(v * op)))
            frame.alpha_composite(el)
        else:
            sys.exit(f"unknown layer type: {kind}")
    return frame


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec")
    ap.add_argument("-o", "--out", required=True, help=".mov (ProRes 4444, alpha) or .mp4 (opaque H.264)")
    ap.add_argument("--still", type=float, help="render only this time to --png, for checking")
    ap.add_argument("--png")
    a = ap.parse_args()
    spec = json.loads(Path(a.spec).read_text())
    if a.still is not None:
        draw_frame(spec, a.still).save(a.png or "still.png")
        print(a.png or "still.png")
        return
    W, H, fps, dur = spec.get("width", 1920), spec.get("height", 1080), spec.get("fps", 30), spec["duration"]
    n = int(round(dur * fps))
    out = Path(a.out)
    if out.suffix.lower() == ".mov":
        venc = ["-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", "-vendor", "apl0"]
    else:
        venc = ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16"]
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(fps),
           "-i", "-", *venc, str(out)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    last_key, last_bytes = None, None
    for i in range(n):
        t = i / fps
        # reuse the previous frame when nothing is animating (holds are most of a card's life)
        key = tuple(None if (e := envelope(l, t)) is None else tuple(round(v, 4) for v in e) for l in spec["layers"])
        if key != last_key:
            last_bytes = draw_frame(spec, t).tobytes()
            last_key = key
        proc.stdin.write(last_bytes)
    proc.stdin.close()
    if proc.wait() != 0:
        sys.exit("ffmpeg failed")
    print(json.dumps({"out": str(out), "frames": n, "duration": dur}))


if __name__ == "__main__":
    main()
