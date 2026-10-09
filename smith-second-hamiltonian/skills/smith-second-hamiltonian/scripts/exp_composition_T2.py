"""T2: exact walk length on G_k for every start, predicted from K's walk and c_{k-1}:
    steps(G_k; v0, d) = steps(K; v0, d) + sum_f N_f(v0, d) * c_{k-1}[f]
N_f = passages of kind f through x in K's lollipop walk.  Hypothesis of the Mirror Lemma:
v0 not in {x} u N(x).  Starts violating it are reported separately (control)."""
import json
from collections import Counter
from general import from_chord
from nested_fast import rotate_to, next_level
CH = [4, 3, 6, 1, 0, 7, 2, 5]; X, R, PERM = 5, 2, (2, 0, 1)
K = from_chord(8, CH); Kc = list(range(8))
xname = {u: "abc"[PERM[k]] for k, u in enumerate(K[X])}
keys = [tuple(s.split("/")) for s in json.load(open("e20_M.json"))["keys"]]
M = json.load(open("e20_M.json"))["M"]; c = [json.load(open("e20_M.json"))["b"]]
for k in range(12): c.append([c0 + sum(M[i][j] * c[-1][j] for j in range(12)) for i, c0 in enumerate(c[0])])

def walk_log(A, cyc):
    v0 = cyc[0]; path = list(cyc); pos = {v: i for i, v in enumerate(path)}; forb = v0; steps = 0; log = []
    while True:
        z, prev = path[-1], path[-2]
        w = [u for u in A[z] if u != prev and u != forb][0]
        if w == v0: return steps, log
        i = pos[w]; s = path[i+1]; log.append((tuple(path), z, w, s))
        path[i+1:] = path[i+1:][::-1]
        for j in range(i+1, len(path)): pos[path[j]] = j
        forb = w; steps += 1

def N_of(log, x):
    N = Counter()
    for path, z, w, s in log:
        if s == x or w == x:
            j = path.index(x); N[(xname[path[j-1]] + xname[path[j+1]], "B1" if s == x else "B3")] += 1
    return N

from general import lollipop_g
starts = [(v, d) for v in range(8) for d in (1, -1)]
pred = {}
for v, d in starts:
    st, log = walk_log(K, rotate_to(Kc, v, d))
    pred[(v, d)] = (st, N_of(log, X))
kl = {v: j for j, v in enumerate(v for v in range(8) if v != X)}
G, Gc = K, Kc; rl = R; ok = Counter(); bad = Counter()
for k in range(1, 9):
    G, Gc = next_level(K, Kc, X, G, [Gc], rl, PERM); rl = R if R < X else R - 1
    for v, d in starts:
        if v == X: continue
        st = lollipop_g(G, rotate_to(Gc, kl[v], d), max_steps=10**8)[0]
        st0, N = pred[(v, d)]
        p = st0 + sum(N[f] * c[k-1][keys.index(f)] for f in N)
        eligible = v not in K[X]
        (ok if p == st else bad)[("eligible" if eligible else "v0 in N(x)")] += 1
        if p != st and eligible: print(f"  MISMATCH k={k} start={(v,d)} predicted {p} actual {st}")
print("exact predictions:", dict(ok), " mismatches:", dict(bad))
