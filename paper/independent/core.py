import itertools
KEDGES = [(i,(i+1)%8) for i in range(8)] + [(0,4),(1,3),(2,6),(5,7)]
X, R = 5, 2
PORTS = {'a':1,'b':3,'c':6}
PNAME = {1:'a',3:'b',6:'c'}
WIRE = {4:6, 6:1, 7:3}   # neighbour of x in copy d -> port label in copy d+1
WNAME = {4:'c', 6:'a', 7:'b'}  # neighbour of x -> inner port name

def adj_from_edges(edges):
    adj = {}
    for u,v in edges:
        adj.setdefault(u,set()).add(v); adj.setdefault(v,set()).add(u)
    return adj

KADJ = adj_from_edges(KEDGES)

def ham_paths(adj, verts, s, t):
    """all Hamiltonian paths of induced subgraph on verts from s to t"""
    verts = set(verts); n = len(verts); out = []
    def rec(path, seen):
        u = path[-1]
        if len(path) == n:
            if u == t: out.append(list(path))
            return
        for w in adj[u]:
            if w in verts and w not in seen and (w != t or len(path) == n-1):
                seen.add(w); path.append(w); rec(path, seen); path.pop(); seen.discard(w)
    rec([s], {s})
    return out

P0V = [v for v in range(8) if v != R]
_P0HP = {}
def p0_path(p, q):
    if (p,q) not in _P0HP:
        hs = ham_paths(KADJ, P0V, p, q)
        assert len(hs) == 1, (p,q,hs)
        _P0HP[(p,q)] = hs[0]
    return _P0HP[(p,q)]

class Gk:
    """G_k: copies d=0..k of K; copy d<k lacks 5, copy d>=1 lacks 2."""
    def __init__(self, k):
        self.k = k
        self.labels = []
        for d in range(k+1):
            for l in range(8):
                if (l == X and d < k) or (l == R and d >= 1): continue
                self.labels.append((d,l))
        self.id = {v:i for i,v in enumerate(self.labels)}
        E = []
        for d in range(k+1):
            for u,v in KEDGES:
                if (d,u) in self.id and (d,v) in self.id:
                    E.append((self.id[(d,u)], self.id[(d,v)]))
            if d < k:
                for u,p in WIRE.items():
                    E.append((self.id[(d,u)], self.id[(d+1,p)]))
        self.edges = E
        self.n = len(self.labels)
        self.adj = [[] for _ in range(self.n)]
        for u,v in E:
            self.adj[u].append(v); self.adj[v].append(u)
    def expand(self, seq, d):
        """seq: labels in copy d (may contain 5 as placeholder if d<k). returns list of (d,l)"""
        out = []
        for i,l in enumerate(seq):
            if l == X and d < self.k:
                u, v = seq[i-1], seq[i+1]
                out += self.expand(p0_path(WIRE[u], WIRE[v]), d+1)
            else:
                out.append((d,l))
        return out
    def start_path(self):
        return [self.id[v] for v in self.expand(list(range(8)), 0)]

def lollipop(adj, S0, record=None, maxsteps=None):
    """Thomason walk. S0 Hamiltonian path starting v0 v1 whose end is adjacent to v0."""
    P = list(S0); n = len(P); v0 = P[0]
    pos = [0]*n
    for i,v in enumerate(P): pos[v] = i
    prev = v0; steps = 0
    while True:
        z = P[-1]; pred = P[-2]
        cand = [w for w in adj[z] if w != pred and w != prev]
        assert len(cand) == 1, (z, pred, prev, adj[z])
        w = cand[0]
        if w == v0: break
        i = pos[w]
        if record is not None: record(P, z, w, P[i+1])
        P[i+1:] = P[:i:-1]
        for j in range(i+1, n): pos[P[j]] = j
        prev = w; steps += 1
        if maxsteps and steps > maxsteps: raise RuntimeError
    return steps, P

def lollipop_literal(adj, S0):
    """second, literal implementation: P' = P[v0..w] . rev(P[s..z])"""
    P = list(S0); v0 = P[0]; prev = v0; steps = 0; trace=[list(P)]
    while True:
        z = P[-1]
        nonpath = [w for w in adj[z] if w != P[-2]]
        assert len(nonpath) == 2 and prev in nonpath
        w = [u for u in nonpath if u != prev][0]
        if w == v0: break
        i = P.index(w)
        P = P[:i+1] + list(reversed(P[i+1:]))
        assert P[i] == w and P[-1] == trace[-1][i+1]
        prev = w; steps += 1; trace.append(list(P))
    return steps, trace
