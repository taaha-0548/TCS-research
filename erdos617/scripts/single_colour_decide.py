"""Decision version of q(r): is there a graph on n vertices with alpha <= r, every (r+1)-set spanning
<= C(r,2)+1 edges, and at most B edges?  UNSAT means q(r, n) > B.  Pure SAT (CaDiCaL), full clause set.
Weak symmetry break: vertex 0 has degree <= every other vertex's degree is NOT encoded (keeps it simple)."""
import itertools, sys, time
from math import comb
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool

def decide(n, r, B):
    pool = IDPool(); x = {p: pool.id(p) for p in itertools.combinations(range(n), 2)}
    cap = comb(r, 2) + 1; S = Cadical153()
    for T in itertools.combinations(range(n), r + 1):
        es = [x[p] for p in itertools.combinations(T, 2)]
        S.add_clause(es)                                            # alpha <= r
        for sub in itertools.combinations(es, cap + 1):             # at most cap edges
            S.add_clause([-v for v in sub])
    enc = CardEnc.atmost(lits=list(x.values()), bound=B, vpool=pool, encoding=EncType.seqcounter)
    for c in enc.clauses: S.add_clause(c)
    t = time.time(); res = S.solve(); return res, time.time() - t

if __name__ == "__main__":
    n, r, B = map(int, sys.argv[1:4])
    res, dt = decide(n, r, B)
    print(f"n={n} r={r} edges<={B}: {'SAT' if res else 'UNSAT'} ({dt:.1f}s)", flush=True)
