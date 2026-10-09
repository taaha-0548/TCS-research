"""E18: deep evaluation of a nested family with lollipop-generated Ham cycles (no DFS).
G_k = K[x <- G_{k-1} - r]. A Ham path of the pole between ports p,q is a Ham cycle of G_{k-1}
through r-p and r-q with r removed; such cycles are produced by lollipop walks started at r
(Thomason: the output contains the fixed edge).  All starts evaluated at every level.
Usage: python3 nested_fast.py chord x r perm levels time_budget"""
import sys, json, time, ast
from general import from_chord, lollipop_g, cyc_edges

def rotate_to(c, v, d):
    n = len(c); i = c.index(v); return [c[(i + d * t) % n] for t in range(n)]

def cycle_through(G, cycles, r, p, q, max_rounds=6):
    """Find a Ham cycle of G containing edges r-p and r-q, expanding the pool by lollipop walks."""
    pool = [tuple(c) for c in cycles]; seen = {frozenset(cyc_edges(c)) for c in pool}
    for _ in range(max_rounds):
        for c in pool:
            E = cyc_edges(c)
            if frozenset((r, p)) in E and frozenset((r, q)) in E: return list(c)
        new = []
        for c in pool:
            for v in (r, p, q):
                for d in (1, -1):
                    _, out, _ = lollipop_g(G, rotate_to(list(c), v, d), max_steps=10**8)
                    k = frozenset(cyc_edges(out))
                    if k not in seen: seen.add(k); new.append(tuple(out))
        if not new: return None
        pool = new
    return None

def next_level(K, Kc, x, G, Gcycles, rl, perm):
    n = len(K); m = len(G) - 1
    ports = list(G[rl])                       # G-labels of r's neighbours = pole ports
    i = Kc.index(x); a, b = Kc[i-1], Kc[(i+1) % n]
    pa = ports[perm[K[x].index(a)]]; pb = ports[perm[K[x].index(b)]]
    c = cycle_through(G, Gcycles, rl, pa, pb)
    if c is None: return None
    c = rotate_to(c, rl, 1)
    if c[1] != pb: c = rotate_to(c, rl, -1)   # c = r, pb, ..., pa
    hp = c[1:][::-1]                          # pa ... pb, a Ham path of G - r
    # assemble G_new: K minus x  +  G minus r
    gl = {v: j for j, v in enumerate(v for v in range(len(G)) if v != rl)}
    off = n - 1; kl = {v: j for j, v in enumerate(v for v in range(n) if v != x)}
    A = [[] for _ in range(off + m)]
    for v in range(n):
        if v == x: continue
        for w in K[v]:
            if w != x: A[kl[v]].append(kl[w])
    for v in range(len(G)):
        if v == rl: continue
        for w in G[v]:
            if w != rl: A[off + gl[v]].append(off + gl[w])
    for k, u in enumerate(K[x]):
        p = ports[perm[k]]; A[kl[u]].append(off + gl[p]); A[off + gl[p]].append(kl[u])
    cyc = [kl[v] for v in Kc[:i]] + [off + gl[v] for v in hp] + [kl[v] for v in Kc[i+1:]]
    assert all(len(set(a)) == 3 for a in A) and len(set(cyc)) == len(A)
    assert all(cyc[(t+1) % len(cyc)] in A[cyc[t]] for t in range(len(cyc)))
    return A, cyc

if __name__ == "__main__":
    CH = ast.literal_eval(sys.argv[1]); X = int(sys.argv[2]); R = int(sys.argv[3])
    PERM = ast.literal_eval(sys.argv[4]); L = int(sys.argv[5]); B = float(sys.argv[6])
    nk = len(CH); K = from_chord(nk, CH); Kc = list(range(nk))
    G, Gc = K, Kc; rl = R; out = []; t0 = time.time()
    for lev in range(L + 1):
        n = len(Gc); best = 0; tot = 0
        for s in range(n):
            for d in (1, -1):
                st = lollipop_g(G, rotate_to(Gc, Gc[s], d), max_steps=10**8)[0]
                best = max(best, st); tot += st
        out.append((n, best)); print(f"level {lev}: n={n} max steps={best}  ({time.time()-t0:.0f}s)", flush=True)
        if lev == L or time.time() - t0 > B: break
        nxt = next_level(K, Kc, X, G, [Gc], rl, PERM)
        if nxt is None: print("no suitable Ham cycle"); break
        G, Gc = nxt
        rl = R if R < X else R - 1           # outer copy of r: K-label shifted past x
    s = [b for _, b in out]; d = nk - 2
    print("level factors:", [round(s[i+1] / s[i], 3) for i in range(len(s) - 1)])
    print("per-vertex, two-level:", [round((s[i+2] / s[i]) ** (1 / (2 * d)), 4) for i in range(len(s) - 2)])
    json.dump(dict(chord=CH, x=X, r=R, perm=PERM, seq=out), open(f"e18_K{nk}_x{X}_r{R}.json", "w"))
