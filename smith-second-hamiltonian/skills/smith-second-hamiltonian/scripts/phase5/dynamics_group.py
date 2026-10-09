"""H1 vs H2 discriminator: the dynamics group of a gadget automaton.
For each site type e = (oriented pair, kind) with backward type e_b (site rule), sigma_e acts on the
union of the left pair class and the right pair class: left state -> forward visit result, right state ->
backward visit result.  By the Site Normal Form sigma_e is an involution.  G = <sigma_e>.
Report |G|, orbits, and whether G restricted to each orbit is the full alternating/symmetric group."""
import sys, json, random, math, itertools
from collections import defaultdict
sys.path.insert(0, "../phase3"); sys.path.insert(0, "../phase1"); sys.path.insert(0, ".."); sys.path.insert(0, "../../../../../paper")
import io, contextlib
import verify as V
from tower import compose, minimise, quotient, from_pole
from lollipop import random_instance
from sympy.combinatorics import Permutation, PermutationGroup
def chord_adj(n, ch): return [[(v - 1) % n, (v + 1) % n, ch[v]] for v in range(n)]
def third(p): return next(c for c in "abc" if c not in p)
def bwd(pr, kd): return ((third(pr), pr[1]), kd) if kd == "B1" else ((pr[0], third(pr)), kd)

def involutions(A):
    idx = {s: i for i, s in enumerate(A["states"])}; n = len(idx); gens = []; bad = 0
    for pr in itertools.permutations("abc", 2):
        for kd in ("B1", "B3"):
            eb = bwd(pr, kd); img = list(range(n))
            for s in A["states"]:
                if A["pair"][s] == frozenset(pr) and (s, pr, kd) in A["table"]:
                    img[idx[s]] = idx[A["table"][(s, pr, kd)][1]]
                elif A["pair"][s] == frozenset(eb[0]) and (s, eb[0], eb[1]) in A["table"]:
                    img[idx[s]] = idx[A["table"][(s, eb[0], eb[1])][1]]
            p = Permutation(img)
            if (p * p) != Permutation(list(range(n))): bad += 1
            gens.append(p)
    return gens, n, bad

def analyse(A):
    gens, n, bad = involutions(A)
    G = PermutationGroup(gens); orbs = G.orbits(); out = []
    for o in sorted(orbs, key=len, reverse=True)[:3]:
        o = sorted(o)
        if len(o) == 1: out.append("1"); continue
        # restrict to the orbit
        pos = {v: i for i, v in enumerate(o)}
        H = PermutationGroup([Permutation([pos[g(v)] for v in o]) for g in gens]); k = len(o)
        if k <= 8:
            order = H.order(); tag = "Sym" if order == math.factorial(k) else ("Alt" if 2 * order == math.factorial(k) else f"order {order}")
        else:
            prim = H.is_primitive()
            tag = ("Alt/Sym" if (prim and H.is_alt_sym(eps=0.001)) else ("primitive, not Alt/Sym" if prim else "imprimitive"))
        out.append(f"{k}:{tag}")
    return dict(states=n, involution_failures=bad, orbits=len(orbs), top_orbits=out)

if __name__ == "__main__":
    rich = json.load(open("../phase3/p31_rich.json")); rng = random.Random(5)
    for _ in range(200):
        G0 = chord_adj(8, random_instance(8, rng)); P, ports, _ = V.pole(G0, rng.randrange(8)); A0 = from_pole(P, ports)
        if len(A0["states"]) >= 5: break
    print("innermost gadget:", analyse(A0))
    for gi in (0, 6, 3, 9, 21, 4):
        g = rich[gi]; P1, ports1, _ = V.pole(g["K"], g["r"]); A = A0; rows = []
        for depth in (1, 2, 3):
            A = compose(P1, ports1, g["x"], g["perm"], A); m, cls = minimise(A); A = quotient(A, cls)
            if len(A["states"]) > 1500: rows.append((depth, len(A["states"]), "too big")); break
            rows.append((depth, analyse(A)))
        print(f"P'#{gi}:")
        for r in rows: print("    depth", r)
