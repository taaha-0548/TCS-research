# Erdős problems: Lean 4 + Mathlib workspace (setup in progress)

- Mathlib `v4.24.0` (Lean 4.24.0), declared in `lakefile.toml`; dependencies resolved in `lake-manifest.json`.
- Status: dependencies fetched. The prebuilt Mathlib cache has not been downloaded yet: it needs the
  toolchain registered under its official name `leanprover/lean4:v4.24.0`, after which
  `lake exe cache get` should work.
- Plan: survey open problems on erdosproblems.com, pick candidates suited to proof by reasoning, and
  formalize any proof found here.
