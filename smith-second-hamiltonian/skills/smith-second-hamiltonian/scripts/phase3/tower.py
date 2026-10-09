"""P3.2: abstract towers.  A_j = Phi(A_{j+1}) for a fixed gadget P' with slot x.
Automaton representation: states have an unordered port pair; table[(s, (u,v), kind)] =
(outcome, s', (u',v')) where (u,v) is the oriented pair of ports (names a,b,c) presented and
(u',v') the oriented pair the state uses afterwards (start, end).  Minimise by Nerode refinement and
track the size of the minimal machine with depth."""
import sys, itertools, json, random
from collections import defaultdict
sys.path.insert(0, "../phase1"); sys.path.insert(0, ".."); sys.path.insert(0, "../../../../../paper")
import verify as V
from compose import composed_visit
from lollipop import random_instance
def chord_adj(n, ch): return [[(v - 1) % n, (v + 1) % n, ch[v]] for v in range(n)]

def from_pole(P, ports):
    name = {p: "abc"[i] for i, p in enumerate(ports)}; ids = {}; pair = {}; table = {}
    for s, t in itertools.permutations(ports, 2):
        for Q in V.ham_paths(P, s, t):
            key = frozenset([Q, Q[::-1]])
            if key not in ids: ids[key] = len(ids); pair[ids[key]] = frozenset((name[s], name[t]))
    for key, i in ids.items():
        for Q in key:
            for kd in ("B1", "B3"):
                o, Qn, cost, _ = V.visit(P, ports, Q, kd)
                j = ids[frozenset([tuple(Qn), tuple(Qn[::-1])])]
                table[(i, (name[Q[0]], name[Q[-1]]), kd)] = (o, j, (name[Qn[0]], name[Qn[-1]]))
    return dict(states=list(ids.values()), pair=pair, table=table)

class AbstractInner:
    def __init__(self, x, port_of, A, s):
        self.x, self.port_of, self.A, self.s = x, port_of, A, s
        self.nb_of = {p: u for u, p in port_of.items()}; self.QX = s
    def visit(self, pred, succ, kind):
        pr = (self.port_of[pred], self.port_of[succ])
        o, s2, pr2 = self.A["table"][(self.s, pr, kind)]
        self.s = s2; self.QX = s2
        return o, pr2, 0

def compose(P1, ports1, x, perm, A):
    name = {p: "abc"[i] for i, p in enumerate(ports1)}
    port_of = {u: "abc"[perm[j]] for j, u in enumerate(P1[x])}
    paths = {}
    for s, t in itertools.permutations(ports1, 2):
        for Q in V.ham_paths(P1, s, t): paths[frozenset([Q, Q[::-1]])] = Q
    ids = {}; pair = {}; table = {}
    def child_pair(Q):
        j = Q.index(x); return frozenset((port_of[Q[j-1]], port_of[Q[j+1]]))
    for key, Q in paths.items():
        for cs in A["states"]:
            if A["pair"][cs] == child_pair(Q):
                ids[(key, cs)] = len(ids); pair[ids[(key, cs)]] = frozenset((name[Q[0]], name[Q[-1]]))
    for (key, cs), i in ids.items():
        for Q in key:
            for kd in ("B1", "B3"):
                inner = AbstractInner(x, port_of, A, cs)
                o, Qf, cost, _ = composed_visit(P1, ports1, Q, kd, inner)
                j = ids[(frozenset([tuple(Qf), tuple(Qf[::-1])]), inner.s)]
                table[(i, (name[Q[0]], name[Q[-1]]), kd)] = (o, j, (name[Qf[0]], name[Qf[-1]]))
    return dict(states=list(ids.values()), pair=pair, table=table)

def minimise(A):
    inputs = defaultdict(list)
    for (s, pr, kd) in A["table"]: inputs[s].append((pr, kd))
    cls = {s: (A["pair"][s], tuple(sorted((i, A["table"][(s,) + i][0], A["table"][(s,) + i][2]) for i in inputs[s]))) for s in A["states"]}
    ids = {v: k for k, v in enumerate(dict.fromkeys(cls.values()))}; cls = {s: ids[cls[s]] for s in A["states"]}
    while True:
        new = {s: (cls[s], tuple(sorted((i, cls[A["table"][(s,) + i][1]]) for i in inputs[s]))) for s in A["states"]}
        ids = {v: k for k, v in enumerate(dict.fromkeys(new.values()))}; new = {s: ids[new[s]] for s in A["states"]}
        if len(set(new.values())) == len(set(cls.values())): return len(set(new.values())), new
        cls = new

def quotient(A, cls):
    """Replace A by its minimal machine (states = classes)."""
    rep = {}
    for s in A["states"]: rep.setdefault(cls[s], s)
    table = {}
    for (s, pr, kd), (o, s2, pr2) in A["table"].items():
        if rep[cls[s]] == s: table[(cls[s], pr, kd)] = (o, cls[s2], pr2)
    return dict(states=sorted(rep), pair={c: A["pair"][rep[c]] for c in rep}, table=table)

if __name__ == "__main__":
    rich = json.load(open("p31_rich.json"))
    rng = random.Random(5)
    base_pole = None
    # innermost automaton: a small memory pole
    for _ in range(200):
        n = 8; G = chord_adj(n, random_instance(n, rng)); P, ports, _ = V.pole(G, rng.randrange(n)); A0 = from_pole(P, ports)
        if len(A0["states"]) >= 5: break
    print("innermost automaton states:", len(A0["states"]), " minimal:", minimise(A0)[0])
    for g in rich[:12]:
        P1, ports1, _ = V.pole(g["K"], g["r"]); x, perm = g["x"], g["perm"]
        A = A0; sizes = []
        try:
            for depth in range(1, 7):
                A = compose(P1, ports1, x, perm, A); m, cls = minimise(A); sizes.append((len(A["states"]), m)); A = quotient(A, cls)
        except (KeyError, AssertionError) as e:
            sizes.append(("err", type(e).__name__))
        print(f"P' n={g['n']} memory={g['memory']}: (states, minimal) by depth = {sizes}")
