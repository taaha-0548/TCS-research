/-
# Non-backtracking walks in graphs of maximum degree 2 never revisit a vertex

This is the abstract fact behind Thomason's algorithm (and behind Lemma 4 of the paper): the state
graph of the lollipop walk has maximum degree 2, the start state has degree 1, and the walk never
steps straight back. Hence it never revisits a state, so on a finite state space it terminates.
-/
namespace Lollipop

variable {S : Type}

/-- `E` has maximum degree 2: among any three neighbours of a vertex, two coincide. -/
def MaxDeg2 (E : S → S → Prop) : Prop :=
  ∀ s a b c, E s a → E s b → E s c → a = b ∨ a = c ∨ b = c

/-- A non-backtracking walk `x 0, x 1, …` in `E` from a vertex of degree at most 1, in a loopless
graph of maximum degree 2. -/
structure NBWalk (E : S → S → Prop) (x : Nat → S) : Prop where
  step : ∀ k, E (x k) (x (k + 1))
  symm : ∀ a b, E a b → E b a
  loopless : ∀ a, ¬ E a a
  deg2 : MaxDeg2 E
  start : ∀ a b, E (x 0) a → E (x 0) b → a = b
  nobacktrack : ∀ k, x (k + 2) ≠ x k

/-- **No revisits.** -/
theorem NBWalk.injective {E : S → S → Prop} {x : Nat → S} (w : NBWalk E x) :
    ∀ j i, i < j → x i ≠ x j := by
  intro j
  induction j using Nat.strongRecOn with
  | _ j ih =>
  intro i hij heq
  -- `x (j-1)` is a neighbour of `x j = x i`
  obtain ⟨j', rfl⟩ : ∃ j', j = j' + 1 := ⟨j - 1, by omega⟩
  have hprev : E (x j') (x i) := heq ▸ w.step j'
  cases i with
  | zero =>
    -- `x j'` and `x 1` are both neighbours of `x 0`
    have h1 : x j' = x 1 := w.start _ _ (w.symm _ _ hprev) (w.step 0)
    rcases Nat.lt_trichotomy j' 1 with h | h | h
    · -- j' = 0: then x 0 = x 1, a loop
      have : j' = 0 := by omega
      subst this
      exact w.loopless _ (heq ▸ w.step 0)
    · -- j' = 1: x 2 = x 0
      subst h
      exact w.nobacktrack 0 heq.symm
    · exact ih j' (by omega) 1 h h1.symm
  | succ i =>
    -- neighbours of `x (i+1)`: `x i`, `x (i+2)`, and `x j'`
    have ha : E (x (i + 1)) (x i) := w.symm _ _ (w.step i)
    have hb : E (x (i + 1)) (x (i + 2)) := w.step (i + 1)
    have hc : E (x (i + 1)) (x j') := w.symm _ _ hprev
    rcases w.deg2 _ _ _ _ ha hb hc with h | h | h
    · exact w.nobacktrack i h.symm
    · -- x j' = x i, and i < j'
      exact ih j' (by omega) i (by omega) h
    · -- x j' = x (i+2)
      rcases Nat.lt_trichotomy (i + 2) j' with h' | h' | h'
      · exact ih j' (by omega) (i + 2) h' h
      · -- j' = i + 2, so x (i+3) = x (i+1)
        subst h'
        exact w.nobacktrack (i + 1) heq.symm
      · -- j' = i + 1, so x (i+1) = x (i+2): a loop
        have : j' = i + 1 := by omega
        subst this
        exact w.loopless _ (h ▸ hb)

end Lollipop
