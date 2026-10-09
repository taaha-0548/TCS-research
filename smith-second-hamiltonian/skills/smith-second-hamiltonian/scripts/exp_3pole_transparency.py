"""E9: are 3-edge-cut gadgets transparent to the lollipop walk?
Host H (random cubic Ham graph, chord form). Replace vertex x (not v0) by a 3-pole X.
Transparent  <=>  the walk on G, projected back onto H (X contracted to x), ends in the same
Ham cycle as the walk on H, for every way C0 can traverse X.
Usage: python3 exp_3pole_transparency.py"""
import random, json, itertools
from lollipop import random_instance
from general import lollipop_g, from_chord, substitute, cyc_edges, is_ham

def pole_from_cubic(adj, r):
    """3-pole = cubic graph minus vertex r; ports = r's neighbours."""
    keep = [v for v in range(len(adj)) if v != r]; idx = {v: i for i, v in enumerate(keep)}
    padj = [[idx[w] for w in adj[v] if w != r] for v in keep]
    return padj, [idx[w] for w in adj[r]]

K4 = [[1,2,3],[0,2,3],[0,1,3],[0,1,2]]
K33 = [[3,4,5],[3,4,5],[3,4,5],[0,1,2],[0,1,2],[0,1,2]]
PRISM = [[1,2,3],[0,2,4],[0,1,5],[0,4,5],[1,3,5],[2,3,4]]
PETERSEN = [[1,4,5],[0,2,6],[1,3,7],[2,4,8],[3,0,9],[0,7,8],[1,8,9],[2,9,5],[3,5,6],[4,6,7]]
CUBE = [[1,3,4],[0,2,5],[1,3,6],[0,2,7],[0,5,7],[1,4,6],[2,5,7],[3,4,6]]
def random_cubic_ham(n, rng): return from_chord(n, random_instance(n, rng))

def project(cyc, X, x):
    out = []
    for v in cyc:
        u = x if v in X else v
        if not out or out[-1] != u: out.append(u)
    if out[0] == out[-1]: out.pop()
    return out

rng = random.Random(3)
poles = {"triangle(K4-v)": pole_from_cubic(K4, 0), "K33-v": pole_from_cubic(K33, 0),
         "prism-v": pole_from_cubic(PRISM, 0), "petersen-v": pole_from_cubic(PETERSEN, 0),
         "cube-v": pole_from_cubic(CUBE, 0)}
for k in range(6):
    g = random_cubic_ham(10, rng); poles[f"rand10-v#{k}"] = pole_from_cubic(g, 0)
res = {}
for name, (padj, ports) in poles.items():
    tests = mism = 0; ex = None
    for _ in range(300):
        n = rng.choice([10, 12, 16, 20, 30]); chord = random_instance(n, rng)
        H = from_chord(n, chord); C = list(range(n))
        x = rng.randrange(2, n - 1)              # keep v0=0, v1=1 and v_{n-1} outside X
        perm = list(ports); rng.shuffle(perm)
        G, cycles, X = substitute(H, C, x, padj, perm)
        if not cycles: continue
        sH, cH, _ = lollipop_g(H, C)
        for c0 in cycles:
            assert is_ham(G, c0)
            sG, cG, _ = lollipop_g(G, c0)
            assert is_ham(G, cG)
            tests += 1
            if cyc_edges(project(cG, X, x)) != cyc_edges(cH):
                mism += 1
                if ex is None: ex = dict(n=n, chord=chord, x=x, ports=perm, c0=c0, sH=sH, sG=sG)
    res[name] = dict(tests=tests, mismatches=mism, example=ex)
    print(f"{name:16s} tests={tests:4d} mismatches={mism}")
json.dump(res, open("e9_3pole.json", "w"), indent=1, default=str)
