"""Structure of the growing transparent-tower groups: abelian? nilpotent? solvable? exponent?"""
import sys, random
from collections import Counter
sys.path.insert(0, "../phase3"); sys.path.insert(0, "../phase1"); sys.path.insert(0, ".."); sys.path.insert(0, "../../../../../paper")
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import selfsimilar2 as S2
from dynamics_group import involutions
from sympy.combinatorics import PermutationGroup
rng = random.Random(11); lib = S2.lib; S = Counter(); shown = 0
for (P1, ports1, A1) in lib[:120]:
    inner = [v for v in range(len(P1)) if v not in ports1]
    if not inner: continue
    for perm in ((0, 1, 2), (1, 2, 0)):
        A0 = rng.choice(lib)[2]
        try: As = [S2.build_tower_automaton(P1, ports1, inner[0], perm, A0, d) for d in (2, 3)]
        except (KeyError, AssertionError, StopIteration): continue
        Gs = [PermutationGroup(involutions(A)[0]) for A in As]
        o = [G.order() for G in Gs]
        if o[1] <= o[0]: continue                      # only the growing ones
        G = Gs[1]
        key = ("abelian" if G.is_abelian else "nonabelian", "nilpotent" if G.is_nilpotent else "not nilpotent", "solvable" if G.is_solvable else "NOT solvable")
        S[key] += 1
        if shown < 5:
            print(f"order {o}: {key}, derived length {len(G.derived_series()) - 1}"); shown += 1
print(dict(S))
