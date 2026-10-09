"""Extract and display an optimal ideal flat counter (c=4, 2 sites per gadget) for small m."""
import sys, random, time, json
from ideal_flat import site_types, run
rng = random.Random(5); c = 4; types = site_types(c)
def climb(m, secs):
    N = 2 * m; owners = [g for g in range(m) for _ in range(2)]; rng.shuffle(owners)
    cur = ([(g, rng.choice(types)) for g in owners], [rng.randrange(c) for _ in range(m)]); curv = run(*cur) or 0; best = (curv, cur)
    t_end = time.time() + secs
    while time.time() < t_end:
        sites, init = list(cur[0]), list(cur[1]); r = rng.random()
        if r < 0.5: i = rng.randrange(N); sites[i] = (sites[i][0], rng.choice(types))
        elif r < 0.8: i, j = rng.randrange(N), rng.randrange(N); sites[i], sites[j] = sites[j], sites[i]
        else: init[rng.randrange(m)] = rng.randrange(c)
        v = run(sites, init)
        if v is not None and (v >= curv or rng.random() < 0.02): cur, curv = (sites, init), v
        if v and v > best[0]: best = (v, (sites, init))
    return best
def show(T, If, Ib):
    t = ",".join(f"{a}>{b}" for a, b in sorted(T.items())) or "-"
    f = ",".join(f"{a}{b}" for a, b in sorted(If.items()) if a < b) or "-"
    b = ",".join(f"{a}{b}" for a, b in sorted(Ib.items()) if a < b) or "-"
    return f"pass[{t}] reflL[{f}] reflR[{b}]"
for m in (2, 3, 4):
    v, (sites, init) = climb(m, 12)
    print(f"\nm={m}: run {v}; initial states {init}")
    for i, (g, (T, If, Ib)) in enumerate(sites): print(f"   site {i}: gadget g{g}  {show(T, If, Ib)}")
