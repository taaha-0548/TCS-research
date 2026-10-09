"""P2(b2): lines of single-site cells.  A cell = (pole table, forward type); backward type by the
site rule (B1: (i,j)->(k,j); B3: (i,j)->(i,k), k = third port).  The particle starts left of cell 0
moving right; at a cell it presents the type for its direction; TRANSMIT -> next cell in the same
direction, REFLECT -> reverse.  Count cell visits until it leaves.  Search for long runs."""
import sys, random, itertools, time, json
sys.path.insert(0, ".."); sys.path.insert(0, "../../../../../paper")
import verify as V
from lollipop import random_instance
def chord_adj(n, ch): return [[(v - 1) % n, (v + 1) % n, ch[v]] for v in range(n)]
def third(p): return next(c for c in "abc" if c not in p)
def bwd_of(pr, kd): return (third(pr) + pr[1], kd) if kd == "B1" else (pr[0] + third(pr), kd)

def pole_table(P, ports):
    name = {p: "abc"[i] for i, p in enumerate(ports)}; T = {}
    for s, t in itertools.permutations(ports, 2):
        for Q in V.ham_paths(P, s, t):
            nq = tuple(name[v] if v in name else v for v in Q)
            for kd in ("B1", "B3"):
                o, Qn, cost, _ = V.visit(P, ports, Q, kd); T[(Q, kd)] = (o[0], Qn)
    return T, name

def make_library(rng, count, sizes=(8, 10, 12)):
    lib = []
    while len(lib) < count:
        n = rng.choice(sizes); G = chord_adj(n, random_instance(n, rng)); P, ports, _ = V.pole(G, rng.randrange(n))
        T, name = pole_table(P, ports)
        for pr in ("ab", "ac", "ba", "bc", "ca", "cb"):
            for kd in ("B1", "B3"):
                inv = {v: k for k, v in name.items()}
                left = [Q for (Q, k) in T if k == kd and name.get(Q[0]) == pr[0] and name.get(Q[-1]) == pr[1]]
                if len(left) >= 1:
                    lib.append(dict(T=T, name=name, fwd=(pr, kd), bwd=bwd_of(pr, kd), left=left))
    return lib

def orient(name, Q, pr):
    return Q if (name[Q[0]], name[Q[-1]]) == (pr[0], pr[1]) else Q[::-1]

def run(cells, init, cap=10**7):
    st = list(init); i, d, visits = 0, 1, 0
    while 0 <= i < len(cells):
        c = cells[i]; pr, kd = c["fwd"] if d > 0 else c["bwd"]
        Q = orient(c["name"], st[i], pr); o, Qn = c["T"][(Q, kd)]; st[i] = Qn; visits += 1
        if o == "R": d = -d
        i += d
        if visits > cap: return None
    return visits

if __name__ == "__main__":
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    lib = make_library(rng, 600); print("cell library:", len(lib))
    res = {}
    for N in range(1, 11):
        best = 0; t0 = time.time()
        cfg = None
        while time.time() - t0 < 12:
            cells = [rng.choice(lib) for _ in range(N)]; init = [rng.choice(c["left"]) for c in cells]
            v = run(cells, init)
            if v and v > best: best, cfg = v, (cells, init)
            # local improvement: mutate one cell
            for _ in range(20):
                if cfg is None: break
                cs, ins = list(cfg[0]), list(cfg[1]); j = rng.randrange(N); cs[j] = rng.choice(lib); ins[j] = rng.choice(cs[j]["left"])
                v = run(cs, ins)
                if v and v > best: best, cfg = v, (cs, ins)
        res[N] = best; print(f"N={N:2d}: longest run found = {best} visits", flush=True)
    json.dump(res, open("p2b_cells.json", "w"))
