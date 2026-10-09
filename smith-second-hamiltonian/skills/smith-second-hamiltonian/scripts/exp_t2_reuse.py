"""E7: classify edges the lollipop walk re-adds, and test attach uniformity on reuse steps.
Usage: python3 exp_t2_reuse.py [n] [trials]"""
import random, sys, json
from collections import Counter
from lollipop import random_instance, neighbors

def walk(n, chord):
    path = list(range(n)); pos = {v: i for i, v in enumerate(path)}
    forb = 0; last = {}; rec = []
    k = 0
    while True:
        z, prev = path[-1], path[-2]
        w = [x for x in neighbors(n, chord, z) if x != prev and x != forb][0]
        if w == 0: return rec
        i = pos[w]; e = frozenset((z, w))
        is_chord = chord[z] == w
        gap = k - last[e] if e in last else None
        rec.append(dict(p=i / n, chord=is_chord, gap=gap, back=(n - 1 - i)))
        last[e] = k; k += 1
        path[i+1:] = path[i+1:][::-1]
        for j in range(i+1, n): pos[path[j]] = j
        forb = w

n = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
T = int(sys.argv[2]) if len(sys.argv) > 2 else 300
rng = random.Random(11)
recs = []
for _ in range(T): recs += walk(n, random_instance(n, rng))
tot = len(recs)
fresh = [r for r in recs if r["gap"] is None]; reuse = [r for r in recs if r["gap"] is not None]
def dec(rs): 
    c = Counter(min(9, int(r["p"] * 10)) for r in rs); return [round(c[d] / max(1, len(rs)), 3) for d in range(10)]
gaps = Counter(min(r["gap"], 10) for r in reuse)
out = dict(n=n, trials=T, steps=tot,
  frac_chord_all=sum(r["chord"] for r in recs) / tot,
  frac_reuse=len(reuse) / tot,
  frac_chord_among_fresh=sum(r["chord"] for r in fresh) / len(fresh),
  frac_chord_among_reuse=sum(r["chord"] for r in reuse) / max(1, len(reuse)),
  reuse_gap_hist={str(g) if g < 10 else ">=10": gaps[g] / len(reuse) for g in sorted(gaps)},
  deciles_fresh=dec(fresh), deciles_reuse=dec(reuse),
  mean_steps_over_half_n=tot / T / (n / 2))
for k, v in out.items(): print(k, v)
json.dump(out, open(f"e7_reuse_n{n}.json", "w"), indent=1)
