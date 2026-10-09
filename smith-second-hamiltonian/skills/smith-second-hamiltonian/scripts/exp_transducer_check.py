"""E14: the abstract walk (H-walk + 3-pole transducer) reproduces the real walk on G exactly:
same final cycle and same number of steps."""
import random
from lollipop import random_instance
from general import from_chord, substitute, lollipop_g, cyc_edges
from exp_3pole_transparency import poles, pole_from_cubic, random_cubic_ham, project
from transducer import visit_B1, visit_B3

def abstract_walk(H, C, x, port_of, Q):
    """port_of[q] = pole port attached to host neighbour q of x. Q: X's path (pole labels),
    unoriented. Returns (final H-cycle, G-step count, internal Q)."""
    v0 = C[0]; S = list(C); forb = v0; steps = 0; n = len(S)
    qport = {p: q for q, p in port_of.items()}
    def orient(S, Q):
        i = S.index(x); qin = S[i-1]; pin = port_of[qin]
        return Q if Q[0] == pin else Q[::-1]
    while True:
        z, prev = S[-1], S[-2]
        w = [u for u in H[z] if u != prev and u != forb][0]
        if w == v0: return S, steps, Q
        i = S.index(w); s = S[i+1]
        if s == x and z != x:                     # 1b: deleting entry edge w-x -> B1 visit
            Qo = orient(S, Q)
            res, Qn, k = visit_B1(padj_g, ports_g, Qo)
            S1 = S[:i+1] + S[i+1:][::-1]           # endpoint x now
            out_port = Qn[-1]; q_exit = qport[out_port]
            j = S1.index(q_exit); S = S1[:j+1] + S1[j+1:][::-1]
            forb = q_exit; Q = Qn; steps += 2 + k
            continue
        if w == x:                                # 1c: adding cut edge z-x -> B3 visit
            Qo = orient(S, Q)
            res, Qn, k = visit_B3(padj_g, ports_g, Qo)
            Sstar = S[:i+1] + S[i+1:][::-1]
            S = Sstar if res == "TRANSMIT" else S
            forb = x; Q = Qn; steps += 1 + k
            continue
        S = S[:i+1] + S[i+1:][::-1]; forb = w; steps += 1

rng = random.Random(17)
allpoles = dict(poles)
for k in range(10):
    m = rng.choice([10, 12, 14, 16]); allpoles[f"rand{m}-v#{k}b"] = pole_from_cubic(random_cubic_ham(m, rng), 0)
tot = bad = 0
for name, (padj, ports) in allpoles.items():
    if name.startswith("petersen"): continue
    padj_g, ports_g = padj, ports
    nb = nt = 0
    for _ in range(120):
        n = rng.choice([10, 14, 20, 30, 50]); chord = random_instance(n, rng)
        H = from_chord(n, chord); C = list(range(n)); x = rng.randrange(2, n - 1)
        if x == chord[0]: continue
        perm = list(ports); rng.shuffle(perm)
        G, cycles, X = substitute(H, C, x, padj, perm)
        # pole label -> G label, and host neighbour -> pole port
        m = len(padj); nG = len(G)
        # substitute(): pole vertex i gets label n+i, last label (n+m-1) is moved into slot x
        lab = {i: (n + i if n + i != nG else x) for i in range(m)}
        lab = {i: (x if n + i == n + m - 1 else n + i) for i in range(m)}
        inv = {g: i for i, g in lab.items()}
        port_of = {q: perm[k] for k, q in enumerate(H[x])}
        for c0 in cycles[:3]:
            i0 = c0.index(next(v for v in c0 if v in X))
            Qg = [v for v in c0 if v in X]          # X is contiguous in C0 (C0 crosses cut twice)
            # C0 as a cyclic list starting at v0 with X contiguous: v0 = 0 not in X
            Q = tuple(inv[v] for v in Qg)
            sG, cG, _ = lollipop_g(G, c0)
            S, sA, _ = abstract_walk(H, C, x, port_of, Q)
            nt += 1; tot += 1
            if cyc_edges(project(cG, X, x)) != cyc_edges(S) or sG != sA:
                nb += 1; bad += 1
    print(f"{name:16s} runs={nt:4d} mismatches={nb}")
print("TOTAL", tot, "mismatches", bad)
