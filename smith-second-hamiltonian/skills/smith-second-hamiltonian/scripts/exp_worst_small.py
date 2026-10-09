"""E1: exact worst-case lollipop length over ALL (cubic Hamiltonian graph, Hamiltonian
cycle, fixed edge, orientation) configurations on n vertices.  Enumerating every labelled
chord matching with start (v0=0, dirn=+1) covers all configurations, since relabelling
moves any start to this one."""
import sys, json, time
from lollipop import all_instances, lollipop

out = {}
for n in range(6, int(sys.argv[1]) + 1, 2):
    t = time.time(); best = -1; best_ch = None; total = 0; cnt = 0
    hist = {}
    for ch in all_instances(n):
        s, _ = lollipop(n, ch, 0, 1)
        cnt += 1; total += s
        hist[s] = hist.get(s, 0) + 1
        if s > best:
            best, best_ch = s, ch[:]
    out[n] = dict(instances=cnt, max_steps=best, mean_steps=total / cnt, worst_chord=best_ch,
                  hist=dict(sorted(hist.items())), secs=round(time.time() - t, 1))
    print(n, cnt, "max", best, "mean %.2f" % (total / cnt), "%.1fs" % (time.time() - t), flush=True)
json.dump(out, open("e1_worst_small.json", "w"), indent=1)
