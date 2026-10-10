"""Structure of near-extremal colourings at n = r^2 + 1 (direction 3, round 7).

For r in {3, 4}:
  * best colourings found by annealing (supersat.anneal), several seeds, kept with their bad counts;
  * the exact optimum of the one-vertex extension of the merged affine plane AG(2,r) (r = 3 prime field,
    r = 4 over GF(4)); all merge choices are equivalent up to collineations (the reviewer's S_{r+1} remark),
    so one merge is enough;
and for every colouring we record:
  colour-class sizes; for the least colour G: t = e(G) - p_r(n) and a heuristic min-m r-partition of
  H = complement(G) (sizes, m, S+); whether all bad sets share a vertex; the minimum number of vertices whose
  deletion leaves no bad set (exact hitting set); for r = 3, whether the K_9 left after deleting a hitting
  vertex is isomorphic to the merged affine colouring."""
import itertools, json, random, sys
from math import comb
import numpy as np
import networkx as nx
from ortools.sat.python import cp_model
from supersat import setup, anneal, counts_of

def p(r, n):
    a, b = divmod(n, r); return r * comb(a, 2) + a * b

# ---------- GF(q) for q = 3 (prime) and q = 4 ----------
def field(q):
    if q == 4:
        def mul(a, b):
            x = 0
            for i in range(2):
                if (b >> i) & 1: x ^= a << i
            if x & 4: x ^= 0b111
            return x
        add = lambda a, b: a ^ b
        neg = lambda a: a
        inv = {a: next(b for b in range(1, 4) if mul(a, b) == 1) for a in range(1, 4)}
    else:
        mul = lambda a, b: (a * b) % q; add = lambda a, b: (a + b) % q; neg = lambda a: (-a) % q
        inv = {a: pow(a, -1, q) for a in range(1, q)}
    return mul, add, neg, inv

def affine_merged(q):
    """Colouring of K_{q^2}: direction classes 0..q-2 single, directions q-1 and infinity merged."""
    mul, add, neg, inv = field(q)
    pts = [(a, b) for a in range(q) for b in range(q)]
    col = {}
    for i, j in itertools.combinations(range(q * q), 2):
        (x1, y1), (x2, y2) = pts[i], pts[j]
        dx, dy = add(x2, neg(x1)), add(y2, neg(y1))
        d = q if dx == 0 else mul(dy, inv[dx])
        col[(i, j)] = d if d <= q - 2 else q - 1
    return col

def bad_sets(col_list, n, r, data):
    edges, sets, se, inc = data
    cnt = counts_of(np.array(col_list, dtype=np.int8), se, r)
    return [tuple(int(v) for v in S) for S in sets[(cnt == 0).any(1)]]

def min_hitting_set(badsets, n):
    if not badsets: return 0, []
    m = cp_model.CpModel(); y = [m.NewBoolVar("") for _ in range(n)]
    for S in badsets: m.AddBoolOr([y[v] for v in S])
    m.Minimize(sum(y)); s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 60; s.Solve(m)
    return int(s.ObjectiveValue()), [v for v in range(n) if s.Value(y[v])]

def furedi_partition(Hadj, n, r, restarts=200, seed=0):
    """Heuristic: r-partition minimising H-edges inside parts (local search, many restarts)."""
    rng = random.Random(seed); best = None
    for _ in range(restarts):
        part = [rng.randrange(r) for _ in range(n)]
        improved = True
        while improved:
            improved = False
            for v in rng.sample(range(n), n):
                inside = [sum(1 for u in Hadj[v] if part[u] == k) for k in range(r)]
                k = min(range(r), key=lambda k: inside[k])
                if inside[k] < inside[part[v]]: part[v] = k; improved = True
        m = sum(1 for v in range(n) for u in Hadj[v] if u > v and part[u] == part[v])
        if best is None or m < best[0]: best = (m, part[:])
    m, part = best
    sizes = sorted([part.count(k) for k in range(r)], reverse=True)
    return m, sizes

def profile(name, col_list, n, r, data):
    edges = data[0]
    B = bad_sets(col_list, n, r, data)
    sizes = [sum(1 for c in col_list if c == k) for k in range(r)]
    g = min(range(r), key=lambda k: sizes[k])
    Hadj = [set() for _ in range(n)]
    for (a, b), c in zip(edges, col_list):
        if c != g: Hadj[a].add(b); Hadj[b].add(a)
    t = sizes[g] - p(r, n)
    m, psizes = furedi_partition(Hadj, n, r)
    Splus = sum(max(0, s - r) for s in psizes)
    common = set(range(n))
    for S in B: common &= set(S)
    hs, hv = min_hitting_set(B, n)
    print(f"[{name}] bad={len(B)}  class sizes={sizes}  least colour: t={t}, Furedi(heur) sizes={psizes} m={m} S+={Splus}"
          f"  common vertex of all bad sets: {sorted(common) if common else 'none'}  min deletion set={hs} {hv}", flush=True)
    return B, hv

def coloured_iso(colA, colB, n, r):
    """Is colouring A of K_n isomorphic to colouring B up to vertex and colour permutations?"""
    def G(col, perm):
        H = nx.Graph(); H.add_nodes_from(range(n))
        for (a, b), c in col.items(): H.add_edge(a, b, c=perm[c])
        return H
    GB = G(colB, list(range(r)))
    em = lambda x, y: x["c"] == y["c"]
    return any(nx.is_isomorphic(G(colA, list(perm)), GB, edge_match=em) for perm in itertools.permutations(range(r)))

if __name__ == "__main__":
    for r in [int(a) for a in sys.argv[1:]] or [3, 4]:
        n = r * r + 1; data = setup(n, r); edges = data[0]
        # exact one-vertex extension of the merged affine plane
        ac = affine_merged(r); newv = r * r
        mdl = cp_model.CpModel()
        x = {u: [mdl.NewBoolVar("") for _ in range(r)] for u in range(newv)}
        for u in x: mdl.AddExactlyOne(x[u])
        badv = []
        for S in itertools.combinations(range(newv), r):
            old = [ac[e] for e in itertools.combinations(S, 2)]
            b = mdl.NewBoolVar("")
            for k in range(r):
                if k not in old: mdl.AddBoolOr([x[u][k] for u in S] + [b])
            badv.append(b)
        mdl.Minimize(sum(badv)); s = cp_model.CpSolver(); s.parameters.num_workers = 4; s.parameters.max_time_in_seconds = 600
        st = s.Solve(mdl)
        print(f"r={r}: exact best extension of merged AG(2,{r}): {s.StatusName(st)} bad = {int(s.ObjectiveValue())}", flush=True)
        colA = [ac[e] if e in ac else next(k for k in range(r) if s.Value(x[e[0]][k])) for e in edges]
        profile(f"r={r} affine+1 (exact)", colA, n, r, data)
        # annealed near-extremal colourings
        iters = 100000 if r == 3 else 600000
        runs = []
        for sd in range(6):
            b, c = anneal(n, r, iters, seed=1000 + sd, data=data); runs.append((b, c.tolist()))
        runs.sort(key=lambda z: z[0])
        for i, (b, c) in enumerate(runs[:3]):
            B, hv = profile(f"r={r} anneal #{i}", c, n, r, data)
            if r == 3 and len(hv) == 1:
                v = hv[0]; keep = [u for u in range(n) if u != v]; idx = {u: i for i, u in enumerate(keep)}
                sub = {(idx[a], idx[b]): cc for (a, b), cc in zip(edges, c) if v not in (a, b)}
                print(f"    K_9 after deleting {v}: isomorphic to merged AG(2,3)? {coloured_iso(sub, affine_merged(3), 9, 3)}", flush=True)
        json.dump(runs[:3], open(f"../extremal_r{r}.json", "w"))
