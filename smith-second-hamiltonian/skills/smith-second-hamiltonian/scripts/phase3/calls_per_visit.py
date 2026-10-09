"""P3.4: calls per visit.  For towers of fixed P', count the calls a single visit at the top makes to
its child (and the total recursion size), over all top states and visit types, as depth grows.
If calls-per-visit stays bounded, the tower can only simulate machines whose head enters shallow cells
rarely; if it grows, the parent can shuttle against its child (Shannon-style)."""
import sys, json, random
from collections import Counter
sys.path.insert(0, "../phase1"); sys.path.insert(0, "../phase2"); sys.path.insert(0, ".."); sys.path.insert(0, "../../../../../paper")
import verify as V
from compose import composed_visit
from tower import compose, from_pole, AbstractInner
from lollipop import random_instance
import itertools
def chord_adj(n, ch): return [[(v - 1) % n, (v + 1) % n, ch[v]] for v in range(n)]

class Counting(AbstractInner):
    def __init__(self, *a, **k): super().__init__(*a, **k); self.calls = 0
    def visit(self, pred, succ, kind): self.calls += 1; return super().visit(pred, succ, kind)

def top_calls(P1, ports1, x, perm, A):
    name = {p: "abc"[i] for i, p in enumerate(ports1)}; port_of = {u: "abc"[perm[j]] for j, u in enumerate(P1[x])}
    worst = 0; hist = Counter()
    for s, t in itertools.permutations(ports1, 2):
        for Q in V.ham_paths(P1, s, t):
            j = Q.index(x); cp = frozenset((port_of[Q[j-1]], port_of[Q[j+1]]))
            for cs in [c for c in A["states"] if A["pair"][c] == cp]:
                for kd in ("B1", "B3"):
                    inner = Counting(x, port_of, A, cs)
                    try: composed_visit(P1, ports1, Q, kd, inner)
                    except (KeyError, AssertionError): continue
                    worst = max(worst, inner.calls); hist[inner.calls] += 1
    return worst, hist

if __name__ == "__main__":
    rich = json.load(open("p31_rich.json")); rng = random.Random(5)
    for _ in range(200):
        G = chord_adj(8, random_instance(8, rng)); P, ports, _ = V.pole(G, rng.randrange(8)); A0 = from_pole(P, ports)
        if len(A0["states"]) >= 5: break
    for gi in range(0, 30, 3):
        g = rich[gi]; P1, ports1, _ = V.pole(g["K"], g["r"]); A = A0; row = []
        try:
            for depth in range(5):
                w, h = top_calls(P1, ports1, g["x"], g["perm"], A); row.append(w)
                A = compose(P1, ports1, g["x"], g["perm"], A)
        except Exception as e: row.append(type(e).__name__)
        print(f"P'#{gi} (n={g['n']}, mem={g['memory']}): max calls per top visit by child depth 0..4 = {row}")
