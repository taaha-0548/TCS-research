"""E16: nested 3-pole substitution.  G_0 = K;  G_k = K with vertex x replaced by the 3-pole
G_{k-1} - r_{k-1}.  |G_k| = |G_{k-1}| + |K| - 2.  Measures lollipop length growth per level.
Usage: python3 nested.py [trials] [levels] [seed]"""
import random, sys, json, math, time
from lollipop import random_instance
from general import from_chord, lollipop_g

def first_ham_path(adj, verts, s, t, budget=200000):
    verts = set(verts); m = len(verts); seen = {s}; p = [s]; cnt = [0]
    def dfs():
        cnt[0] += 1
        if cnt[0] > budget: raise TimeoutError
        v = p[-1]
        if len(p) == m: return v == t
        for w in adj[v]:
            if w in verts and w not in seen and (w != t or len(p) == m - 1):
                seen.add(w); p.append(w)
                if dfs(): return True
                p.pop(); seen.discard(w)
        return False
    return list(p) if dfs() else None

def subst(Kadj, Kcyc, x, Padj, Pcyc_ports, rng):
    """Replace x in K by pole P (Padj on 0..m-1, ports = 3 vertices with degree 2).
    Ham cycle: K's cycle with x replaced by a Ham path of P between the matching ports."""
    n = len(Kadj); m = len(Padj); ports = Pcyc_ports
    off = n
    A = [list(a) for a in Kadj] + [[off + w for w in Padj[i]] for i in range(m)]
    perm = list(ports); rng.shuffle(perm)
    for k, u in enumerate(Kadj[x]):
        p = off + perm[k]
        A[u] = [p if y == x else y for y in A[u]]; A[p].append(u)
    i = Kcyc.index(x); a, b = Kcyc[i-1], Kcyc[(i+1) % n]
    pa = off + perm[Kadj[x].index(a)]; pb = off + perm[Kadj[x].index(b)]
    hp = first_ham_path(A, range(off, off + m), pa, pb)
    if hp is None: return None
    cyc = Kcyc[:i] + hp + Kcyc[i+1:]
    # drop x: relabel so vertices are 0..N-1
    keep = [v for v in range(len(A)) if v != x]; idx = {v: j for j, v in enumerate(keep)}
    A2 = [[idx[w] for w in A[v]] for v in keep]
    return A2, [idx[v] for v in cyc]

def to_pole(A, r):
    keep = [v for v in range(len(A)) if v != r]; idx = {v: j for j, v in enumerate(keep)}
    return [[idx[w] for w in A[v] if w != r] for v in keep], [idx[w] for w in A[r]]

def best_walk(A, cyc, starts=6, rng=None):
    n = len(cyc); best = 0
    for s in [0] + [rng.randrange(n) for _ in range(starts - 1)]:
        for d in (1, -1):
            c = [cyc[(s + d * t) % n] for t in range(n)]
            best = max(best, lollipop_g(A, c, max_steps=5 * 10**6)[0])
    return best

if __name__ == "__main__":
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    L = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    rng = random.Random(int(sys.argv[3]) if len(sys.argv) > 3 else 1)
    results = []; t0 = time.time()
    for trial in range(T):
        if time.time() - t0 > 240: break
        nk = rng.choice([6, 8, 10])
        K = from_chord(nk, random_instance(nk, rng)); Kc = list(range(nk))
        x = rng.randrange(2, nk - 1); r = rng.randrange(nk)
        G, Gc = K, Kc; seq = []
        try:
            for lev in range(L):
                seq.append((len(G), best_walk(G, Gc, rng=rng)))
                P, ports = to_pole(G, r if lev == 0 else rng.randrange(len(G)))
                out = subst(K, Kc, x, P, ports, rng)
                if out is None: break
                G, Gc = out
        except (TimeoutError, RuntimeError):
            pass
        if len(seq) >= 4:
            (n1, s1), (n2, s2) = seq[-2], seq[-1]
            base = (s2 / max(1, s1)) ** (1 / (n2 - n1)) if s1 > 0 else 0
            results.append(dict(nk=nk, seq=seq, base=base))
    results.sort(key=lambda d: -d["base"])
    for d in results[:8]: print(f"K={d['nk']} base~{d['base']:.4f}  {d['seq']}")
    print("trials with >=4 levels:", len(results))
    json.dump(results[:20], open("e16_nested.json", "w"), indent=1)
