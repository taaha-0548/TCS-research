"""q(r, n): minimum number of edges of a graph G on n vertices with
   (A) alpha(G) <= r                      (every (r+1)-set spans >= 1 edge)
   (C) every (r+1)-set spans <= C(r,2)+1 edges   (the other r-1 colours each need an edge).
Every colour class of a balanced r-colouring of K_n satisfies (A) and (C).
If q(r, r^2+1) > M_r = C(r^2+1, 2)/r, the minority colour alone gives a contradiction.
Exact for small cases via CP-SAT with lazy (CEGAR) generation of the (r+1)-set constraints."""
import itertools, sys, time
from math import comb
from ortools.sat.python import cp_model

def violated(n, r, E, cap):
    adj = [[False]*n for _ in range(n)]
    for (i, j) in E: adj[i][j] = adj[j][i] = True
    bad = []
    for S in itertools.combinations(range(n), r + 1):
        e = sum(adj[a][b] for a, b in itertools.combinations(S, 2))
        if e == 0 or e > cap: bad.append(S)
    return bad

def q(n, r, timeout=1500, full=None, workers=4):
    cap = comb(r, 2) + 1
    pairs = list(itertools.combinations(range(n), 2))
    full = full if full is not None else comb(n, r + 1) <= 20000
    sets = list(itertools.combinations(range(n), r + 1)) if full else []
    t0 = time.time(); rounds = 0
    while True:
        m = cp_model.CpModel()
        x = {p: m.NewBoolVar(f"x{p}") for p in pairs}
        for S in sets:
            es = [x[p] for p in itertools.combinations(S, 2)]
            m.AddBoolOr(es); m.Add(sum(es) <= cap)
        # symmetry breaking (weak): vertex 0 has minimum degree
        deg = [sum(x[p] for p in pairs if v in p) for v in range(n)]
        for v in range(1, n): m.Add(deg[0] <= deg[v])
        m.Minimize(sum(x.values()))
        s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = timeout; s.parameters.log_search_progress = False; s.parameters.num_workers = workers
        st = s.Solve(m); rounds += 1
        if st not in (cp_model.OPTIMAL,):
            ub = s.ObjectiveValue() if st == cp_model.FEASIBLE else None
            return None, f"{s.StatusName(st)} bound={s.BestObjectiveBound()} best={ub}", None, time.time() - t0
        E = [p for p in pairs if s.Value(x[p])]
        if full: return len(E), "OPTIMAL", E, time.time() - t0
        bad = violated(n, r, E, cap)
        if not bad: return len(E), "OPTIMAL", E, time.time() - t0
        sets += bad[:2000]

if __name__ == "__main__":
    for (n, r) in [tuple(map(int, a.split(","))) for a in sys.argv[1:]]:
        val, st, E, dt = q(n, r)
        M = comb(n, 2) / r
        print(f"r={r} n={n}: q={val} status={st} M_r={M:.1f} turan_p={'%d' % (r*comb(n//r,2)+(n//r)*(n%r))} ({dt:.1f}s)", flush=True)
        if st == "OPTIMAL": print("  edges:", E, flush=True)
