"""Cycle 13 (Single-Reflection Lemma).  Claim: in P = P'[x <- X] (one slot), every visit to P makes at most
one REFLECTing call to X, and the visit REFLECTs iff it made exactly one.  (Corollary of the Retrace
Lemma: the visit is a line whose sites all hold the same gadget X.)  Consequences: T-down (transmitting
visits make only transmitting calls, recursively) and, in a single-slot tower of depth d, at most one
reflecting visit per level in the whole walk.
Test: random P' (n = 8, 10, 12), random slot, random wiring, random inner poles X (n = 6..10)."""
import sys, random, itertools
from collections import Counter
sys.path.insert(0, "../phase3"); sys.path.insert(0, "../phase1"); sys.path.insert(0, ".."); sys.path.insert(0, "../../../../../paper")
import verify as V
from tower import from_pole, AbstractInner
from compose import composed_visit
from lollipop import random_instance
from selfsimilar2 import chord_adj, paths_of

class LogInner(AbstractInner):
    def __init__(self, *a):
        super().__init__(*a); self.outs = []
    def visit(self, pred, succ, kind):
        o, pr2, c = super().visit(pred, succ, kind); self.outs.append(o); return o, pr2, c

rng = random.Random(13); C = Counter(); bad = []
inners = []
while len(inners) < 40:
    n = rng.choice([6, 8, 10]); K = chord_adj(n, random_instance(n, rng))
    try:
        P, ports, _ = V.pole(K, rng.randrange(n)); A = from_pole(P, ports)
    except Exception: continue
    if len(A["states"]) >= 2: inners.append(A)
trials = 0
while trials < 400:
    n = rng.choice([8, 10, 12]); K = chord_adj(n, random_instance(n, rng))
    try: P1, ports1, _ = V.pole(K, rng.randrange(n))
    except Exception: continue
    xs = [v for v in range(len(P1)) if P1[v] and v not in ports1]
    if not xs: continue
    x = rng.choice(xs); perm = list(range(3)); rng.shuffle(perm); A = rng.choice(inners)
    name = {p: "abc"[i] for i, p in enumerate(ports1)}; port_of = {u: "abc"[perm[j]] for j, u in enumerate(P1[x])}
    try: paths = paths_of(P1, ports1)
    except Exception: continue
    trials += 1
    for key, Q in paths.items():
        j = Q.index(x); cp = frozenset((port_of[Q[j-1]], port_of[Q[j+1]]))
        for cs in A["states"]:
            if A["pair"][cs] != cp: continue
            for Qo in key:
                for kd in ("B1", "B3"):
                    inner = LogInner(x, port_of, A, cs)
                    try: o, Qf, _, _ = composed_visit(P1, ports1, Qo, kd, inner)
                    except Exception as e: C["compose error"] += 1; continue
                    r = inner.outs.count("REFLECT")
                    C[(o, f"{r} R-calls")] += 1
                    if r > 1 or (o == "REFLECT") != (r == 1): bad.append((trials, o, inner.outs))
print("visits by (outcome, #reflecting calls):", dict(C))
print("counterexamples to the Single-Reflection Lemma:", len(bad), bad[:3])
