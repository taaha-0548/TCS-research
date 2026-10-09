"""E17c: screen with sustained growth (geometric mean of the last 3 level factors),
then extend the best families deeper.  Usage: python3 nested_deep.py nk screen_s deep_levels seed"""
import random, sys, time, json
from lollipop import random_instance
from general import from_chord
from nested_family import family
nk, budget, D, seed = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
rng = random.Random(seed); perms = [(0,1,2),(0,2,1),(1,0,2),(1,2,0),(2,0,1),(2,1,0)]
t0 = time.time(); found = {}
while time.time() - t0 < budget:
    ch = random_instance(nk, rng); x = rng.randrange(2, nk - 1)
    if x == ch[0]: continue
    r = rng.choice([v for v in range(nk) if v != x]); perm = rng.choice(perms)
    key = (tuple(ch), x, r, perm)
    if key in found: continue
    try: seq = family(from_chord(nk, ch), list(range(nk)), x, r, perm, 4)
    except (TimeoutError, RuntimeError, AssertionError): continue
    if len(seq) < 5 or min(s for _, s in seq[1:]) == 0: continue
    g = (seq[4][1] / seq[1][1]) ** (1 / 3)
    found[key] = (g, seq)
best = sorted(found.items(), key=lambda kv: -kv[1][0])[:4]
need = 1.1812 ** (nk - 2)
print(f"|K|={nk}: screened {len(found)}; sustained factor needed: {need:.3f}")
out = []
for (ch, x, r, perm), (g, seq) in best:
    if time.time() - t0 > budget + 150: break
    try: seq = family(from_chord(nk, list(ch)), list(range(nk)), x, r, perm, D)
    except (TimeoutError, RuntimeError, AssertionError): pass
    facs = [round(seq[i+1][1] / seq[i][1], 3) for i in range(len(seq) - 1) if seq[i][1]]
    per_v = (seq[-1][1] / seq[-3][1]) ** (1 / (seq[-1][0] - seq[-3][0]))
    print(f"  chord={list(ch)} x={x} r={r} perm={perm}\n    seq={seq}\n    level factors={facs}  per-vertex (last 2 levels)={per_v:.4f}")
    out.append(dict(chord=list(ch), x=x, r=r, perm=perm, seq=seq, per_vertex=per_v))
json.dump(out, open(f"e17c_K{nk}.json", "w"), indent=1)
