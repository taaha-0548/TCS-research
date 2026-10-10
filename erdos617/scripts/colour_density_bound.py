"""Theorem E check: N(r) <= r^2 + floor(r/2), unconditional.
Minority colour G, t = e(G) - p_r(n) <= T(n) := floor(C(n,2)/r) - p_r(n).  Furedi: an r-partition V_1..V_r with
m = sum_j e(H[V_j]) <= t.  Each of the other r-1 colours has alpha <= r inside V_j, hence >= p_r(|V_j|) edges
there, all of them H-edges: m >= (r-1) sum_j p_r(|V_j|) >= (r-1) * min over r-partitions of n of sum_j p_r(s_j).
Necessary: (r-1) * minP(n) <= T(n).  Report the largest n passing (exact integers), plus the rejected n=r^2+1..
Also verify the claim on the witness r=7 covering frame: (D) on V_1 rejects it."""
from math import comb
import sys

def p(r, n):
    a, b = divmod(n, r); return r * comb(a, 2) + a * b

def minP(r, n):
    # min over partitions of n into r parts of sum p_r(s_j): DP (p_r is convex in s, balanced is optimal; check by DP)
    INF = 10**18; best = [0] + [INF] * n
    for _ in range(r):
        nb = [INF] * (n + 1)
        for tot in range(n + 1):
            if best[tot] == INF: continue
            for s in range(0, n - tot + 1):
                v = best[tot] + p(r, s)
                if v < nb[tot + s]: nb[tot + s] = v
        best = nb
    return best[n]

def T(r, n):
    return comb(n, 2) // r - p(r, n)

for r in [int(a) for a in sys.argv[1:]] or range(2, 16):
    n = r * r
    while (r - 1) * minP(r, n + 1) <= T(r, n + 1): n += 1
    # confirm monotone: nothing passes in the next r^2 values
    later = [m for m in range(n + 1, n + r * r) if (r - 1) * minP(r, m) <= T(r, m)]
    print(f"r={r:2d}: N(r) <= {n}  (r^2 + floor(r/2) = {r*r + r//2})  later passes: {later[:3]}", flush=True)
