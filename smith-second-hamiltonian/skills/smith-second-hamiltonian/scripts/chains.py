"""Chain graphs: cap (K3) - k two-vertex gadgets - pac (K3); consecutive parts joined by 3 edges.
Gadget type (i, j): the incoming edge i goes to vertex v (the other two to u), and the
outgoing edge j leaves from u (the other two from v).  This is the Brianski-Szady shape
(2k+6 vertices) with every wiring allowed; types are applied periodically."""
import sys, itertools
from general import lollipop_g

def chain(types):
    adj = {}
    def add(a, b): adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
    cap = [0, 1, 2]; add(0, 1); add(1, 2); add(0, 2)
    ends = list(cap); nxt = 3
    for (i, j) in types:
        u, v = nxt, nxt + 1; nxt += 2
        for k in range(3): add(ends[k], v if k == i else u)
        outs = [u if k == j else v for k in range(3)]
        ends = outs
    pac = [nxt, nxt + 1, nxt + 2]; add(pac[0], pac[1]); add(pac[1], pac[2]); add(pac[0], pac[2])
    for k in range(3): add(ends[k], pac[k])
    n = nxt + 3
    A = [adj[v] for v in range(n)]
    assert all(len(set(a)) == 3 for a in A), "not simple cubic"
    return A

def ham_cycles(A, limit=50):
    n = len(A); out = []; seen = [False] * n; path = [0]; seen[0] = True
    def dfs():
        if len(out) >= limit: return
        v = path[-1]
        if len(path) == n:
            if 0 in A[v] and path[1] < path[-1]: out.append(path[:])
            return
        for w in A[v]:
            if not seen[w]:
                seen[w] = True; path.append(w); dfs(); path.pop(); seen[w] = False
    dfs(); return out

def max_walk(A, cycles):
    best = 0
    for c in cycles:
        n = len(c)
        for s in range(n):
            for d in (1, -1):
                cyc = [c[(s + d * t) % n] for t in range(n)]
                st, _, _ = lollipop_g(A, cyc); best = max(best, st)
    return best

if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    types = [(i, j) for i in range(3) for j in range(3)]
    res = {}
    for period in (1, 2):
        for pat in itertools.product(types, repeat=period):
            row = []
            for k in range(period, 4 * period + 1, period):
                try: A = chain(list(pat) * (k // period))
                except AssertionError: row = None; break
                cs = ham_cycles(A)
                if not cs: row = None; break
                row.append((len(A), len(cs), max_walk(A, cs)))
            if row: res[pat] = row
    for pat, row in sorted(res.items(), key=lambda kv: -kv[1][-1][2])[:8]:
        print(pat, row)
