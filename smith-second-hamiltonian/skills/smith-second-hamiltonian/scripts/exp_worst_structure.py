"""E3: structure of the exact worst-case instances from E1."""
import json, itertools
from lollipop import neighbors, count_ham_cycles_through, lollipop

d = json.load(open("e1_worst_small.json"))

def edges(n, ch):
    E = set()
    for v in range(n):
        for w in neighbors(n, ch, v):
            E.add(frozenset((v, w)))
    return [tuple(e) for e in E]

def components(n, E):
    adj = {v: [] for v in range(n)}
    for a, b in E:
        adj[a].append(b); adj[b].append(a)
    seen = set(); comps = []
    for s in range(n):
        if s in seen: continue
        comp = {s}; st = [s]; seen.add(s)
        while st:
            v = st.pop()
            for w in adj[v]:
                if w not in seen:
                    seen.add(w); comp.add(w); st.append(w)
        comps.append(comp)
    return comps

def has_cycle(comp, E):
    sub = [e for e in E if e[0] in comp and e[1] in comp]
    return len(sub) >= len(comp)

def cyclic_edge_conn(n, ch, kmax=4):
    E = edges(n, ch)
    for k in range(1, kmax + 1):
        for cut in itertools.combinations(E, k):
            rest = [e for e in E if e not in cut]
            comps = components(n, rest)
            if len(comps) >= 2 and sum(1 for c in comps if has_cycle(c, rest)) >= 2:
                return k
    return f">{kmax}"

for n in sorted(d, key=int):
    n_i = int(n); ch = d[n]["worst_chord"]
    total = sum(count_ham_cycles_through(n_i, ch, 0, w) for w in neighbors(n_i, ch, 0)) // 2
    hist = d[n]["hist"]; mx = d[n]["max_steps"]
    print(f"n={n_i:2d} max={mx:3d} #worst-labellings={hist[str(mx)]:5d} ham_cycles={total:3d} "
          f"cyc_edge_conn={cyclic_edge_conn(n_i, ch)} chords={[(v, ch[v]) for v in range(n_i) if v < ch[v]]}")
