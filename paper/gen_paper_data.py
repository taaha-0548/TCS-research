"""Data for the full paper: integer certificate, exact step counts, worked-example trace of G_1."""
import itertools, json
from fractions import Fraction as F
import numpy as np
import verify as V
V.KCYC = []
cs = V.ham_cycles(V.K)
for E in cs:
    c = [0]; prev = None
    while len(c) < 8:
        nxt = next(w for w in V.K[c[-1]] if frozenset((c[-1], w)) in E and w != prev); prev = c[-1]; c.append(nxt)
    if c[1] != 1 and c[-1] == 1: c = [0] + c[1:][::-1]
    V.KCYC.append(c)
P0, ports, idx = V.pole(V.K, V.R); name = {p: "abc"[i] for i, p in enumerate(ports)}
xname = {idx[u]: "abc"[V.PERM[j]] for j, u in enumerate(V.K[V.X])}
keys = sorted((name[s] + name[t], kd) for s, t in itertools.permutations(ports, 2) for kd in ("B1", "B3"))
c0 = {}; Mr = {}
for s, t in itertools.permutations(ports, 2):
    Q = V.ham_paths(P0, s, t)[0]
    for kd in ("B1", "B3"):
        o, Qn, cost, mv = V.visit(P0, ports, Q, kd); c0[(name[s]+name[t], kd)] = cost; Mr[(name[s]+name[t], kd)] = V.passages(mv, idx[V.X], xname)
M = [[Mr[e].get(f, 0) for f in keys] for e in keys]
st = keys.index(("ca", "B3")); R = {st}; stack = [st]
while stack:
    i = stack.pop()
    for j in range(12):
        if M[i][j] and j not in R: R.add(j); stack.append(j)
Rl = sorted(R)
MR = np.array([[M[i][j] for j in Rl] for i in Rl], float)
w, Vv = np.linalg.eig(MR); v = np.abs(Vv[:, int(np.argmax(w.real))].real); v = v / v.min()
best = None
for scale in range(1, 400):
    u = [max(1, round(x * scale)) for x in v]
    for lam in (F(2947, 1000), F(2945, 1000), F(294, 100)):
        if all(sum(F(MR[i][j]) * u[j] for j in range(len(Rl))) >= lam * u[i] for i in range(len(Rl))):
            if best is None or lam > best[1] or (lam == best[1] and max(u) < max(best[0])): best = (u, lam)
            break
    if best and best[1] == F(2947, 1000) and max(best[0]) < 1000: break
u, lam = best
print("R =", [ "/".join(keys[i]) for i in Rl ])
print("integer certificate u =", u, " lambda =", lam, float(lam) ** (1/6))
c = [[c0[e] for e in keys]]
for _ in range(14): c.append([c[0][i] + sum(M[i][j] * c[-1][j] for j in range(12)) for i in range(12)])
steps = [(8 + 6 * k, 4 + c[k-1][st]) for k in range(1, 15)]
print("steps:", steps)
# worked example: walk on G_1 from (0,1), with full states
adj, Ck, cycs = V.build(1)
def lab(v): return f"{v[1]}" if v[0] == 1 else f"{v[1]}'"
path = list(Ck); pos = {v: i for i, v in enumerate(path)}; last = path[0]; trace = [(" ".join(lab(v) for v in path), None)]
inner = {v for v in adj if v[0] == 0}
while True:
    z, pred = path[-1], path[-2]
    wv = next(t for t in adj[z] if t != pred and t != last)
    if wv == path[0]: break
    i = pos[wv]; path[i+1:] = path[i+1:][::-1]
    for j in range(i+1, len(path)): pos[path[j]] = j
    last = wv; trace.append((" ".join(lab(v) for v in path), f"({lab(z)},{lab(wv)})" + (" *" if path[-1] in inner else "")))
print("G_1 walk steps:", len(trace) - 1)
for p, m in trace: print("  ", m or "start", "|", p)
json.dump(dict(keys=["/".join(e) for e in keys], M=M, c0=[c0[e] for e in keys], R=Rl, u=u, lam=str(lam), steps=steps, trace=trace), open("paper_data.json", "w"))
