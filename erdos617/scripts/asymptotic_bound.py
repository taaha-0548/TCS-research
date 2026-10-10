"""Upper bound on N(r) (largest n with a balanced r-colouring of K_n) from the minority colour + Furedi stability.
Minority colour G: e(G) <= floor(C(n,2)/r).  H = complement(G) is K_{r+1}-free, t := e(G) - p_r(n).
Furedi (2015): H becomes r-partite after deleting <= t edges, so some r-partition V_1..V_r has
sum_j e(H[V_j]) <= t.  Inside a part of size s:
  * G[V_j] has no K_{r+1}           => e(H[V_j]) >= p_r(s) (Turan; in particular >= s - r),
  * every (r+1)-subset has >= r-1 H-edges (other r-1 colours) => e(H[V_j]) >= (r-1) C(s,2) / C(r+1,2).
So min over partitions of sum_j phi(s_j) <= t is necessary.  Report the largest n passing this test."""
from math import comb, ceil
import sys

def p(r, n):
    a, b = divmod(n, r); return r * comb(a, 2) + a * b

def phi(r, s):
    if s <= r: return 0
    return max(p(r, s), ceil((r - 1) * comb(s, 2) / comb(r + 1, 2)))

def min_sum(r, n):
    # min sum_j phi(s_j) over r parts summing to n (DP over parts; phi nondecreasing)
    INF = 10**18; best = [0] + [INF] * n
    for _ in range(r):
        nb = [INF] * (n + 1)
        for tot in range(n + 1):
            if best[tot] == INF: continue
            for s in range(0, n - tot + 1):
                v = best[tot] + phi(r, s)
                if v < nb[tot + s]: nb[tot + s] = v
        best = nb
    return best[n]

def bound(r):
    n = r * r
    while True:
        t = comb(n + 1, 2) // r - p(r, n + 1)
        if min_sum(r, n + 1) > t: return n
        n += 1

for r in [int(a) for a in sys.argv[1:]] or [3, 4, 5, 6, 8, 10, 15, 20, 30]:
    b = bound(r); print(f"r={r:3d}: N(r) <= {b:6d}   r^2={r*r:6d}   ratio={b/(r*r):.4f}", flush=True)
