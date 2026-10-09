"""E10: validity of projected outputs, and dependence of the outcome on X's internal state.
Also tabulates, per 3-pole, h_ab = #Ham paths of X between port pairs."""
import random, itertools
from collections import Counter
from lollipop import random_instance
from general import lollipop_g, from_chord, substitute, cyc_edges, is_ham, ham_paths
from exp_3pole_transparency import poles, project

rng = random.Random(8)
for name, (padj, ports) in poles.items():
    if name.startswith("petersen"): continue
    h = {}
    for a, b in itertools.combinations(range(3), 2):
        h[(a, b)] = len(ham_paths(padj, range(len(padj)), ports[a], ports[b])) // 1
    invalid = 0; hosts = 0; state_dep = 0; agree_some = 0; kinds = Counter()
    for _ in range(200):
        n = rng.choice([12, 16, 20]); chord = random_instance(n, rng)
        H = from_chord(n, chord); C = list(range(n)); x = rng.randrange(2, n - 1)
        perm = list(ports); rng.shuffle(perm)
        G, cycles, X = substitute(H, C, x, padj, perm)
        if len(cycles) < 1: continue
        hosts += 1
        _, cH, _ = lollipop_g(H, C); EH = cyc_edges(cH)
        outs = []
        for c0 in cycles:
            _, cG, _ = lollipop_g(G, c0); p = project(cG, X, x)
            if not is_ham(H, p): invalid += 1
            outs.append(frozenset(cyc_edges(p)))
        if len(set(outs)) > 1: state_dep += 1
        kinds[(len(set(outs)), sum(o == EH for o in outs), len(outs))] += 1
    print(f"{name:16s} h(ab,ac,bc)={list(h.values())} hosts={hosts} invalid_proj={invalid} "
          f"state-dependent hosts={state_dep}  (distinct outs, #agree with H, #c0) top={kinds.most_common(3)}")
