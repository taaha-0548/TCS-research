"""Readable transducer table: states named by (port pair, index), outcomes per visit type."""
import sys
from collections import defaultdict
from transducer import transducer
from exp_3pole_transparency import poles

def show(name):
    padj, ports = poles[name]
    T = transducer(padj, ports)
    pn = {p: "abc"[k] for k, p in enumerate(ports)}
    groups = defaultdict(list)
    for Q in T:
        key = frozenset((Q[0], Q[-1]))
        if Q not in groups[key] and Q[::-1] not in groups[key]: groups[key].append(Q)
    def nm(Q):
        key = frozenset((Q[0], Q[-1])); L = groups[key]
        i = L.index(Q) if Q in L else L.index(Q[::-1])
        return "".join(sorted(pn[p] for p in key)) + str(i)
    print(f"== {name}: h = " + ", ".join(f"{''.join(sorted(pn[p] for p in k))}:{len(v)}" for k, v in groups.items()))
    for Q in sorted(T, key=lambda q: (nm(q), pn[q[0]])):
        row = []
        for kind in ("B1", "B3"):
            res, Qn, k = T[Q][kind]
            row.append(f"{kind}: {res[0]} -> {nm(Qn)} ({pn[Qn[0]]}->{pn[Qn[-1]]}) [{k}]")
        print(f"  {nm(Q)} oriented {pn[Q[0]]}->{pn[Q[-1]]}:   " + "   ".join(row))

for name in sys.argv[1:]: show(name)
