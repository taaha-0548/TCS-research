"""E5: test H2.2 -- steps/(n/2) is approximately Exp(1) on random instances.
Compares empirical quantiles with Exp(1) quantiles and computes the KS distance."""
import random, math, json, sys
from lollipop import random_instance, lollipop

rng = random.Random(99)
res = {}
for n, trials in [(200, 4000), (1000, 1500)]:
    xs = sorted(lollipop(n, random_instance(n, rng), 0, 1)[0] / (n / 2) for _ in range(trials))
    m = len(xs)
    ks = max(max(abs((i + 1) / m - (1 - math.exp(-x))), abs(i / m - (1 - math.exp(-x)))) for i, x in enumerate(xs))
    q = {p: xs[int(p * m) - 1] for p in (0.1, 0.25, 0.5, 0.75, 0.9, 0.99)}
    qexp = {p: -math.log(1 - p) for p in q}
    res[n] = dict(trials=trials, mean=sum(xs) / m, ks=ks, quantiles=q, exp_quantiles=qexp)
    print(f"n={n} trials={trials} mean(steps/(n/2))={sum(xs)/m:.3f} KS={ks:.4f} "
          f"(5% critical ~{1.36/math.sqrt(m):.4f})")
    for p in q:
        print(f"   q{int(p*100):>2}: empirical {q[p]:.3f}   Exp(1) {qexp[p]:.3f}")
json.dump(res, open("e5_exponential_law.json", "w"), indent=1)
