"""A1/A2: the production simulator, the independent edge-set simulator and the brute-force state
graph must agree (steps and final cycle) on random cubic graphs and on the family's first levels."""
import sys, random
sys.path.insert(0, "..")
from lollipop import random_instance
from general import from_chord, lollipop_g, is_ham, cyc_edges
from nested_fast import rotate_to, next_level
from indep import indep_walk, state_graph_partner
rng = random.Random(101); agree = tot = 0
for _ in range(300):
    n = rng.choice([8, 10, 12, 14, 16]); A = from_chord(n, random_instance(n, rng))
    C = rotate_to(list(range(n)), rng.randrange(n), rng.choice([1, -1]))
    s1, c1, _ = lollipop_g(A, C); s2, c2 = indep_walk(A, C); s3, c3 = state_graph_partner(A, C)
    tot += 1; agree += (s1 == s2 == s3 and cyc_edges(c1) == cyc_edges(c2) == cyc_edges(c3) and is_ham(A, c3))
print(f"random graphs: {agree}/{tot} agree (production = independent = brute force)")
CH = [4, 3, 6, 1, 0, 7, 2, 5]; X, R, PERM = 5, 2, (2, 0, 1)
K = from_chord(8, CH); Kc = list(range(8)); G, Gc = K, Kc; rl = R
for k in range(3):
    ok = 0; m = 0
    for s in range(len(Gc)):
        for d in (1, -1):
            C = rotate_to(Gc, Gc[s], d)
            a = lollipop_g(G, C)[0]; b = indep_walk(G, C)[0]; c = state_graph_partner(G, C)[0]
            ok += (a == b == c); m += 1
    print(f"family level {k} (n={len(G)}): {ok}/{m} starts agree")
    G, Gc = next_level(K, Kc, X, G, [Gc], rl, PERM); rl = R if R < X else R - 1
