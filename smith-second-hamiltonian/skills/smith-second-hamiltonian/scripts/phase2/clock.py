"""P2(a): the nested host G_k as a clock.  Morphism sigma on the 12 visit types of P_0 (ordered
passages through x), patterns of sites per vertex per visit type, and the prediction
   sites of vertex u at depth d (1 <= d <= k)  =  concat_{f in sigma^(d-1)(w0)} pattern_u(f)
compared with the actual host line of G_k.  A site is (kind, predecessor-label, successor-label)."""
import sys, itertools
sys.path.insert(0, ".."); sys.path.insert(0, "../../../../../paper")
import verify as V
from linemirror import host_line, rotation_between

V.KCYC = []
for E in V.ham_cycles(V.K):
    c = [0]; prev = None
    while len(c) < 8:
        nxt = next(w for w in V.K[c[-1]] if frozenset((c[-1], w)) in E and w != prev); prev = c[-1]; c.append(nxt)
    if c[1] != 1 and c[-1] == 1: c = [0] + c[1:][::-1]
    V.KCYC.append(c)
P0, ports, idx = V.pole(V.K, V.R); inv = {i: v for v, i in idx.items()}
name = {p: "abc"[i] for i, p in enumerate(ports)}; xname = {idx[u]: "abc"[V.PERM[j]] for j, u in enumerate(V.K[V.X])}
X0 = idx[V.X]
visits = {}
for s, t in itertools.permutations(ports, 2):
    Q = V.ham_paths(P0, s, t)[0]
    for kd in ("B1", "B3"): visits[(name[s] + name[t], kd)] = V.visit(P0, ports, Q, kd)[3]

def label(v):            # K-label of a P0 vertex; ports of the inner pole are named by x-neighbours
    return inv[v] if isinstance(v, int) else v

def sigma(e):
    out = []
    for pieces, z, w, s in visits[e]:
        if s == X0 or w == X0:
            for pc in pieces:
                if X0 in pc: j = pc.index(X0); out.append((xname[pc[j-1]] + xname[pc[j+1]], "B1" if s == X0 else "B3"))
    return out

def pattern(e, u):
    """Sites of P0-vertex u (K-label) during a visit of type e: (kind, pred, succ) in K labels.
    pred/succ of x are replaced by the inner port it is wired to -- handled by marking 'x'."""
    out = []
    for pieces, z, w, s in visits[e]:
        for vv, kind in ((s, "B1"), (w, "B3")):
            if isinstance(vv, int) and vv != X0 and inv[vv] == u:
                for pc in pieces:
                    if vv in pc:
                        j = pc.index(vv)
                        nb = lambda t: ("x" if t == X0 else (inv[t] if isinstance(t, int) else t))
                        out.append((kind, nb(pc[j-1]) if j > 0 else "cut", nb(pc[j+1]) if j + 1 < len(pc) else "cut"))
    return out

def K_walk_passages():
    line, moves = host_line(V.K, V.KCYC[0])
    out = []
    for i in range(len(line) - 1):
        z, w, s = rotation_between(line[i], line[i+1]); A = line[i]
        if s == V.X or w == V.X:
            j = A.index(V.X); out.append(("abc"[V.PERM[V.K[V.X].index(A[j-1])]] + "abc"[V.PERM[V.K[V.X].index(A[j+1])]], "B1" if s == V.X else "B3"))
    return out

if __name__ == "__main__":
    w0 = K_walk_passages(); print("w0 =", w0)
    print("sigma lengths:", {"/".join(e): len(sigma(e)) for e in sorted(visits)})
    for k in (3, 4, 5):
        adj, Ck, _ = V.build(k); lab = {v: i for i, v in enumerate(adj)}; inv_lab = {i: v for v, i in lab.items()}
        A = [[lab[w] for w in adj[v]] for v in adj]
        line, moves = host_line(A, [lab[v] for v in Ck])
        actual = {}
        for i in range(len(line) - 1):
            z, w, s = rotation_between(line[i], line[i+1]); S = line[i]
            for vv, kind in ((s, "B1"), (w, "B3")):
                j = S.index(vv)
                actual.setdefault(inv_lab[vv], []).append((kind, inv_lab[S[j-1]], inv_lab[S[j+1]] if j + 1 < len(S) else "end"))
        word = list(w0); ok = tot = 0
        for d in range(1, k + 1):
            level = k - d
            for u in range(8):
                if u in (V.R, V.X) and level != 0 or (level == 0 and u == V.R): continue
                if level != 0 and u == V.X: continue
                pred = [site for f in word for site in pattern(f, u)]
                act = actual.get((level, u), [])
                # compare kinds and the K-labels of neighbours that are in the same copy
                def norm(seq):
                    return [(kd, p[1] if isinstance(p, tuple) and p[0] == level else "o", q[1] if isinstance(q, tuple) and q[0] == level else "o") for kd, p, q in seq]
                def normp(seq):
                    return [(kd, p if isinstance(p, int) else "o", q if isinstance(q, int) else "o") for kd, p, q in seq]
                tot += 1; ok += (norm(act) == normp(pred))
            word = [g for f in word for g in sigma(f)]
        print(f"k={k}: vertices checked {tot}, site sequences predicted exactly {ok}")
