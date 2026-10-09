"""E17: deterministic nested families F(K, x, r, perm):
   G_0 = K,  G_k = K[x <- (G_{k-1} - r_k)],  r_k = the copy of vertex r in the OUTER K of G_{k-1},
   ports wired by the fixed permutation perm.  |G_k| = |K| + k(|K| - 2).
Stage 1 screens random (K, x, r, perm) up to 4 levels; stage 2 extends the best to many levels.
Usage: python3 nested_family.py [screen_trials] [deep_levels] [seed]"""
import random, sys, json, time
from lollipop import random_instance
from general import from_chord, lollipop_g
from nested import first_ham_path, to_pole

def subst_fixed(K, Kc, x, P, ports, perm):
    n = len(K); m = len(P); off = n
    A = [list(a) for a in K] + [[off + w for w in P[i]] for i in range(m)]
    for k, u in enumerate(K[x]):
        p = off + ports[perm[k]]
        A[u] = [p if y == x else y for y in A[u]]; A[p].append(u)
    i = Kc.index(x); a, b = Kc[i-1], Kc[(i+1) % n]
    pa = off + ports[perm[K[x].index(a)]]; pb = off + ports[perm[K[x].index(b)]]
    hp = first_ham_path(A, range(off, off + m), pa, pb, budget=2 * 10**6)
    if hp is None: return None
    cyc = Kc[:i] + hp + Kc[i+1:]
    keep = [v for v in range(len(A)) if v != x]; idx = {v: j for j, v in enumerate(keep)}
    return [[idx[w] for w in A[v]] for v in keep], [idx[v] for v in cyc]

def family(K, Kc, x, r, perm, levels):
    G, Gc = K, Kc; rl = r; out = []
    for lev in range(levels + 1):
        n = len(Gc); best = 0
        for s in range(n):                       # all starts, both directions
            for d in (1, -1):
                c = [Gc[(s + dd) % n] for dd in range(0, d * n, d)]
                best = max(best, lollipop_g(G, c, max_steps=3 * 10**7)[0])
        out.append((n, best))
        if lev == levels: break
        P, ports = to_pole(G, rl)
        nxt = subst_fixed(K, Kc, x, P, ports, perm)
        if nxt is None: break
        G, Gc = nxt
        rl = r if r < x else r - 1               # outer copy of r keeps its label (x dropped)
    return out

def base_of(seq):
    (n1, s1), (n2, s2) = seq[-2], seq[-1]
    return (s2 / s1) ** (1 / (n2 - n1)) if s1 > 0 and s2 > 0 else 0.0

if __name__ == "__main__":
    S = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    D = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    rng = random.Random(int(sys.argv[3]) if len(sys.argv) > 3 else 2)
    perms = [(0,1,2),(0,2,1),(1,0,2),(1,2,0),(2,0,1),(2,1,0)]
    cands = []; t0 = time.time()
    for _ in range(S):
        if time.time() - t0 > 120: break
        nk = rng.choice([6, 8, 8, 10])
        ch = random_instance(nk, rng); K = from_chord(nk, ch); Kc = list(range(nk))
        x = rng.randrange(2, nk - 1)
        if x == ch[0]: continue
        r = rng.choice([v for v in range(nk) if v != x])
        perm = rng.choice(perms)
        try: seq = family(K, Kc, x, r, perm, 3)
        except (TimeoutError, RuntimeError, AssertionError): continue
        if len(seq) == 4: cands.append((base_of(seq) * (seq[-1][1] > seq[-2][1]), seq, nk, ch, x, r, perm))
    cands.sort(key=lambda c: -c[0])
    print("screened", len(cands))
    deep = []
    for b, seq, nk, ch, x, r, perm in cands[:6]:
        if time.time() - t0 > 270: break
        K = from_chord(nk, ch)
        try: seq = family(K, list(range(nk)), x, r, perm, D)
        except (TimeoutError, RuntimeError, AssertionError) as e: pass
        ratios = [round((seq[i+1][1] / seq[i][1]) ** (1 / (seq[i+1][0] - seq[i][0])), 4) for i in range(len(seq) - 1) if seq[i][1]]
        print(f"K={nk} chord={ch} x={x} r={r} perm={perm}\n   seq={seq}\n   per-vertex ratios={ratios}")
        deep.append(dict(nk=nk, chord=ch, x=x, r=r, perm=perm, seq=seq, ratios=ratios))
    json.dump(deep, open("e17_nested_family.json", "w"), indent=1)
