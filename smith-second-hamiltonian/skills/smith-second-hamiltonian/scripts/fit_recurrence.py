"""Find the shortest integer linear recurrence (with constant term) fitting a sequence exactly."""
import sys, ast
from fractions import Fraction
s = ast.literal_eval(sys.argv[1])
def solve(M, b):
    n = len(M); A = [[Fraction(x) for x in row] + [Fraction(y)] for row, y in zip(M, b)]
    for c in range(n):
        p = next((r for r in range(c, n) if A[r][c] != 0), None)
        if p is None: return None
        A[c], A[p] = A[p], A[c]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c] / A[c][c]; A[r] = [a - f * b for a, b in zip(A[r], A[c])]
    return [A[i][n] / A[i][i] for i in range(n)]
for order in range(1, 7):
    for const in (False, True):
        k = order + const
        rows = [[s[i - j] for j in range(1, order + 1)] + ([1] if const else []) for i in range(order, order + k)]
        if order + k > len(s): continue
        sol = solve(rows, [s[i] for i in range(order, order + k)])
        if sol is None: continue
        ok = all(sum(sol[j] * s[i - 1 - j] for j in range(order)) + (sol[-1] if const else 0) == s[i] for i in range(order, len(s)))
        if ok:
            print(f"order {order}, constant={const}: coefficients {[str(c) for c in sol]}  (fits all {len(s)} terms, {len(s) - order - k} spare checks)")
            raise SystemExit
print("no recurrence of order <= 6 found")
