"""Render card blocks + overlays and emit the Editroom operation list (ops.json)."""
import json, subprocess, os
F = 1 / 30
fr = lambda t: round(round(t / F) * F, 3)
E = json.load(open('edl.json'))
OV = '~/Desktop/Ai-Auto-editor/edit-genius/scripts/overlay.py'
os.makedirs('graphics', exist_ok=True)

# 1. split long demos into two framings
v1 = []
for x in E['v1']:
    if x['kind'] == 'rec' and x['dur'] > 7.0:
        mid_t = fr(x['t0'] + x['dur'] / 2)
        mid_R = x['R0'] + (x['R1'] - x['R0']) * (mid_t - x['t0']) / x['dur']
        a = {**x, 't1': mid_t, 'dur': round(mid_t - x['t0'], 3), 'R1': round(mid_R, 3)}
        fill = x['scale'] <= 1.12
        b = {**x, 't0': mid_t, 'dur': round(x['t1'] - mid_t, 3), 'R0': round(mid_R, 3),
             'scale': round(min(1.6, max(1.3, x['scale'] * 1.25)), 3),
             'fx': 0.5 if fill else x['fx'], 'fy': 0.45 if fill else x['fy']}
        v1 += [a, b]
    else:
        v1.append(x)

# 2. group consecutive cards into blocks and render each block
ops, blocks, cur = [], [], []
for x in v1 + [{'kind': 'end'}]:
    if x['kind'] == 'card':
        cur.append(x)
        continue
    if cur:
        blocks.append(cur); cur = []
    if x['kind'] == 'rec':
        blocks.append(x)

def render(spec, name):
    path = f'graphics/{name}'
    json.dump(spec, open(path + '.json', 'w'))
    subprocess.run(['uv', 'run', '--quiet', '--script', OV, path + '.json', '-o', path + ('.mp4' if spec.get('background') else '.mov')], check=True, capture_output=True)
    return os.path.abspath(path + ('.mp4' if spec.get('background') else '.mov'))

n = 0
for b in blocks:
    if isinstance(b, list):
        n += 1
        t0, t1 = b[0]['t0'], b[-1]['t1']
        layers = []
        for i, c in enumerate(b):
            s = c['t0'] - t0
            e = (c['t1'] - t0) - (F if i < len(b) - 1 else 0)   # one blank frame between phrases
            layers.append({"type": "phrase", "start": round(s, 3), "end": round(e, 3), "x": 0.5, "y": 0.5,
                           "size": 100, "max_width": 1500, "font": "times-bold", "color": "#000000",
                           "runs": c['runs'], "in": {"fade": 0.1, "rise": 6}, "out": {"fade": 0.067}})
        spec = {"width": 1920, "height": 1080, "fps": 30, "duration": round(t1 - t0, 3), "background": "#ECE4DA", "layers": layers}
        ops.append({"op": "card", "t0": t0, "dur": round(t1 - t0, 3), "file": render(spec, f'card_{n:02d}'),
                    "text": ' | '.join(''.join(r['text'] for r in c['runs']) for c in b)})
    else:
        sp = (b['R1'] - b['R0']) / b['dur']
        ops.append({"op": "rec", "t0": b['t0'], "dur": b['dur'], "R0": b['R0'], "R1": b['R1'],
                    "speed": round(sp, 4), "scale": b['scale'], "fx": b['fx'], "fy": b['fy']})

# 3. overlays (V2)
EMOJI_POS = {"croissant": (0.70, 0.47), "middle_finger": (0.66, 0.47), "exploding_head": (0.82, 0.24), "thumbs_up": (0.71, 0.47)}
for i, o in enumerate(E['v2']):
    d = o['dur']
    if o['kind'] == 'kbd':
        lay = {"type": "kbd", "text": o['payload'], "start": 0, "end": d, "x": 0.06, "y": 0.86, "size": 54, "font": "sf",
               "anchor": "left", "color": "#FFFFFF", "stroke": "#000000", "stroke_width": 3, "in": {"fade": 0.08}, "out": {"fade": 0.08}}
    else:
        key = next(k for k in EMOJI_POS if k in o['payload'])
        x, y = EMOJI_POS[key]
        lay = {"type": "image", "path": o['payload'], "start": 0, "end": d, "x": x, "y": y, "height": 0.16,
               "in": {"pop": 0.18}, "out": {"fade": 0.1}}
    spec = {"width": 1920, "height": 1080, "fps": 30, "duration": d, "background": None, "layers": [lay]}
    ops.append({"op": "overlay", "t0": o['t'], "dur": d, "file": render(spec, f'ov_{i:02d}'), "what": o['payload']})

json.dump(ops, open('ops.json', 'w'), indent=1)
recs = [o for o in ops if o['op'] == 'rec']; cards = [o for o in ops if o['op'] == 'card']
cuts = len(v1)
print(f"{len(recs)} screen shots, {len(cards)} card blocks ({sum(1 for x in v1 if x['kind']=='card')} phrases), "
      f"{len(ops)-len(recs)-len(cards)} overlays; visual changes {cuts} in {v1[-1]['t1']:.0f}s → {60*cuts/v1[-1]['t1']:.1f}/min")
