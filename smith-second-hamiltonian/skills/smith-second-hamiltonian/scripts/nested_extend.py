"""E18: extend one nested family deep, evaluating all starts up to level A, then only the
top-5 (start, direction) pairs of the previous level (outer-K labels are stable).
Usage: python3 nested_extend.py levels all_upto"""
import sys, json, time
from general import from_chord, lollipop_g
from nested import to_pole
from nested_family import subst_fixed
CH = [4, 3, 6, 1, 0, 7, 2, 5]; X = 5; R = 2; PERM = (2, 0, 1)   # E17c family (K=8)
L = int(sys.argv[1]); A = int(sys.argv[2])
K = from_chord(8, CH); Kc = list(range(8))
G, Gc = K, Kc; rl = R; out = []; top = None; t0 = time.time()
def run(G, Gc, s, d):
    n = len(Gc); c = [Gc[(s + d * t) % n] for t in range(n)]
    st, cyc, _ = lollipop_g(G, c, max_steps=10**8); return st
for lev in range(L + 1):
    n = len(Gc); pos = {v: i for i, v in enumerate(Gc)}
    if lev <= A or top is None:
        cand = [(Gc[s], d) for s in range(n) for d in (1, -1)]
    else:
        cand = top
    res = sorted(((run(G, Gc, pos[v], d), v, d) for v, d in cand if v in pos), reverse=True)
    best = res[0][0]; top = [(v, d) for _, v, d in res[:5]]
    out.append((n, best)); print(f"level {lev}: n={n} steps={best}  ({time.time()-t0:.0f}s)", flush=True)
    if lev == L: break
    P, ports = to_pole(G, rl)
    G, Gc = subst_fixed(K, Kc, X, P, ports, PERM)
    rl = R if R < X else R - 1
json.dump(out, open("e18_extend.json", "w"))
s = [b for _, b in out]
print("two-level factors:", [round(s[i+2] / s[i], 3) for i in range(len(s) - 2)])
print("per-vertex (two-level):", [round((s[i+2] / s[i]) ** (1/12), 4) for i in range(len(s) - 2)])
