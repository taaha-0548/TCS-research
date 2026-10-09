"""Cycle 17 (written, not yet run).  In towers that are exponential AND multi-reflecting (cycle 16), does the number of
reflecting visits (all levels) inside one top visit grow with depth?  Bounded => a constant number of turns
(single-turn-like, likely predictable); growing => genuine repeated upward shuttling.
Exact: rc(entry) = [outcome R] + sum of rc over its sub-calls; minimisation keeps rc in the signature."""
import io, contextlib, random, time, sys, json
sys.path.insert(0, "../phase3")
from collections import Counter, defaultdict
with contextlib.redirect_stdout(io.StringIO()):
    from selfsimilar2 import chord_adj, paths_of
    from cycle15 import bases
import verify as V
from tower import AbstractInner, quotient
from compose import composed_visit
from lollipop import random_instance

class CInner(AbstractInner):
    def __init__(self, *a):
        super().__init__(*a); self.rc = 0; self.nR = 0
    def visit(self, pred, succ, kind):
        pr = (self.port_of[pred], self.port_of[succ]); self.rc += self.A["rc"][(self.s, pr, kind)]
        o, pr2, c = super().visit(pred, succ, kind); self.nR += o == "REFLECT"; return o, pr2, c

def level(P1, ports1, x, perm, A):
    name = {p: "abc"[i] for i, p in enumerate(ports1)}; port_of = {u: "abc"[perm[j]] for j, u in enumerate(P1[x])}
    paths = paths_of(P1, ports1); states = []; pair = {}; table = {}; rc = {}; multi = False
    def cpair(Q):
        j = Q.index(x); return frozenset((port_of[Q[j-1]], port_of[Q[j+1]]))
    for key, Q in paths.items():
        for cs in A["states"]:
            if A["pair"][cs] == cpair(Q): st = (key, cs); states.append(st); pair[st] = frozenset((name[Q[0]], name[Q[-1]]))
    for (key, cs) in states:
        for Q in key:
            for kd in ("B1", "B3"):
                inner = CInner(x, port_of, A, cs)
                o, Qf, _, _ = composed_visit(P1, ports1, Q, kd, inner)
                k = ((key, cs), (name[Q[0]], name[Q[-1]]), kd)
                table[k] = (o, (frozenset([tuple(Qf), tuple(Qf[::-1])]), inner.s), (name[Qf[0]], name[Qf[-1]]))
                rc[k] = (o == "REFLECT") + inner.rc
                multi |= inner.nR >= 2 or (o == "TRANSMIT" and inner.nR > 0)
    return dict(states=states, pair=pair, table=table, rc=rc), multi

def minimise_rc(A):
    inputs = defaultdict(list)
    for (s, pr, kd) in A["table"]: inputs[s].append((pr, kd))
    sig = lambda s: (A["pair"][s], tuple(sorted((i, A["table"][(s,) + i][0], A["table"][(s,) + i][2], A["rc"][(s,) + i]) for i in inputs[s])))
    cls = {s: sig(s) for s in A["states"]}; ids = {v: k for k, v in enumerate(dict.fromkeys(cls.values()))}; cls = {s: ids[cls[s]] for s in A["states"]}
    while True:
        new = {s: (cls[s], tuple(sorted((i, cls[A["table"][(s,) + i][1]]) for i in inputs[s]))) for s in A["states"]}
        ids = {v: k for k, v in enumerate(dict.fromkeys(new.values()))}; new = {s: ids[new[s]] for s in A["states"]}
        if len(set(new.values())) == len(set(cls.values())): break
        cls = new
    Q = quotient(A, new); rep = {}
    for s in A["states"]: rep.setdefault(new[s], s)
    Q["rc"] = {(c, pr, kd): A["rc"][(rep[c], pr, kd)] for (c, pr, kd) in Q["table"]}
    return Q

for B in bases: B["rc"] = {k: v[0] == "REFLECT" for k, v in B["table"].items()}
rng = random.Random(16); found = []; t0 = time.time(); trend = Counter()
while time.time() - t0 < 230 and len(found) < 25:
    n = rng.choice([8, 10, 12]); K = chord_adj(n, random_instance(n, rng)); r = rng.randrange(n)
    try: P1, ports1, _ = V.pole(K, r)
    except Exception: continue
    xs = [v for v in range(len(P1)) if P1[v] and v not in ports1]
    if not xs: continue
    x = rng.choice(xs); perm = list(range(3)); rng.shuffle(perm); bi = rng.randrange(len(bases)); A = bases[bi]
    sizes, mx, multi = [], [], []
    try:
        for lev in range(6):
            A, m = level(P1, ports1, x, perm, A)
            if not A["states"]: break
            A = minimise_rc(A); sizes.append(len(A["states"])); mx.append(max(A["rc"].values())); multi.append(m)
            if len(A["states"]) > 2500: break
    except Exception: continue
    if len(sizes) < 5 or sizes[4] < 2.5 * sizes[3] or not (multi[3] or multi[4]): continue
    t = "max R per top visit grows" if mx[-1] > mx[-2] > mx[-3] else "bounded"
    trend[t] += 1
    found.append(dict(n=n, K=K, r=r, x=x, perm=perm, base=bi, sizes=sizes, maxR=mx))
    print(f"sizes {sizes}  max reflections per top visit {mx}", flush=True)
print(dict(trend)); json.dump(found, open("cycle17_candidates.json", "w"))
