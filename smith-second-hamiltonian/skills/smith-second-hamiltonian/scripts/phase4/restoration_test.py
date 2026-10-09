"""Is 'deeper restored' universal for nested-cavity machines (2 sites per gadget, order L1..Lm Rm..R1)?
Random ideal designs (c = 4 and c = 6), random initial states.  For every excursion into level j
(particle at site index >= j, entered from the left, until it leaves to the left), check that the
gadgets of levels >= j+2 are restored.  Also test the stronger 'levels >= j+1 restored'."""
import random, itertools
from collections import Counter
from ideal_flat import site_types
rng = random.Random(4); S = Counter()
for c in (4, 6):
    types = site_types(c) if c == 4 else None
    if c == 6:
        import ideal_flat as IF
        types = []
        S6 = list(range(6))
        for _ in range(4000):           # random ideal site types for c = 6
            k = rng.choice([0, 2, 4, 6]); A = rng.sample(S6, k); B = rng.sample(S6, k); T = dict(zip(A, B))
            def inv(rest):
                rest = rest[:]; rng.shuffle(rest); d = {}
                for a, b in zip(rest[::2], rest[1::2]): d[a] = b; d[b] = a
                return d
            types.append((T, inv([s for s in S6 if s not in A]), inv([s for s in S6 if s not in B])))
    for trial in range(3000):
        m = rng.randrange(2, 7)
        sites = [None] * (2 * m)
        for j in range(m): sites[j] = (j, rng.choice(types)); sites[2*m-1-j] = (j, rng.choice(types))
        st = [rng.randrange(c) for _ in range(m)]; i, d = 0, 1; T = []
        Tinv = [{v: k for k, v in Tm.items()} for (g, (Tm, If, Ib)) in sites]; steps = 0
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
                    S[(c, "levels>=j+2 restored", all(s0[q] == s1[q] for q in range(j + 1, m)))] += 1
                    S[(c, "levels>=j+1 restored", all(s0[q] == s1[q] for q in range(j, m)))] += 1
for k, v in sorted(S.items(), key=str): print(k, v)
