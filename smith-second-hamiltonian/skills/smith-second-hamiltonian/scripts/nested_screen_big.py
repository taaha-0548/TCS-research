"""E17b: screen nested families with |K| = 8 or 10 by their per-level growth factor."""
import random, sys, time, json
from lollipop import random_instance
from general import from_chord
from nested_family import family
nk = int(sys.argv[1]); levels = int(sys.argv[2]); budget = float(sys.argv[3]); rng = random.Random(int(sys.argv[4]))
perms = [(0,1,2),(0,2,1),(1,0,2),(1,2,0),(2,0,1),(2,1,0)]
need = 1.1812 ** (nk - 2); t0 = time.time(); found = []
while time.time() - t0 < budget:
    ch = random_instance(nk, rng); K = from_chord(nk, ch); x = rng.randrange(2, nk - 1)
    if x == ch[0]: continue
    r = rng.choice([v for v in range(nk) if v != x]); perm = rng.choice(perms)
    try: seq = family(K, list(range(nk)), x, r, perm, levels)
    except (TimeoutError, RuntimeError, AssertionError): continue
    if len(seq) < levels + 1 or seq[-2][1] == 0: continue
    f = seq[-1][1] / seq[-2][1]
    found.append((f, seq, ch, x, r, perm))
found.sort(key=lambda t: -t[0])
print(f"|K|={nk}: screened {len(found)} families; factor needed to beat 1.1812: {need:.3f}")
for f, seq, ch, x, r, perm in found[:5]:
    print(f"  last factor {f:.3f}  seq={seq}  chord={ch} x={x} r={r} perm={perm}")
json.dump([dict(f=f, seq=s, chord=c, x=x, r=r, perm=p) for f, s, c, x, r, p in found[:10]], open(f"e17b_K{nk}.json", "w"), indent=1)
