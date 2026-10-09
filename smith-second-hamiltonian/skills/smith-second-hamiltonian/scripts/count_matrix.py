"""E20: derive the cost recursion c_{k+1} = M c_k + b structurally.
For each visit to the pole P_{k+1} (= G_{k+1} - r), run the visit's internal walk and record each
sub-visit into the nested pole region P_k (its type B1/B3 and oriented state, named by ports of
P_k).  M[e][f] = number of sub-visits of kind f during visit e.  Checks M is level-independent."""
import sys, json
from collections import Counter
from general import from_chord, lollipop_g, cyc_edges
from nested_fast import rotate_to
from level_tables import all_cycles
import nested_fast

CH = [4, 3, 6, 1, 0, 7, 2, 5]; X, R, PERM = 5, 2, (2, 0, 1)

def next_level_tracked(K, Kc, x, G, Gc, rl, perm):
    """Same as nested_fast.next_level, also returns the label map old G -> new G (r dropped)."""
    out = nested_fast.next_level(K, Kc, x, G, [Gc], rl, perm)
    n = len(K); off = n - 1
    gl = {v: j for j, v in enumerate(v for v in range(len(G)) if v != rl)}
    return out, {v: off + gl[v] for v in gl}

def visit_walk(P, ports, Q, kind):
    """Generator of (path, z, w, s) for each step of a B1 or B3 visit walk on pole P (pole labels).
    Mirrors transducer.visit_B1/visit_B3 but on the full path representation used for tracking."""
    raise NotImplementedError

def instrumented(P, ports, Q, kind, inner):
    """Run the visit and classify sub-visits into `inner` (vertex set of the nested pole).
    Implementation: embed the pole in a minimal host (a single vertex h joined to the 3 ports
    is not simple cubic), so instead we replay the visit with the transducer routines while
    recording every intermediate path."""
    from transducer import rot
    a = Q[0]; b = Q[-1]; c = [p for p in ports if p not in (a, b)][0]
    states = []  # list of path snapshots restricted to the pole, plus endpoint
    if kind == "B1":
        R_ = list(Q[::-1]); forb = ("cut", a)
        while True:
            states.append(tuple(R_))
            z = R_[-1]; prev = R_[-2] if len(R_) > 1 else ("cut", b)
            cands = [w for w in P[z] if w != prev and w != forb]
            if z in ports and z != b: cands.append(("cut", z))
            cands = [w for w in cands if w != forb and w != prev]
            w = cands[0]
            if isinstance(w, tuple): break
            R_ = rot(R_, w); forb = w
    else:
        i = Q.index(c); X1 = list(Q[:i+1]); X2 = list(Q[i+1:][::-1]); pb = c; forb = c
        while True:
            states.append(tuple(X1) + ("|",) + tuple(X2))
            z = X2[-1]; prev = X2[-2] if len(X2) > 1 else None
            w = [u for u in P[z] if u != prev and u != forb][0]
            if w in X2: X2 = rot(X2, w)
            elif w == pb: break
            else:
                j = X1.index(w); nX1 = X1[:j+1] + X2[::-1]; nX2 = X1[j+1:][::-1]
                pb = nX1[-1]; X1, X2 = nX1, nX2
            forb = w
    # sub-visit detection: count maximal runs of states whose endpoint lies in `inner`
    runs = 0; inside = False; entries = Counter()
    for st in states:
        z = st[-1]
        if z in inner and not inside:
            runs += 1; inside = True
        elif z not in inner:
            inside = False
    return len(states), runs

K = from_chord(8, CH); Kc = list(range(8)); G, Gc = K, Kc; rl = R
inner_prev = None; results = []
for lev in range(7):
    cycles = all_cycles(G, Gc)
    keep = [v for v in range(len(G)) if v != rl]; idx = {v: j for j, v in enumerate(keep)}
    P = [[idx[w] for w in G[v] if w != rl] for v in keep]
    ports = [idx[p] for p in G[rl]]; name = {p: "abc"[k] for k, p in enumerate(ports)}
    inner = {idx[v] for v in inner_prev} if inner_prev is not None else set()
    row = {}
    for cyc in cycles:
        c = rotate_to(cyc, rl, 1); hp = [idx[v] for v in c[1:]]
        for Q in (tuple(hp), tuple(hp[::-1])):
            for kind in ("B1", "B3"):
                L_, runs = instrumented(P, ports, Q, kind, inner)
                row[f"{name[Q[0]]}{name[Q[-1]]}/{kind}"] = (L_, runs)
    print(f"level {lev}: n={len(G)} " + " ".join(f"{k}:{v[1]}" for k, v in sorted(row.items())), flush=True)
    results.append(row)
    (G, Gc), lab = next_level_tracked(K, Kc, X, G, Gc, rl, PERM)
    inner_prev = set(lab.values()); rl = R if R < X else R - 1
json.dump([{k: list(v) for k, v in r.items()} for r in results], open("e20_subvisits.json", "w"), indent=1)
