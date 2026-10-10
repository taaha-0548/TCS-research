"""Cycle 18 (local procedure trees; hypothesis L1).
The local procedure of a gadget P' (slot x, wiring) is the tree of its visits when every passage through
x is answered T or R by an arbitrary child: P' only uses the answer (the exit port follows from it).
RForcesR(P'): in every visit's tree, after any R answer every reachable return is R.
Lean lemma L1 (Machine.lean): RForcesR(P') => in every tower built from P' (any base), a transmitting
visit makes only transmitting calls at every depth (T-down).  Prediction tested here: towers whose P'
satisfies RForcesR never violate T-down; violations need P' that fails it."""
import io, contextlib, json, random, sys, time
sys.path.insert(0, "../phase3"); sys.path.insert(0, "../phase1"); sys.path.insert(0, ".."); sys.path.insert(0, "../../../../../paper")
from collections import Counter
with contextlib.redirect_stdout(io.StringIO()):
    from selfsimilar2 import chord_adj, paths_of
    from cycle15 import level, bases
import verify as V
from compose import composed_visit
from lollipop import random_instance

class NeedAnswer(Exception): pass
class Oracle:
    def __init__(self, x, port_of, answers):
        self.x, self.port_of, self.answers, self.i, self.QX = x, port_of, answers, 0, None
        self.nb_of = {p: u for u, p in port_of.items()}; self.calls = []
    def visit(self, pred, succ, kind):
        a, b = self.port_of[pred], self.port_of[succ]
        if self.i >= len(self.answers): raise NeedAnswer((a, b, kind))
        o = self.answers[self.i]; self.i += 1; self.calls.append(((a, b, kind), o))
        c = next(p for p in "abc" if p not in (a, b))
        exitp = a if o == "REFLECT" else c
        return o, (None, exitp), 0

def tree(P1, ports1, x, port_of, Q, kd, cap=40):
    """Leaves: list of (answer sequence, outcome). Explores all answer sequences (DFS)."""
    leaves, stack, truncated = [], [()], False
    while stack:
        ans = stack.pop()
        if len(ans) > cap: truncated = True; continue
        try:
            o, *_ = composed_visit(P1, ports1, Q, kd, Oracle(x, port_of, list(ans)))
            leaves.append((ans, o))
        except NeedAnswer:
            stack.append(ans + ("TRANSMIT",)); stack.append(ans + ("REFLECT",))
        except AssertionError:
            pass                                   # answer pattern inconsistent with P' dynamics
    return leaves, truncated

def rforcesr(P1, ports1, x, perm):
    port_of = {u: "abc"[perm[j]] for j, u in enumerate(P1[x])}
    bad = tot = 0; trunc = False; maxcalls = 0
    for key, Q in paths_of(P1, ports1).items():
        for Qo in key:
            for kd in ("B1", "B3"):
                leaves, t = tree(P1, ports1, x, port_of, Qo, kd); trunc |= t
                for ans, o in leaves:
                    tot += 1; maxcalls = max(maxcalls, len(ans))
                    if "REFLECT" in ans and o == "TRANSMIT": bad += 1
    return bad, tot, trunc, maxcalls

if __name__ == "__main__":
    rich = json.load(open("../phase3/p31_rich.json"))
    for gi in (21, 0, 6, 15, 9, 3):
        g = rich[gi]; P1, ports1, _ = V.pole(g["K"], g["r"])
        print(f"rich P'#{gi}: RForcesR violations/leaves, truncated, max calls =", rforcesr(P1, ports1, g["x"], tuple(g["perm"])), flush=True)
    rng = random.Random(18); tab = Counter(); t0 = time.time()
    while time.time() - t0 < 200:
        n = rng.choice([8, 10, 12]); K = chord_adj(n, random_instance(n, rng))
        try: P1, ports1, _ = V.pole(K, rng.randrange(n))
        except Exception: continue
        xs = [v for v in range(len(P1)) if P1[v] and v not in ports1]
        if not xs: continue
        x = rng.choice(xs); perm = list(range(3)); rng.shuffle(perm)
        try: bad, tot, trunc, mc = rforcesr(P1, ports1, x, perm)
        except Exception: continue
        if tot == 0: continue
        local = "RForcesR" if bad == 0 else "fails RForcesR"
        viol = False
        for A in rng.sample(bases, 4):                       # several bases, levels 1..3
            try:
                for lev in range(3):
                    A, c = level(P1, ports1, x, perm, A)
                    if not A["states"] or len(A["states"]) > 1500: break
                    viol |= (c[">=2 R-calls"] + c["T after R"]) > 0
            except Exception: pass
        tab[(local, "T-down violated somewhere" if viol else "T-down holds")] += 1
    print("random gadgets (local property, observed T-down over 4 bases x 3 levels):")
    for k, v in sorted(tab.items()): print("  ", k, v)
