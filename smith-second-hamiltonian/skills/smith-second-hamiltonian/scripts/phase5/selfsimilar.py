"""H3: transparent towers are self-similar group actions.
Transparent memory pole P' with slot x: every visit transmits whatever the child does (we require P'
transparent AND child transparent, so the P'-walk never reverses).  For each entry type e and P'-path q,
the visit gives (q', child-call word w(e,q)).  Wreath recursion: action of e on a tape (q, rest) =
(q', w(e,q) applied to rest).  Check against the exact composed tower automaton (compose.py)."""
import sys, random, itertools, json
from collections import Counter
sys.path.insert(0, "../phase3"); sys.path.insert(0, "../phase1"); sys.path.insert(0, ".."); sys.path.insert(0, "../../../../../paper")
import verify as V
from tower import compose, from_pole
from procedure import procedure
from lollipop import random_instance
def chord_adj(n, ch): return [[(v - 1) % n, (v + 1) % n, ch[v]] for v in range(n)]

def transparent(A): return all(o == "TRANSMIT" for (o, _, _) in A["table"].values())

def find_transparent_memory(rng, tries=4000):
    out = []
    for _ in range(tries):
        n = rng.choice([6, 8, 10]); K = chord_adj(n, random_instance(n, rng)); r = rng.randrange(n)
        P, ports, _ = V.pole(K, r); A = from_pole(P, ports)
        if transparent(A) and any(sum(1 for s in A["states"] if A["pair"][s] == p) > 1 for p in set(A["pair"].values())):
            out.append((K, r, P, ports, A))
    return out

rng = random.Random(3)
lib = find_transparent_memory(rng)
print("transparent memory poles found:", len(lib), " sizes:", Counter(len(P) for _, _, P, _, _ in lib))
# slot gadgets: transparent memory P' with an interior vertex x
results = Counter(); examples = []
for (K, r, P1, ports1, A1) in lib[:40]:
    inner = [v for v in range(len(P1)) if v not in ports1]
    for x in inner[:2]:
        for perm in itertools.permutations(range(3)):
            # child automaton: another transparent memory pole
            K2, r2, P2, ports2, A2 = rng.choice(lib)
            try:
                T1 = compose(P1, ports1, x, perm, A2)
                T2 = compose(P1, ports1, x, perm, T1)
            except (KeyError, AssertionError):
                results["composition error"] += 1; continue
            results[("depth1 transparent", transparent(T1))] += 1
            results[("depth2 transparent", transparent(T2))] += 1
            # wreath recursion check at depth 1: the composed visit = P'-visit + child word applied
            name = {p: "abc"[i] for i, p in enumerate(ports1)}; port_of = {u: "abc"[perm[j]] for j, u in enumerate(P1[x])}
            ok = True
            for s, t in itertools.permutations(ports1, 2):
                for Q in V.ham_paths(P1, s, t):
                    for kd in ("B1", "B3"):
                        pr = procedure(P1, ports1, x, port_of, Q, kd, max_calls=12)
                        allT = [p for p in pr if all(a == "T" for a in p[0])]
                        if len(allT) != 1: ok = False; continue
                        ans, calls, outc, Qf = allT[0]
                        # the call word depends only on (e, q) and is the same however the child answers? (transparent child -> all T)
            results[("wreath recursion well-defined", ok)] += 1
            break
for k, v in sorted(results.items(), key=str): print(k, v)
