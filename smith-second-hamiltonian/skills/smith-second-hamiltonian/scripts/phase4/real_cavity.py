"""Nested cavity machine with REAL gadget automata: line order L_1 L_2 ... L_m R_m ... R_1, gadget g_j
has two sites (L_j, R_j), port pairs chained consistently (as in a real host), last site R_1 may be
any type.  Hill-climb gadgets, site types, initial states.  Does the best run grow exponentially?"""
import sys, random, time, itertools
sys.path.insert(0, "../phase3"); sys.path.insert(0, ".."); sys.path.insert(0, "../../../../../paper")
import verify as V
from lollipop import random_instance
from tower import from_pole
def chord_adj(n, ch): return [[(v - 1) % n, (v + 1) % n, ch[v]] for v in range(n)]
def third(p): return next(c for c in "abc" if c not in p)
def after(pr, kd): return frozenset((pr[1], third(pr)) if kd == "B1" else (pr[0], third(pr)))
def bwd(pr, kd): return ((third(pr), pr[1]), kd) if kd == "B1" else ((pr[0], third(pr)), kd)
rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
lib = []
while len(lib) < 120:
    n = rng.choice([6, 8, 10]); A = from_pole(*V.pole(chord_adj(n, random_instance(n, rng)), rng.randrange(n))[:2])
    if len(A["states"]) >= 3: lib.append(A)

def random_gadget_conf():
    for _ in range(100):
        A = rng.choice(lib); s0 = rng.choice(A["states"]); p0 = A["pair"][s0]
        pr1 = tuple(rng.sample(sorted(p0), 2)); k1 = rng.choice(["B1", "B3"]); p1 = after(pr1, k1)
        if not any(A["pair"][s] == p1 for s in A["states"]): continue
        pr2 = tuple(rng.sample(sorted(p1), 2)); k2 = rng.choice(["B1", "B3"]); p2 = after(pr2, k2)
        if not any(A["pair"][s] == p2 for s in A["states"]): continue
        return dict(A=A, s0=s0, t1=(pr1, k1), t2=(pr2, k2))
    return None

def run(conf, cap=3_000_000):
    m = len(conf); order = [(j, 0) for j in range(m)] + [(j, 1) for j in reversed(range(m))]
    st = [g["s0"] for g in conf]; i, d, n = 0, 1, 0
    while 0 <= i < len(order):
        j, w = order[i]; g = conf[j]; t = g["t1"] if w == 0 else g["t2"]
        pr, kd = t if d > 0 else bwd(*t)
        key = (st[j], pr, kd)
        if key not in g["A"]["table"]: return None
        o, st[j], _ = g["A"]["table"][key]; n += 1
        if o == "REFLECT": d = -d
        i += d
        if n > cap: return None
    return n

for m in range(1, 9):
    best = 0; cur = None; curv = 0; t_end = time.time() + 14
    while time.time() < t_end:
        if cur is None or rng.random() < 0.05:
            c = [random_gadget_conf() for _ in range(m)]
            if None in c: continue
        else:
            c = list(cur); j = rng.randrange(m); g = random_gadget_conf()
            if g is None: continue
            c[j] = g
        v = run(c)
        if v is not None and (v >= curv or rng.random() < 0.02): cur, curv = c, v
        if v and v > best: best = v
    print(f"real gadgets, nested cavities, m={m} (N={2*m} sites): best run {best}", flush=True)
