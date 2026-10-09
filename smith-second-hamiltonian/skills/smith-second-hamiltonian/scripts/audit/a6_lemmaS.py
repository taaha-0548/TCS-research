"""A6: Lemma S at larger sizes: every simple random pole (h_ij = 1 for all pairs) never reflects."""
import sys, random, itertools, time
from collections import Counter
sys.path.insert(0, "..")
from lollipop import random_instance
from general import from_chord
from transducer import transducer, ham_paths_between
from a5_lemmaC_general import pole
rng = random.Random(77); t0 = time.time(); S = Counter()
while time.time() - t0 < 200:
    n = rng.choice([10, 12, 14, 16, 18, 20, 22]); G = from_chord(n, random_instance(n, rng))
    P, ports = pole(G, rng.randrange(n))
    h = [len(ham_paths_between(P, ports[a], ports[b])) for a, b in itertools.combinations(range(3), 2)]
    if h != [1, 1, 1]: S["not simple"] += 1; continue
    T = transducer(P, ports)
    refl = any(v[k][0] == "REFLECT" for v in T.values() for k in v)
    S[("simple", n - 1, "REFLECTS" if refl else "transparent")] += 1
for k, v in sorted(S.items(), key=str): print(k, v)
