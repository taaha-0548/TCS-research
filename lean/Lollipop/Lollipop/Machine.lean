/-
# Recursive bounce machines (towers of 3-pole gadgets)

Abstract model of a tower `P_1 = P'[x ← P_2], P_2 = P'[x ← P_3], …`. By the Transducer Theorem,
a visit to a level is a finite interaction: the level's internal walk makes *calls* (passages
through the slot `x`, each with a visit type `e : E`) to the level below, each answered
`true` (transmit) or `false` (reflect), and finally *returns* an outcome and a new local state.
The parent uses only the answer, since the exit port follows from it.

* `Proc E S`: a local procedure, as a finite decision tree.
* `IGadget E σ`: an automaton `σ → E → outcome × new state × flag`. The flag records that every
  nested call, at every depth, transmitted.
* `compose δ child`: the gadget `P'[x ← child]`, with state `S × σ`.
* `tower δ base d`: depth-`d` tower.

Main results (all proved):
* `tower_TDown` (**Lemma L1**): if every local procedure has the property `RForcesR` (after a
  reflecting answer, every reachable return reflects), then in every tower built from it, over
  any base, a transmitting visit makes only transmitting calls at every depth.
* `run_of_ok`, `run_child_of_ok` (**Lemma L2**): in a visit whose calls all transmit, the outcome
  and new local state are those of the all-transmit branch, which depends only on the local state
  and the entry type. The child is acted on by the fixed *call word* of that branch. So the
  transmitting dynamics is a functionally recursive self-similar action
  `g_e (s, c) = (s', w_{s,e} · c)`.
-/
namespace Lollipop.RBM

/-- A local procedure: call the child with a visit type and branch on its answer, or return an
outcome (`true` = transmit) with a new local state. -/
inductive Proc (E S : Type) where
  | ret (o : Bool) (s : S) : Proc E S
  | call (e : E) (k : Bool → Proc E S) : Proc E S

/-- An instrumented gadget: outcome, new state, and the flag "all nested calls transmitted". -/
abbrev IGadget (E σ : Type) := σ → E → Bool × σ × Bool

variable {E S σ : Type}

/-- Run a procedure against a child gadget. Returns outcome, new local state, new child state and
the flag "every answer was transmit and every child call had its flag set". -/
def Proc.run (child : IGadget E σ) : Proc E S → σ → Bool × S × σ × Bool
  | .ret o s, c => (o, s, c, true)
  | .call e k, c =>
    let r := child c e
    let t := (k r.1).run child r.2.1
    (t.1, t.2.1, t.2.2.1, r.1 && r.2.2 && t.2.2.2)

/-- `P'[x ← child]`. -/
def compose (δ : S → E → Proc E S) (child : IGadget E σ) : IGadget E (S × σ) :=
  fun q e =>
    let t := (δ q.1 e).run child q.2
    (t.1, (t.2.1, t.2.2.1), t.2.2.2)

/-- Every reachable return reflects. -/
def Proc.AllRetsR : Proc E S → Prop
  | .ret o _ => o = false
  | .call _ k => ∀ a, (k a).AllRetsR

/-- After any reflecting answer, every reachable return reflects. -/
def Proc.RForcesR : Proc E S → Prop
  | .ret _ _ => True
  | .call _ k => (k false).AllRetsR ∧ (k true).RForcesR

/-- A gadget has property T-down if every transmitting visit has its flag set. -/
def TDown (G : IGadget E σ) : Prop := ∀ q e, (G q e).1 = true → (G q e).2.2 = true

theorem run_of_AllRetsR (child : IGadget E σ) :
    ∀ (p : Proc E S) (c : σ), p.AllRetsR → (p.run child c).1 = false
  | .ret o s, c, h => by simpa [Proc.run, Proc.AllRetsR] using h
  | .call e k, c, h => by
    simp only [Proc.run]
    exact run_of_AllRetsR child (k (child c e).1) _ (h _)

theorem run_TDown {child : IGadget E σ} (hc : TDown child) :
    ∀ (p : Proc E S) (c : σ), p.RForcesR → (p.run child c).1 = true → (p.run child c).2.2.2 = true
  | .ret o s, c, _, _ => by simp [Proc.run]
  | .call e k, c, hp, ho => by
    simp only [Proc.run] at ho ⊢
    cases ha : (child c e).1 with
    | false =>
      rw [ha] at ho
      rw [run_of_AllRetsR child (k false) _ hp.1] at ho
      exact absurd ho (by simp)
    | true =>
      rw [ha] at ho
      have hf : (child c e).2.2 = true := hc c e ha
      have ht := run_TDown hc (k true) _ hp.2 ho
      simp [hf, ht]

/-- **Lemma L1, one level.** `RForcesR` at every local procedure transfers T-down from the child
to the composed gadget. -/
theorem compose_TDown {δ : S → E → Proc E S} (hδ : ∀ s e, (δ s e).RForcesR)
    {child : IGadget E σ} (hc : TDown child) : TDown (compose δ child) := by
  intro q e ho
  exact run_TDown hc (δ q.1 e) q.2 (hδ q.1 e) ho

/-- State space of the depth-`d` tower over a base with state space `B`. -/
def TowerState (S B : Type) : Nat → Type
  | 0 => B
  | d + 1 => S × TowerState S B d

/-- The depth-`d` tower. -/
def tower (δ : S → E → Proc E S) {B : Type} (base : IGadget E B) :
    (d : Nat) → IGadget E (TowerState S B d)
  | 0 => base
  | d + 1 => compose δ (tower δ base d)

/-- **Lemma L1.** If every local procedure satisfies `RForcesR` and the base has T-down (e.g. a
base pole whose visits make no calls), then every tower has T-down: a transmitting visit makes
only transmitting calls, at every depth. -/
theorem tower_TDown {δ : S → E → Proc E S} (hδ : ∀ s e, (δ s e).RForcesR)
    {B : Type} {base : IGadget E B} (hb : TDown base) : ∀ d, TDown (tower δ base d)
  | 0 => hb
  | d + 1 => compose_TDown hδ (tower_TDown hδ hb d)

/-! ## Lemma L2: all-transmit visits act by a fixed call word -/

/-- Follow the all-transmit branch: outcome and new local state. -/
def Proc.allT : Proc E S → Bool × S
  | .ret o s => (o, s)
  | .call _ k => (k true).allT

/-- The calls made along the all-transmit branch. -/
def Proc.callWord : Proc E S → List E
  | .ret _ _ => []
  | .call e k => e :: (k true).callWord

/-- Apply a word of visits to a gadget state (ignoring outcomes). -/
def applyWord (G : IGadget E σ) : List E → σ → σ
  | [], c => c
  | e :: w, c => applyWord G w (G c e).2.1

/-- **Lemma L2 (local part).** If all calls transmitted, the outcome and new local state are
those of the all-transmit branch: they depend only on the local state and the entry type, not on
the child. -/
theorem run_of_ok (child : IGadget E σ) :
    ∀ (p : Proc E S) (c : σ), (p.run child c).2.2.2 = true →
      ((p.run child c).1, (p.run child c).2.1) = p.allT
  | .ret o s, c, _ => by simp [Proc.run, Proc.allT]
  | .call e k, c, h => by
    simp only [Proc.run, Bool.and_eq_true] at h ⊢
    obtain ⟨⟨ha, _⟩, ht⟩ := h
    rw [ha] at ht ⊢
    exact run_of_ok child (k true) _ ht

/-- **Lemma L2 (child part).** If all calls transmitted, the child is acted on by the call word
of the all-transmit branch. -/
theorem run_child_of_ok (child : IGadget E σ) :
    ∀ (p : Proc E S) (c : σ), (p.run child c).2.2.2 = true →
      (p.run child c).2.2.1 = applyWord child p.callWord c
  | .ret o s, c, _ => by simp [Proc.run, Proc.callWord, applyWord]
  | .call e k, c, h => by
    simp only [Proc.run, Bool.and_eq_true] at h ⊢
    obtain ⟨⟨ha, _⟩, ht⟩ := h
    rw [ha] at ht ⊢
    simp only [Proc.callWord, applyWord]
    exact run_child_of_ok child (k true) _ ht

/-- **Corollary (cascade).** In a tower with `RForcesR` and a T-down base, a transmitting top
visit at state `(s, c)` with entry `e` produces local state `(δ s e).allT.2` and child state
`applyWord child (δ s e).callWord c`. That is, transmitting visits act by the functionally recursive
self-similar rule `g_e (s, c) = (s', w_{s,e} · c)`. -/
theorem tower_transmit_selfsimilar {δ : S → E → Proc E S} (hδ : ∀ s e, (δ s e).RForcesR)
    {B : Type} {base : IGadget E B} (hb : TDown base) (d : Nat)
    (s : S) (c : TowerState S B d) (e : E)
    (ho : (tower δ base (d + 1) (s, c) e).1 = true) :
    (tower δ base (d + 1) (s, c) e).2.1 =
      ((δ s e).allT.2, applyWord (tower δ base d) (δ s e).callWord c) := by
  have hok := tower_TDown hδ hb (d + 1) (s, c) e ho
  simp only [tower, compose] at hok ⊢
  have h1 := run_of_ok (tower δ base d) (δ s e) c hok
  have h2 := run_child_of_ok (tower δ base d) (δ s e) c hok
  rw [h2]
  have : ((δ s e).run (tower δ base d) c).2.1 = (δ s e).allT.2 := by
    have := congrArg Prod.snd h1; simpa using this
  rw [this]

end Lollipop.RBM
