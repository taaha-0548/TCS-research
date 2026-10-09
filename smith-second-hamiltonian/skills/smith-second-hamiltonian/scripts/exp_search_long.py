"""E4: simulated-annealing search for long lollipop walks at larger n.
Move: pick two chords {a,b},{c,d} and reconnect as {a,c},{b,d} or {a,d},{b,c}."""
import random, math, json, sys, time
from lollipop import lollipop, random_instance, valid_chord

def score(n, ch):
    s, _ = lollipop(n, ch, 0, 1)
    return s

def anneal(n, iters, rng, seed_ch=None):
    ch = seed_ch[:] if seed_ch else random_instance(n, rng)
    cur = score(n, ch); best, best_ch = cur, ch[:]
    T0 = max(1.0, cur * 0.3)
    for it in range(iters):
        T = T0 * (1 - it / iters) + 0.01
        a = rng.randrange(n); c = rng.randrange(n)
        b, d = ch[a], ch[c]
        if len({a, b, c, d}) < 4: continue
        new = ch[:]
        if rng.random() < 0.5: new[a], new[c], new[b], new[d] = c, a, d, b
        else: new[a], new[d], new[b], new[c] = d, a, c, b
        if not valid_chord(n, new): continue
        s = score(n, new)
        if s >= cur or rng.random() < math.exp((s - cur) / T):
            ch, cur = new, s
            if s > best: best, best_ch = s, new[:]
    return best, best_ch

rng = random.Random(7)
res = {}
for n in [int(x) for x in sys.argv[1:]]:
    t = time.time(); best, bch = -1, None
    while time.time() - t < 35:
        b, c = anneal(n, 4000, rng)
        if b > best: best, bch = b, c
    res[n] = dict(best=best, chord=bch, per_vertex_base=best ** (1 / n))
    print(n, "best", best, "best^(1/n) = %.4f" % best ** (1 / n), flush=True)
json.dump(res, open("e4_search.json", "w"), indent=1)
