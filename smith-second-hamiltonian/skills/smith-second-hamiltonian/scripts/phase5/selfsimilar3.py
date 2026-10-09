"""H4 probe: dynamics group (site involutions) of homogeneous TRANSPARENT towers, order by depth.
Finite & stabilising => the automaton group is finite (predictable); growing => infinite group."""
import sys, random, itertools
from collections import Counter
sys.path.insert(0, "../phase3"); sys.path.insert(0, "../phase1"); sys.path.insert(0, ".."); sys.path.insert(0, "../../../../../paper")
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import selfsimilar2 as S2
from dynamics_group import involutions
from sympy.combinatorics import PermutationGroup
rng = random.Random(11); lib = S2.lib; trend = Counter(); shown = 0
for (P1, ports1, A1) in lib[:120]:
    inner = [v for v in range(len(P1)) if v not in ports1]
    if not inner: continue
    for perm in ((0, 1, 2), (1, 2, 0)):
        A0 = rng.choice(lib)[2]
        try: As = [S2.build_tower_automaton(P1, ports1, inner[0], perm, A0, d) for d in (1, 2, 3, 4)]
        except (KeyError, AssertionError, StopIteration): continue
        orders = []
        for A in As:
            if len(A["states"]) > 400: orders.append("big"); continue
            gens, n, bad = involutions(A); orders.append(PermutationGroup(gens).order())
        ints = [o for o in orders if isinstance(o, int)]
        key = "stabilises (finite group)" if len(ints) >= 3 and ints[-1] == ints[-2] else ("grows" if len(ints) >= 2 and ints[-1] > ints[-2] else "?")
        trend[key] += 1
        if shown < 10: print(f"P' n={len(P1)} perm={perm}: states {[len(A['states']) for A in As]}, |G| by depth {orders}"); shown += 1
print(dict(trend))
