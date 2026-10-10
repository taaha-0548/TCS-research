"""Erdős Problem #617 (Erdős–Gyárfás balanced colourings).
A colouring of the edges of K_n with r colours is *balanced* if every K_{r+1} sees all r colours.
Conjecture: for r >= 3 there is no balanced r-colouring of K_{r^2+1}.
SAT model: x[e][k] = edge e has colour k; exactly one colour per edge; for every (r+1)-set S and colour k,
some edge of S has colour k.  Optional symmetry: cyclic colourings of Z_n (colour depends on the
difference i - j mod n, up to sign)."""
import itertools, sys, time
from pysat.solvers import Cadical153
from pysat.card import CardEnc

def solve(n, r, cyclic=False, timeout_note=""):
    if cyclic:
        cls = {}
        for i, j in itertools.combinations(range(n), 2):
            d = (j - i) % n; cls[(i, j)] = min(d, n - d)
        keys = sorted(set(cls.values()))
    else:
        cls = {e: e for e in itertools.combinations(range(n), 2)}; keys = list(cls.values())
    var = {(c, k): 1 + idx * r + k for idx, c in enumerate(keys) for k in range(r)}
    top = len(var); S = Cadical153()
    for c in keys:
        lits = [var[(c, k)] for k in range(r)]
        enc = CardEnc.equals(lits=lits, bound=1, top_id=top); top = max(top, enc.nv)
        for cl in enc.clauses: S.add_clause(cl)
    for T in itertools.combinations(range(n), r + 1):
        cs = {cls[e] for e in itertools.combinations(T, 2)}
        for k in range(r): S.add_clause([var[(c, k)] for c in cs])
    S.add_clause([var[(keys[0], 0)]])                     # colour symmetry
    t = time.time(); sat = S.solve(); dt = time.time() - t
    col = None
    if sat:
        m = set(l for l in S.get_model() if l > 0)
        col = {e: next(k for k in range(r) if var[(cls[e], k)] in m) for e in itertools.combinations(range(n), 2)}
    return sat, dt, col

def is_balanced(n, r, col):
    return all(len({col[e] for e in itertools.combinations(T, 2)}) == r for T in itertools.combinations(range(n), r + 1))

if __name__ == "__main__":
    for n, r in [(9, 3), (10, 3)]:
        sat, dt, col = solve(n, r)
        print(f"r={r} n={n}: balanced colouring {'EXISTS' if sat else 'does not exist'} ({dt:.2f}s)" + (f", verified={is_balanced(n, r, col)}" if sat else ""), flush=True)
