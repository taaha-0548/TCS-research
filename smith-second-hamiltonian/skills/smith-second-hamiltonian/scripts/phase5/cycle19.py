"""Cycle 19 (hypothesis L1'): RForcesR over branches realizable by a reversible child.
Free reversible child: symbolic states; an answer is forced when the Site Normal Form axioms determine it
  (1) Retrace: (q, e) -T-> q'   =>  (q', bwd e) -T-> q
  (2) Involution: (q, e) -R-> q'' (q'' != q)  =>  (q'', e) -R-> q
otherwise it branches (new states are fresh).  Branches that make more than CAP calls with no free choice
left are forced infinite loops (unrealizable by a finite reversible system) and are pruned.
L1': in every realizable branch, an R answer forces an R return."""
import sys, json, random, time, io, contextlib
sys.path.insert(0, "../phase3"); sys.path.insert(0, "../phase1"); sys.path.insert(0, ".."); sys.path.insert(0, "../../../../../paper")
from collections import Counter
with contextlib.redirect_stdout(io.StringIO()):
    from selfsimilar2 import chord_adj, paths_of
    from cycle15 import level, bases
import verify as V
from compose import composed_visit
from lollipop import random_instance
def third(p): return next(c for c in "abc" if c not in p)
def bwd(t):
    a, b, kd = t
    return (third((a, b)), b, kd) if kd == "B1" else (a, third((a, b)), kd)

class NeedAnswer(Exception): pass
class TooLong(Exception): pass
class RevOracle:
    def __init__(self, x, port_of, free, cap):
        self.x, self.port_of, self.free, self.cap = x, port_of, free, cap
        self.nb_of = {p: u for u, p in port_of.items()}
        self.know = {}; self.q = 0; self.nstates = 1; self.fi = 0; self.calls = []; self.QX = None
    def visit(self, pred, succ, kind):
        t = (self.port_of[pred], self.port_of[succ], kind)
        if len(self.calls) >= self.cap: raise TooLong()
        if (self.q, t) in self.know:
            o, q2 = self.know[(self.q, t)]; forced = True
        else:
            if self.fi >= len(self.free): raise NeedAnswer()
            o = self.free[self.fi]; self.fi += 1; forced = False
            q2 = self.nstates; self.nstates += 1
            self.know[(self.q, t)] = (o, q2)
            if o == "TRANSMIT": self.know.setdefault((q2, bwd(t)), ("TRANSMIT", self.q))
            else: self.know.setdefault((q2, t), ("REFLECT", self.q))
        self.calls.append((t, o, forced)); self.q = q2
        exitp = t[0] if o == "REFLECT" else third(t[:2])
        return o, (None, exitp), 0

def tree(P1, ports1, x, port_of, Q, kd, cap=30, maxfree=14):
    leaves, pruned, stack = [], 0, [()]
    while stack:
        free = stack.pop()
        if len(free) > maxfree: pruned += 1; continue
        orc = RevOracle(x, port_of, list(free), cap)
        try:
            o, *_ = composed_visit(P1, ports1, Q, kd, orc); leaves.append((orc.calls, o))
        except NeedAnswer:
            stack.append(free + ("TRANSMIT",)); stack.append(free + ("REFLECT",))
        except TooLong: pruned += 1
        except AssertionError: pruned += 1
    return leaves, pruned

def check(P1, ports1, x, perm):
    port_of = {u: "abc"[perm[j]] for j, u in enumerate(P1[x])}
    bad = tot = pr = 0; ex = None
    for key, Q in paths_of(P1, ports1).items():
        for Qo in key:
            for kd in ("B1", "B3"):
                leaves, p = tree(P1, ports1, x, port_of, Qo, kd); pr += p
                for calls, o in leaves:
                    tot += 1
                    if any(c[1] == "REFLECT" for c in calls) and o == "TRANSMIT":
                        bad += 1; ex = ex or [(''.join(c[0][:2]) + '/' + c[0][2], c[1][0], 'f' if c[2] else '') for c in calls]
    return bad, tot, pr, ex

if __name__ == "__main__":
    rich = json.load(open("../phase3/p31_rich.json"))
    for gi in (21, 0, 6, 15, 9, 3):
        g = rich[gi]; P1, ports1, _ = V.pole(g["K"], g["r"])
        b, t, p, ex = check(P1, ports1, g["x"], tuple(g["perm"]))
        print(f"rich P'#{gi}: L1' violations {b}/{t} realizable leaves (pruned {p})" + (f"  e.g. {ex}" if ex else ""), flush=True)
    rng = random.Random(19); tab = Counter(); t0 = time.time()
    while time.time() - t0 < 150:
        n = rng.choice([8, 10, 12]); K = chord_adj(n, random_instance(n, rng))
        try: P1, ports1, _ = V.pole(K, rng.randrange(n))
        except Exception: continue
        xs = [v for v in range(len(P1)) if P1[v] and v not in ports1]
        if not xs: continue
        x = rng.choice(xs); perm = list(range(3)); rng.shuffle(perm)
        try: b, t, p, _ = check(P1, ports1, x, perm)
        except Exception: continue
        if t == 0: continue
        viol = False
        for A in rng.sample(bases, 4):
            try:
                for lev in range(3):
                    A, c = level(P1, ports1, x, perm, A)
                    if not A["states"] or len(A["states"]) > 1500: break
                    viol |= (c[">=2 R-calls"] + c["T after R"]) > 0
            except Exception: pass
        tab[("L1' holds" if b == 0 else "L1' fails", "T-down violated" if viol else "T-down holds")] += 1
    print("random gadgets: (local L1', observed T-down over 4 bases x 3 levels)")
    for k, v in sorted(tab.items()): print("  ", k, v)
