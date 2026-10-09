"""E12: Mirror hypothesis for 3-poles.
Index the host walk's states S_0..S_L (Ham paths of H from v0). Run the walk on G and, at every
step where the endpoint lies outside X, project the path onto H and look up its index.
Mirror hypothesis: consecutive distinct indices differ by exactly 1 (the projected walk moves
along H's line), and direction changes happen only across excursions into X."""
import random
from collections import Counter
from lollipop import random_instance
from general import from_chord, substitute, cyc_edges
from exp_3pole_transparency import poles, project

def host_line(H, C):
    v0 = C[0]; path = list(C); n = len(path); pos = {v: i for i, v in enumerate(path)}
    forb = v0; line = [tuple(path)]
    while True:
        z, prev = path[-1], path[-2]
        w = [u for u in H[z] if u != prev and u != forb][0]
        if w == v0: return line
        i = pos[w]; path[i+1:] = path[i+1:][::-1]
        for j in range(i+1, n): pos[path[j]] = j
        forb = w; line.append(tuple(path))

def g_trace(G, c0, X, x):
    """Yield (projected path tuple or None, endpoint_in_X) per G-state."""
    v0 = c0[0]; path = list(c0); n = len(path); pos = {v: i for i, v in enumerate(path)}
    forb = v0; out = []
    while True:
        z = path[-1]
        if z in X: out.append(None)
        else:
            p = []
            for v in path:
                u = x if v in X else v
                if not p or p[-1] != u: p.append(u)
            out.append(tuple(p))
        prev = path[-2]
        w = [u for u in G[z] if u != prev and u != forb][0]
        if w == v0: return out, path
        i = pos[w]; path[i+1:] = path[i+1:][::-1]
        for j in range(i+1, n): pos[path[j]] = j
        forb = w

rng = random.Random(4)
for name, (padj, ports) in poles.items():
    if name.startswith("petersen"): continue
    viol = 0; runs = 0; jumps = Counter(); inplace = 0; bounces = Counter(); notfound = 0; reversal_outside = 0
    for _ in range(150):
        n = rng.choice([12, 16, 20, 30]); chord = random_instance(n, rng)
        H = from_chord(n, chord); C = list(range(n)); x = rng.randrange(2, n - 1)
        if x == chord[0]: continue                       # keep X away from v0
        perm = list(ports); rng.shuffle(perm)
        G, cycles, X = substitute(H, C, x, padj, perm)
        line = host_line(H, C); idx = {s: i for i, s in enumerate(line)}
        for c0 in cycles:
            runs += 1
            tr, _ = g_trace(G, c0, X, x)
            seq = []  # (index, excursion_before)
            bounce_in_place = 0
            exc = False
            for s in tr:
                if s is None: exc = True; continue
                if s not in idx: notfound += 1; exc = False; continue
                i = idx[s]
                if not seq or seq[-1][0] != i:
                    seq.append((i, exc)); exc = False
                elif exc:
                    seq[-1] = (i, True); bounce_in_place += 1
            b = 0
            for k in range(1, len(seq)):
                if abs(seq[k][0] - seq[k-1][0]) != 1 and not seq[k][1]: viol += 1
                jumps[abs(seq[k][0] - seq[k-1][0]) if seq[k][1] else 'plain1' if abs(seq[k][0]-seq[k-1][0])==1 else 'plainX'] += 1
                if k >= 2:
                    d1 = seq[k-1][0] - seq[k-2][0]; d2 = seq[k][0] - seq[k-1][0]
                    if d1 * d2 < 0:
                        b += 1
                        if not seq[k][1] and not seq[k-1][1]: reversal_outside += 1
            bounces[b + bounce_in_place] += 1; inplace += bounce_in_place
    print(f"{name:16s} runs={runs:4d} non-adjacent plain moves={viol} unmatched states={notfound} "
          f"reversals w/o X-excursion={reversal_outside} in-place bounces={inplace} bounce hist={dict(sorted(bounces.items()))} jumps={dict(jumps)}")
