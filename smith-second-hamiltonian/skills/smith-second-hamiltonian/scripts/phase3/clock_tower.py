"""P3.3: clock x tower.  The tower automaton (depth d, fixed P') is substituted at vertex u = 0 of a
depth-D copy inside the clock host G_k (u's three neighbours 1, 4, 7 lie in its own copy).  The
lollipop walk is then the line-mirror system on u's site sequence (morphic word), with the tower
automaton.  We record reflections, run length, and how many distinct tower states occur."""
import sys, json, random, itertools
sys.path.insert(0, "../phase2"); sys.path.insert(0, "../phase1"); sys.path.insert(0, ".."); sys.path.insert(0, "../../../../../paper")
import verify as V
import clock as C
from clock_check import pattern_full
from tower import compose, minimise, quotient, from_pole
from lollipop import random_instance
def chord_adj(n, ch): return [[(v - 1) % n, (v + 1) % n, ch[v]] for v in range(n)]
def third(p): return next(c for c in "abc" if c not in p)
def bwd_of(pr, kd): return (third(pr) + pr[1], kd) if kd == "B1" else (pr[0] + third(pr), kd)

def site_word(k, D, u=0):
    word = list(C.K_walk_passages())
    for _ in range(D - 1): word = [g for f in word for g in C.sigma(f)]
    return [site for f in word for site in pattern_full(f, u, k - D == 0)]

def run(sites, A, s0, wiring):
    st = s0; i, d, refl, visits, seen = 0, 1, 0, 0, {s0}
    while 0 <= i < len(sites):
        kd, p, q = sites[i]
        pr = (wiring[p], wiring[q]); typ = (pr, kd) if d > 0 else bwd_of(pr, kd)
        o, st, _ = A["table"][(st, typ[0], typ[1])]; seen.add(st); visits += 1
        if o == "REFLECT": d = -d; refl += 1
        i += d
    return ("far" if i >= len(sites) else "start"), visits, refl, len(seen)

if __name__ == "__main__":
    rich = json.load(open("p31_rich.json")); rng = random.Random(5)
    for _ in range(200):
        G = chord_adj(8, random_instance(8, rng)); P, ports, _ = V.pole(G, rng.randrange(8)); A0 = from_pole(P, ports)
        if len(A0["states"]) >= 5: break
    for gi in (0, 6, 9, 4, 11):
        g = rich[gi]; P1, ports1, _ = V.pole(g["K"], g["r"])
        A = A0
        for depth in range(3): A = compose(P1, ports1, g["x"], g["perm"], A); m, cls = minimise(A); A = quotient(A, cls)
        for (k, D) in ((5, 3), (7, 5)):
            sites = site_word(k, D)
            best = None
            for perm in itertools.permutations("abc"):
                wiring = dict(zip((1, 4, 7), perm))
                p0 = frozenset((wiring[sites[0][1]], wiring[sites[0][2]]))
                for s0 in [s for s in A["states"] if A["pair"][s] == p0][:6]:
                    try: r = run(sites, A, s0, wiring)
                    except KeyError: continue
                    if best is None or r[2] > best[2]: best = r
            print(f"tower P'#{gi} (min size {len(A['states'])}), clock sites {len(sites)}: end/visits/reflections/states-seen = {best}")
