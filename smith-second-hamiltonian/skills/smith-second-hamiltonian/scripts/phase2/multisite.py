"""P2(b3): abstract line-mirror systems with m multi-site gadgets.
Each gadget g (a realisable pole automaton) has s sites; the sites are interleaved along the line.
Consistency (as in real hosts): a gadget's consecutive sites chain port pairs: a site's forward type
uses the gadget's current pair (either orientation); after it the pair becomes {out,c} (B1) or
{in,c} (B3).  The particle starts at the left moving right.  We search for long runs."""
import sys, random, itertools, time, json
sys.path.insert(0, ".."); sys.path.insert(0, "../../../../../paper")
import verify as V
from lollipop import random_instance
from cells import pole_table, bwd_of, orient

def chord_adj(n, ch): return [[(v - 1) % n, (v + 1) % n, ch[v]] for v in range(n)]
def third(p): return next(c for c in "abc" if c not in p)

def gadget_library(rng, count):
    lib = []
    while len(lib) < count:
        n = rng.choice([8, 10, 12]); G = chord_adj(n, random_instance(n, rng)); P, ports, _ = V.pole(G, rng.randrange(n))
        T, name = pole_table(P, ports)
        if max(sum(1 for (Q, k) in T if k == "B1" and name[Q[0]] + name[Q[-1]] == pr) for pr in ("ab", "ac", "bc")) > 1:
            lib.append((T, name))
    return lib

def random_system(rng, lib, m, s):
    gads = []; seqs = []
    for g in range(m):
        T, name = rng.choice(lib)
        has = {"".join(sorted(name[Q[0]] + name[Q[-1]])) for (Q, k) in T}
        pair = rng.choice(sorted(has)); types = []
        for _ in range(s):
            opts = []
            for pr in (pair, pair[::-1]):
                for kd in ("B1", "B3"):
                    nxt = "".join(sorted(pr[1] + third(pr) if kd == "B1" else pr[0] + third(pr)))
                    if nxt in has: opts.append((pr, kd, nxt))
            pr, kd, pair = rng.choice(opts); types.append((pr, kd))
        start_pair = types[0][0]
        init = [Q for (Q, k) in T if k == "B1" and {name[Q[0]], name[Q[-1]]} == set(start_pair)]
        gads.append(dict(T=T, name=name, init=rng.choice(init))); seqs.append(types)
    order = [g for g in range(m) for _ in range(s)]; rng.shuffle(order)
    cnt = [0] * m; sites = []
    for g in order: sites.append((g, seqs[g][cnt[g]])); cnt[g] += 1
    return gads, sites

def run(gads, sites, cap=10**7):
    st = [g["init"] for g in gads]; i, d, visits = 0, 1, 0
    while 0 <= i < len(sites):
        g, (pr, kd) = sites[i]; G = gads[g]
        typ = (pr, kd) if d > 0 else bwd_of(pr, kd)
        Q = orient(G["name"], st[g], typ[0]); o, Qn = G["T"][(Q, typ[1])]; st[g] = Qn; visits += 1
        if o == "R": d = -d
        i += d
        if visits > cap: return None
    return visits

if __name__ == "__main__":
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1); lib = gadget_library(rng, 60)
    s = int(sys.argv[2]) if len(sys.argv) > 2 else 3; out = {}
    for m in range(1, 9):
        best = 0; t0 = time.time()
        while time.time() - t0 < 10:
            gads, sites = random_system(rng, lib, m, s)
            try: v = run(gads, sites)
            except (KeyError, StopIteration): continue
            if v and v > best: best = v
        out[m] = best; print(f"m={m} gadgets x s={s} sites (N={m*s}): longest run {best}", flush=True)
    json.dump(out, open(f"p2b3_multisite_s{s}.json", "w"))
