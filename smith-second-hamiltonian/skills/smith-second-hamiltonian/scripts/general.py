"""Lollipop walk on a general cubic graph (adjacency lists) and 3-pole substitution tools."""
import itertools, random

def lollipop_g(adj, cycle, max_steps=10**7):
    """cycle: vertex list of a Ham cycle; fixed vertex cycle[0], first edge (cycle[0],cycle[1]).
    Returns (steps, final_cycle_vertex_list, added_edges_sequence)."""
    v0 = cycle[0]; path = list(cycle); n = len(path)
    pos = {v: i for i, v in enumerate(path)}; forb = v0; steps = 0; seq = []
    while True:
        z, prev = path[-1], path[-2]
        c = [w for w in adj[z] if w != prev and w != forb]
        assert len(c) == 1, (z, adj[z], prev, forb)
        w = c[0]
        if w == v0: return steps, path, seq
        seq.append((z, w))
        i = pos[w]; path[i+1:] = path[i+1:][::-1]
        for j in range(i+1, n): pos[path[j]] = j
        forb = w; steps += 1
        if steps > max_steps: raise RuntimeError("too long")

def is_ham(adj, cyc):
    n = len(adj)
    return len(set(cyc)) == n == len(cyc) and all(cyc[(i+1) % n] in adj[cyc[i]] for i in range(n))

def cyc_edges(cyc):
    return {frozenset((cyc[i], cyc[(i+1) % len(cyc)])) for i in range(len(cyc))}

def ham_paths(adj, verts, s, t):
    """All Ham paths of the induced subgraph on verts from s to t (small only)."""
    verts = set(verts); out = []
    def dfs(p, seen):
        v = p[-1]
        if len(p) == len(verts):
            if v == t: out.append(p[:])
            return
        for w in adj[v]:
            if w in verts and w not in seen and (w != t or len(p) == len(verts) - 1):
                seen.add(w); p.append(w); dfs(p, seen); p.pop(); seen.remove(w)
    dfs([s], {s}); return out

def from_chord(n, chord):
    return [[(v-1) % n, (v+1) % n, chord[v]] for v in range(n)]

def substitute(adj, cycle, x, pole_adj, ports):
    """Replace vertex x of host (adj, cycle) by a 3-pole.
    pole_adj: adjacency of the pole on vertices 0..m-1 (port vertices have degree 2 inside).
    ports: the 3 pole vertices that receive x's 3 host edges, in the order of adj[x].
    Returns (new_adj, list of possible new cycles, X vertex set)."""
    n = len(adj); m = len(pole_adj)
    lab = {i: n + i for i in range(m)}
    new = [list(a) for a in adj] + [[lab[j] for j in pole_adj[i]] for i in range(m)]
    new[x] = []
    for k, u in enumerate(adj[x]):
        p = lab[ports[k]]
        new[u] = [p if y == x else y for y in new[u]]
        new[p].append(u)
    # remove x by relabelling last vertex into x's slot
    last = len(new) - 1
    def rl(v): return x if v == last else v
    new[x] = new[last]; new.pop()
    new = [[rl(v) for v in a] for a in new]
    X = {rl(lab[i]) for i in range(m)}
    # cycles: x's cycle neighbours a (before) and b (after) map to ports; fill with Ham paths of X
    i = cycle.index(x); a, b = cycle[i-1], cycle[(i+1) % n]
    pa = rl(lab[ports[adj[x].index(a)]]); pb = rl(lab[ports[adj[x].index(b)]])
    cycles = []
    for hp in ham_paths(new, X, pa, pb):
        c = cycle[:i] + hp + cycle[i+1:]
        c = [rl(v) for v in c]
        cycles.append(c)
    return new, cycles, X
