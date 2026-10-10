"""Direction 3: supersaturation at n = r^2 + 1.

bad(chi) = number of (r+1)-sets of K_n that miss at least one colour under the r-colouring chi.
The conjecture says bad(chi) >= 1 for n = r^2+1.  Here we estimate min bad(chi):
  exact   : CP-SAT minimisation (small cases only, e.g. r = 3),
  search  : simulated annealing with incremental counts (r = 3, 4, 5),
  affine1 : best one-vertex extension of the affine-plane colouring (r prime: AG(2,r), r-1 single
            directions + one merged pair of directions), optimising only the r^2 new edges.
Also reports, for the best colouring found, how the bad sets are distributed (per colour, per vertex)."""
import itertools, random, sys, time
from math import comb
import numpy as np

def setup(n, r):
    edges = list(itertools.combinations(range(n), 2)); eid = {e: i for i, e in enumerate(edges)}
    sets = np.array(list(itertools.combinations(range(n), r + 1)), dtype=np.int32)
    se = np.array([[eid[(a, b)] for a, b in itertools.combinations(S, 2)] for S in sets], dtype=np.int32)
    inc = [[] for _ in edges]
    for si, row in enumerate(se):
        for e in row: inc[e].append(si)
    inc = [np.array(x, dtype=np.int32) for x in inc]
    return edges, sets, se, inc

def counts_of(col, se, r):
    c = np.zeros((len(se), r), dtype=np.int16)
    for k in range(r): c[:, k] = (col[se] == k).sum(1)
    return c

def anneal(n, r, iters, seed=0, T0=2.0, T1=0.02, init=None, data=None, fixed=None):
    rng = random.Random(seed)
    edges, sets, se, inc = data or setup(n, r)
    col = np.array(init if init is not None else [rng.randrange(r) for _ in edges], dtype=np.int8)
    cnt = counts_of(col, se, r); bad = int((cnt == 0).any(1).sum())
    best, bestcol = bad, col.copy()
    movable = [i for i in range(len(edges)) if fixed is None or i not in fixed]
    for it in range(iters):
        T = T0 * (T1 / T0) ** (it / iters)
        e = rng.choice(movable); old = int(col[e]); new = rng.randrange(r - 1); new += new >= old
        S = inc[e]; sub = cnt[S]
        before = (sub == 0).any(1).sum()
        sub2 = sub.copy(); sub2[:, old] -= 1; sub2[:, new] += 1
        after = (sub2 == 0).any(1).sum()
        d = int(after - before)
        if d <= 0 or rng.random() < np.exp(-d / T):
            cnt[S] = sub2; col[e] = new; bad += d
            if bad < best: best, bestcol = bad, col.copy()
    return best, bestcol

def exact(n, r, timeout=600, cap=None):
    from ortools.sat.python import cp_model
    edges, sets, se, inc = setup(n, r)
    m = cp_model.CpModel()
    x = [[m.NewBoolVar("") for _ in range(r)] for _ in edges]
    for e in range(len(edges)): m.AddExactlyOne(x[e])
    m.Add(x[0][0] == 1)
    bads = []
    for row in se:
        b = m.NewBoolVar("")
        for k in range(r):
            m.AddBoolOr([x[e][k] for e in row] + [b])          # colour k missing => bad
        bads.append(b)
    if cap is None: m.Minimize(sum(bads))
    else: m.Add(sum(bads) <= cap)
    s = cp_model.CpSolver(); s.parameters.num_workers = 4; s.parameters.max_time_in_seconds = timeout
    st = s.Solve(m)
    return s.StatusName(st), s.ObjectiveValue(), s.BestObjectiveBound()

def affine_colouring(r):
    """AG(2,r), r prime.  Points (a,b); direction of the line through two points: slope in F_r or inf.
    Colours: directions 0..r-2 -> colours 0..r-2; directions r-1 and inf merged -> colour r-1."""
    pts = [(a, b) for a in range(r) for b in range(r)]
    def direction(p, q):
        dx, dy = (q[0] - p[0]) % r, (q[1] - p[1]) % r
        if dx == 0: return r          # infinity
        return (dy * pow(dx, -1, r)) % r
    col = {}
    for i, j in itertools.combinations(range(r * r), 2):
        d = direction(pts[i], pts[j]); col[(i, j)] = d if d <= r - 2 else r - 1
    return col

def report(col, n, r, data):
    edges, sets, se, inc = data
    cnt = counts_of(np.array(col, dtype=np.int8), se, r)
    badmask = (cnt == 0).any(1); bad = int(badmask.sum())
    per_col = [int((cnt[:, k] == 0).sum()) for k in range(r)]
    per_vertex = np.zeros(n, dtype=int)
    for S in sets[badmask]: per_vertex[S] += 1
    sizes = [sum(1 for e in range(len(edges)) if col[e] == k) for k in range(r)]
    return bad, per_col, sorted(per_vertex.tolist(), reverse=True), sizes

if __name__ == "__main__":
    mode, r = sys.argv[1], int(sys.argv[2]); n = int(sys.argv[3]) if len(sys.argv) > 3 else r * r + 1
    if mode == "exact":
        print(f"r={r} n={n} exact:", exact(n, r), flush=True)
    elif mode == "decide":
        k = int(sys.argv[4])
        print(f"r={r} n={n} bad<={k}:", exact(n, r, timeout=1500, cap=k)[0], flush=True)
    elif mode == "search":
        data = setup(n, r); iters = int(sys.argv[4]) if len(sys.argv) > 4 else 200000; runs = 4
        best = None
        for sd in range(runs):
            t = time.time(); b, c = anneal(n, r, iters, seed=sd, data=data)
            print(f"r={r} n={n} run {sd}: best bad = {b} ({time.time()-t:.0f}s)", flush=True)
            if best is None or b < best[0]: best = (b, c)
        bad, per_col, pv, sizes = report(best[1], n, r, data)
        print(f"  best={bad}  missing-colour counts per colour={per_col}  colour class sizes={sizes}")
        print(f"  bad sets per vertex (sorted)={pv}", flush=True)
    elif mode == "extend":
        # find a balanced colouring of K_{r^2} by annealing (bad = 0), then optimise one extra vertex
        n0 = r * r; d0 = setup(n0, r); iters = int(sys.argv[4]) if len(sys.argv) > 4 else 200000
        found = []
        for sd in range(8):
            b, c = anneal(n0, r, iters, seed=100 + sd, data=d0)
            print(f"r={r} K_{n0} search seed {sd}: bad={b}", flush=True)
            if b == 0: found.append(c)
            if len(found) >= 3: break
        data = setup(n0 + 1, r); edges = data[0]; old = {e: i for i, e in enumerate(d0[0])}
        for idx, c in enumerate(found):
            init = [int(c[old[e]]) if e in old else 0 for e in edges]
            fixed = {i for i, e in enumerate(edges) if n0 not in e}
            best = min((anneal(n0 + 1, r, 40000, seed=sd, init=init, data=data, fixed=fixed) for sd in range(4)),
                       key=lambda z: z[0])
            bad, per_col, pv, sizes = report(best[1], n0 + 1, r, data)
            print(f"  balanced K_{n0} #{idx} + 1 vertex: best bad = {bad}  per colour={per_col}  top vertices={pv[:4]}", flush=True)
    elif mode == "affine1":
        assert n == r * r + 1
        data = setup(n, r); edges = data[0]
        ac = affine_colouring(r); new = r * r
        init = [ac[e] if e in ac else 0 for e in edges]
        fixed = {i for i, e in enumerate(edges) if new not in e}
        best = None
        for sd in range(4):
            b, c = anneal(n, r, int(sys.argv[4]) if len(sys.argv) > 4 else 50000, seed=sd, init=init, data=data, fixed=fixed)
            if best is None or b < best[0]: best = (b, c)
        bad, per_col, pv, sizes = report(best[1], n, r, data)
        print(f"r={r} affine+1 (only new vertex's edges optimised): best bad = {bad}  per colour={per_col}  sizes={sizes}")
        print(f"  bad sets per vertex (sorted)={pv[:6]} ...", flush=True)
