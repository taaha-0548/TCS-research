"""D5 'covering-only' model, frame (r+2, r-1, r, ..., r) at n = r^2+1.

V_1 has r+2 vertices and H[V_1] is free.  K is a G-clique of size r-1.  The other parts are r-cliques with no
cross edges to V_1 or K in this model.  Every H-edge uv inside V_1 is blocked by covering: N_K(u) | N_K(v) = K.

Base constraints (always on):
  (cap on V_1)  every (r+1)-subset of V_1 spans >= r-1 H-edges,
  (D2, y=1)     for all a != b in V_1:  d_K(a) + d_K(b) + [ab in G] <= r.
Options:
  full    the exact (r+1)-set cap on every (r+1)-subset of V_1 u K  (G-edges <= C(r,2)+1),
  dens    coloured density (S6) on every subset W of V_1 u K (other colours' Turan bound)
  budget  t = I + |E+| - m <= C(r,2) and m <= t, with I = 2 for these sizes, |E+| = sum_u d_K(u), m = e(H[V_1]).
Usage: python3 covering_frame.py r [full] [budget]"""
import itertools, sys
from math import comb
from ortools.sat.python import cp_model

def p_turan(r, k):
    a, b = divmod(k, r); return r * comb(a, 2) + a * b

def solve(r, full=False, budget=False, show=False, dens=False):
    V = list(range(r + 2)); K = list(range(r + 2, 2 * r + 1))
    m = cp_model.CpModel()
    h = {e: m.NewBoolVar("") for e in itertools.combinations(V, 2)}
    N = {(u, k): m.NewBoolVar("") for u in V for k in K}
    d = {u: sum(N[(u, k)] for k in K) for u in V}
    H = lambda a, b: h[(min(a, b), max(a, b))]
    for S in itertools.combinations(V, r + 1):
        m.Add(sum(H(a, b) for a, b in itertools.combinations(S, 2)) >= r - 1)
    for (a, b), x in h.items():
        for k in K: m.AddBoolOr([x.Not(), N[(a, k)], N[(b, k)]])
        m.Add(d[a] + d[b] + (1 - x) <= r)
    if full:
        for S in itertools.combinations(V + K, r + 1):
            sv = [u for u in S if u in V]; sk = [k for k in S if k in K]
            g = comb(len(sk), 2) + sum(1 - H(a, b) for a, b in itertools.combinations(sv, 2)) \
                + sum(N[(u, k)] for u in sv for k in sk)
            m.Add(g <= comb(r, 2) + 1)
    if dens:
        # (S6)/(D) on every subset W of V_1 u K with |W| >= r+1: e_G(W) <= C(|W|,2) - (r-1) p_r(|W|)
        allv = V + K
        for k in range(r + 1, len(allv) + 1):
            lim = comb(k, 2) - (r - 1) * p_turan(r, k)
            for S in itertools.combinations(allv, k):
                sv = [u for u in S if u in V]; sk = [x for x in S if x in K]
                g = comb(len(sk), 2) + sum(1 - H(a, b) for a, b in itertools.combinations(sv, 2)) \
                    + sum(N[(u, x)] for u in sv for x in sk)
                m.Add(g <= lim)
    if budget:
        E = sum(d.values()); mm = sum(h.values())
        m.Add(2 + E - mm <= comb(r, 2)); m.Add(mm <= 2 + E - mm)
    s = cp_model.CpSolver(); s.parameters.num_workers = 4; s.parameters.max_time_in_seconds = 900
    st = s.Solve(m); name = s.StatusName(st)
    if show and st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        Hed = [e for e, x in h.items() if s.Value(x)]
        degs = {u: sum(s.Value(N[(u, k)]) for k in K) for u in V}
        print("   H[V_1] edges:", Hed); print("   d_K:", degs)
    return "SAT" if name in ("OPTIMAL", "FEASIBLE") else name

if __name__ == "__main__":
    r = int(sys.argv[1]); full = "full" in sys.argv; budget = "budget" in sys.argv; dens = "dens" in sys.argv
    print(f"r={r} full_cap={full} budget={budget} dens={dens}:", solve(r, full, budget, show=True, dens=dens), flush=True)
