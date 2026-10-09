"""T1: M computed from the tiny P_0 = K - r (passages through x) vs M measured on the real
nested graphs (E20).  Also T_0, the outcome table of P_0."""
import json
from general import from_chord, lollipop_g
from nested_fast import rotate_to
from transducer import visit_B1, visit_B3, ham_paths_between
from nested_lemma import visit_moves, passages_through_vertex
CH = [4, 3, 6, 1, 0, 7, 2, 5]; X, R, PERM = 5, 2, (2, 0, 1)
K = from_chord(8, CH)
keep = [v for v in range(8) if v != R]; idx = {v: j for j, v in enumerate(keep)}
P0 = [[idx[w] for w in K[v] if w != R] for v in keep]
ports = [idx[p] for p in K[R]]; pname = {p: "abc"[k] for k, p in enumerate(ports)}
x = idx[X]
xname = {idx[u]: "abc"[PERM[k]] for k, u in enumerate(K[X])}   # inner pole port attached to u
states = []
for s, t in [(ports[i], ports[j]) for i in range(3) for j in range(3) if i != j]:
    states += ham_paths_between(P0, s, t)
print("P0 states (h per oriented pair):", {pname[q[0]] + pname[q[-1]]: sum(1 for z in states if z[0] == q[0] and z[-1] == q[-1]) for q in states})
keys = sorted((pname[Q[0]] + pname[Q[-1]], k) for Q in states for k in ("B1", "B3"))
M0 = {}; table = {}
for Q in states:
    for kind, fn in (("B1", visit_B1), ("B3", visit_B3)):
        e = (pname[Q[0]] + pname[Q[-1]], kind)
        res, Qn, cost = fn(P0, ports, Q); table[e] = (res, pname[Qn[0]] + pname[Qn[-1]], cost)
        M0[e] = passages_through_vertex(visit_moves(P0, ports, Q, kind), x, xname)
E20 = json.load(open("e20_M.json"))
k20 = [tuple(s.split("/")) for s in E20["keys"]]
M0mat = [[M0[e][f] for f in k20] for e in k20]
print("T_0 (P_0 table):", {"/".join(e): v[:2] for e, v in sorted(table.items())})
print("c_0 from P_0:", [table[e][2] for e in k20], " vs b from E20:", E20["b"])
print("M from P_0 equals E20 M:", M0mat == E20["M"])
if M0mat != E20["M"]:
    for e, r1, r2 in zip(k20, M0mat, E20["M"]):
        if r1 != r2: print("  row", "/".join(e), r1, "vs", r2)
json.dump(dict(keys=E20["keys"], M0=M0mat, T0={"/".join(e): v for e, v in table.items()}), open("t1_M0.json", "w"), indent=1)
