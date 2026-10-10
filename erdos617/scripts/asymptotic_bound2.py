"""Refined minority-colour bound on N(r), adding the imbalance constraint.

Setup (see README, F3/F4).  Minority colour G on n vertices, t = e(G) - p_r(n) <= T(n) := floor(C(n,2)/r) - p_r(n).
Furedi: an r-partition V_1..V_r with M = (non-edges of G inside parts), |M| <= t.
Writing E+ for the G-edges between parts,
    e(G) = sum_j C(s_j,2) - |M| + |E+|  =>  I + |E+| = t + |M| <= 2t,   I := sum_j C(s_j,2) - p_r(n) >= 0.
Inside a part of size s:  |M_j| >= phi(s) = max(p_r(s), ceil((r-1) C(s,2)/C(r+1,2))) for s > r (0 otherwise).
Necessary: exist sizes with sum s_j = n,  sum phi(s_j) <= T(n)  and  I <= 2 T(n).
(E+ >= 0 is dropped here; the blocking lemma is what would add it.)
DP over parts with numpy over the I-dimension; reports the largest n passing."""
import sys
from math import comb, ceil
import numpy as np

def p(r, n):
    a, b = divmod(n, r); return r * comb(a, 2) + a * b

def phi(r, s):
    if s <= r: return 0
    return max(p(r, s), ceil((r - 1) * comb(s, 2) / comb(r + 1, 2)))

def feasible(r, n):
    T = comb(n, 2) // r - p(r, n)
    Qmax = p(r, n) + 2 * T                       # sum_j C(s_j,2) must be <= Qmax
    INF = 10**9
    smax = n
    # dp[tot][q] = min sum phi using parts so far with total size tot and sum C(s,2) = q
    dp = np.full((n + 1, Qmax + 1), INF, dtype=np.int64); dp[0, 0] = 0
    for _ in range(r):
        nd = np.full_like(dp, INF)
        for s in range(0, smax + 1):
            c = comb(s, 2)
            if c > Qmax: break
            f = phi(r, s)
            if f > T: break
            # shift dp by (s, c)
            src = dp[: n + 1 - s, : Qmax + 1 - c] + f
            np.minimum(nd[s:, c:], src, out=nd[s:, c:])
        dp = nd
    return dp[n].min() <= T

def bound(r):
    n = r * r
    while feasible(r, n + 1): n += 1
    return n

if __name__ == "__main__":
    for r in [int(a) for a in sys.argv[1:]] or [3, 4, 5, 6, 7, 8, 10, 12]:
        b = bound(r)
        print(f"r={r:3d}: N(r) <= {b:5d}  r^2={r*r:5d}  excess={b - r*r:4d}  excess/r^1.5={(b - r*r)/r**1.5:.3f}", flush=True)
