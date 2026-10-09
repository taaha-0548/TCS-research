"""Generate the two appendix tables for paper.tex (pasted inline): visits of P0 and the G_1 walk."""
import itertools, json
import verify as V
P0, ports, idx = V.pole(V.K, V.R); inv = {i: v for v, i in idx.items()}
name = {p: "abc"[i] for i, p in enumerate(ports)}; xname = {idx[u]: "abc"[V.PERM[j]] for j, u in enumerate(V.K[V.X])}
def L(v): return str(inv[v])
out = []
for s, t in itertools.permutations(ports, 2):
    Q = V.ham_paths(P0, s, t)[0]
    for kd in ("B1", "B3"):
        o, Qn, cost, moves = V.visit(P0, ports, Q, kd)
        mv = []
        for pieces, z, w, ss in moves[1:]:
            tag = "^{\\dagger}" if ss == idx[V.X] else ("^{\\ddagger}" if w == idx[V.X] else "")
            mv.append(f"${L(z)}{L(w)}{tag}$")
        et = "$^{\\dagger}$" if moves[0][3] == idx[V.X] else ""
        ps = V.passages(moves, idx[V.X], xname)
        out.append(f"{name[s]}{name[t]}/{kd}{et} & {''.join(L(v) for v in Q)} & {' '.join(mv)} & {cost} & {', '.join(k[0]+'/'+k[1] for k in sorted(ps))} \\\\")
open("tab_visits.tex", "w").write("\n".join(out) + "\n")
d = json.load(open("paper_data.json"))
rows = []
for i, (p, m) in enumerate(d["trace"]):
    mm = "--" if m is None else m.replace(" *", "").replace("'", "'")
    star = "" if m is None or "*" not in m else "$\\bullet$"
    pp = p.replace("'", "$'$")
    mm = mm.replace("'", "$'$")
    rows.append(f"{i} & {mm} & {star} & {pp} \\\\")
open("tab_trace.tex", "w").write("\n".join(rows) + "\n")
print(open("tab_visits.tex").read()); print(open("tab_trace.tex").read())
