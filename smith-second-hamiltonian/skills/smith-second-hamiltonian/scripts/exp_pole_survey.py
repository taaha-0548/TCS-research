"""E15: survey random 3-poles (random cubic Hamiltonian graph minus a vertex) by transducer class:
  transparent   - never reflects
  fixed-mirror  - reflects, but T/R never depends on the internal path index
  active-memory - for some port pair, orientation and visit type, T/R depends on the index"""
import random, json
from collections import Counter, defaultdict
from transducer import transducer
from exp_3pole_transparency import pole_from_cubic, random_cubic_ham

def classify(padj, ports):
    T = transducer(padj, ports)
    if not T: return "no-states", 0
    refl = any(v[k][0] == "REFLECT" for v in T.values() for k in v)
    if not refl: return "transparent", len(T)
    by = defaultdict(set)
    for Q, v in T.items():
        for k in v: by[(Q[0], Q[-1], k)].add(v[k][0])
    return ("active-memory" if any(len(s) > 1 for s in by.values()) else "fixed-mirror"), len(T)

rng = random.Random(23); out = {}
for m in (8, 10, 12, 14, 16):
    c = Counter(); maxst = 0
    for _ in range(150 if m <= 12 else 60):
        g = random_cubic_ham(m, rng); padj, ports = pole_from_cubic(g, rng.randrange(m))
        k, ns = classify(padj, ports); c[k] += 1; maxst = max(maxst, ns)
    out[m] = dict(c); print(f"|X|={m-1:2d}: {dict(c)}  max oriented states={maxst}")
json.dump(out, open("e15_pole_survey.json", "w"), indent=1)
