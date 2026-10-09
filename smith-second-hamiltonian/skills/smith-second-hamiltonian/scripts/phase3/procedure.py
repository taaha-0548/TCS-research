"""Phase 3 / P3.1: the cell procedure induced by a gadget P' with one slot x.

A visit (Q', kind) to P' runs P''s internal dynamics; each passage through x is a CALL to the child
(type f in the 12 visit types) answered TRANSMIT or REFLECT.  We enumerate all answer sequences and
record, for each, the sequence of calls and the result (outcome of the visit, new P'-path).
Interpreted as a Turing-machine cell: local state = P'-path; head arrives with `kind`/orientation;
calls = moves right; the visit's exit = move left."""
import sys
sys.path.insert(0, "../phase1"); sys.path.insert(0, ".."); sys.path.insert(0, "../../../../../paper")
import verify as V
from compose import composed_visit

class Oracle:
    """Plays the child: answers calls from a prescribed list, records the calls."""
    def __init__(self, x, port_of, answers):
        self.x, self.port_of, self.answers, self.calls, self.QX = x, port_of, list(answers), [], None
        self.nb_of = {p: u for u, p in port_of.items()}
        self.exhausted = False
    def visit(self, pred, succ, kind):
        a, b = self.port_of[pred], self.port_of[succ]
        self.calls.append((a + b, kind))
        if not self.answers: self.exhausted = True; raise StopIteration
        ans = self.answers.pop(0)
        third = next(c for c in "abc" if c not in (a, b))
        if kind == "B1":
            exit_port = third if ans == "T" else a
            return ("TRANSMIT" if ans == "T" else "REFLECT"), (b, exit_port), 0
        return ("TRANSMIT" if ans == "T" else "REFLECT"), (a, b), 0

class OracleInner:
    """Adapter with the interface composed_visit expects (x, visit, nb_of, QX)."""
    def __init__(self, oracle): self.o = oracle; self.x = oracle.x; self.nb_of = {p: u for u, p in oracle.port_of.items()}; self.QX = ()
    def visit(self, pred, succ, kind):
        res, Qn, k = self.o.visit(pred, succ, kind); self.QX = Qn; return res, Qn, k

def procedure(P1, ports1, x, xname, Q1, kind, max_calls=8):
    """All answer sequences up to max_calls: returns list of (answers, calls, outcome, final_path)."""
    out = []
    def explore(prefix):
        o = Oracle(x, xname, prefix); inner = OracleInner(o)
        try:
            res, Qf, cost, _ = composed_visit(P1, ports1, Q1, kind, inner)
            out.append((tuple(prefix), tuple(o.calls), res[0], Qf))
        except StopIteration:
            if len(prefix) < max_calls:
                explore(prefix + ["T"]); explore(prefix + ["R"])
        except AssertionError:
            pass
    explore([]); return out
