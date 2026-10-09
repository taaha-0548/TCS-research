"""E8: stopping hazard and reuse probability as functions of time t = step/(n/2).
C2 (Exp(1) law) predicts hazard * (n/2) = 1 at every t.
Usage: python3 exp_t2_hazard.py [n] [trials]"""
import random, sys, json
from lollipop import random_instance, neighbors

def walk(n, chord):
    path = list(range(n)); pos = {v: i for i, v in enumerate(path)}
    forb = 0; seen = set(); reuse = []
    while True:
        z, prev = path[-1], path[-2]
        w = [x for x in neighbors(n, chord, z) if x != prev and x != forb][0]
        if w == 0: return reuse
        e = frozenset((z, w)); reuse.append(e in seen); seen.add(e)
        i = pos[w]
        path[i+1:] = path[i+1:][::-1]
        for j in range(i+1, n): pos[path[j]] = j
        forb = w

n = int(sys.argv[1]) if len(sys.argv) > 1 else 400
T = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
rng = random.Random(5)
B, W = 8, 0.25            # bins of width 0.25 in t, up to t = 2
alive = [0] * B; stops = [0] * B; rs = [0] * B; rc = [0] * B
for _ in range(T):
    r = walk(n, random_instance(n, rng)); L = len(r)
    for k in range(min(L + 1, int(B * W * n / 2))):
        b = int(k / (n / 2) / W)
        alive[b] += 1
        if k == L: stops[b] += 1
        elif k < L: rs[b] += r[k]; rc[b] += 1
out = []
for b in range(B):
    h = stops[b] / alive[b] * (n / 2) if alive[b] else None
    out.append(dict(t=(b + 0.5) * W, hazard_x_half_n=h, reuse_prob=rs[b] / rc[b] if rc[b] else None, n_alive=alive[b]))
    print(f"t~{(b+.5)*W:.3f}  hazard*(n/2)={h:.3f}  P(reuse)={rs[b]/max(1,rc[b]):.3f}  samples={alive[b]}")
json.dump(dict(n=n, trials=T, bins=out), open(f"e8_hazard_n{n}.json", "w"), indent=1)
