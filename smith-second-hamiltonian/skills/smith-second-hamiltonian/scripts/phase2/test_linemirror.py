"""P2.1 validation: abstract line-mirror simulation == real lollipop walk on G = H[x <- X_x],
with 1-3 gadgets (memory allowed), marked vertices pairwise at distance >= 3 and away from v0."""
import sys, random, itertools, time
from collections import Counter, deque
sys.path.insert(0, ".."); sys.path.insert(0, "../../../../../paper")
import verify as V
from lollipop import random_instance
from linemirror import host_line, site_types, run_line_mirror

def chord_adj(n, ch): return [[(v - 1) % n, (v + 1) % n, ch[v]] for v in range(n)]
def dist(adj, a):
    d = {a: 0}; q = deque([a])
    while q:
        u = q.popleft()
        for w in adj[u]:
            if w not in d: d[w] = d[u] + 1; q.append(w)
    return d

def pole_table(PX, portsX):
    T = {}
    for s, t in itertools.permutations(portsX, 2):
        for Q in V.ham_paths(PX, s, t):
            for kd in ("B1", "B3"):
                o, Qn, cost, _ = V.visit(PX, portsX, Q, kd); T[(Q, kd)] = (o, Qn, cost)
    return T

def trial(rng):
    n = rng.choice([16, 20, 26, 32]); H = chord_adj(n, random_instance(n, rng)); C = list(range(n))
    m = rng.choice([1, 2, 3]); M = []
    for x in rng.sample(range(2, n - 1), n - 3):
        if x in H[0] or x == 0: continue
        if all(dist(H, x)[y] >= 3 for y in M): M.append(x)
        if len(M) == m: break
    gadgets = {}
    for x in M:
        k = rng.choice([6, 8, 10]); K2 = chord_adj(k, random_instance(k, rng)); PX, portsX, _ = V.pole(K2, rng.randrange(k))
        perm = list(range(3)); rng.shuffle(perm)
        gadgets[x] = dict(P=PX, ports=portsX, perm=perm, T=pole_table(PX, portsX), port={"abc"[i]: portsX[i] for i in range(3)})
    # build G and the lifted cycle
    lab = {}; adjG = {}
    for v in range(n):
        if v not in gadgets: adjG[("h", v)] = []
    for x, g in gadgets.items():
        for i in range(len(g["P"])): adjG[(x, i)] = [(x, w) for w in g["P"][i]]
    for v in range(n):
        if v in gadgets: continue
        for w in H[v]:
            if w not in gadgets: adjG[("h", v)].append(("h", w))
    port_name = {}
    for x, g in gadgets.items():
        port_name[x] = {}
        for j, u in enumerate(H[x]):
            p = g["ports"][g["perm"][j]]; adjG[("h", u)].append((x, p)); adjG[(x, p)].append(("h", u))
            port_name[x][u] = "abc"[g["perm"][j]]
    cyc = []; state0 = {}
    for i, v in enumerate(C):
        if v not in gadgets: cyc.append(("h", v)); continue
        g = gadgets[v]; a, b = C[i-1], C[(i+1) % n]
        pa = g["ports"][g["perm"][H[v].index(a)]]; pb = g["ports"][g["perm"][H[v].index(b)]]
        hp = V.ham_paths(g["P"], pa, pb)
        if not hp: return None
        Q = rng.choice(hp); state0[v] = Q; cyc += [(v, q) for q in Q]
    L = {u: i for i, u in enumerate(adjG)}; A = [[L[w] for w in adjG[u]] for u in adjG]
    assert all(len(set(a)) == 3 for a in A)
    steps_real = V.lollipop(A, [L[u] for u in cyc])
    # final cycle of the real walk: rerun with path capture
    v0 = L[cyc[0]]; path = [L[u] for u in cyc]; pos = {u: i for i, u in enumerate(path)}; last = v0
    while True:
        z, pred = path[-1], path[-2]; w = next(u for u in A[z] if u != pred and u != last)
        if w == v0: break
        i = pos[w]; path[i+1:] = path[i+1:][::-1]
        for j in range(i+1, len(path)): pos[path[j]] = j
        last = w
    inv = {i: u for u, i in L.items()}
    proj = []
    for i in path:
        u = inv[i]; hv = u[1] if u[0] == "h" else u[0]
        if not proj or proj[-1] != hv: proj.append(hv)
    line, moves = host_line(H, C)
    fwd, bwd = site_types(H, line, M, port_name)
    end, steps_abs = run_line_mirror(line, fwd, bwd, gadgets, state0)
    far_cycle = list(line[-1]); start_cycle = list(C)
    def E(c): return {frozenset((c[i], c[(i+1) % len(c)])) for i in range(len(c))}
    real_end = "far" if E(proj) == E(far_cycle) else ("start" if E(proj) == E(start_cycle) else "OTHER")
    sites = len(fwd)
    import linemirror as LM; refl = list(LM.LAST_REFLECTIONS)
    return dict(ok=(end == real_end and steps_abs == steps_real), m=len(M), sites=sites, memory=any(
        Counter((Q[0], Q[-1]) for (Q, k) in g["T"] if k == "B1").most_common(1)[0][1] > 1 for g in gadgets.values()),
        nrefl=len(refl), ngad=len(set(refl)), reflected=steps_real > len(line) - 1 + sum(1 for _ in fwd) * 0 and end == "start")

rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 2); t0 = time.time(); S = Counter(); bad = []
while time.time() - t0 < float(sys.argv[2] if len(sys.argv) > 2 else 120):
    try: r = trial(rng)
    except (AssertionError, KeyError, StopIteration, RuntimeError) as e: S[("error", type(e).__name__)] += 1; continue
    if r is None: continue
    S[(f"{r['m']} gadget(s)", "memory" if r["memory"] else "simple", "exact" if r["ok"] else "MISMATCH")] += 1
    cat = "0 reflections" if r["nrefl"] == 0 else ("1 reflection" if r["nrefl"] == 1 else ">=2 reflections")
    if r["ngad"] >= 2: cat += ", at >=2 different gadgets"
    S[("coverage", cat, "exact" if r["ok"] else "MISMATCH")] += 1
    if not r["ok"] and len(bad) < 3: bad.append(r)
for k, v in sorted(S.items(), key=str): print(k, v)
print("mismatches sample:", bad)
