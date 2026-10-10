"""Counterexamples to the *single-colour* lemma for large r.
G = B + (r-2) disjoint K_r, where B = complement of a blow-up L of C_5 on 2r+1 vertices.
Then alpha(G) = 2 + (r-2) = r (L triangle-free), |G| = r^2+1.  We check exactly that every
(r+1)-set spans <= C(r,2)+1 edges of G, and compare e(G) with M_r = C(r^2+1,2)/r.
If e(G) <= M_r, the minority colour alone (with alpha<=r and the (r+1)-set cap) cannot give a
contradiction: any proof must use the other colours."""
import itertools
from math import comb

def minL_table(parts):
    # minL[s] = min over (k_i <= n_i, sum k = s) of sum k_i k_{i+1} (cyclic)
    best = {}
    for ks in itertools.product(*[range(p + 1) for p in parts]):
        s = sum(ks); e = sum(ks[i] * ks[(i + 1) % 5] for i in range(5))
        if e < best.get(s, 10**9): best[s] = e
    return best

def check(r, parts):
    assert sum(parts) == 2 * r + 1
    mL = minL_table(parts)
    cap = comb(r, 2) + 1
    for s in range(0, r + 2):
        if s > 2 * r + 1: continue
        eB = comb(s, 2) - mL[s]
        rest = r + 1 - s
        eK = comb(rest, 2) if rest <= r else comb(r, 2)   # concentrate the rest in one K_r
        if eB + eK > cap: return None
    eL = sum(parts[i] * parts[(i + 1) % 5] for i in range(5))
    return (r - 2) * comb(r, 2) + comb(2 * r + 1, 2) - eL

for r in range(3, 31):
    best = None
    for parts in itertools.combinations_with_replacement(range(1, 2 * r), 5):
        if sum(parts) != 2 * r + 1: continue
        for perm in set(itertools.permutations(parts)):
            if perm[0] != max(perm): continue
            e = check(r, perm)
            if e is not None and (best is None or e < best[0]): best = (e, perm)
    M = comb(r * r + 1, 2) / r
    print(f"r={r:2d}  M_r={M:7.1f}  best valid e(G)={best[0] if best else None}  parts={best[1] if best else None}  "
          f"{'<= M_r  => single-colour lemma FAILS' if best and best[0] <= M else ''}", flush=True)
