"""Change-window test for nested-cavity machines: for every excursion entering level j, the deepest
gadget whose state differs at the end (relative depth).  Bounded window => polynomial DP for all NCMs."""
import random
from collections import Counter
from ideal_flat import site_types
rng = random.Random(8); types = site_types(4); W = Counter(); byM = {}
for trial in range(6000):
    m = rng.randrange(3, 10)
    sites = [None] * (2 * m)
    for j in range(m): sites[j] = (j, rng.choice(types)); sites[2*m-1-j] = (j, rng.choice(types))
    st = [rng.randrange(4) for _ in range(m)]; i, d = 0, 1; T = []; steps = 0
    Tinv = [{v: k for k, v in Tm.items()} for (g, (Tm, If, Ib)) in sites]
    while 0 <= i < len(sites) and steps < 10**6:
        T.append((i, tuple(st))); g, (Tm, If, Ib) = sites[i]; s = st[g]
        if d > 0:
            if s in Tm: st[g] = Tm[s]
            else: st[g] = If[s]; d = -d
        else:
            if s in Tinv[i]: st[g] = Tinv[i][s]
            else: st[g] = Ib[s]; d = -d
        i += d; steps += 1
    T.append((i, tuple(st)))
    for j in range(1, m):
        inside = False
        for t, (i2, s2) in enumerate(T):
            if i2 >= j and not inside: inside = True; a = t
            if i2 < j and inside:
                inside = False; s0, s1 = T[a][1], T[t][1]
                ch = [q - j for q in range(j, m) if s0[q] != s1[q]]
                w = max(ch) if ch else -1
                W[w] += 1; byM.setdefault(m, Counter())[w] += 1
print("deepest changed level relative to entry (all m):", dict(sorted(W.items())))
for m in sorted(byM): print(f"  m={m}: max relative depth seen {max(byM[m])}, distribution {dict(sorted(byM[m].items()))}")
