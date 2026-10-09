"""Hypothesis F on long host lines: host = nested G_k (line length L), constant-size memory gadgets in
all available slots (pairwise distance >= 3, away from v0).  Hill-climb visits; compare with L."""
import sys, random, time
from collections import deque
sys.path.insert(0, "../phase2"); sys.path.insert(0, "../phase3"); sys.path.insert(0, ".."); sys.path.insert(0, "../../../../../paper")
import verify as V
from linemirror import host_line
from flat_optimise import library, simulate, init_state, dist
V.KCYC = []
for E in V.ham_cycles(V.K):
    c = [0]; prev = None
    while len(c) < 8:
        nxt = next(w for w in V.K[c[-1]] if frozenset((c[-1], w)) in E and w != prev); prev = c[-1]; c.append(nxt)
    if c[1] != 1 and c[-1] == 1: c = [0] + c[1:][::-1]
    V.KCYC.append(c)
rng = random.Random(7); lib = library(rng, 80)
for k in (4, 5, 6):
    adj, Ck, _ = V.build(k); lab = {v: i for i, v in enumerate(adj)}; H = [[lab[w] for w in adj[v]] for v in adj]
    C = [lab[v] for v in Ck]; line, _ = host_line(H, C); L = len(line) - 1
    slots = []
    for x in rng.sample(range(len(H)), len(H)):
        if x == C[0] or x in H[C[0]]: continue
        if all(dist(H, x)[y] >= 3 for y in slots): slots.append(x)
    M = slots; best = (0, 0); conf = None; t0 = time.time()
    while time.time() - t0 < 60:
        c = {} if conf is None or rng.random() < 0.1 else dict(conf)
        for x in (M if not c else [rng.choice(M)]):
            for _ in range(30):
                A = rng.choice(lib); perm = list(range(3)); rng.shuffle(perm); ss = init_state(H, line, x, A, perm)
                if ss: c[x] = (A, perm, rng.choice(ss)); break
        if len(c) < len(M): continue
        r = simulate(H, line, M, c)
        if r and r[0] > best[0]: best = r; conf = c
    print(f"host G_{k}: n={len(H)}, line L={L}, slots {len(M)}: best visits {best[0]}, reflections {best[1]}, visits/L = {best[0]/L:.2f}", flush=True)
