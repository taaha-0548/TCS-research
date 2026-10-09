"""Site Normal Form test.  For a pole automaton and a site (forward type e_f, backward e_b by the site
rule): left states L (pair of e_f), right states R (pair of e_b).
 (1) forward TRANSMIT q -> q' in R  and  backward visit at q' TRANSMITs back to q          (Retrace)
 (2) forward REFLECT q -> q'' in L, q'' != q, and forward visit at q'' REFLECTs back to q  (involution)
 (3) same as (1)/(2) from the right with e_b."""
import sys, random, itertools
from collections import Counter
sys.path.insert(0, "../phase3"); sys.path.insert(0, ".."); sys.path.insert(0, "../../../../../paper")
import verify as V
from lollipop import random_instance
from tower import from_pole
def chord_adj(n, ch): return [[(v - 1) % n, (v + 1) % n, ch[v]] for v in range(n)]
def third(p): return next(c for c in "abc" if c not in p)
def bwd_of(pr, kd): return ((third(pr), pr[1]), kd) if kd == "B1" else ((pr[0], third(pr)), kd)

rng = random.Random(2); S = Counter()
for _ in range(4000):
    n = rng.choice([6, 8, 10, 12]); A = from_pole(*V.pole(chord_adj(n, random_instance(n, rng)), rng.randrange(n))[:2])
    for pr in itertools.permutations("abc", 2):
        for kd in ("B1", "B3"):
            ef = (pr, kd); eb = bwd_of(pr, kd)
            Lset = [s for s in A["states"] if A["pair"][s] == frozenset(pr)]
            for q in Lset:
                o, q2, pr2 = A["table"][(q, pr, kd)]
                if o == "TRANSMIT":
                    if A["pair"][q2] != frozenset(eb[0]): S["(1) transmit lands off the right pair"] += 1; continue
                    o2, q3, _ = A["table"][(q2, eb[0], eb[1])]
                    S["(1) retrace " + ("ok" if (o2 == "TRANSMIT" and q3 == q) else "FAIL")] += 1
                else:
                    if A["pair"][q2] != frozenset(pr): S["(2) reflect lands off the left pair"] += 1; continue
                    o2, q3, _ = A["table"][(q2, pr, kd)]
                    S["(2) involution " + ("ok" if (o2 == "REFLECT" and q3 == q and q2 != q) else "FAIL")] += 1
            Rset = [s for s in A["states"] if A["pair"][s] == frozenset(eb[0])]
            for q in Rset:
                o, q2, _ = A["table"][(q, eb[0], eb[1])]
                if o == "TRANSMIT":
                    o2, q3, _ = A["table"][(q2, pr, kd)]
                    S["(3) retrace from right " + ("ok" if (o2 == "TRANSMIT" and q3 == q) else "FAIL")] += 1
                else:
                    o2, q3, _ = A["table"][(q2, eb[0], eb[1])]
                    S["(3) involution from right " + ("ok" if (o2 == "REFLECT" and q3 == q and q2 != q) else "FAIL")] += 1
for k, v in sorted(S.items()): print(k, v)
