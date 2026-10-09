"""Hill-climb flat ideal systems: m gadgets with s sites each (c states), orderings and site types
mutated, maximise the run.  Does the best run grow exponentially in m?"""
import sys, random, time
from ideal_flat import site_types, run
rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
c = int(sys.argv[2]) if len(sys.argv) > 2 else 4; s = int(sys.argv[3]) if len(sys.argv) > 3 else 2
types = site_types(c)
for m in range(1, 9):
    N = m * s; best = 0; t_end = time.time() + 14
    owners = [g for g in range(m) for _ in range(s)]; rng.shuffle(owners)
    cur = ([(g, rng.choice(types)) for g in owners], [rng.randrange(c) for _ in range(m)]); curv = run(*cur) or 0
    while time.time() < t_end:
        sites, init = list(cur[0]), list(cur[1]); r = rng.random()
        if r < 0.5: i = rng.randrange(N); sites[i] = (sites[i][0], rng.choice(types))
        elif r < 0.8: i, j = rng.randrange(N), rng.randrange(N); sites[i], sites[j] = sites[j], sites[i]
        else: init[rng.randrange(m)] = rng.randrange(c)
        v = run(sites, init)
        if v is not None and (v >= curv or rng.random() < 0.02): cur, curv = (sites, init), v
        if v and v > best: best = v
    print(f"c={c}, s={s} sites/gadget, m={m} (N={N}): best run {best}", flush=True)
