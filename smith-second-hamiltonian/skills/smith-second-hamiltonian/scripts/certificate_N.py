"""N(start) . u > 0 for eligible starts (v0 not in N[x]) of K's walk: closes the lower bound."""
import json
from collections import Counter
from fractions import Fraction as F
from general import from_chord
from nested_fast import rotate_to
CH = [4, 3, 6, 1, 0, 7, 2, 5]; X, R, PERM = 5, 2, (2, 0, 1)
K = from_chord(8, CH); Kc = list(range(8)); xname = {u: "abc"[PERM[k]] for k, u in enumerate(K[X])}
cert = json.load(open("certificate.json")); u = [F(s) for s in cert["u"]]
keys = [tuple(s.split("/")) for s in json.load(open("e20_M.json"))["keys"]]
for v in range(8):
    if v == X or v in K[X]: continue
    for d in (1, -1):
        cyc = rotate_to(Kc, v, d); path = list(cyc); pos = {a: i for i, a in enumerate(path)}; forb = v; N = Counter(); steps = 0
        while True:
            z, prev = path[-1], path[-2]
            w = [a for a in K[z] if a != prev and a != forb][0]
            if w == v: break
            i = pos[w]; s = path[i+1]
            if s == X or w == X:
                j = path.index(X); N[(xname[path[j-1]] + xname[path[j+1]], "B1" if s == X else "B3")] += 1
            path[i+1:] = path[i+1:][::-1]
            for j in range(i+1, 8): pos[path[j]] = j
            forb = w; steps += 1
        Nu = sum(N[f] * u[keys.index(f)] for f in N)
        print(f"start v0={v} d={d:+d}: K-steps={steps}, passages={dict(N)}, N.u = {float(Nu):.1f}")
