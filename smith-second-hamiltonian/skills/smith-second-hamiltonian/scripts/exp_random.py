"""E2: lollipop length on uniformly random (cycle + chord matching) instances."""
import random, json, statistics, sys, time
from lollipop import random_instance, lollipop

rng = random.Random(2026)
res = {}
for n in [20, 50, 100, 200, 500, 1000, 2000, 5000]:
    trials = 2000 if n <= 500 else (400 if n <= 2000 else 100)
    t = time.time(); xs = []
    for _ in range(trials):
        ch = random_instance(n, rng)
        s, _ = lollipop(n, ch, 0, 1)
        xs.append(s)
    xs.sort()
    res[n] = dict(trials=trials, mean=statistics.mean(xs), median=xs[len(xs)//2],
                  p99=xs[int(0.99*len(xs))-1], max=xs[-1], mean_over_n=statistics.mean(xs)/n)
    print(n, trials, "mean %.1f  mean/n %.3f  median %d  p99 %d  max %d  (%.0fs)" % (
        res[n]['mean'], res[n]['mean_over_n'], res[n]['median'], res[n]['p99'], res[n]['max'], time.time()-t), flush=True)
json.dump(res, open("e2_random.json", "w"), indent=1)
