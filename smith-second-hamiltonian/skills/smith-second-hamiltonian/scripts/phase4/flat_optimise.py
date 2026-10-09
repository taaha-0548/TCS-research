"""Hypothesis F (flat polynomiality): constant-size gadgets substituted into a host with a short line.
Fixed random host H (line length L), m slots pairwise at distance >= 3 (away from v0); each slot gets
a gadget from a library of small memory poles, a wiring and an initial path.  Hill-climb the total
number of visits of the exact line-mirror system.  Report best runs vs m."""
import sys, random, itertools, time, json
from collections import deque
sys.path.insert(0, "../phase2"); sys.path.insert(0, "../phase3"); sys.path.insert(0, ".."); sys.path.insert(0, "../../../../../paper")
import verify as V
from lollipop import random_instance
from linemirror import host_line, site_types
from tower import from_pole
def chord_adj(n, ch): return [[(v - 1) % n, (v + 1) % n, ch[v]] for v in range(n)]
def dist(adj, a):
    d = {a: 0}; q = deque([a])
    while q:
        u = q.popleft()
        for w in adj[u]:
            if w not in d: d[w] = d[u] + 1; q.append(w)
    return d
def third(p): return next(c for c in "abc" if c not in p)

def library(rng, count):
    lib = []
    while len(lib) < count:
        n = rng.choice([6, 8, 10]); G = chord_adj(n, random_instance(n, rng)); A = from_pole(*V.pole(G, rng.randrange(n))[:2])
        if len(A["states"]) >= 4: lib.append(A)
    return lib

def simulate(H, line, M, conf, cap=2_000_000):
    """conf[x] = (A, perm, state).  Exact abstract run (visits counted)."""
    port_name = {x: {u: "abc"[conf[x][1][j]] for j, u in enumerate(H[x])} for x in M}
    fwd, bwd = site_types(H, line, M, port_name)
    st = {x: conf[x][2] for x in M}; L = len(line) - 1; pos, d, visits, refl = 0, 1, 0, 0
    while True:
        if pos == L and d == 1: return visits, refl
        if pos == 0 and d == -1: return visits, refl
        i = pos if d == 1 else pos - 1; info = (fwd if d == 1 else bwd).get(i)
        if info is None: pos += d; continue
        x, pr, kind = info; A = conf[x][0]
        key = (st[x], (pr[0], pr[1]), kind)
        if key not in A["table"]: return None
        o, s2, _ = A["table"][key]; st[x] = s2; visits += 1
        if kind == "B3":
            if o == "TRANSMIT": pos += d
            else: d = -d; refl += 1
        else:
            if o == "TRANSMIT": pos += 2 * d
            else: d = -d; refl += 1
        if visits > cap: return None

def init_state(H, line, x, A, perm):
    S = line[0]; j = S.index(x); pn = {u: "abc"[perm[k]] for k, u in enumerate(H[x])}
    pr = frozenset((pn[S[j-1]], pn[S[j+1]]))
    return [s for s in A["states"] if A["pair"][s] == pr]

if __name__ == "__main__":
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1); lib = library(rng, 80)
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 120
    H = chord_adj(n, random_instance(n, rng)); C = list(range(n)); line, _ = host_line(H, C)
    slots = []
    for x in rng.sample(range(3, n - 2), n - 5):
        if x in H[0]: continue
        if all(dist(H, x)[y] >= 3 for y in slots): slots.append(x)
    print(f"host n={n}, line length {len(line)-1}, available slots {len(slots)}")
    results = {}
    for m in (1, 2, 4, 6, 8, 12, 16, 20):
        if m > len(slots): break
        M = slots[:m]; best = (0, 0); t0 = time.time()
        def rand_conf():
            conf = {}
            for x in M:
                for _ in range(20):
                    A = rng.choice(lib); perm = list(range(3)); rng.shuffle(perm); ss = init_state(H, line, x, A, perm)
                    if ss: conf[x] = (A, perm, rng.choice(ss)); break
                else: return None
            return conf
        conf = None
        while time.time() - t0 < 20:
            c = rand_conf() if conf is None or rng.random() < 0.2 else dict(conf)
            if c is None: continue
            if conf is not None and c is not None and rng.random() >= 0.2:
                x = rng.choice(M)
                for _ in range(20):
                    A = rng.choice(lib); perm = list(range(3)); rng.shuffle(perm); ss = init_state(H, line, x, A, perm)
                    if ss: c[x] = (A, perm, rng.choice(ss)); break
            r = simulate(H, line, M, c)
            if r and r[0] > best[0]: best = r; conf = c
        results[m] = best; print(f"  m={m:2d} gadgets: best visits {best[0]:6d}, reflections {best[1]}", flush=True)
    json.dump(results, open(f"flat_n{n}.json", "w"))
