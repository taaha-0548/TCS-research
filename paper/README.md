# Longer Thomason chains via 3-pole composition (draft manuscript)

**Claim.** 3-connected planar cubic graphs with exactly three Hamiltonian cycles on which Thomason's
lollipop algorithm takes Θ(ρ^{n/6}) = Θ(1.19742^n) steps, where ρ = 2.9477… is the largest root of
λ⁴ − 2λ³ − 2λ² − 2λ − 1. The previous best is Ω(1.1812^n) (Briański–Szady, Discrete Math. 2022).

## Files

| File | What it is |
|---|---|
| `paper.tex` | the complete manuscript, single self-contained file (13 pages); compile with `pdflatex paper.tex` three times |
| `paper.pdf` | compiled version |
| `verify.py` | standalone reproducibility script (standard library only, under 1 s): `python3 verify.py 10` |
| `verify_output.txt` | output of the last run (ALL CHECKS PASSED) |
| `gen_paper_data.py`, `gen_tables.py` | regenerate the integer certificate, the step table, the appendix tables (`tab_visits.tex`, `tab_trace.tex`) and `paper_data.json` from the definitions in `verify.py` |

The research history, independent audits (A1–A8) and exploratory code are in
`../smith-second-hamiltonian/` (see `references/composition-proof.md`, section 7).

## Before showing this to reviewers (author checklist)

These could not be done from the research environment (paper sites were blocked):

1. **Literature, full text.** Read Briański–Szady (arXiv:1903.02515) and confirm:
   - their bound is Ω(1.1812^n) for the same notion of "steps" (a ±1 difference in counting is
     harmless; a different notion, e.g. counting Hamiltonian cycles, is not);
   - the exact wording of their open question about faster-growing families (the abstract and
     introduction cite it);
   - their family's class (3-connected planar; exactly 3 Hamiltonian cycles?) to phrase the
     comparison accurately.
2. **No newer record.** On Google Scholar, check "cited by" for Briański–Szady and for Cameron 2001,
   and search arXiv for "Thomason" / "lollipop" from 2022 onwards.
3. **Prior use of the method.** Skim Krawczyk 1999, Cameron 2001, Zhong 2018, and Thomassen's
   reduction to cyclically 4-edge-connected graphs (cited by Zhong) for arguments like the Mirror
   Lemma. If they exist, cite them and present ours as a sharpening or generalisation.
4. **Independent reading.** Have one person read Sections 3–5 (Mirror Lemma, Transducer Theorem,
   Lemmas 4–5) line by line, and replay two or three rows of the appendix by hand.
5. **Bibliography.** Fill in the entries marked `% TODO verify` (Zhong pages; DHHL venue).
6. **Authors and disclosure.** Fill in the author block. Check the target venue's policy on
   AI-assisted research and disclose as it requires.
7. **Proofread** `paper.pdf` (compiled and visually checked; figures render correctly).

## Suggested venues

arXiv (math.CO with cross-list cs.DM) first; then *Discrete Mathematics* (where Briański–Szady
appeared), *Electronic Journal of Combinatorics*, or *Information Processing Letters* for a short
version.
