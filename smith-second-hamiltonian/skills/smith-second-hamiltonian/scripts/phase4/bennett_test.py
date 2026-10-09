"""Strategy C test: Bennett structure of a nested-cavity run.  Site order: L_1..L_m R_m..R_1 (indices
0..2m-1); gadget g owns sites i and 2m-1-i for level i+1 (index i = level-1, in the extracted designs the
gadget owning both walls of level j may be any label, we read ownership from the design).
Excursion into level j = maximal time interval with the particle at site index >= j (entered from the
left).  For each, record: number of excursions into level j+1 inside it, and which gadgets changed."""
import sys, io, contextlib
from collections import Counter
with contextlib.redirect_stdout(io.StringIO()):
    from ideal_extract import climb

def trace(sites, init):
    st = list(init); i, d = 0, 1; T = []
    Tinv = [{v: k for k, v in Tm.items()} for (g, (Tm, If, Ib)) in sites]
    while 0 <= i < len(sites):
        T.append((i, tuple(st)))
        g, (Tm, If, Ib) = sites[i]; s = st[g]
        if d > 0:
            if s in Tm: st[g] = Tm[s]
            else: st[g] = If[s]; d = -d
        else:
            if s in Tinv[i]: st[g] = Tinv[i][s]
            else: st[g] = Ib[s]; d = -d
        i += d
    T.append((i, tuple(st))); return T

for m in (3, 4, 5):
    v, (sites, init) = climb(m, 10)
    owner_of_level = [sites[j][0] for j in range(m)]      # gadget at left wall L_{j+1}
    nested_ok = all(sites[j][0] == sites[2*m-1-j][0] for j in range(m))
    T = trace(sites, init)
    print(f"\nm={m}: run {v}, properly nested (same gadget on L_j and R_j): {nested_ok}")
    for j in range(1, m):
        # excursions into region index >= j
        exc = []; inside = False
        for t, (i, st) in enumerate(T):
            if i >= j and not inside: inside = True; t0 = t
            if i < j and inside: inside = False; exc.append((t0, t))
        sub = []
        for (a, b) in exc:
            k = 0; ins = False
            for (i, st) in T[a:b]:
                if i >= j + 1 and not ins: ins = True; k += 1
                if i < j + 1 and ins: ins = False
            sub.append(k)
        changed = Counter()
        for (a, b) in exc:
            s0, s1 = T[a][1], T[b][1]
            deeper = [owner_of_level[q] for q in range(j, m)]
            restored = all(s0[g] == s1[g] for g in deeper[1:])  # strictly deeper than level j+1's gadget
            changed[("deeper restored" if restored else "deeper CHANGED")] += 1
        print(f"  level {j}: {len(exc)} excursions; sub-excursions per excursion {Counter(sub)}; {dict(changed)}")
