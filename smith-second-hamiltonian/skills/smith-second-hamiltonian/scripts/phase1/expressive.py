"""P1.2: expressiveness of 3-pole automata.
A pole is a Mealy machine: states = Hamiltonian paths of X between two ports (unoriented);
inputs = visit types (oriented port pair, kind B1/B3), enabled in states using that pair;
output = TRANSMIT/REFLECT; next state = successor path.
 * Nerode classes: states equivalent iff every enabled input sequence gives the same outputs.
 * interacting memory: some input e1 moves a state s to s1, and then the outcome of some input e2
   applied at s1 differs from its outcome at the state s2 reached from s by another input e1'
   that leads to the same port pair -- i.e. which way you passed earlier changes a later answer.
 * toggle: some input e has outcome R at state s and T at state s' (same pair), and s, s' are
   reachable from each other.  Interacting memory with toggles is what reversible motion-planning
   hardness needs (memory that one traversal writes and another reads)."""
import sys, random, itertools, json, time
from collections import Counter, defaultdict
sys.path.insert(0, ".."); sys.path.insert(0, "../../../../../paper")
import verify as V
from lollipop import random_instance

def chord_adj(n, ch): return [[(v - 1) % n, (v + 1) % n, ch[v]] for v in range(n)]

def machine(P, ports):
    name = {p: "abc"[i] for i, p in enumerate(ports)}
    states = []
    for s, t in itertools.combinations(ports, 2): states += [frozenset([Q, Q[::-1]]) for Q in V.ham_paths(P, s, t)]
    states = list(dict.fromkeys(states))
    canon = {}
    for st in states:
        for Q in st: canon[Q] = st
    delta = {}
    for st in states:
        for Q in st:
            for kd in ("B1", "B3"):
                o, Qn, cost, _ = V.visit(P, ports, Q, kd)
                delta[(st, name[Q[0]] + name[Q[-1]], kd)] = (o[0], canon[tuple(Qn)])
    return states, delta, name

def nerode(states, delta):
    inputs = defaultdict(list)
    for (st, pr, kd) in delta: inputs[st].append((pr, kd))
    # initial partition: by port pair and by output vector on enabled inputs
    def pair(st): return frozenset(next(iter(st))[i] for i in (0, -1))
    cls = {st: (pair(st), tuple(sorted((i, delta[(st,) + i][0]) for i in inputs[st]))) for st in states}
    while True:
        new = {st: (cls[st], tuple(sorted((i, cls[delta[(st,) + i][1]]) for i in inputs[st]))) for st in states}
        ids = {v: k for k, v in enumerate(dict.fromkeys(new.values()))}; new = {st: ids[new[st]] for st in states}
        if len(set(new.values())) == len(set(cls.values())): return new
        cls = new

def analyse(P, ports):
    states, delta, name = machine(P, ports)
    cls = nerode(states, delta)
    by_pair = defaultdict(set)
    for st in states: by_pair[frozenset(next(iter(st))[i] for i in (0, -1))].add(cls[st])
    memory = max(len(v) for v in by_pair.values())
    # toggle: same input, two states of the same pair (different classes), different outputs,
    # and one reachable from the other through the machine
    succ = defaultdict(set)
    for (st, pr, kd), (o, nx) in delta.items(): succ[st].add(nx)
    def reach(a):
        seen = {a}; stack = [a]
        while stack:
            u = stack.pop()
            for v in succ[u]:
                if v not in seen: seen.add(v); stack.append(v)
        return seen
    R = {st: reach(st) for st in states}
    toggle = False; interacting = False
    for (s1, pr, kd), (o1, _) in delta.items():
        for s2 in states:
            if s2 is s1 or (s2, pr, kd) not in delta: continue
            o2 = delta[(s2, pr, kd)][0]
            if o1 != o2 and cls[s1] != cls[s2]:
                if s2 in R[s1] and s1 in R[s2]: toggle = True
                # interacting: s2 reached from s1 by inputs of a DIFFERENT type than (pr, kd)
                for (t, pr2, kd2), (o, nx) in delta.items():
                    if t is s1 and (pr2, kd2) != (pr, kd) and nx is s2: interacting = True
    return dict(states=len(states), classes=len(set(cls.values())), memory=memory, toggle=toggle, interacting=interacting)

if __name__ == "__main__":
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1); budget = float(sys.argv[2]) if len(sys.argv) > 2 else 120
    t0 = time.time(); S = Counter(); smallest = {}
    while time.time() - t0 < budget:
        n = rng.choice([6, 8, 10, 12, 14]); G = chord_adj(n, random_instance(n, rng))
        P, ports, _ = V.pole(G, rng.randrange(n))
        a = analyse(P, ports)
        key = ("memory>1" if a["memory"] > 1 else "no outcome memory", "toggle" if a["toggle"] else "-", "interacting" if a["interacting"] else "-")
        S[(n - 1,) + key] += 1
        if a["interacting"] and a["toggle"] and (n - 1) not in smallest: smallest[n - 1] = dict(G=G, a=a)
    for k, v in sorted(S.items()): print(k, v)
    print("smallest poles with interacting toggle memory:", {k: v["a"] for k, v in sorted(smallest.items())})
    json.dump({str(k): v for k, v in smallest.items()}, open("p12_examples.json", "w"))
