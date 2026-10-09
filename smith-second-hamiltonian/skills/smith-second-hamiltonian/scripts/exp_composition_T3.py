"""T3: Composition Lemma on random nested families F(K, x, r, perm).
Prediction from P_0 = K - r alone: table T_0 and M (passages through x), c_k = c_0 + M c_{k-1}.
Truth: direct transducer of P_k = G_k - r_k (all oriented Ham paths, all visits), k <= 3.
Families are grouped by whether the hypotheses hold:
  H1: P_0 is transparent-simple (every visit TRANSMITs, one Ham path per port pair)
  H2: r not adjacent to x (so the inner pole's cut edges lie inside P)."""
import random, sys, json, itertools, time
from collections import Counter
from lollipop import random_instance
from general import from_chord, lollipop_g, cyc_edges
from nested_fast import next_level, rotate_to
from transducer import visit_B1, visit_B3, ham_paths_between
from nested_lemma import visit_moves, passages_through_vertex

def pole_states(P, ports):
    out = []
    for s, t in itertools.permutations(ports, 2): out += ham_paths_between(P, s, t)
    return out

def table_of(P, ports, states, pname):
    T = {}
    for Q in states:
        for kind, fn in (("B1", visit_B1), ("B3", visit_B3)):
            res, Qn, cost = fn(P, ports, Q)
            T.setdefault((pname[Q[0]] + pname[Q[-1]], kind), []).append((res, pname[Qn[0]] + pname[Qn[-1]], cost))
    return T

def pole(G, r):
    keep = [v for v in range(len(G)) if v != r]; idx = {v: j for j, v in enumerate(keep)}
    P = [[idx[w] for w in G[v] if w != r] for v in keep]; ports = [idx[p] for p in G[r]]
    return P, ports, idx, {p: "abc"[k] for k, p in enumerate(ports)}

def run_family(CH, x, r, perm, L):
    nk = len(CH); K = from_chord(nk, CH); Kc = list(range(nk))
    P0, ports0, idx0, pn0 = pole(K, r)
    st0 = pole_states(P0, ports0)
    T0 = table_of(P0, ports0, st0, pn0)
    simple = all(len(v) == 1 for v in T0.values())
    transp = all(o[0] == "TRANSMIT" for v in T0.values() for o in v)
    if not simple: return None                       # prediction undefined without h = 1
    if x in K[r]: return "notH2"                     # x is a port of P_0: passages undefined
    keys = sorted(T0)
    xname = {idx0[u]: "abc"[perm[k]] for k, u in enumerate(K[x])}
    M = {e: Counter() for e in keys}
    for Q in st0:
        for kind in ("B1", "B3"):
            e = (pn0[Q[0]] + pn0[Q[-1]], kind)
            M[e] = passages_through_vertex(visit_moves(P0, ports0, Q, kind), idx0[x], xname)
    c = {e: T0[e][0][2] for e in keys}; c0 = dict(c)
    G, Gc = K, Kc; rl = r; verdicts = []
    for k in range(1, L + 1):
        nxt = next_level(K, Kc, x, G, [Gc], rl, perm)
        if nxt is None: return dict(H1=transp, H2=x not in K[r], result="no-cycle")
        G, Gc = nxt; rl = r if r < x else r - 1
        cpred = {e: c0[e] + sum(M[e][f] * c[f] for f in M[e]) for e in keys}
        P, ports, idx, pn = pole(G, rl)
        Tk = table_of(P, ports, pole_states(P, ports), pn)
        same_outcomes = all(len(Tk.get(e, [])) == 1 and Tk[e][0][:2] == T0[e][0][:2] for e in keys)
        same_costs = same_outcomes and all(Tk[e][0][2] == cpred[e] for e in keys)
        verdicts.append((same_outcomes, same_costs))
        c = {e: Tk[e][0][2] for e in keys} if same_outcomes else cpred
    return dict(H1=transp, H2=x not in K[r], result=verdicts)

if __name__ == "__main__":
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 7)
    budget = float(sys.argv[2]) if len(sys.argv) > 2 else 240
    perms = list(itertools.permutations(range(3)))
    t0 = time.time(); summary = Counter(); fails = []
    while time.time() - t0 < budget:
        nk = rng.choice([6, 8, 10]); CH = random_instance(nk, rng)
        x = rng.randrange(1, nk); r = rng.choice([v for v in range(nk) if v != x])
        if x in (CH[0], 1, nk - 1) or 0 in (x, ):   # keep x away from v0 = 0 for cycle bookkeeping
            continue
        perm = rng.choice(perms)
        try: out = run_family(CH, x, r, perm, 3)
        except (TimeoutError, RuntimeError, AssertionError): continue
        if out is None: summary["skipped: P_0 has h != 1"] += 1; continue
        if out == "notH2": summary["skipped: r adjacent to x (H2 fails, prediction undefined)"] += 1; continue
        if out["result"] == "no-cycle": summary["skipped: wiring admits no Ham cycle"] += 1; continue
        hyp = ("H1" if out["H1"] else "notH1") + "+" + ("H2" if out["H2"] else "notH2")
        allok = all(a and b for a, b in out["result"])
        summary[(hyp, "exact" if allok else "FAILS")] += 1
        if not allok and out["H1"] and out["H2"]: fails.append(dict(CH=CH, x=x, r=r, perm=perm, res=out["result"]))
    for k, v in sorted(summary.items(), key=str): print(k, v)
    print("failures under both hypotheses:", len(fails))
    for f in fails[:5]: print("  ", f)
    json.dump(dict(summary={str(k): v for k, v in summary.items()}, fails=fails), open("t3_composition.json", "w"), indent=1)
