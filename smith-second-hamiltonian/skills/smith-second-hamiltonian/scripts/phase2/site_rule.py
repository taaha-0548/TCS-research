"""P2(b1): relation between the forward and backward visit types of a single site, from random hosts."""
import sys, random
from collections import Counter, defaultdict
sys.path.insert(0, ".."); sys.path.insert(0, "../../../../../paper")
from lollipop import random_instance
from linemirror import host_line, site_types
def chord_adj(n, ch): return [[(v - 1) % n, (v + 1) % n, ch[v]] for v in range(n)]
rng = random.Random(4); rel = defaultdict(Counter)
for _ in range(3000):
    n = rng.choice([12, 20, 30]); H = chord_adj(n, random_instance(n, rng))
    x = rng.randrange(3, n - 2)
    if x in H[0]: continue
    perm = list(range(3)); rng.shuffle(perm); pn = {u: "abc"[perm[j]] for j, u in enumerate(H[x])}
    line, _ = host_line(H, list(range(n)))
    fwd, bwd = site_types(H, line, [x], {x: pn})
    # pair a B1 site (entry step i, exit step i+1) or a B3 site (step i)
    for i, (xx, pr, kd) in fwd.items():
        if kd == "B3":
            b = bwd.get(i); rel[(pr, kd)][b[1:] if b else None] += 1
        else:
            b = bwd.get(i + 1); rel[(pr, kd)][b[1:] if b else None] += 1
for k in sorted(rel): print(k, "->", dict(rel[k]))
