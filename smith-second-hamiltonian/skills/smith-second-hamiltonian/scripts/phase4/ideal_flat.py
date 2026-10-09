"""Flat line-mirror systems with IDEAL normal-form tunnel gadgets (abstract, not necessarily
realisable).  A gadget has c states.  A site of the gadget = (A, T, I_f, I_b): the forward-transmit
set A with bijection T: A -> B, a fixed-point-free involution I_f on S\\A (forward reflections) and
I_b on S\\B (backward reflections); backward transmit = T^-1.  Search for the longest run as a
function of the number of sites N, for c = 2, 4."""
import sys, random, itertools, time

def involutions(elems):
    elems = list(elems)
    if not elems: yield {}; return
    if len(elems) % 2: return
    a = elems[0]
    for b in elems[1:]:
        rest = [e for e in elems if e not in (a, b)]
        for inv in involutions(rest):
            d = dict(inv); d[a] = b; d[b] = a; yield d

def site_types(c):
    S = list(range(c)); out = []
    for k in range(0, c + 1):
        for A in itertools.combinations(S, k):
            if (c - k) % 2: continue
            for B in itertools.combinations(S, k):
                for perm in itertools.permutations(B):
                    T = dict(zip(A, perm))
                    for If in involutions([s for s in S if s not in A]):
                        for Ib in involutions([s for s in S if s not in B]):
                            out.append((T, If, Ib))
    return out

def run(sites, init, cap=10**6):
    st = list(init); i, d, n = 0, 1, 0
    Tinv = [{v: k for k, v in T.items()} for (g, (T, If, Ib)) in sites]
    while 0 <= i < len(sites):
        g, (T, If, Ib) = sites[i]; s = st[g]; n += 1
        if d > 0:
            if s in T: st[g] = T[s]
            else: st[g] = If[s]; d = -d
        else:
            ti = Tinv[i]
            if s in ti: st[g] = ti[s]
            else: st[g] = Ib[s]; d = -d
        i += d
        if n > cap: return None
    return n

if __name__ == "__main__":
    rng = random.Random(1)
    for c in (2, 4):
        types = site_types(c); print(f"c={c}: {len(types)} ideal site types")
        for m in (1, 2, 3, 4, 6):
            for N in (4, 8, 12, 16):
                if N < m: continue
                best = 0; t0 = time.time()
                while time.time() - t0 < 2.5:
                    owners = [rng.randrange(m) for _ in range(N)]
                    sites = [(g, rng.choice(types)) for g in owners]
                    v = run(sites, [rng.randrange(c) for _ in range(m)])
                    if v and v > best: best = v
                print(f"   m={m} gadgets, N={N:2d} sites: longest run {best}", flush=True)
