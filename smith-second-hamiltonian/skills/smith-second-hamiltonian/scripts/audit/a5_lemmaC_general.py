"""A5: Lemma C in general.  P' = K' - r' (random), x in P' with N(x) inside P' (x not adjacent to r'),
X = random pole (cubic graph minus a vertex), P = P'[x <- X] with random wiring.
For every state Q of P and kind, compare with the contracted state Q/X of P':
  (b) same outcome, successor contracts to P''s successor;   (c) cost = c_{P'} + sum_f M c_X[f].
(a) h(P) = h(P').  Positive group: X simple.  Negative control: X not simple."""
import sys, random, itertools, time
from collections import Counter
sys.path.insert(0, "..")
from lollipop import random_instance
from general import from_chord
from transducer import visit_B1, visit_B3, ham_paths_between
from nested_lemma import visit_moves, passages_through_vertex

def pole(G, r):
    keep = [v for v in range(len(G)) if v != r]; idx = {v: j for j, v in enumerate(keep)}
    return [[idx[w] for w in G[v] if w != r] for v in keep], [idx[p] for p in G[r]]

def states(P, ports):
    out = []
    for s, t in itertools.permutations(ports, 2): out += ham_paths_between(P, s, t)
    return out

def table(P, ports):
    T = {}
    for Q in states(P, ports):
        for kind, fn in (("B1", visit_B1), ("B3", visit_B3)): T[(Q, kind)] = fn(P, ports, Q)
    return T

def run(rng):
    n1 = rng.choice([8, 10, 12]); Kp = from_chord(n1, random_instance(n1, rng)); rp = rng.randrange(n1)
    Pp, portsP = pole(Kp, rp)
    inner = [v for v in range(len(Pp)) if v not in portsP]          # x not a port: N(x) inside P'
    if not inner: return None
    x = rng.choice(inner)
    n2 = rng.choice([4, 6, 8, 10]); KX = from_chord(n2, random_instance(n2, rng)) if n2 > 4 else [[1,2,3],[0,2,3],[0,1,3],[0,1,2]]
    PX, portsX = pole(KX, rng.randrange(n2))
    perm = list(range(3)); rng.shuffle(perm)
    m = len(Pp); off = m
    P = [list(a) for a in Pp] + [[off + w for w in PX[i]] for i in range(len(PX))]
    nbx = list(Pp[x])
    for j, u in enumerate(nbx):
        p = off + portsX[perm[j]]; P[u] = [p if y == x else y for y in P[u]]; P[p].append(u)
    P[x] = []
    keep = [v for v in range(len(P)) if v != x]; lab = {v: i for i, v in enumerate(keep)}
    P = [[lab[w] for w in P[v]] for v in keep]; ports = [lab[p] for p in portsP]
    Xset = {lab[off + i] for i in range(len(PX))}; xin = {lab[off + portsX[i]]: i for i in range(3)}
    TX = table(PX, portsX); simpleX = all(len(ham_paths_between(PX, portsX[a], portsX[b])) == 1 for a, b in itertools.permutations(range(3), 2))
    TPp = table(Pp, portsP); TP = table(P, ports)
    def contract(Q):
        out = []
        for v in Q:
            u = x if v in Xset else keep[v] if keep[v] < m else None
            if u is None: u = x
            if not out or out[-1] != u: out.append(u)
        return tuple(out)
    # X-cost by (oriented X-port pair, kind): named by X port index
    cX = {}
    for (Q, kind), (res, Qn, cost) in TX.items(): cX.setdefault((portsX.index(Q[0]), portsX.index(Q[-1]), kind), []).append((res, cost))
    xname = {u: "abc"[perm[j]] for j, u in enumerate(nbx)}
    hP = Counter((Q[0], Q[-1]) for (Q, k) in TP if k == "B1"); hPp = Counter((lab[Q[0]], lab[Q[-1]]) for (Q, k) in TPp if k == "B1")
    res = dict(simpleX=simpleX, h_equal=(hP == hPp), outcome_ok=True, cost_ok=True)
    for (Q, kind), (o, Qn, cost) in TP.items():
        Qc = contract(Q); o2, Qn2, cost2 = TPp[(Qc, kind)]
        if o != o2 or contract(Qn) != Qn2: res["outcome_ok"] = False
        if simpleX:
            M = passages_through_vertex(visit_moves(Pp, portsP, Qc, kind), x, xname)
            pred = cost2 + sum(cnt * cX[("abc".index(pr[0]), "abc".index(pr[1]), kd)][0][1] for (pr, kd), cnt in M.items())
            if pred != cost: res["cost_ok"] = False
    return res

if __name__ == "__main__":
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 5); t0 = time.time(); S = Counter()
    budget = float(sys.argv[2]) if len(sys.argv) > 2 else 250
    while time.time() - t0 < budget:
        try: r = run(rng)
        except (KeyError, AssertionError, IndexError) as e: S[("error", type(e).__name__)] += 1; continue
        if r is None: continue
        g = "X simple" if r["simpleX"] else "X NOT simple (control)"
        S[(g, "h(P)=h(P')", r["h_equal"])] += 1
        S[(g, "outcomes match", r["outcome_ok"])] += 1
        if r["simpleX"]: S[(g, "costs match", r["cost_ok"])] += 1
    for k, v in sorted(S.items(), key=str): print(k, v)
