"""Strategy B vs C test: is the final joint state of a nested-cavity system a PRODUCT of per-gadget
maps (no real interaction), or genuinely coupled?  Also: Bennett structure -- after each sub-run at
level j, are all deeper gadgets restored (uncompute) and only level j changed (commit)?"""
import itertools, random, time
from ideal_flat import site_types, run
from ideal_extract import climb

def final_state(sites, init):
    st = list(init); i, d = 0, 1
    Tinv = [{v: k for k, v in T.items()} for (g, (T, If, Ib)) in sites]
    while 0 <= i < len(sites):
        g, (T, If, Ib) = sites[i]; s = st[g]
        if d > 0:
            if s in T: st[g] = T[s]
            else: st[g] = If[s]; d = -d
        else:
            if s in Tinv[i]: st[g] = Tinv[i][s]
            else: st[g] = Ib[s]; d = -d
        i += d
    return tuple(st), ("start" if i < 0 else "far")

for m in (2, 3, 4):
    v, (sites, init) = climb(m, 8)
    c = 4; table = {}
    for s0 in itertools.product(range(c), repeat=m):
        table[s0] = final_state(sites, s0)
    # product test: does final[g] depend only on initial[g]?
    coupled = []
    for g in range(m):
        dep = {}
        for s0, (fs, end) in table.items():
            dep.setdefault(s0[g], set()).add(fs[g])
        if any(len(vals) > 1 for vals in dep.values()): coupled.append(g)
    ends = {}
    for s0, (fs, end) in table.items(): ends.setdefault(end, 0); ends[end] += 1
    perm = len(set(fs for fs, _ in table.values())) == len(table)
    print(f"m={m} (best run {v}): final-state map is a permutation: {perm}; "
          f"gadgets whose final state depends on OTHER gadgets: {coupled or 'none (product map)'}; exits {ends}")
