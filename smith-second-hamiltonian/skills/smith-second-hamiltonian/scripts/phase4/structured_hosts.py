"""Longest nested chain in structured hosts (prism, Moebius ladder), over Hamiltonian cycles and starts."""
import sys, itertools
sys.path.insert(0, "../phase2"); sys.path.insert(0, ".."); sys.path.insert(0, "../../../../../paper")
import verify as V
from host_chains import chain
def prism(m):
    adj = [[] for _ in range(2*m)]
    for i in range(m):
        for a, b in ((i, (i+1) % m), (m+i, m+(i+1) % m), (i, m+i)): adj[a].append(b); adj[b].append(a)
    return adj
def moebius(m):   # 2m-cycle plus diameters
    n = 2*m; adj = [[(v-1) % n, (v+1) % n, (v+m) % n] for v in range(n)]; return adj
def cycles(adj, limit=60):
    n = len(adj); out = []; seen = [False]*n; seen[0] = True; p = [0]
    def dfs():
        if len(out) >= limit: return
        v = p[-1]
        if len(p) == n:
            if 0 in adj[v]: out.append(p[:])
            return
        for w in adj[v]:
            if not seen[w]: seen[w] = True; p.append(w); dfs(); p.pop(); seen[w] = False
    dfs(); return out
for name, f in (("prism", prism), ("moebius", moebius)):
    for m in (6, 10, 16, 24, 40):
        adj = f(m); best = (0, 0)
        for c in cycles(adj, 40):
            n = len(c)
            for s in range(0, n, max(1, n // 8)):
                for d in (1, -1):
                    cy = [c[(s + d*t) % n] for t in range(n)]
                    L, ch = chain(adj, cy)
                    if ch > best[1]: best = (L, ch)
        print(f"{name} m={m} (n={2*m}): best nested chain {best[1]} (line {best[0]})", flush=True)
