#!/usr/bin/env python3
"""Reproducibility script for "Longer Thomason chains via 3-pole composition".

Standalone (Python 3.8+, standard library only). Checks every computational claim of the paper:
  [1] K: cubic, exactly 3 Hamiltonian cycles; P0 = K - r is simple (one Ham path per port pair).
  [2] The 12 visits of P0: all TRANSMIT; their costs c0; the passage matrix M (Lemma C).
  [3] Exact algebra: c_{k+1} = c0 + M c_k; the reachable set R; the two printed certificates of
      Table 3 (M_R u >= 2947/1000 u and M_R u' >= 29477/10000 u'), in exact rational arithmetic.
  [4] End-to-end: build G_k explicitly, run Thomason's lollipop algorithm from (v0, v1) = (0, 1),
      compare with the formula 4 + c_{k-1}[ca/B3]  (k = 1..KMAX).
  [5] Graph class for small k: cubic, exactly 3 Hamiltonian cycles (exhaustive), 3-edge-connected.
Run:  python3 verify.py [KMAX]      (default KMAX = 12, all of Table 1; about 2 seconds)."""
import sys, itertools
from fractions import Fraction as F

# ---------------------------------------------------------------- the base graph K
# K = 8-cycle 0-1-...-7-0 plus chords {0,4}, {1,3}, {2,6}, {5,7};  x = 5 is substituted,
# r = 2 is deleted to form the pole; PERM wires the j-th neighbour of x to port PERM[j].
CHORD = [4, 3, 6, 1, 0, 7, 2, 5]
X, R, PERM = 5, 2, (2, 0, 1)
K = [[(v - 1) % 8, (v + 1) % 8, CHORD[v]] for v in range(8)]       # adjacency in this fixed order

# ---------------------------------------------------------------- Thomason's lollipop algorithm
def lollipop(adj, cycle):
    """Hamiltonian cycle `cycle` (vertex list), fixed vertex cycle[0], fixed edge cycle[0]cycle[1].
    Start path = cycle minus the edge (cycle[-1], cycle[0]).  A step at endpoint z adds the unique
    edge zw with w != predecessor(z), w != last attachment, and deletes w's edge towards z
    (reverse the path after w).  Stops when that edge would go to cycle[0].  Returns #steps."""
    v0 = cycle[0]; path = list(cycle); pos = {v: i for i, v in enumerate(path)}; last = v0; steps = 0
    while True:
        z, pred = path[-1], path[-2]
        cand = [w for w in adj[z] if w != pred and w != last]
        assert len(cand) == 1
        w = cand[0]
        if w == v0: return steps
        i = pos[w]; path[i+1:] = path[i+1:][::-1]
        for j in range(i + 1, len(path)): pos[path[j]] = j
        last = w; steps += 1

def ham_cycles(adj, limit=None):
    """All Hamiltonian cycles (as edge sets) by exhaustive search with a degree pruning rule."""
    n = len(adj); seen = [False] * n; seen[0] = True; path = [0]; out = set()
    def alive():
        e = path[-1]
        return all(seen[v] or sum(1 for w in adj[v] if not seen[w] or w in (e, 0)) >= 2 for v in range(n))
    def dfs():
        v = path[-1]
        if len(path) == n:
            if 0 in adj[v]:
                out.add(frozenset(frozenset((path[i], path[(i + 1) % n])) for i in range(n)))
            return
        for w in adj[v]:
            if not seen[w]:
                seen[w] = True; path.append(w)
                if alive(): dfs()
                path.pop(); seen[w] = False
    dfs(); return out

# ---------------------------------------------------------------- 3-poles and visits
def pole(adj, r):
    keep = [v for v in range(len(adj)) if v != r]; idx = {v: i for i, v in enumerate(keep)}
    return [[idx[w] for w in adj[v] if w != r] for v in keep], [idx[p] for p in adj[r]], idx

def ham_paths(P, s, t):
    m = len(P); out = []
    def dfs(p, seen):
        if len(p) == m:
            if p[-1] == t: out.append(tuple(p))
            return
        for w in P[p[-1]]:
            if w not in seen and (w != t or len(p) == m - 1):
                seen.add(w); p.append(w); dfs(p, seen); p.pop(); seen.discard(w)
    dfs([s], {s}); return out

def rot(seq, w):
    i = seq.index(w); return seq[:i+1] + seq[i+1:][::-1]

def visit(P, ports, Q, kind):
    """One visit to pole P whose internal path is Q, oriented from the port nearer v0 (Q[0]) to Q[-1].
    B1: the walk deletes the entry cut edge at Q[0]; B3: it adds the unused cut edge at the third port.
    Returns (outcome, new path, cost, moves) where moves is the list (pieces, z, w, s) of all moves
    including the entry move, used to count passages through a vertex."""
    a, b = Q[0], Q[-1]; c = next(p for p in ports if p not in (a, b)); moves = []
    if kind == "B1":
        moves.append(((tuple(Q),), "out", "out", a))
        Rr = list(Q[::-1]); last = ("cut", a); cost = 0
        while True:
            z = Rr[-1]; pred = Rr[-2]
            cand = [w for w in P[z] if w != pred and w != last]
            if z in ports and z != b and last != ("cut", z): cand.append(("cut", z))
            assert len(cand) == 1
            w = cand[0]
            if isinstance(w, tuple):
                return ("REFLECT" if z == a else "TRANSMIT"), tuple(Rr), cost, moves
            s = Rr[Rr.index(w) + 1]; moves.append(((tuple(Rr),), z, w, s))
            Rr = rot(Rr, w); last = w; cost += 1
    i = Q.index(c); moves.append(((tuple(Q),), "out", c, Q[i+1]))
    X1, X2 = list(Q[:i+1]), list(Q[i+1:][::-1]); pb = c; last = c; flips = 0; cost = 0
    while True:
        z = X2[-1]; pred = X2[-2] if len(X2) > 1 else None
        w = next(u for u in P[z] if u != pred and u != last); cost += 1
        if w in X2:
            moves.append(((tuple(X1), tuple(X2)), z, w, X2[X2.index(w) + 1])); X2 = rot(X2, w)
        elif w == pb:
            moves.append(((tuple(X1), tuple(X2)), z, w, "out"))
            return ("TRANSMIT" if flips % 2 else "REFLECT"), tuple(X1 + X2[::-1]), cost, moves
        else:
            j = X1.index(w); moves.append(((tuple(X1), tuple(X2)), z, w, X1[j+1]))
            X1, X2 = X1[:j+1] + X2[::-1], X1[j+1:][::-1]; pb = X1[-1]; flips += 1
        last = w

def passages(moves, x, name):
    """Passages through vertex x: kind B1 if a move makes x the endpoint (deleted edge w-x, s = x),
    kind B3 if a move attaches to x (w = x); state = names of x's (predecessor, successor)."""
    out = {}
    for pieces, z, w, s in moves:
        if s == x or w == x:
            for pc in pieces:
                if x in pc: j = pc.index(x); key = (name[pc[j-1]] + name[pc[j+1]], "B1" if s == x else "B3")
            out[key] = out.get(key, 0) + 1
    return out

# ---------------------------------------------------------------- the family G_k
def build(k):
    """G_k with vertices (level, v); returns adjacency dict and its Hamiltonian cycle C_k starting
    (k,0),(k,1).  Ham paths of the pole come from the cycles of G_{k-1} (exactly 3 of them)."""
    if k == 0:
        adj = {(0, v): [(0, w) for w in K[v]] for v in range(8)}
        return adj, [(0, v) for v in range(8)], [[(0, v) for v in c] for c in KCYC]
    padj, _, pcycs = build(k - 1); rold = (k - 1, R); ports = [(k - 1, u) for u in K[R]]
    adj = {(k, v): [(k, w) for w in K[v] if w != X] for v in range(8) if v != X}
    for v, nb in padj.items():
        if v != rold: adj[v] = [w for w in nb if w != rold]
    for j, u in enumerate(K[X]): p = ports[PERM[j]]; adj[(k, u)].append(p); adj[p].append((k, u))
    hp = {}
    for cyc in pcycs:
        i = cyc.index(rold); c2 = cyc[i:] + cyc[:i]; path = c2[1:]
        hp[(path[0], path[-1])] = path; hp[(path[-1], path[0])] = path[::-1]
    cycs = []
    for cyc in KCYC:
        i = cyc.index(X); a, b = cyc[i - 1], cyc[(i + 1) % 8]
        pa, pb = ports[PERM[K[X].index(a)]], ports[PERM[K[X].index(b)]]
        cycs.append([(k, v) for v in cyc[:i]] + hp[(pa, pb)] + [(k, v) for v in cyc[i+1:]])
    base = next(cy for cy in cycs if cy[0] == (k, 0) and cy[1] == (k, 1))
    return adj, base, cycs

def three_edge_connected(adj):
    V = list(adj); E = [(u, w) for u in V for w in adj[u] if str(u) < str(w)]
    def connected(removed):
        start = V[0]; seen = {start}; st = [start]
        while st:
            u = st.pop()
            for w in adj[u]:
                if w not in seen and (u, w) not in removed and (w, u) not in removed:
                    seen.add(w); st.append(w)
        return len(seen) == len(V)
    return all(connected({e}) for e in E) and all(connected({e, f}) for e, f in itertools.combinations(E, 2))

def main(KMAX):
    ok = True
    def check(cond, msg):
        nonlocal ok; ok &= bool(cond); print(("  ok   " if cond else "  FAIL ") + msg)
    print("[1] base graph")
    cyc_sets = ham_cycles(K)
    check(all(len(set(a)) == 3 for a in K), "K is simple cubic")
    check(len(cyc_sets) == 3, f"K has exactly 3 Hamiltonian cycles (found {len(cyc_sets)})")
    global KCYC
    KCYC = []
    for E in cyc_sets:                                   # turn edge sets into vertex lists from 0
        c = [0]; prev = None
        while len(c) < 8:
            nxt = next(w for w in K[c[-1]] if frozenset((c[-1], w)) in E and w != prev)
            prev = c[-1]; c.append(nxt)
        if c[1] != 1 and c[-1] == 1: c = [0] + c[1:][::-1]
        KCYC.append(c)
    P0, ports, idx = pole(K, R); name = {p: "abc"[i] for i, p in enumerate(ports)}
    h = {(name[s], name[t]): len(ham_paths(P0, s, t)) for s, t in itertools.permutations(ports, 2)}
    check(all(v == 1 for v in h.values()), f"P0 = K - r is simple: h = {h}")
    check(X not in K[R], "r is not adjacent to x (hypothesis H2)")

    print("[2] the 12 visits of P0")
    xname = {idx[u]: "abc"[PERM[j]] for j, u in enumerate(K[X])}
    keys = sorted((name[s] + name[t], kd) for s, t in itertools.permutations(ports, 2) for kd in ("B1", "B3"))
    c0, Mrow = {}, {}
    for s, t in itertools.permutations(ports, 2):
        Q = ham_paths(P0, s, t)[0]
        for kd in ("B1", "B3"):
            out, Qn, cost, moves = visit(P0, ports, Q, kd); e = (name[s] + name[t], kd)
            check(out == "TRANSMIT", f"visit {e[0]}/{e[1]}: {out}, cost {cost}, passages {passages(moves, idx[X], xname)}")
            c0[e] = cost; Mrow[e] = passages(moves, idx[X], xname)
    M = [[Mrow[e].get(f, 0) for f in keys] for e in keys]
    print("    keys:", ["/".join(e) for e in keys]); print("    c0  :", [c0[e] for e in keys])
    for e, row in zip(keys, M): print("    M[" + "/".join(e) + "] =", row)

    print("[3] exact recursion and growth certificate")
    start = keys.index(("ca", "B3")); Rset = {start}; stack = [start]
    while stack:
        i = stack.pop()
        for j in range(12):
            if M[i][j] and j not in Rset: Rset.add(j); stack.append(j)
    Rl = sorted(Rset); MR = [[M[i][j] for j in Rl] for i in Rl]
    # Perron vector by power iteration on MR + I (exact fractions are not needed for u: any u works)
    u = [1.0] * len(Rl)
    for _ in range(2000):
        v = [sum(MR[i][j] * u[j] for j in range(len(Rl))) + u[i] for i in range(len(Rl))]
        s = max(v); u = [t / s for t in v]
    u = [F(round(t * 10**8)) for t in u]
    lam = F(29477, 10000)
    check(all(sum(F(MR[i][j]) * u[j] for j in range(len(Rl))) >= lam * u[i] for i in range(len(Rl))) and min(u) > 0,
          f"M_R u >= {lam} u exactly, u > 0 on R ({len(Rl)} reachable entries)")
    print(f"    certified base per vertex: (29477/10000)^(1/6) = {float(lam) ** (1/6):.6f}")
    names = [keys[i][0] + "/" + keys[i][1] for i in Rl]
    check(names == ["ab/B1", "ab/B3", "ac/B1", "ac/B3", "ba/B3", "bc/B1", "bc/B3", "ca/B3", "cb/B1", "cb/B3"],
          f"R = the ten types other than ba/B1, ca/B1")
    for lam_t, vec in ((F(2947, 1000), [77, 442, 227, 442, 330, 227, 330, 227, 77, 227]),
                       (F(29477, 10000), [746, 4283, 2199, 4283, 3198, 2199, 3198, 2199, 746, 2199])):
        check(all(sum(MR[i][j] * vec[j] for j in range(len(Rl))) >= lam_t * vec[i] for i in range(len(Rl))),
              f"Table 3 vector {vec[:3]}...: M_R u >= {lam_t} u exactly")
    c = [[c0[e] for e in keys]]
    for _ in range(KMAX): c.append([c[0][i] + sum(M[i][j] * c[-1][j] for j in range(12)) for i in range(12)])

    print(f"[4] end-to-end: lollipop walk on G_k from (0,1), k = 1..{KMAX}")
    for k in range(1, KMAX + 1):
        adj, Ck, cycs = build(k); lab = {v: i for i, v in enumerate(adj)}
        A = [[lab[w] for w in adj[v]] for v in adj]
        steps = lollipop(A, [lab[v] for v in Ck]); pred = 4 + c[k - 1][start]
        check(steps == pred, f"k={k:2d} n={len(adj):3d}: steps = {steps:8d}, formula 4 + c_(k-1)[ca/B3] = {pred}")

    print("[5] graph class, small k (exhaustive)")
    for k in range(0, 4):
        adj, Ck, cycs = build(k); lab = {v: i for i, v in enumerate(adj)}
        A = [[lab[w] for w in adj[v]] for v in adj]
        check(all(len(set(a)) == 3 for a in A) and len(ham_cycles(A)) == 3 and three_edge_connected(adj),
              f"k={k} n={len(A)}: simple cubic, exactly 3 Hamiltonian cycles, 3-edge-connected")
    print("\nALL CHECKS PASSED" if ok else "\nSOME CHECK FAILED"); return ok

if __name__ == "__main__":
    sys.exit(0 if main(int(sys.argv[1]) if len(sys.argv) > 1 else 12) else 1)
