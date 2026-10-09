"""E11: classify G-walk outputs after projection: H's lollipop output (agree), the start cycle C
(local swap inside X), or some other Ham cycle of H."""
import random
from collections import Counter
from lollipop import random_instance
from general import lollipop_g, from_chord, substitute, cyc_edges
from exp_3pole_transparency import poles, project

rng = random.Random(21)
for name, (padj, ports) in poles.items():
    if name.startswith("petersen"): continue
    cnt = Counter()
    for _ in range(300):
        n = rng.choice([12, 16, 20, 30]); chord = random_instance(n, rng)
        H = from_chord(n, chord); C = list(range(n)); x = rng.randrange(2, n - 1)
        perm = list(ports); rng.shuffle(perm)
        G, cycles, X = substitute(H, C, x, padj, perm)
        _, cH, _ = lollipop_g(H, C); EH, EC = cyc_edges(cH), cyc_edges(C)
        for c0 in cycles:
            _, cG, _ = lollipop_g(G, c0); E = cyc_edges(project(cG, X, x))
            cnt["agree" if E == EH else "swap(=C)" if E == EC else "OTHER"] += 1
    print(f"{name:16s} {dict(cnt)}")
