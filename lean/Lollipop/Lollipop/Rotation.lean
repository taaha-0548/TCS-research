/-
# The lollipop rotation as a list operation

A state of the lollipop walk is a Hamiltonian path `P = [v₀, v₁, …, z]`. A step at the endpoint `z`
along a non-path edge `zw`, where `w = P[i]`, produces

  `P' = P[0..i] ++ reverse P[i+1..]`

(add `zw`, delete `w s` with `s = P[i+1]`). This file proves the basic facts the walk relies on:
the rotation permutes the vertices, keeps the prefix up to `w`, is undone by rotating again at the
same index, ends at `s`, and keeps the sequence a path when `z w` is an edge.
-/
namespace Lollipop

variable {V : Type}

/-- Rotation of `P` at index `i`: keep `P[0..i]`, reverse the rest. -/
def rot (P : List V) (i : Nat) : List V :=
  P.take (i + 1) ++ (P.drop (i + 1)).reverse

theorem rot_perm (P : List V) (i : Nat) : (rot P i).Perm P := by
  unfold rot
  calc (P.take (i + 1) ++ (P.drop (i + 1)).reverse).Perm (P.take (i + 1) ++ P.drop (i + 1)) :=
        List.Perm.append_left _ (List.reverse_perm _)
    _ = P := List.take_append_drop _ _

theorem rot_length (P : List V) (i : Nat) : (rot P i).length = P.length :=
  (rot_perm P i).length_eq

theorem rot_nodup {P : List V} (h : P.Nodup) (i : Nat) : (rot P i).Nodup :=
  (rot_perm P i).nodup_iff.mpr h

theorem rot_mem {P : List V} {i : Nat} {v : V} : v ∈ rot P i ↔ v ∈ P :=
  (rot_perm P i).mem_iff

/-- The prefix up to and including `w = P[i]` is unchanged. -/
theorem rot_take (P : List V) (i : Nat) : (rot P i).take (i + 1) = P.take (i + 1) := by
  unfold rot
  by_cases h : i + 1 ≤ P.length
  · rw [List.take_append_of_le_length (by simp [List.length_take]; omega)]
    simp [List.take_take]
  · have : P.drop (i + 1) = [] := List.drop_eq_nil_of_le (by omega)
    simp [this, List.take_take]

theorem rot_drop (P : List V) (i : Nat) : (rot P i).drop (i + 1) = (P.drop (i + 1)).reverse := by
  unfold rot
  by_cases h : i + 1 ≤ P.length
  · rw [List.drop_append_of_le_length (by simp [List.length_take]; omega)]
    have : (P.take (i + 1)).length = i + 1 := by simp [List.length_take]; omega
    simp [List.drop_eq_nil_of_le (by omega : (P.take (i + 1)).length ≤ i + 1)]
  · have : P.drop (i + 1) = [] := List.drop_eq_nil_of_le (by omega)
    simp [this]

/-- Rotating twice at the same index gives back the original path (the state graph is
undirected: the rotation of `P'` along `s w` is `P`). -/
theorem rot_rot (P : List V) (i : Nat) : rot (rot P i) i = P := by
  show (rot P i).take (i + 1) ++ ((rot P i).drop (i + 1)).reverse = P
  rw [rot_take, rot_drop, List.reverse_reverse, List.take_append_drop]

/-- The new endpoint is `s = P[i+1]`. -/
theorem rot_getLast? (P : List V) (i : Nat) (h : i + 1 < P.length) :
    (rot P i).getLast? = P[i + 1]? := by
  have hne : (P.drop (i + 1)).reverse ≠ [] := by simp; omega
  simp only [rot, List.getLast?_append, List.getLast?_reverse, List.head?_drop]
  cases hp : P[i + 1]? with
  | none => simp at hp; omega
  | some v => simp

end Lollipop
