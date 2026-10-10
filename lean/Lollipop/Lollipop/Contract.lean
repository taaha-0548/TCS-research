/-
# Contracting a vertex set commutes with rotation

`X : V → Bool` marks the vertices of a 3-pole. Contracting `X` to a single vertex `x` maps a sequence
of vertices to a sequence over `Option V` (`none` is `x`): each maximal block of consecutive
`X`-vertices becomes one `none`. This is the map `π` of the Mirror Lemma, up to the treatment of a
trailing block.

Main result, `collapse_rot`: if neither the deleted edge `w s` nor the added edge `z w` has both
ends in `X`, then contracting after the rotation is the same as rotating after contracting, at the
image of `w`. This is the principle used in every case of the Mirror Lemma ("contracting a
contiguous block commutes with reversing a suffix, provided the cut point is not inside the
block").
-/
import Lollipop.Rotation

namespace Lollipop

variable {V : Type} (X : V → Bool)

/-- Image of a vertex in the contracted graph. -/
def img (v : V) : Option V := if X v then none else some v

/-- Contract every maximal block of consecutive `X`-vertices to one `none`. -/
def collapse : List V → List (Option V)
  | [] => []
  | [v] => [img X v]
  | v :: w :: l => if X v && X w then collapse (w :: l) else img X v :: collapse (w :: l)

/-- `l` starts with an `X`-vertex. -/
def headX (l : List V) : Bool := match l.head? with | some v => X v | none => false
/-- `l` ends with an `X`-vertex. -/
def lastX (l : List V) : Bool := match l.getLast? with | some v => X v | none => false

theorem collapse_cons (v : V) (l : List V) :
    collapse X (v :: l) = if X v && headX X l then collapse X l else img X v :: collapse X l := by
  cases l with
  | nil => simp [collapse, headX]
  | cons w l => simp [collapse, headX]

theorem collapse_eq_nil {l : List V} : collapse X l = [] ↔ l = [] := by
  induction l with
  | nil => simp [collapse]
  | cons v l ih =>
    rw [collapse_cons]
    cases l with
    | nil => simp [collapse, headX]
    | cons w l' =>
      split
      · simp [ih]
      · simp

/-- The contraction of `l` starts with `none` exactly when `l` starts in `X`. -/
theorem collapse_head_none (l : List V) :
    (collapse X l).head? = some none ↔ headX X l = true := by
  induction l with
  | nil => simp [collapse, headX]
  | cons v l ih =>
    rw [collapse_cons]
    by_cases h : (X v && headX X l) = true
    · rw [if_pos h, ih]
      simp at h
      have e : headX X (v :: l) = true := by simp [headX, h.1]
      exact ⟨fun _ => e, fun _ => h.2⟩
    · rw [if_neg h]
      simp [img, headX]

theorem collapse_cons_of_head_none {l : List V} (h : headX X l = true) :
    collapse X l = none :: (collapse X l).tail := by
  have := (collapse_head_none X l).mpr h
  cases hc : collapse X l with
  | nil => rw [hc] at this; simp at this
  | cons c r => rw [hc] at this; simp at this; simp [this]

/-- **Contraction of a concatenation.** The two contracted pieces are glued, merging one `none`
when both sides of the junction lie in `X`. -/
theorem collapse_append (A B : List V) :
    collapse X (A ++ B) =
      if lastX X A && headX X B then collapse X A ++ (collapse X B).tail
      else collapse X A ++ collapse X B := by
  induction A with
  | nil => simp [lastX, collapse]
  | cons v A ih =>
    cases A with
    | nil =>
      rw [List.singleton_append, collapse_cons]
      simp only [lastX, List.getLast?_singleton, collapse]
      by_cases h : (X v && headX X B) = true
      · rw [if_pos h, if_pos h]
        simp at h
        rw [collapse_cons_of_head_none X h.2]
        simp [img, h.1]
      · rw [if_neg h, if_neg h]; simp
    | cons w A' =>
      have hl : lastX X (v :: w :: A') = lastX X (w :: A') := by
        simp [lastX, List.getLast?_cons_cons]
      have hh : headX X ((w :: A') ++ B) = X w := by simp [headX]
      rw [List.cons_append, collapse_cons, hh, ih, hl]
      simp only [collapse]
      by_cases h1 : (X v && X w) = true <;> by_cases h2 : (lastX X (w :: A') && headX X B) = true <;>
        simp [h1, h2]

theorem lastX_reverse (l : List V) : lastX X l.reverse = headX X l := by
  simp [lastX, headX, List.getLast?_reverse]

theorem headX_reverse (l : List V) : headX X l.reverse = lastX X l := by
  simp [lastX, headX, List.head?_reverse]

/-- **Contraction commutes with reversal.** -/
theorem collapse_reverse (l : List V) : collapse X l.reverse = (collapse X l).reverse := by
  induction l with
  | nil => simp [collapse]
  | cons v l ih =>
    rw [List.reverse_cons, collapse_append, ih, lastX_reverse]
    have h1 : headX X [v] = X v := by simp [headX]
    have h2 : collapse X [v] = [img X v] := rfl
    rw [h1, h2, collapse_cons X v l]
    by_cases h : (X v && headX X l) = true
    · have h' : (headX X l && X v) = true := by simp at h ⊢; exact ⟨h.2, h.1⟩
      rw [if_pos h', if_pos h]; simp
    · have h' : ¬ (headX X l && X v) = true := by
        simp at h ⊢; intro a
        cases hv : X v
        · rfl
        · simp [h hv] at a
      rw [if_neg h', if_neg h]; simp

/-- Rotation of a concatenation at the last index of the first piece. -/
theorem rot_append (A B : List V) (hA : A ≠ []) :
    rot (A ++ B) (A.length - 1) = A ++ B.reverse := by
  have h : A.length - 1 + 1 = A.length := by
    cases A with
    | nil => exact absurd rfl hA
    | cons _ _ => simp
  unfold rot
  rw [h, List.take_left' rfl, List.drop_left' rfl]

/-- **Block contraction commutes with rotation.** Split `P` after `w = P[i]` into `A ++ B` (so `B`
starts with `s` and ends with `z`). If `w` and `s` are not both in `X`, and `w` and `z` are not
both in `X`, then contracting the rotated path equals rotating the contracted path at the image
of `w`. -/
theorem collapse_rot (P : List V) (i : Nat) (hi : i + 1 < P.length)
    (hws : ¬ (lastX X (P.take (i + 1)) = true ∧ headX X (P.drop (i + 1)) = true))
    (hwz : ¬ (lastX X (P.take (i + 1)) = true ∧ lastX X (P.drop (i + 1)) = true)) :
    collapse X (rot P i) =
      rot (collapse X P) ((collapse X (P.take (i + 1))).length - 1) := by
  have hA : collapse X (P.take (i + 1)) ≠ [] := by
    rw [Ne, collapse_eq_nil]; intro h
    rw [List.take_eq_nil_iff] at h
    rcases h with h | h
    · omega
    · subst h; simp at hi
  have hP : collapse X P = collapse X (P.take (i + 1)) ++ collapse X (P.drop (i + 1)) := by
    conv => lhs; rw [← List.take_append_drop (i + 1) P]
    rw [collapse_append]
    have : (lastX X (P.take (i + 1)) && headX X (P.drop (i + 1))) = false := by
      cases h1 : lastX X (P.take (i + 1)) <;> cases h2 : headX X (P.drop (i + 1)) <;> simp_all
    rw [this]; simp
  rw [hP, rot_append _ _ hA]
  unfold rot
  rw [collapse_append, headX_reverse, collapse_reverse]
  have : (lastX X (P.take (i + 1)) && lastX X (P.drop (i + 1))) = false := by
    cases h1 : lastX X (P.take (i + 1)) <;> cases h2 : lastX X (P.drop (i + 1)) <;> simp_all
  rw [this]; simp

end Lollipop
