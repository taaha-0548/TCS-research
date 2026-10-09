"""E23: nested families with NON-simple poles (memory, reflections), screened by direct simulation.
Deterministic family F(K, x, r, perm) as in nested_family.py; K random with > 3 Ham cycles allowed.
Sustained growth = geometric mean of the last 3 level factors (max over all starts of C_k)."""
import random, sys, time, json
from lollipop import random_instance
from general import from_chord
from nested_family import family
nk, budget, seed = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3])
rng = random.Random(seed); perms = [(0,1,2),(0,2,1),(1,0,2),(1,2,0),(2,0,1),(2,1,0)]
t0 = time.time(); res = []
while time.time() - t0 < budget:
    ch = random_instance(nk, rng); x = rng.randrange(2, nk - 1)
    if x == ch[0]: continue
    r = rng.choice([v for v in range(nk) if v != x and v not in ((x-1) % nk, (x+1) % nk, ch[x])])
    perm = rng.choice(perms)
    try: seq = family(from_chord(nk, ch), list(range(nk)), x, r, perm, 4)
    except Exception: continue
    if len(seq) < 5 or min(s for _, s in seq[1:]) == 0: continue
    g = (seq[4][1] / seq[1][1]) ** (1 / 3)
    res.append((g ** (1 / (nk - 2)), seq, ch, x, r, perm))
res.sort(key=lambda t: -t[0])
print(f"|K|={nk}: {len(res)} families screened; best sustained per-vertex growth:")
for b, seq, ch, x, r, perm in res[:5]: print(f"  {b:.4f}  seq={seq}  chord={ch} x={x} r={r} perm={perm}")
json.dump([dict(base=b, seq=s, chord=c, x=x, r=r, perm=p) for b, s, c, x, r, p in res[:20]], open(f"e23_memory_K{nk}.json", "w"))
