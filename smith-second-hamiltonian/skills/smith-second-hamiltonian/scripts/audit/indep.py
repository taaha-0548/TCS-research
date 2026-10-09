"""Independent implementations for the audit (no code shared with lollipop.py/general.py).

indep_walk: Thomason's lollipop walk written from the definition with edge sets:
  state = set of path edges; the path is re-read from v0 after every move.
state_graph_partner: brute force over ALL Hamiltonian paths starting with v0 v1, builds the
  rotation graph explicitly and walks the component of the start leaf."""
def path_from_edges(adj, E, v0, v1, n):
    p = [v0, v1]
    while len(p) < n:
        a, b = p[-2], p[-1]
        nxt = [w for w in adj[b] if w != a and frozenset((b, w)) in E]
        assert len(nxt) == 1, "edge set is not a Hamiltonian path"
        p.append(nxt[0])
    return p

def indep_walk(adj, cycle, max_steps=10**8):
    n = len(cycle); v0, v1 = cycle[0], cycle[1]
    E = {frozenset((cycle[i], cycle[i+1])) for i in range(n - 1)}   # cycle minus edge (last, v0)
    last_attach = v0; steps = 0
    while True:
        p = path_from_edges(adj, E, v0, v1, n)
        z = p[-1]
        cand = [w for w in adj[z] if frozenset((z, w)) not in E and w != last_attach]
        assert len(cand) == 1, (z, cand)
        w = cand[0]
        if w == v0:
            return steps, p
        s = p[p.index(w) + 1]
        E.remove(frozenset((w, s))); E.add(frozenset((z, w)))
        last_attach = w; steps += 1
        if steps > max_steps: raise RuntimeError

def all_ham_paths_from(adj, v0, v1):
    n = len(adj); out = []; seen = {v0, v1}; p = [v0, v1]
    def dfs():
        if len(p) == n: out.append(tuple(p)); return
        for w in adj[p[-1]]:
            if w not in seen:
                seen.add(w); p.append(w); dfs(); p.pop(); seen.discard(w)
    dfs(); return out

def state_graph_partner(adj, cycle):
    """Brute-force Thomason component: returns (distance from start leaf to other leaf, final path)."""
    v0, v1 = cycle[0], cycle[1]
    P = all_ham_paths_from(adj, v0, v1); idx = {p: i for i, p in enumerate(P)}
    def nbrs(p):
        z = p[-1]; out = []
        for w in adj[z]:
            if w == p[-2] or w == v0: continue
            i = p.index(w); out.append(p[:i+1] + p[i+1:][::-1])
        return out
    start = tuple(cycle); prev = None; cur = start; d = 0
    while True:
        nb = [q for q in nbrs(cur) if q != prev]
        if not nb: return d, list(cur)
        assert len(nb) == 1
        prev, cur = cur, nb[0]; d += 1
