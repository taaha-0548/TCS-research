"""P2(a) exact check: sites of every vertex at every depth of G_k = substitution of the morphic word
sigma^(d-1)(w0) by per-visit patterns.  Neighbours in other copies are written 'o'; at the
innermost depth x = 5 is an ordinary vertex."""
import clock as C, verify as V
from linemirror import host_line, rotation_between
def pattern_full(e, u, innermost):
    out = []
    for pieces, z, w, s in C.visits[e]:
        for vv, kind in ((s, "B1"), (w, "B3")):
            if isinstance(vv, int) and C.inv[vv] == u and (vv != C.X0 or innermost):
                for pc in pieces:
                    if vv in pc:
                        j = pc.index(vv)
                        def nb(t):
                            if not isinstance(t, int): return "o"
                            if t == C.X0 and not innermost: return "o"
                            return C.inv[t]
                        out.append((kind, nb(pc[j-1]) if j > 0 else "o", nb(pc[j+1]) if j + 1 < len(pc) else "o"))
    return out
for k in (3, 4, 5, 6, 7):
    adj, Ck, _ = V.build(k); lab = {v: i for i, v in enumerate(adj)}; inv_lab = {i: v for v, i in lab.items()}
    A = [[lab[w] for w in adj[v]] for v in adj]
    line, moves = host_line(A, [lab[v] for v in Ck]); actual = {}
    for i in range(len(line) - 1):
        z, w, s = rotation_between(line[i], line[i+1]); S = line[i]
        for vv, kind in ((s, "B1"), (w, "B3")):
            j = S.index(vv); actual.setdefault(inv_lab[vv], []).append((kind, inv_lab[S[j-1]], inv_lab[S[j+1]] if j + 1 < len(S) else "end"))
    word = list(C.K_walk_passages()); ok = tot = 0; bad = []
    for d in range(1, k + 1):
        level = k - d
        for u in range(8):
            if u == V.R or (level != 0 and u == V.X): continue
            pred = [site for f in word for site in pattern_full(f, u, level == 0)]; act = actual.get((level, u), [])
            n1 = [(kd, p[1] if isinstance(p, tuple) and p[0] == level else "o", q[1] if isinstance(q, tuple) and q[0] == level else "o") for kd, p, q in act]
            tot += 1; good = (n1 == pred); ok += good
            if not good: bad.append((d, u, len(n1), len(pred)))
        word = [g for f in word for g in C.sigma(f)]
    print(f"k={k}: {ok}/{tot} vertices exact (all depths 1..k); visits at innermost depth = {len(word)}; failures {bad}")
