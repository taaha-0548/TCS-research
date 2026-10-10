/-
# Paths as chains, and the rotation keeps a path a path
-/
import Lollipop.Rotation

namespace Lollipop

variable {V : Type}

/-- `Chain R l`: consecutive entries of `l` are related by `R` (a walk in the graph `R`). -/
def Chain (R : V → V → Prop) : List V → Prop
  | [] => True
  | [_] => True
  | a :: b :: l => R a b ∧ Chain R (b :: l)

@[simp] theorem chain_nil (R : V → V → Prop) : Chain R [] := trivial
@[simp] theorem chain_singleton (R : V → V → Prop) (a : V) : Chain R [a] := trivial
@[simp] theorem chain_cons_cons (R : V → V → Prop) (a b : V) (l : List V) :
    Chain R (a :: b :: l) ↔ R a b ∧ Chain R (b :: l) := Iff.rfl

theorem chain_cons (R : V → V → Prop) (a : V) (l : List V) :
    Chain R (a :: l) ↔ (∀ y ∈ l.head?, R a y) ∧ Chain R l := by
  cases l with
  | nil => simp
  | cons b l => simp

theorem chain_append (R : V → V → Prop) (l₁ l₂ : List V) :
    Chain R (l₁ ++ l₂) ↔
      Chain R l₁ ∧ Chain R l₂ ∧ ∀ x ∈ l₁.getLast?, ∀ y ∈ l₂.head?, R x y := by
  induction l₁ with
  | nil => simp
  | cons a l₁ ih =>
    cases l₁ with
    | nil =>
      simp only [List.nil_append, List.cons_append, List.getLast?_singleton, Option.mem_def,
        Option.some.injEq, forall_eq', chain_singleton, true_and]
      rw [chain_cons]; exact And.comm
    | cons b l₁ =>
      simp only [List.cons_append, chain_cons_cons] at ih ⊢
      rw [ih]
      have : (a :: b :: l₁).getLast? = (b :: l₁).getLast? := by simp [List.getLast?_cons_cons]
      rw [this]
      constructor
      · rintro ⟨h1, h2, h3, h4⟩; exact ⟨⟨h1, h2⟩, h3, h4⟩
      · rintro ⟨⟨h1, h2⟩, h3, h4⟩; exact ⟨h1, h2, h3, h4⟩

theorem chain_reverse {R : V → V → Prop} (hR : ∀ a b, R a b → R b a) :
    ∀ l : List V, Chain R l → Chain R l.reverse
  | [] , _ => trivial
  | [_], _ => trivial
  | a :: b :: l, ⟨hab, h⟩ => by
    have ih := chain_reverse hR (b :: l) h
    rw [List.reverse_cons]
    rw [chain_append]
    refine ⟨ih, trivial, ?_⟩
    intro x hx y hy
    simp at hy; subst hy
    simp [List.getLast?_reverse] at hx; subst hx
    exact hR _ _ hab

theorem chain_take_drop {R : V → V → Prop} {l : List V} (h : Chain R l) (n : Nat) :
    Chain R (l.take n) ∧ Chain R (l.drop n) := by
  rw [← List.take_append_drop n l, chain_append] at h
  exact ⟨h.1, h.2.1⟩

/-- **The rotation keeps a path a path.** If `P` is a walk in a symmetric graph `adj`, `z` is
its last vertex and `adj z P[i]`, then `rot P i` is again a walk. -/
theorem rot_chain {adj : V → V → Prop} (hsym : ∀ a b, adj a b → adj b a)
    {P : List V} (hP : Chain adj P) {i : Nat} (hi : i + 1 < P.length)
    {z : V} (hz : P.getLast? = some z) (hzw : adj z P[i]) :
    Chain adj (rot P i) := by
  obtain ⟨h1, h2⟩ := chain_take_drop hP (i + 1)
  unfold rot
  rw [chain_append]
  refine ⟨h1, chain_reverse hsym _ h2, ?_⟩
  intro x hx y hy
  have hx' : x = P[i] := by
    rw [List.getLast?_take] at hx
    simp at hx
    rcases hx with hx | ⟨hl, _⟩
    · rw [List.getElem?_eq_getElem (by omega : i < P.length)] at hx; simpa using hx.symm
    · omega
  have hy' : y = z := by
    rw [List.head?_reverse, List.getLast?_drop] at hy
    simp at hy
    rw [hz] at hy; simpa using hy.2.symm
  subst hx' hy'
  exact hsym _ _ hzw

end Lollipop
