# Longer Thomason chains via 3-pole composition (draft manuscript)

**Claim.** 3-connected planar cubic graphs with exactly three Hamiltonian cycles on which Thomason's
lollipop algorithm takes Θ(ρ^{n/6}) = Θ(1.19742^n) steps, where ρ = 2.9477… is the largest root of
λ⁴ − 2λ³ − 2λ² − 2λ − 1. The previous best is Ω(1.1812^n) (Briański–Szady, Discrete Math. 2022).

## Files

| File | What it is |
|---|---|
| `paper.tex` | the complete manuscript, single self-contained file (14 pages); compile with `pdflatex paper.tex` three times |
| `paper.pdf` | compiled version |
| `verify.py` | standalone reproducibility script (standard library only, about 2 s): `python3 verify.py` (checks k ≤ 12, all of Table 1) |
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
5. ~~**Bibliography.**~~ Done (verification round 1): Zhong pages, DHHL venue (MCU 2022, LNCS 13419), Eppstein
   volume, IML problem collection added; DMSZ running time corrected to O(1.23103^n).
6. **Authors and disclosure.** Fill in the author block. Check the target venue's policy on
   AI-assisted research and disclose as it requires.
7. **Proofread** `paper.pdf` (compiled and visually checked; figures render correctly).

## Verification round 1 (October 2026)

Three independent checks, then fixes:
- **Independent referee reading** of all proofs: no error that breaks a proof. Fixed:
  - Lemma 4: "unique lift" became "unique type-A lift", with "every visit ends in type A".
  - Lemmas 5 and 7: restricted to visits that occur, with the occurrence argument made explicit.
  - Theorem 3: now states that the whole internal step sequence is host-independent.
  - Lemma 6: wording of the 3-edge-connectivity argument.
  - Perron argument separated from the rational certificates.
  - Notation: Θ(ρ^{n/6}) rather than Θ(1.19742^n).
- **Numbers:**
  - Corrected ρ^{1/6} = 1.1974227… (it previously read 1.197421…).
  - Table 3 now prints the 29477/10000 certificate.
  - `verify.py` checks both certificates and all of Table 1.
- **Search (Section 8):** the dedup was by spectrum, which can merge non-isomorphic graphs.
  - Re-run with exact isomorphism (`../smith-second-hamiltonian/.../scripts/search_iso.py`): 5, 17, 80, 474 Hamiltonian cubic graphs (the known counts).
  - At n = 14, three graphs had been dropped, but none has exactly 3 Hamiltonian cycles. Results unchanged.
  - The abstract's claim is now scoped to simple-pole nestings.
- **Literature (search snippets only; full texts blocked here):**
  - No result beating 1.1812^n found; BKN 2024 still cites it as the best.
  - The Briański–Szady class is the same as ours (3-connected planar cubic, exactly three Hamiltonian cycles).
  - Items 1–3 above still need a full-text check by the author.

## Suggested venues

arXiv (math.CO with cross-list cs.DM) first; then *Discrete Mathematics* (where Briański–Szady
appeared), *Electronic Journal of Combinatorics*, or *Information Processing Letters* for a short
version.
