"""P1.1 test: composed transducer (P' + table of X) == direct transducer of P = P'[x <- X],
for arbitrary X (with memory).  Every state of P, both kinds: outcome, successor, cost."""
import sys, random, itertools, time
from collections import Counter
sys.path.insert(0, ".."); sys.path.insert(0, "../../../../../paper")
import verify as V
from lollipop import random_instance
from compose import Inner, composed_visit

def chord_adj(n, ch): return [[(v - 1) % n, (v + 1) % n, ch[v]] for v in range(n)]

def table(P, ports):
    T = {}
    for s, t in itertools.permutations(ports, 2):
        for Q in V.ham_paths(P, s, t):
            for kd in ("B1", "B3"):
                o, Qn, cost, _ = V.visit(P, ports, Q, kd); T[(Q, kd)] = (o, Qn, cost)
    return T

def trial(rng):
    n1 = rng.choice([8, 10, 12]); K1 = chord_adj(n1, random_instance(n1, rng)); r1 = rng.randrange(n1)
    P1, ports1, _ = V.pole(K1, r1)
    inner_cands = [v for v in range(len(P1)) if v not in ports1]
    if not inner_cands: return None
    x = rng.choice(inner_cands)
    n2 = rng.choice([4, 6, 8, 10])
    K2 = [[1,2,3],[0,2,3],[0,1,3],[0,1,2]] if n2 == 4 else chord_adj(n2, random_instance(n2, rng))
    PX, portsX, _ = V.pole(K2, rng.randrange(n2)); perm = list(range(3)); rng.shuffle(perm)
    TX = table(PX, portsX)
    hX = Counter((Q[0], Q[-1]) for (Q, k) in TX if k == "B1")
    simpleX = all(v == 1 for v in hX.values()) and len(hX) == 6
    # build P directly
    m = len(P1); off = m
    P = [list(a) for a in P1] + [[off + w for w in PX[i]] for i in range(len(PX))]
    nbx = list(P1[x]); port_of = {}
    for j, u in enumerate(nbx):
        p = off + portsX[perm[j]]; P[u] = [p if y == x else y for y in P[u]]; P[p].append(u); port_of[u] = portsX[perm[j]]
    P[x] = []
    keep = [v for v in range(len(P)) if v != x]; lab = {v: i for i, v in enumerate(keep)}
    P = [[lab[w] for w in P[v]] for v in keep]; ports = [lab[p] for p in ports1]
    toP1 = {lab[v]: v for v in keep if v < m}; toX = {lab[off + i]: i for i in range(len(PX))}
    TP = table(P, ports)
    ok = Counter()
    for (Q, kd), (o, Qn, cost) in TP.items():
        Q1 = []; QX = []
        for v in Q:
            if v in toX: QX.append(toX[v]); u = x
            else: u = toP1[v]
            if not Q1 or Q1[-1] != u: Q1.append(u)
        inner = Inner(x, TX, port_of, QX)
        try:
            o2, Q1f, cost2, QXf = composed_visit(P1, ports1, tuple(Q1), kd, inner)
        except AssertionError as e:
            ok["composition error"] += 1; continue
        # lift the final path of P' to P
        lift = []
        Xpath = [lab[off + i] for i in QXf]
        for u in Q1f:
            if u == x:
                pred = lift[-1] if lift else None
                # orient X's path so that it starts at the port adjacent to the previous vertex
                if pred is not None and Xpath[0] in P[pred]: lift += Xpath
                else: lift += Xpath[::-1]
            else: lift.append(lab[u])
        good = (o == o2 and cost == cost2 and tuple(lift) == tuple(Qn))
        ok["exact" if good else "MISMATCH"] += 1
    return simpleX, ok

rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 3); t0 = time.time()
budget = float(sys.argv[2]) if len(sys.argv) > 2 else 200
S = Counter(); pairs = Counter()
while time.time() - t0 < budget:
    r = trial(rng)
    if r is None: continue
    simpleX, ok = r; g = "X simple" if simpleX else "X with memory"
    pairs[g] += 1
    for k, v in ok.items(): S[(g, k)] += v
print("pole pairs tested:", dict(pairs))
for k, v in sorted(S.items()): print("  ", k, v)
