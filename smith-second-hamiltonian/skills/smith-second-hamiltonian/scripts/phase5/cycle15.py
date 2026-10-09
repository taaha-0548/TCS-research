"""Cycle 15.  Do multi-reflection visits persist up a tower?  Random single-slot towers (random P', slot,
wiring, base pole; bases include the T-down violators h = [1,1,3], [1,3,3]).  Per level, count visits that
make >= 2 reflecting calls or that TRANSMIT after a reflecting call."""
import io, contextlib, random, sys, time
from collections import Counter, defaultdict
with contextlib.redirect_stdout(io.StringIO()):
    from selfsimilar2 import chord_adj, paths_of
import verify as V
from tower import from_pole, AbstractInner
from compose import composed_visit
from lollipop import random_instance

class LogInner(AbstractInner):
    def __init__(self, *a):
        super().__init__(*a); self.outs = []
    def visit(self, pred, succ, kind):
        o, pr2, c = super().visit(pred, succ, kind); self.outs.append(o); return o, pr2, c

def level(P1, ports1, x, perm, A):
    name = {p: "abc"[i] for i, p in enumerate(ports1)}; port_of = {u: "abc"[perm[j]] for j, u in enumerate(P1[x])}
    paths = paths_of(P1, ports1); states = []; pair = {}; table = {}; c = Counter()
    def cpair(Q):
        j = Q.index(x); return frozenset((port_of[Q[j-1]], port_of[Q[j+1]]))
    for key, Q in paths.items():
        for cs in A["states"]:
            if A["pair"][cs] == cpair(Q): st = (key, cs); states.append(st); pair[st] = frozenset((name[Q[0]], name[Q[-1]]))
    for (key, cs) in states:
        for Q in key:
            for kd in ("B1", "B3"):
                inner = LogInner(x, port_of, A, cs)
                o, Qf, _, _ = composed_visit(P1, ports1, Q, kd, inner)
                table[((key, cs), (name[Q[0]], name[Q[-1]]), kd)] = (o, (frozenset([tuple(Qf), tuple(Qf[::-1])]), inner.s), (name[Qf[0]], name[Qf[-1]]))
                r = inner.outs.count("REFLECT")
                c["visits"] += 1
                if r >= 2: c[">=2 R-calls"] += 1
                if o == "TRANSMIT" and r: c["T after R"] += 1
    return dict(states=states, pair=pair, table=table), c
def h(A): return sorted(Counter(A["pair"][s] for s in A["states"]).values())

rng = random.Random(15); bases = []
while len(bases) < 60:
    n = rng.choice([6, 8, 10]); K = chord_adj(n, random_instance(n, rng))
    try: P, ports, _ = V.pole(K, rng.randrange(n)); A = from_pole(P, ports)
    except Exception: continue
    if any(o == "REFLECT" for o, _, _ in A["table"].values()): bases.append(A)
if __name__ == "__main__":
    summary = defaultdict(Counter); t0 = time.time(); towers = 0
    while time.time() - t0 < 240:
        n = rng.choice([8, 10, 12]); K = chord_adj(n, random_instance(n, rng))
        try: P1, ports1, _ = V.pole(K, rng.randrange(n))
        except Exception: continue
        xs = [v for v in range(len(P1)) if P1[v] and v not in ports1]
        if not xs: continue
        x = rng.choice(xs); perm = list(range(3)); rng.shuffle(perm); A = rng.choice(bases); tag = str(h(A))
        try:
            rows = []
            for lev in range(1, 4):
                A, c = level(P1, ports1, x, perm, A)
                if not A["states"] or len(A["states"]) > 1500: break
                rows.append(c)
        except Exception: continue
        if len(rows) < 3: continue
        towers += 1
        bad = tuple(r[">=2 R-calls"] + r["T after R"] > 0 for r in rows)
        summary["all"][bad] += 1
        summary[tag][bad] += 1
    print(f"{towers} random towers of depth 3; key = (level-1 bad?, level-2 bad?, level-3 bad?)")
    for k, v in summary.items(): print(f"  base h={k}: {dict(v)}")
