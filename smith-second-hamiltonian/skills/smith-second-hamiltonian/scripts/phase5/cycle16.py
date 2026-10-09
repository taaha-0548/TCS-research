"""Cycle 16.  Cross-tabulate (a) the growth regime of the minimal automaton of random single-slot towers
(depth 1..5, minimising each level) with (b) whether multi-reflection visits occur at the top levels
(levels 4, 5).  Question: are towers that are exponential-incompressible AND multi-reflecting common?"""
import io, contextlib, random, time, sys
sys.path.insert(0, "../phase3")
from collections import Counter, defaultdict
with contextlib.redirect_stdout(io.StringIO()):
    from selfsimilar2 import chord_adj
    from cycle15 import level, bases
from tower import minimise, quotient
import verify as V
from lollipop import random_instance
rng = random.Random(16); tab = Counter(); examples = defaultdict(list); t0 = time.time(); N = 0
while time.time() - t0 < 200:
    n = rng.choice([8, 10, 12]); K = chord_adj(n, random_instance(n, rng))
    try: P1, ports1, _ = V.pole(K, rng.randrange(n))
    except Exception: continue
    xs = [v for v in range(len(P1)) if P1[v] and v not in ports1]
    if not xs: continue
    x = rng.choice(xs); perm = list(range(3)); rng.shuffle(perm); bi = rng.randrange(len(bases)); A = bases[bi]
    sizes, badl = [], []
    try:
        for lev in range(5):
            A, c = level(P1, ports1, x, perm, A)
            if not A["states"]: break
            m, cls = minimise(A); A = quotient(A, cls); sizes.append(m)
            badl.append(c[">=2 R-calls"] + c["T after R"] > 0)
            if m > 3000: break
    except Exception: continue
    if len(sizes) < 5: continue
    N += 1
    r = sizes[4] / sizes[3]
    reg = "bounded" if sizes[4] == sizes[3] else ("exponential (x>=2.5)" if r >= 2.5 else "polynomial")
    mr = "multi-R at top" if (badl[3] or badl[4]) else "single-turn at top"
    tab[(reg, mr)] += 1
    if len(examples[(reg, mr)]) < 3: examples[(reg, mr)].append(dict(n=n, K=K, r=None, x=x, perm=perm, base=bi, sizes=sizes, bad=badl))
print(f"{N} random towers of depth 5")
for k in sorted(tab): print(f"  {k}: {tab[k]}   e.g. sizes {[e['sizes'] for e in examples[k]]}")
import json
json.dump({str(k): v for k, v in examples.items()}, open("cycle16_examples.json", "w"))
