"""E20: full sub-visit matrix M and offset b for the nested K=8 family; checks
c_{k+1} = M c_k + b exactly at every level, and prints M's characteristic polynomial."""
import sys, json
from collections import Counter
from fractions import Fraction
from general import from_chord
from nested_fast import rotate_to
import nested_fast
from level_tables import all_cycles
from transducer import rot, visit_B1, visit_B3
CH = [4, 3, 6, 1, 0, 7, 2, 5]; X, R, PERM = 5, 2, (2, 0, 1)
L = int(sys.argv[1]) if len(sys.argv) > 1 else 6

def snapshots(P, ports, Q, kind):
    """Sequence of (sequence-of-pole-vertices, endpoint) for the visit; pieces joined in path order."""
    a, b = Q[0], Q[-1]; c = [p for p in ports if p not in (a, b)][0]; snaps = []
    if kind == "B1":
        Rr = list(Q[::-1]); forb = ("cut", a)
        while True:
            snaps.append((tuple(Rr),))
            z = Rr[-1]; prev = Rr[-2] if len(Rr) > 1 else ("cut", b)
            cands = [w for w in P[z] if w != prev and w != forb]
            if z in ports and z != b: cands.append(("cut", z))
            w = [u for u in cands if u != forb and u != prev][0]
            if isinstance(w, tuple): return snaps
            Rr = rot(Rr, w); forb = w
    i = Q.index(c); X1 = list(Q[:i+1]); X2 = list(Q[i+1:][::-1]); pb = c; forb = c
    while True:
        snaps.append((tuple(X1), tuple(X2)))
        z = X2[-1]; prev = X2[-2] if len(X2) > 1 else None
        w = [u for u in P[z] if u != prev and u != forb][0]
        if w in X2: X2 = rot(X2, w)
        elif w == pb: snaps.append((tuple(X1 + X2[::-1]),)); return snaps
        else:
            j = X1.index(w); nX1 = X1[:j+1] + X2[::-1]; nX2 = X1[j+1:][::-1]
            pb = nX1[-1]; X1, X2 = nX1, nX2
        forb = w

def classify(snaps, inner, iname):
    """Each maximal run of snapshots with endpoint inside `inner` is one sub-visit.  Its kind and
    entry state are read off the last snapshot before the run: the inner block's orientation, and
    whether the inner block is still whole (B1 entry deletes the entry edge: block intact, endpoint
    becomes its first vertex) or the attachment was inside it (B3)."""
    subs = Counter(); i = 0
    while i < len(snaps):
        z = snaps[i][-1][-1]
        if z in inner and i > 0 and snaps[i-1][-1][-1] not in inner:
            prev = snaps[i-1]; seq = [v for piece in prev for v in piece]
            blk = [v for v in seq if v in inner]
            pos = [seq.index(v) for v in blk]
            assert pos == list(range(pos[0], pos[0] + len(pos))), "inner block not contiguous"
            Qi = tuple(blk)                          # oriented in path order
            cur = [v for piece in snaps[i] for v in piece]
            # B1: new endpoint = first vertex of the old inner block (entry edge deleted)
            kind = "B1" if cur[-1] == Qi[0] else "B3"
            subs[(iname[Qi[0]] + iname[Qi[-1]], kind)] += 1
            while i < len(snaps) and snaps[i][-1][-1] in inner: i += 1
        else: i += 1
    return subs

K = from_chord(8, CH); Kc = list(range(8)); G, Gc = K, Kc; rl = R
prev_inner = None; prev_iname = None; levels = []
for lev in range(L + 1):
    cycles = all_cycles(G, Gc)
    keep = [v for v in range(len(G)) if v != rl]; idx = {v: j for j, v in enumerate(keep)}
    P = [[idx[w] for w in G[v] if w != rl] for v in keep]
    ports = [idx[p] for p in G[rl]]; name = {p: "abc"[k] for k, p in enumerate(ports)}
    inner = {idx[v] for v in prev_inner} if prev_inner else set()
    iname = {idx[v]: nm for v, nm in prev_iname.items()} if prev_iname else {}
    costs = {}; Mrow = {}
    for cyc in cycles:
        c = rotate_to(cyc, rl, 1); hp = [idx[v] for v in c[1:]]
        for Q in (tuple(hp), tuple(hp[::-1])):
            for kind, fn in (("B1", visit_B1), ("B3", visit_B3)):
                key = (name[Q[0]] + name[Q[-1]], kind)
                costs[key] = fn(P, ports, Q)[2]
                if inner: Mrow[key] = classify([(tuple(Q),)] + snapshots(P, ports, Q, kind), inner, iname)
    levels.append(dict(costs=costs, M=Mrow))
    if lev == L: break
    # next level; remember where this level's pole sits inside the next graph, with port names
    nxt = nested_fast.next_level(K, Kc, X, G, [Gc], rl, PERM)
    off = len(K) - 1; gl = {v: j for j, v in enumerate(v for v in range(len(G)) if v != rl)}
    prev_inner = {off + gl[v] for v in gl}
    prev_iname = {off + gl[p]: name[idx[p]] for p in G[rl]}
    G, Gc = nxt; rl = R if R < X else R - 1

keys = sorted(levels[0]["costs"])
Ms = [tuple(tuple(lv["M"][e][f] for f in keys) for e in keys) for lv in levels[1:]]
print("M identical at all levels 1..L:", all(m == Ms[0] for m in Ms))
M = Ms[0]
bs = []
for k in range(1, L + 1):
    ck = levels[k]["costs"]; cp = levels[k-1]["costs"]
    bs.append(tuple(ck[e] - sum(M[i][j] * cp[keys[j]] for j in range(len(keys))) for i, e in enumerate(keys)))
print("offset b identical at all levels:", all(b == bs[0] for b in bs)); [print("   b_k =", b) for b in bs]
print("keys:", ["/".join(k) for k in keys])
for e, row in zip(keys, M): print("  ", "/".join(e), row)
# characteristic polynomial (Faddeev-LeVerrier, exact)
n = len(keys); A = [[Fraction(x) for x in r] for r in M]
def mul(X, Y): return [[sum(X[i][t] * Y[t][j] for t in range(n)) for j in range(n)] for i in range(n)]
coef = [Fraction(1)]; Mk = [[Fraction(0)] * n for _ in range(n)]; I = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
for k in range(1, n + 1):
    Mk = mul(A, [[Mk[i][j] + coef[-1] * I[i][j] for j in range(n)] for i in range(n)])
    coef.append(-sum(Mk[i][i] for i in range(n)) / k)
print("char poly coefficients (lambda^12 ... 1):", [int(c) for c in coef])
json.dump(dict(keys=["/".join(k) for k in keys], M=M, b=bs[0], charpoly=[int(c) for c in coef]), open("e20_M.json", "w"))
