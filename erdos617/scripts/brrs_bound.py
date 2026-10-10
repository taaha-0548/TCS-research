"""Consequence of the local Fajtlowicz bound (BRRS 2016 conjecture; claimed proved in arXiv 2609.00210):
    alpha(G) >= sum_u 2/(d(u) + omega(u) + 1).
Apply to the minority colour G of a balanced r-colouring of K_n: omega(u) <= r (no monochromatic K_{r+1}),
e(G) <= floor(C(n,2)/r).  The sum is minimised (convex, decreasing in d) by the most balanced integer degree
sequence using the full degree budget 2*floor(C(n,2)/r).  If that minimum exceeds r then alpha(G) >= r+1:
no balanced colouring.  Report the largest n NOT excluded, for each r (exact rational arithmetic)."""
from fractions import Fraction
from math import comb
import sys

def min_sum(n, r):
    D = 2 * (comb(n, 2) // r)             # max total degree of the minority colour
    q, rem = divmod(D, n)                  # rem vertices of degree q+1, n-rem of degree q
    return (n - rem) * Fraction(2, q + r + 1) + rem * Fraction(2, q + 2 + r)

for r in [int(a) for a in sys.argv[1:]] or range(2, 21):
    n = r * r
    while min_sum(n + 1, r) <= r: n += 1
    print(f"r={r:2d}: N(r) <= {n}   (r^2={r*r}, r^2+r-2={r*r+r-2})", flush=True)
