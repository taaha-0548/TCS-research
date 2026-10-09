"""A3: independent construction of the family and its 3 Hamiltonian cycles.
Vertices are tuples (level, v).  G_k = (copy of K minus x at level k) + (G_{k-1} minus its outer r).
Edges: K-edges among non-x vertices; G_{k-1} edges avoiding its outer r; and the j-th neighbour of x
(order K[x]) joined to port perm[j] of G_{k-1}, ports = neighbours of G_{k-1}'s outer r in the
order of K[r].  Hamiltonian cycles by recursion: a cycle of G_k = a cycle of K through edge pair
{u,u'} at x, with x replaced by the Hamiltonian path of G_{k-1} - r between the matching ports
(= a cycle of G_{k-1} through r's two edges, with r removed)."""
import sys, json
sys.path.insert(0, "..")
from general import from_chord
from indep import indep_walk
CH = [4, 3, 6, 1, 0, 7, 2, 5]; X, R, PERM = 5, 2, (2, 0, 1)
Kadj = from_chord(8, CH)
def K_ham_cycles():
    out = set()
    def dfs(p, seen):
        if len(p) == 8:
            if p[0] in Kadj[p[-1]]:
                c = p[:]; i = c.index(min(c)); c = c[i:] + c[:i]
                if c[1] > c[-1]: c = [c[0]] + c[1:][::-1]
                out.add(tuple(c))
            return
        for w in Kadj[p[-1]]:
            if w not in seen: seen.add(w); p.append(w); dfs(p, seen); p.pop(); seen.discard(w)
    dfs([0], {0}); return [list(c) for c in out]
KC = K_ham_cycles()

def build(k):
    """Returns adjacency dict and the list of Hamiltonian cycles (as vertex lists)."""
    if k == 0:
        adj = {(0, v): [(0, w) for w in Kadj[v]] for v in range(8)}
        return adj, [[(0, v) for v in c] for c in KC]
    padj, pcyc = build(k - 1)
    r_old = (k - 1, R) if k - 1 > 0 or True else None
    ports = [(k - 1, u) for u in Kadj[R]]               # outer copies of r's neighbours, K[r] order
    adj = {}
    for v in range(8):
        if v == X: continue
        adj[(k, v)] = [(k, w) for w in Kadj[v] if w != X]
    for v, nb in padj.items():
        if v == r_old: continue
        adj[v] = [w for w in nb if w != r_old]
    for j, u in enumerate(Kadj[X]):
        p = ports[PERM[j]]; adj[(k, u)].append(p); adj[p].append((k, u))
    # Hamiltonian paths of the pole between port pairs, from G_{k-1}'s cycles
    hp = {}
    for c in pcyc:
        i = c.index(r_old); c2 = c[i:] + c[:i]          # r, a, ..., b
        path = c2[1:]
        hp[(path[0], path[-1])] = path; hp[(path[-1], path[0])] = path[::-1]
    cycles = []
    for c in KC:
        i = c.index(X); a, b = c[i - 1], c[(i + 1) % 8]
        pa = ports[PERM[Kadj[X].index(a)]]; pb = ports[PERM[Kadj[X].index(b)]]
        cyc = [(k, v) for v in c[:i]] + hp[(pa, pb)] + [(k, v) for v in c[i+1:]]
        cycles.append(cyc)
    return adj, cycles

def check(adj, cyc):
    n = len(adj)
    assert all(len(set(nb)) == 3 for nb in adj.values()), "not cubic/simple"
    assert len(set(cyc)) == n == len(cyc) and all(cyc[(t+1) % n] in adj[cyc[t]] for t in range(n))

if __name__ == "__main__":
    M = json.load(open("../e20_M.json")); keys = M["keys"]; Mm = M["M"]; c0 = M["b"]
    c = [c0]
    for _ in range(14): c.append([c0[i] + sum(Mm[i][j] * c[-1][j] for j in range(12)) for i in range(12)])
    j = keys.index("ca/B3")
    L = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    for k in range(0, L + 1):
        adj, cycles = build(k); n = len(adj)
        for cy in cycles: check(adj, cy)
        # C_k: the cycle coming from K's cycle 0..7, started at (k,0) towards (k,1)
        base = [cy for cy in cycles if all(v in cy for v in [(k, 0), (k, 1)])]
        Ck = None
        for cy in cycles:
            i = cy.index((k, 0))
            if cy[(i + 1) % n] == (k, 1) and cy[(i - 1) % n] == (k, 7): Ck = cy[i:] + cy[:i]
            elif cy[(i - 1) % n] == (k, 1) and cy[(i + 1) % n] == (k, 7):
                cy2 = cy[::-1]; i = cy2.index((k, 0)); Ck = cy2[i:] + cy2[:i]
        lab = {v: t for t, v in enumerate(adj)}; A = [[lab[w] for w in adj[v]] for v in adj]
        steps, _ = indep_walk(A, [lab[v] for v in Ck])
        pred = 4 + c[k - 1][j] if k >= 1 else None
        print(f"k={k} n={n} cycles={len(cycles)} independent steps(0,+1)={steps}  predicted={pred}  match={steps == pred if pred else '-'}", flush=True)
