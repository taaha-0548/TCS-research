"""Cycle 11 (mechanism for O').  T-down: a TRANSMIT visit of level j makes only TRANSMIT calls to level j+1,
recursively ('all-T').  If true, triangularity on pass-through lines is an induction: each level only ever
sees T answers, so its trajectory depends on its own state and entry symbol, and the entry symbol it sends
down depends on levels <= j.
We rebuild the tower automaton with a flag per table entry: allT = top outcome T and every sub-call allT."""
import io, contextlib, json, random
from collections import Counter, defaultdict
with contextlib.redirect_stdout(io.StringIO()):
    import cycle6 as C6
    from cycle7 import lines_from
import selfsimilar2 as S2
import verify as V
from tower import from_pole, AbstractInner
from compose import composed_visit
from lollipop import random_instance

class LoggingInner(AbstractInner):
    def __init__(self, *a):
        super().__init__(*a); self.flags = []
    def visit(self, pred, succ, kind):
        pr = (self.port_of[pred], self.port_of[succ]); key = (self.s, pr, kind)
        self.flags.append(self.A["allT"][key])
        return super().visit(pred, succ, kind)

def build(P1, ports1, x, perm, A0, depth):
    A = dict(A0); A["allT"] = {k: v[0] == "TRANSMIT" for k, v in A0["table"].items()}
    stats = []
    for _ in range(depth):
        name = {p: "abc"[i] for i, p in enumerate(ports1)}; port_of = {u: "abc"[perm[j]] for j, u in enumerate(P1[x])}
        paths = S2.paths_of(P1, ports1); states = []; pair = {}; table = {}; allT = {}
        c = Counter()
        def cpair(Q):
            j = Q.index(x); return frozenset((port_of[Q[j-1]], port_of[Q[j+1]]))
        for key, Q in paths.items():
            for cs in A["states"]:
                if A["pair"][cs] == cpair(Q): st = (key, cs); states.append(st); pair[st] = frozenset((name[Q[0]], name[Q[-1]]))
        for (key, cs) in states:
            for Q in key:
                for kd in ("B1", "B3"):
                    inner = LoggingInner(x, port_of, A, cs)
                    o, Qf, _, _ = composed_visit(P1, ports1, Q, kd, inner)
                    k = ((key, cs), (name[Q[0]], name[Q[-1]]), kd)
                    table[k] = (o, (frozenset([tuple(Qf), tuple(Qf[::-1])]), inner.s), (name[Qf[0]], name[Qf[-1]]))
                    allT[k] = (o == "TRANSMIT") and all(inner.flags)
                    if o == "TRANSMIT": c["T, all sub-calls allT" if all(inner.flags) else "T, some sub-call not allT"] += 1
                    else: c["R"] += 1
        A = dict(states=states, pair=pair, table=table, allT=allT); stats.append(dict(c))
    return A, stats

if __name__ == "__main__":
    rich = json.load(open("../phase3/p31_rich.json")); rng = random.Random(5)
    for _ in range(200):
        G0 = [[(v - 1) % 8, (v + 1) % 8, c] for v, c in enumerate(random_instance(8, rng))]
        P, ports, _ = V.pole(G0, rng.randrange(8)); A0 = from_pole(P, ports)
        if len(A0["states"]) >= 5: break
    for gi in (21, 0, 6, 15, 9):
        g = rich[gi]; P1, ports1, _ = V.pole(g["K"], g["r"])
        A, stats = build(P1, ports1, g["x"], tuple(g["perm"]), A0, 3)
        print(f"P'#{gi}: per-level visit census {stats}", flush=True)
        # pass-through lines: are all visits along the run allT?
        classes = defaultdict(list)
        for s in A["states"]: classes[A["pair"][s]].append(s)
        cnt = Counter()
        for p, S in classes.items():
            for L in range(1, 5):
                for line in lines_from(p, L):
                    for s in S:
                        (r, path) = C6.run_line(A, line, s)
                        if r is None or r[1] != "far": continue
                        cnt["bounce-free" if all(o == "T" for _, _, o in path) else "with bounces"] += 1
        print(f"        pass-through runs: {dict(cnt)}", flush=True)
