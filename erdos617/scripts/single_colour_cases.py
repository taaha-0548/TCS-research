"""Decide whether q(r, n) <= B (single colour: alpha <= r, (r+1)-set cap C(r,2)+1, <= B edges) with CP-SAT,
split by the minimum degree d of vertex 0, whose neighbourhood is fixed to {1..d} (WLOG).
UNSAT in every case d = 0..floor(2B/n) proves q(r, n) > B."""
import itertools, sys, time
from math import comb
from ortools.sat.python import cp_model

def case(n, r, B, d, timeout):
    pairs = list(itertools.combinations(range(n), 2)); cap = comb(r, 2) + 1
    m = cp_model.CpModel(); x = {p: m.NewBoolVar("") for p in pairs}
    for T in itertools.combinations(range(n), r + 1):
        es = [x[p] for p in itertools.combinations(T, 2)]
        m.AddBoolOr(es); m.Add(sum(es) <= cap)
    deg = [sum(x[p] for p in pairs if v in p) for v in range(n)]
    for j in range(1, n): m.Add(x[(0, j)] == (1 if j <= d else 0))
    for v in range(1, n): m.Add(deg[v] >= d)
    m.Add(sum(x.values()) <= B)
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = timeout; s.parameters.num_workers = 4
    t = time.time(); st = s.Solve(m)
    return s.StatusName(st), time.time() - t

if __name__ == "__main__":
    n, r, B = map(int, sys.argv[1:4]); timeout = float(sys.argv[4]) if len(sys.argv) > 4 else 3600
    for d in range(0, 2 * B // n + 1):
        st, dt = case(n, r, B, d, timeout)
        print(f"n={n} r={r} edges<={B} mindeg={d}: {st} ({dt:.1f}s)", flush=True)
