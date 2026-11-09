# Which Recursions Are Series? Conditions, Information Loss, and a Bounded Correspondence to Productivity

> **Status: working draft requiring revision.** This upload preserves the reviewed body text. Known mathematical-exposition errors, bilingual differences, and a missing literature-check file remain unresolved; see the [review report (Chinese)](../reviews/check-2026-11-09.md).

*English working draft · v1.0 · 2026-11-09 · Recursion and Series research group*
*Chinese version: [`essay_final.md`](essay_final.md). The editions are not yet synchronized; known differences and substantive errors are recorded in the review.*

> **Label convention.** Each assertion carries a label:
> **[proved]** a complete proof given in the text; **[example]** a finite, runnable instance (reproducible with `fold_checks.py` or `propositions_checks.py`), never a substitute for proof; **[conjecture]** a working hypothesis with no proof, not a conclusion; **[literature]** an established result, not claimed as ours; **[open]** an explicit blank we do not claim to fill.

---

## Abstract

We take the familiar intuition that "a recursion is just a finite series" and ask where exactly it holds. The result has three layers: a **methodological correction** (saying "recursion is folding" only relabels; it adds no explanation), a **presentational contribution** (a classification table that records not the type of recursion but *what is lost when it is linearised*; the organisation is ours, every mathematical row belongs to existing frameworks [L1]), and a **bounded correspondence** to productivity (finite series placed side by side with stream productivity, with the general coinduction question explicitly left open and no originality claimed). Three propositions carry the mathematical weight: **Prop. 1** gives the finite-sum representation over a commutative additive monoid, with a counterexample; **Prop. 2** (= Proposition A) proves ordered-tree aggregation for any monoid, and explains why "commutativity is needed" is a common misreading; **Prop. 3** (= Proposition B) proves that additive aggregation over a shared DAG must carry path multiplicities — which is why memoisation reduces recomputation without changing repeated contribution.

> Label note: every substantive assertion in this abstract is developed in §1–§7 with a `[proved]` / `[example]` / `[open]` tag; no new assertion is introduced here.

**Keywords**: recursion; finite series; fold; monoid; path multiplicity; productivity; unfold

---

## 1 The research question

The question starts from a detail. Writing `sum_to(n)`, what comes to mind is `n + (n-1) + … + 1`: each call "takes out" one term and hands the rest to the next layer. The picture looks very much like the partial sums of a series.

The source research already corrected this once: *"single-chain additive recursion can be exactly represented as a finite sum; multiplication, concatenation and branching recursion keep their own operations and structures."* The correction is right, but it answers only half the question. It gives a **sufficient condition** and does not say:

> **Under what conditions can a recursive computation be compressed into a linear aggregate? What is preserved, and what is discarded?**

That is the main question of this essay. It is more testable than "is recursion a series?", because it demands **conditions**, **counterexamples** and a **list of losses** — three things that can be refuted. [open]

We do **not** claim that the correspondence between `foldr` on lists and a particular structural recursion pattern, nor catamorphism as its type-level version, is our contribution. Both are standard results in programming-language theory [L1], and fold being uniquely determined by its defining equation (the universality property) is tutorial-level material [L3]. We use them as a **methodological contrast**: renaming something does not mean we have learned something.

### 1.1 Why this question deserves a separate treatment

"Recursion is a series" is not an isolated misconception; it is a natural mental model. The unfolding of a recursion really does consist of a queue of terms revealed one at a time, and partial sums really are "accumulate term by term". In the mind the two are almost the same picture.

The problem is that the picture is **exactly right in a very useful special case** — chains, with addition — and therefore it generalises itself automatically. The cost of that generalisation is not getting one answer wrong but losing **judgement**: when the algorithm becomes tree-shaped, memoised, or combines with a non-commutative operation, people reason with the wrong justification for why it still works or why it no longer does. Our aim is to replace that intuition with an explicit list of conditions.

Three concrete questions follow, and they are the three threads of the essay:

1. **When can compression happen?** Under what conditions does a recursive computation equal a linear aggregate (Prop. 1, Prop. 2)?
2. **What does compression lose?** Which invariants are given up during the move, and can other information restore them (the table in §4)?
3. **Where does the infinite side correspond?** Are "producing the terms" and "these terms having a sum" the same thing (§7)?

Each question has a definite answer form: the first two are answered by propositions and counterexamples, the third by a definition and a prohibition.

---

## 2 Methodological correction: why "recursion is folding" does not do explanatory work

Start from the statement most likely to stop a reader:

> single-chain additive recursion is a finite sum → the general case is folding → so recursion is "unfold the structure, then fold it back".

**Step one: "is a finite sum" must be narrowed.** Prop. 1 says: **if** the recursion is **chain**-shaped (at most one recursive sub-call per layer), the combining operation is `+`, **and** the program actually satisfies the recurrence and exact algebraic hypotheses of Prop. 1 (`(M,+,0)` a commutative additive monoid, base case returning `c`), **then** it can be written as a finite sum. Note that "looks like a chain with a plus sign" is not itself a guarantee: the conditions are about the algebra and the recurrence form, not about the shape of the source code. This is a **sufficient condition, not a necessary one** — changing the operation gives products or concatenations, and adding branching can still yield a finite sum (Prop. 2 in §5 is exactly the latter case). The two conditions are independent, but "satisfying them is enough" does not mean "failing them is impossible". [proved]

**Step two: restating one case as a general explanation adds no knowledge.** A right fold on lists satisfies `F([]) = e` and `F(x:xs) = x ⊗ F(xs)`; a right-nested chain recursion satisfies `G(0) = e` and `G(n) = a_n ⊗ G(n-1)`. They are two spellings of the same object [literature]. So within **this specific case**, "recursion is folding" merely rewrites a definition and adds no new testable content; and presenting it as "the general essence of recursion" **goes beyond what can be supported here** — we neither have proved, nor intend to prove, that it holds for all recursions.

We should be careful about scope: from "one list structural recursion can be rewritten with `foldr`" it does **not** follow that "every recursion is a fold". For this language, for effectful programs, and for non-structural recursion (the last row of the table in §4), separate conditions are needed. We claim no such negative result, and no theorem of the form "folding ≡ primitive recursion". [open]

What we do claim is much weaker and sufficient: **restating "the laws of recursion" as "the laws of folding" adds no new falsifiable content within the list–monoid case.** It is therefore a good framework for teaching and writing, and not something to sell as a research contribution.

This whole passage is **our view, not a theorem**: that a fold is uniquely determined by its recursive equation (universality) is established tutorial-level material [L3]; our point is only that within the list–monoid case the restatement yields no new falsifiable proposition. We do **not** claim or prove "folding holds for all recursion and therefore explains nothing", and we certainly do not generalise from one case to all cases. [open]

---

## 3 Finite sums: a sufficient condition and a counterexample

### 3.1 Proposition 1 (finite-sum representation over an additive monoid) [proved]

Let `(M, +, 0)` be a **commutative additive monoid** (`+` associative and commutative, `0` the unit; for example the additive parts of ℕ, ℤ, ℝ, or of any semiring or commutative ring). Let `F: ℕ → M` satisfy

```
F(0) = c,        F(n) = a_n + F(n-1)   (n ≥ 1),        a_k, c ∈ M.
```

Then for every non-negative integer `n`:

```
F(n) = c + Σ_{k=1}^{n} a_k.
```

**Proof (induction).** For `n = 0` the empty sum is defined as `0` and `F(0) = c`. Assume `F(m) = c + Σ_{k=1}^{m} a_k`. Then
`F(m+1) = a_{m+1} + F(m) = a_{m+1} + c + Σ_{k=1}^{m} a_k = c + Σ_{k=1}^{m+1} a_k`. ∎

**Which conditions the proof actually uses.** Only three: **associativity** of `+` (regrouping the brackets of `a_n + (a_{n-1} + …)`), **commutativity** of `+` (arranging the terms into `Σ`), and `0` as the **additive identity** (empty sum at `n = 0`). **No** additive inverse and **no** multiplicative structure is required.

Why a monoid rather than something richer: **the addition of a semiring is already commutative** ("non-commutative ring" refers to multiplication; its addition is still commutative). Hence the additive part of any semiring is itself a commutative additive monoid, and Prop. 1 holds on it directly, with no need for ring multiplication or additive inverses. As for the subtraction counterexamples in §3.4 and §5, each is stated in its own algebra — **the essay does not require every example to share one algebraic universe**, which is normal practice in conceptual writing: examples expose boundaries; they are not obliged to support a unified algebraic framework.

#### 3.1.1 What each step of the proof does

Unfolding the induction makes it easier to see what it relies on. Assume `F(m) = c + Σ_{k=1}^{m} a_k` and prove `F(m+1) = c + Σ_{k=1}^{m+1} a_k`.

Step 1: replace `F(m+1)` by `a_{m+1} + F(m)` using the recurrence. This step uses only the definition and is independent of any algebraic property.

Step 2: substitute the induction hypothesis into `F(m)`, giving `a_{m+1} + (c + Σ_{k=1}^{m} a_k)`. Note the brackets: the hypothesis supplies a single object whose boundary must be respected.

Step 3: **merge** `a_{m+1}` with the sum into one summand block. This is where the axioms are used — associativity lets `a_{m+1} + (c + X)` be rewritten as `(a_{m+1} + c) + X`, and commutativity lets `c` move to the front. If the operation is not associative, this step fails and leaves **bracket traces** (§3.4 and §5).

Step 4: obtain `c + Σ_{k=1}^{m+1} a_k`; induction is complete.

So the "secret" of Prop. 1 is not in the definition but in step 3: **the rearrangability of the expression**. This also explains why the same derivation fails for floating point — step 3 is not legal there (§3.4).

#### 3.1.2 Relation to "just compute it with a loop"

Another reading of Prop. 1: **chain-shaped additive recursion is equivalent to a loop, and the loop's value is that finite sum.** The equivalence is trivial numerically but not trivial when discussing whether an optimisation is safe. Turning a recursion into a loop, vectorising the loop, or handing the sum to a parallel library are all, at bottom, performing step-3 rearrangements; the legitimacy of the rearrangement is exactly what Prop. 1 encodes.

In other words, Prop. 1 is not only a mathematical exercise; it is the formal basis for "**why a sum may be reordered safely**". Rearrangement preserves semantics if and only if associativity and commutativity hold and there is no overflow or rounding. All later discussion of cost and alignment in this essay rests on that basis. [proved]

### 3.2 How strong is the sufficient condition, and where does it fail

Prop. 1 looks like nothing more than "substituting the recurrence repeatedly", but it delivers three things at once: an **equation**, a **proof**, and a **visible list of hypotheses**. That is useful in engineering: if a chain-shaped recursion satisfies these hypotheses, you may safely rewrite it as a loop, as a vectorised `sum`, or hand it to a maths library, without fear of semantic drift. Conversely, it tells you precisely when you may **not**.

Failure can occur in exactly four places:

**（a）The chain breaks.** As soon as one layer makes two or more recursive sub-calls, `F(n)` is no longer "a sum of a queue of `a_k`" but a **tree-shaped combination** of terms. A sum may still exist, but it is no longer the conclusion of Prop. 1 (see §5).

**（b）The operation changes.** Replace `+` by `×`, string concatenation or `max`, and the formula's shape may survive but the word "sum" no longer applies. The first two rows of the table in §4 are this case (they are contrast rows, not value-preserving transformations).

**（c）The operation's properties are lost.** Even if the form is still `+`, if the implemented addition is not associative (the commonest case being floating point, §3.4), the "brackets may be regrouped freely" that the inductive proof relies on does not hold.

**（d）The input leaves the domain.** Prop. 1 holds for every non-negative integer `n`; negative numbers, infinities, and implementations that do not terminate are outside it. This is not a technicality but the whole boundary of the theorem: it never claimed to cover infinite processes.

Put together, Prop. 1's position becomes clear: it is not "a property of recursion" but "a **certificate** for **a class of** recursions". That positioning drives everything that follows.

### 3.3 Residual computation versus the Lagrange remainder [proved]

One of the source research's core distinctions must be preserved explicitly in the text, not left to the reference list. For `0 ≤ r ≤ n`, unfolding only the first `r` layers gives

```
F(n) = Σ_{j=0}^{r-1} a_{n-j} + F(n-r).
```

Here `F(n-r)` is the **not-yet-unfolded subproblem**. It is part of an exact equation: the equation holds exactly, `F(n-r)` is merely "not yet evaluated". At `r = n` it evaluates to the base case `c` — **`c` need not be zero**; it is the value supplied by the termination condition, not a "vanishing remainder".

The Lagrange remainder of Taylor's theorem is, by contrast,

```
R_m(x) = f^{(m+1)}(ξ) / (m+1)! · (x - a)^{m+1},      ξ between a and x,
```

whose validity depends on smoothness conditions such as `f ∈ C^{m+1}` and the existence of derivatives. The two share the shape "whole = unfolded part + residual part" but share no substantive condition: `F(n-r)` involves no derivatives, needs no continuity, and is not an approximation error — it is the **exact** unfolded part.

**This distinction is conceptual clarification, not a new result of ours**; but it is an explicit goal of the study and is therefore stated as a conclusion in its own right, not as a footnote. [proved]

### 3.4 Counterexample: chain and `+` both preserved, associativity lost [example]

Is anything missing from Prop. 1's sufficient conditions? Consider **floating-point** addition. Chain recursion, a `+` operation, and commutativity of addition are all present, but IEEE 754 double precision **fails associativity**: `(0.1+0.2)+0.3 = 0.6000000000000001` while `0.1+(0.2+0.3) = 0.6`. This is not a failure of commutativity — for these three finite floats the reordered additions agree; what breaks is "brackets may be regrouped arbitrarily", the very step used in the proof. We make no claim here about all floating-point values, including `NaN`, `±inf` and signed zero (`nan == nan` is `False`; `inf + (-inf)` is `NaN`). [example]

### 3.5 From "certificate" to error analysis

Treating Prop. 1 as a certificate has a side benefit: it makes **error analysis** tractable. When condition (c) fails in a floating-point implementation, the question is not "does the equation still hold" but "by how much does it deviate". For a sum of `n` terms, worst-case rounding error grows linearly with the number of terms; in practice it is usually far below this bound, but "usually" is not a bound. Contrast this with the geometric series in §7.3: there the error `2^{-N}` is a **mathematical object** (the tail sum) with an exact expression, whereas floating-point error is not a tail sum but the **implementation's** deviation from a mathematical value. Both are called "error"; one is about series, the other about machines. The distinction reappears in §7 and is the same type of mistake as "residual computation ≠ Lagrange remainder". [open]

### 3.6 Worked example: why the same recursion admits three spellings

Consider the simplest chain accumulation. It admits at least three spellings, and Prop. 1 tells us they agree:

```python
# Spelling 1: right-nested (closest to the "series" intuition)
def f(n): return 0 if n == 0 else n + f(n - 1)

# Spelling 2: tail recursion (accumulator)
def g(n, acc=0): return acc if n == 0 else g(n - 1, acc + n)

# Spelling 3: explicit loop (closest to an implementation)
def h(n):
    acc = 0
    for k in range(n, 0, -1):
        acc += k
    return acc
```

They agree because all three compute `0 + 1 + … + n`, and `+` on integers is associative and commutative, so **rearrangement does not change the result**. Remove that premise and the three diverge: on floats, the three orders of `0.1 + 0.2 + 0.3` may differ in the last digit (§3.4); on non-commutative operations, most operations other than `max` forbid rearrangement.

The example shows something easily overlooked: **the equivalence of recursion, tail recursion and loops is not a syntactic fact but an algebraic one.** They may be rewritten into one another because the result depends on the axioms of the combining operation, not on the shape in which it was written. The "ordinary recursion → tail recursion" row of the table can therefore be read with more content: what it gives up is not the result but the freedom of evaluation order. [example]

---

## 4 Classification: what is lost when linearising (the spine)

This is the essay's **presentational contribution** (not a new theorem; see `lit-check.md` §2–§3). The table does not classify "types of recursion" but records, for each move in going from a recursive computation to a linear aggregate, **which invariant is broken**; every mathematical row belongs to existing frameworks [L1]. Each row has an executable check; the scripts are divided as follows: `fold_checks.py` covers the numeric, floating-point, DAG and productivity demonstrations; `propositions_checks.py` covers Props. 2 and 3 (23 tree shapes and 75 topologically numbered DAGs with 5421 weight assignments); `productive_series_checks.py` covers §7. The `factorial`, `repeat` and `tree_sum` cells currently exist **only as hand-computable equalities in the text** and are not yet in a script; coverage will be claimed once the code appendix supplies them.

**Table 1. Structural moves and information loss**

> Before reading, remember one thing: **the first two rows are contrast rows, not "value-preserving compression".** "Series → product" and "series → concatenation" change the **combining operation**, hence the meaning of the returned value (`120` and `"ababab"` are not two algorithms to the same problem but two different problems). From the third row on, the table handles moves at the **structural level** for the same kind of computation, comparing whether the value survives and what is given up. Reading the first two rows as "transformations that still give the same value" is the commonest misreading of this table. [open]

| Move | Call shape | Invariant lost | Invariant kept / gained | Check |
|---|---|---|---|---|
| series → product | chain → chain | combining operation changes from `+` to `×`, identity from `0` to `1`. **Not** an example of losing commutativity (integer multiplication is commutative too) | multiplicative structure of `n!` | `factorial(5) == 120` [example] |
| series → concatenation | chain → chain | commutativity (string concatenation is not commutative) | order is encoded in the value itself | `repeat("ab",3) == "ababab"` [example] |
| **chain → tree** (same preorder direction) | chain → tree | **the nesting position itself**: the result is shape-independent, but the traversal direction must stay fixed | equal multisets with fixed direction give the same sum under `+` (§5 corollary) | `tree_sum` on `1(2,3) == 6`; swapping left/right changes the preorder sequence [example] |
| tree sum → ordered aggregate | tree → list | brackets / tree shape | the preorder ordered product equals `S(T)` (Prop. 2, proof in §5) | 23 tree shapes all pass [example] |
| tree → DAG | tree → DAG | if the aggregation counts **each node once**, path multiplicity is lost; execution cost drops | the graph itself **retains** all path information; `F(n)` unchanged | diamond: multiplicity-weighted **16** vs per-node-once **11**; `fib(20)` **21891** vs **21** executions [example] |
| ordinary → tail recursion | chain → chain | any pending **arithmetic combination** at the call site | state made explicit, aligns with loops; **but CPython still keeps a frame per tail call and performs no tail-call elimination** | `tsum([1,2,3,4]) == 10` [example]; established results in [L4] |
| recursion → nested recursion | any | the recursion **does not directly fit** the list/tree substructure folding form of this essay (two parameters, nested calls) | nothing: the analogy stops here; **no** claim that no higher-order or richer encoding exists | `ack(2,3) == 9` [example] |

Three rows need separate comment.

**The "chain → tree" row determines the theoretical status.** The source correction — "a tree recursion can also have a finite sum" — is true and exposes Prop. 1's limit: **the conclusion holds while the hypothesis fails**, so Prop. 1 is a **certificate**, not a characterisation. [proved]

What a tree actually gives up is not indexability: the nodes of a finite tree can always be enumerated into a sequence, and indexing is no obstacle. What a tree gives up is **nesting structure**: `tree_sum` is independent of shape as long as the multiset of weights and the traversal direction are fixed (§5 corollary); but under a non-commutative operation such as string concatenation, changing the preorder sequence changes the result. The tree loses "which term sits at which level, next to which others" — **bracket information**, not "whether terms may be queued". [proved]

**The "tree sum → ordered aggregate" row answers the same-leaves-different-values counterexample, but the objects must first be distinguished.** Prop. 2 concerns **weighted node trees** (weights on nodes, shape affecting only grouping), whereas `(1-1)-1 = -1` and `1-(1-1) = 1` come from **operator expression trees**. The same leaves `[1,1,1]` do not determine the value, so leaf order plus the leaf list alone is insufficient — this refutes only the weak claim "reconstruct using leaves alone", and is neither an instance of Prop. 2 nor an impossibility proof for linear encodings. Prop. 2 does not settle expression-tree evaluation in general; it supplies the analogous result for weighted node trees. [example]

**The "ordinary → tail recursion" row is likewise not our discovery**: the difference between left and right folds, and accumulator/direct-style rewriting, have been treated systematically, with an equivalence condition stated in terms of left-permutativity, which is more general than associativity or commutativity [L4]. We use only commutative monoids (Prop. 3) and **do not involve permutativity**, so we do not cover L4's scope.

**The "tree → DAG" row is where memoisation really sits, and we must be precise about who loses what.** Memoisation does not change the returned value; it changes the **execution structure** (tree becomes DAG). The DAG itself **does not lose** path information — the number of root-to-node paths is determined by the graph and can simply be counted (Prop. 3). What is lost is a **wrong aggregation**: counting each node's contribution exactly once (for example "node count" or "unweighted node sum"). That number is in general not `F(r)`. The row should thus be read as "ignoring path multiplicity goes wrong", not "the DAG drops multiplicities".

### 4.5 How to read the table, and what it does not promise

The table is easily misread as "four types of recursion"; it is not. Each row describes **one move**: from an understood shape to a more general one, recording what is kept and what is given up. A single program can occupy several rows at once — a memoised Fibonacci is both "chain → tree" (the naive version) and "tree → DAG" (the memoised version). The table's role is not to classify programs but to supply **precise vocabulary when discussing compression**: when someone says "this optimisation just compresses the recursion into a fold", you can ask which row, and whether what was given up is order, brackets, or multiplicity.

The table also **promises nothing about performance**. Phrases such as "execution cost drops" and "aligns with loops" describe observable facts at the level of computational structure, not complexity analysis. Real cost depends on language, memory layout, compiler and data size; we assert no asymptotics. [open]

One more thing belongs in the text: **the organisation of the table is ours; every mathematical row is not.** Ordered tree + monoid → preorder aggregate is an instance of catamorphism on ordered binary trees [L1]; the difference between left and right folds and accumulator/continuation style rewriting have been treated systematically [L4]; path counting on DAGs is standard graph theory. Putting them together makes "compression" discussable row by row; it does not propose a new theorem. [open]

---

## 5 Proposition 2 (monoids: order suffices, commutativity is not needed)

The formal statement and proof in this section and in §6 are by Goupote (see `propositions_ab.md`); what follows is the compressed body text. The two must not diverge; if they do, `propositions_ab.md` governs.

### 5.1 Statement [proved]

Let `(M, ⊗, e)` be a monoid (`⊗` associative, `e` a two-sided identity). Every node of a finite ordered binary tree `T` carries a weight `w(v) ∈ M`:

```
S(∅)             = e
S(Node(w, L, R)) = w ⊗ (S(L) ⊗ S(R))
```

Let `pre(T)` be the list of weights obtained by root, left subtree preorder, right subtree preorder, with `fold([]) = e` and `fold([x] ++ xs) = x ⊗ fold(xs)`. Then

```
S(T) = fold(pre(T)).
```

### 5.2 Proof [proved]

**Lemma (list concatenation).** `fold(xs ++ ys) = fold(xs) ⊗ fold(ys)`.
*Proof.* For `xs = []` this is the left identity law. If `xs = x :: zs`, the induction hypothesis gives `x ⊗ (fold(zs) ⊗ fold(ys))`, which associativity rewrites as `(x ⊗ fold(zs)) ⊗ fold(ys)`. ∎

**Main proof (structural induction on trees).** Empty tree: both sides are `e`. In the inductive step, replace the subtrees' `S` by `fold(pre(L))` and `fold(pre(R))` and apply the concatenation lemma with the definition of `fold` to obtain `fold([w] ++ pre(L) ++ pre(R))`, i.e. `fold(pre(T))`. ∎

### 5.2.1 Premise by premise: why these and not others

**Why a monoid.** The proof uses the algebra twice: in the concatenation lemma, associativity of `⊗` rewrites `x ⊗ (fold(zs) ⊗ fold(ys))` as `(x ⊗ fold(zs)) ⊗ fold(ys)`; and when `xs = []`, the left identity law. **Commutativity is used nowhere**, because the node order is supplied by the preorder sequence and is not free. This is why "commutativity is needed" is a common misreading: it confuses "adding commutativity lets you shuffle the order" (true) with "the proof needs commutativity" (false).

**Why ordered trees.** Without a fixed left/right distinction (for example an unordered multi-way tree), the same tree can yield different weight sequences and the notation `fold(pre(T))` loses meaning. Ordering is not decoration; it is what makes "preorder" definable.

**Why trees and lists admit the same sentence.** Because preorder provides a map from trees to lists, and the proposition guarantees that `fold` of that map agrees with structural recursion on the tree. The proposition therefore shows that **a value-preserving path exists** between tree structural recursion and list folds, provided the operation is a monoid. The path is not the identity map: it does discard the tree shape, but the value survives.

**Why it cannot simply be extended to arbitrary structures.** For structures with sharing (DAGs), the preorder sequence is no longer unique and the same path may be walked several times; `fold(pre(T))` would over- or under-count. That is exactly the case of §6 and the substance of the "tree → DAG" row. [proved]

### 5.3 Conditions and boundaries [proved]

- **Only a sufficient condition, not a characterisation.** Commutativity is not necessary because nodes are ordered; **adding** commutativity gives a stronger sufficient condition — "`S(T)` depends only on the multiset of weights". This remains merely sufficient: particular weights or instances may happen to agree even over a non-commutative carrier, but that is not what the proposition guarantees. [proved]
- **The conclusion covers values only.** Not evaluation order, memory cost, or effect equivalence. [proved]
- **The same-leaves-different-values counterexample does not target Prop. 2.** `(1-1)-1 = -1` and `1-(1-1) = 1` both have leaves `[1,1,1]`, showing that leaf order with brackets discarded is insufficient to recover an expression tree's value; but that expression tree and Prop. 2's weighted node tree **are not the same object**, and the counterexample refutes a weak reconstruction claim rather than an instance of Prop. 2. [example]

### 5.4 Experiment [example]

`essay/propositions_checks.py` enumerates **all ordered binary tree shapes with at most four nodes** (23 shapes), comparing structural evaluation with the preorder aggregate, and verifies `rab ≠ rba` using string concatenation (a non-commutative monoid). Running `python3 essay/propositions_checks.py` prints `A: 23 ordered tree shapes passed; concatenation rab != rba`.

### 5.4.1 What "checking" by exhaustion can and cannot do

The A part enumerates all ordered binary tree shapes of at most four nodes — 23 of them (including the empty tree) — and compares structural evaluation with the preorder aggregate. What can this scale rule out?

**What it can rule out**: if the proposition were subtly reversed (for example "commutativity is required" or "preorder should be postorder"), counterexamples would almost certainly appear among 23 shapes, because four nodes already include enough left–right asymmetric shapes. **What it cannot rule out**: any generalisation to richer graph elements (multiple branching, labels, repeated weights). Enumeration **falsifies implementation errors at small scale**; it does not prove. The proof is in §5.2.

This is also our stance on reproducible experiments: the experiment **catches what was written wrongly**, the proof **establishes truth for all cases**. They are not interchangeable, but the conclusion is dubious without either. [example]

### 5.5 A cost extrapolation: why index-based aggregation is cheaper

Prop. 2 says only whether the value is right, but changing the way values are checked from "scan every element" to "pair by index" can change the constant factor dramatically. The clearest example is **non-zero counting**.

Take a sparse vector (`n` dimensions, only `k` non-zero components). Two ways to check:

- **Linear scan**: walk `n` positions checking each, cost `Θ(n)`, independent of `k`.
- **Non-adaptive focusing (NAF)**: walk only the `k` non-zero entries, cost `Θ(k)`.

When `k ≪ n` the latter is far faster — a technique used repeatedly in sparse matrices, inverted indexes and sparse feature vectors. Its correctness comes from Prop. 2: with a fixed traversal direction and `+` a commutative monoid, "add by position" and "add by index" give the same sum.

**The real value of the row** is this: the tree gives up nesting but keeps "combination is independent of position", and position-independence is exactly the premise of every index-based aggregation. Replace the combining operation with a non-commutative one (recording the first occurrence rather than counting), and the speedup vanishes — that is a different row. [example] (The algorithmic background is established engineering practice; no novelty is claimed.) [open]

### 5.6 Reconfirming traversal order

A corollary of Prop. 2 is easily overlooked: `S(T)` is independent of the traversal **starting point** (for a fixed direction) but not of the **direction**. Under left–right preorder, swapping the root's subtrees generally changes the result for non-commutative operations but not for commutative ones. The "chain → tree" row records this as "result independent of shape, but traversal direction must be fixed".

The practical form: when converting a tree aggregate into an ordered stream, **the traversal direction must be stated**, otherwise the conclusion is not reproducible. Many "tree sums are shape-independent" statements seem mysterious only because the two qualifiers — under which operation, in which direction — were omitted. [proved]

---

## 6 Proposition 3 (DAG aggregation must carry path multiplicities)

### 6.1 Statement [proved]

Let `G = (V, E)` be a **finite directed acyclic multigraph** with root `r`, keeping only nodes reachable from `r`; edges point from parent to child, and **parallel edges are counted separately**. Let `(M, +, 0)` be a **commutative monoid**, with local contribution `b(v) ∈ M` per node, and define uniquely in reverse topological order

```
V(v) = b(v) + Σ_{(v,u) ∈ E} V(u)          (0 for a node with no outgoing edge)
```

Let `m(v)` be the number of directed paths from `r` to `v` (the empty path gives `m(r) = 1`), and let `k·x` denote `k`-fold monoid addition (`0·x = 0`). Then

```
V(r) = Σ_{v ∈ V} m(v) · b(v).
```

### 6.2 Proof (reverse topological induction) [proved]

For any node `u`, let `p_u(v)` be the number of paths from `u` to `v`, zero if unreachable. First prove by reverse topological induction that

```
V(u) = Σ_v p_u(v) · b(v).
```

A terminal node has only the empty path to itself, so the claim holds. For a general node, substitute the induction hypotheses of all children; **commutativity and associativity** allow contributions to be gathered by `v`. On the other hand every non-empty path from `u` to `v` has a unique first edge, so `p_u(v) = 1_{u=v} + Σ_{(u,z) ∈ E} p_z(v)`, with parallel edges counted separately. Both sides agree, giving the equation; taking `u = r` yields the result. ∎

### 6.3 Conditions and boundaries [proved]

- **No multiplication or ring structure required**, only a commutative monoid. (Compared with Prop. 2, the input structures differ, so no overall ranking of assumption strength is made.)
- **The proof does not apply to non-commutative combining operations**: grouping by node reorders contributions and `Σ` cannot be gathered freely.
- **Not directly applicable to cyclic graphs**: the premise of topological induction disappears; a fixed-point theory would be needed, which is outside our scope. [open]
- **"Depth" is likewise not guaranteed.** `V(v)=b(v)+Σ V(u)` relies on reverse topological order for a unique solution; a local form such as `V(v)=b(v)+max_u V(u)` is another algebra (the max monoid), and the proposition does not cover arbitrary non-linear combinations.
- **Value preservation under memoisation needs premises.** "Memoisation does not change the returned value" refers to **pure functions with correct cache keys and no invalidation**; with side effects, external state, or faulty key design, the cache changes results and Prop. 3 does not apply.

### 6.4 Where memoisation really sits [proved]

Memoisation evaluates each node **once** (improving efficiency), but its contribution still enters `V(r)` **with multiplicity `m(v)`** — these are two different numbers and cannot cancel. This presupposes purity, correct keys and no invalidation (§6.3, last item).

`m(v)` is the **number of root-to-node paths**, i.e. the coefficient of the node in the value formula `V(r) = Σ m(v)·b(v)`; it is **not** the number of times the node's value is read at runtime. How often a cached value is read depends on graph structure and access order; it is not generally equal to `m(v)`, and the two cannot serve as each other's counting unit (in the graph model each has a definite structural relation; we do not claim they are unrelated). The `fib(20)` comparison shows only "evaluation count drops while the returned value is unchanged": naive recursion executes its body **21891** times, memoised **21** times, both returning `F(20) = 6765`. [example] (Counting unit: actual body executions, not wrapper calls.)

### 6.5 Experiment [example]

`essay/propositions_checks.py`, diamond case: edges `r→a, r→b, a→c, b→c`, contributions `b(r)=1, b(a)=2, b(b)=3, b(c)=5`; path multiplicities `r:1, a:1, b:1, c:2`, recursive result and weighted aggregate both **16**, while ignoring multiplicities gives **11**. Add a parallel edge `a→c`: `c`'s multiplicity becomes `3`, the result **21**, while the "unweighted node sum" stays 11. Additionally 75 topologically numbered DAGs with 5421 weight assignments were exhausted; all passed.

### 6.6 This proposition's boundaries, item by item

The proof uses only two things: the topological order guaranteed by finiteness and acyclicity, and the addition and scalar multiple of a commutative monoid. Its boundaries therefore follow exactly:

- **Non-commutative combining operations do not apply.** Grouping by node reorders contributions; the correct treatment retains the **order** information of paths rather than summing.
- **Cycles do not apply.** The premise of topological induction disappears; least/greatest fixed-point theory would be needed, which we do not cover. [open]
- **Path counts may be infinite in infinite graphs.** If `m(v)` is infinite both sides may diverge; the proposition is stated for finite graphs only.
- **Floating point does not apply.** The proposition requires exact arithmetic; with floats, "weight by multiplicity" and "accumulate in topological order" can differ, and the analysis of §3.5 applies.

**A corollary worth stressing**: on a DAG, the **fastest correct algorithm** and the **fastest wrong one** often differ by a single line — "add each node once" looks more like an optimisation, but it does not compute `V(r)`. Prop. 3's value is that it writes that difference as a formula: the gap is `Σ (m(v) - 1)·b(v)`. [proved]

---

## 7 Bounded correspondence: from finite series to productivity

This section establishes only a **correspondence** and does not address the general coinduction question. [open] Strict frameworks for coalgebra, coinduction and corecursion already exist [L5], and the duality between initial and terminal (final) algebras is established at the type-theory level [L2]; hence we **claim no new theoretical result**, only a bounded extension of the finite-case language and an explicit statement of where it stops.

### 7.1 Unfolding streams from states: the abstract definition and the productivity condition

The formal content and proofs follow Goupote's material `productive_series.md` (accepted); this is the compressed version.

**Abstract unfold [literature].** Let `A` be a set of items, `S` a set of states, and `γ : S → A × S` a total function. Starting from `s₀`, define recursively

```
(aₙ, sₙ₊₁) = γ(sₙ).
```

In the stream model `A^ℕ`, define `ana(γ)(s₀) = (a₀, a₁, a₂, …)`, which satisfies `out(ana(γ)(s)) = (a, ana(γ)(s′))` where `γ(s) = (a, s′)`. This is the stream unfold (anamorphism) for the functor `F(X) = A × X`; we do **not** generalise to arbitrary functors.

**Existence and uniqueness [proved].** Existence: each coordinate is defined by finitely many iterations. Uniqueness: by induction on coordinates, any map satisfying the equation has the same head and the same successive coordinates. ∎

**Program-level productivity [proved].** "The program is productive" means: for every natural `N`, **computing from the initial state and obtaining the first `N` items completes in finitely many steps**. It requires that every required state transition and item computation is executable and terminating.

Two things must be kept apart here: **the abstract total function `γ` does not by itself guarantee that a given program has this property** — `γ` is a mathematical object, whereas whether the program can actually produce the next state, and at what cost, is a different question. Productivity **also does not** require a uniform time bound per item, and **does not** require holding the whole infinite stream in memory.

**The abstract coalgebra must not be identified with program productivity.** "A stream exists satisfying `out ∘ ana = F ana ∘ γ`" and "this program hands over each prefix in finitely many steps" are assertions at different levels: the former is a set-level fact, the latter an execution property. §7.1 uses the former to define objects and the latter to draw the boundary; the two are never substituted for each other. [open]

### 7.2 Partial sums aligned with finite recursion

Let `aₙ ∈ ℚ` and define `P₀ = 0`, `Pₙ₊₁ = Pₙ + aₙ`, so `P_N = Σ_{k=0}^{N-1} a_k`. Terms and partial sums can be produced together from an **extended state**: **convention** `γ(s) = (a, s′)`, and

```
Γ((s, p)) = ( (a, p + a), (s′, p + a) ).
```

Unfolding from `(s₀, 0)` yields `(a₀, P₁), (a₁, P₂), …`. Note that `Γ`'s return order **agrees exactly** with that of `γ`: item first, state second (`A × S`); the extended state is `(s′, p + a)`, whose first component is the **state** and whose second is the **accumulated value**. This return order is used consistently throughout; nowhere is it reversed.

Define the return-value recursion `R(0) = 0`, `R(N+1) = R(N) + a_N`. Induction on `N` immediately gives

```
R(N) = P_N.
```

[proved] The alignment compares **finite return values** only; it does not treat the infinite process as an ordinary call that eventually returns. Writing the addition as `a_N + R(N)` gives the same value over the rationals; we use the accumulator form throughout for alignment with `Γ`.

### 7.2.1 Why "alignment" and not "equivalence"

The alignment between Prop. 1 and §7.2 concerns **finite prefixes** only: `R(N) = P_N`, both sides being finite sums. This looks like mere wording but determines the whole boundary of §7.

Treating a recursive call as "a complete computation that will eventually return" invites the claim that "the result of an infinite recursion is the sum of the series". But an infinite process **has no return value** — it produces a sequence. More accurately: **a recursion has a value at the finite level and is replaced by a sequence at the infinite level.** These are not two spellings of one mathematical object but two different objects: the former a function `ℕ → M`, the latter a stream `A^ℕ` together with its partial sums.

This distinction also explains why §7.1 separates "abstract unfold" from "program productivity": at the abstract level we discuss the **existence** of a stream (a set and a map); at the execution level, **whether prefixes are obtainable**. Confusing them yields false propositions such as "an infinite recursion certainly returns a partial sum". [proved]

### 7.3 An instance with exact error (the geometric series)

Take `S = ℕ` and `γ(n) = (2^{-(n+1)}, n+1)`. Then `aₙ = 2^{-(n+1)}` and

```
P_N = 1 - 2^{-N}     (N ≥ 0).
```

**Proof [proved].** For `N = 0` both sides are `0`; if it holds, adding `2^{-(N+1)}` gives `P_{N+1} = 1 - 2^{-(N+1)}`. ∎

Since `2^{-N} → 0`, the series converges to `1`, and the tail sum (error) is `1 - P_N = 2^{-N}`. **We can speak of "error" here because the existence of the limit and its difference from the partial sums have been proved independently**; the error is the tail sum of this series, **not** a Lagrange remainder inferred from the recursive shape — the §3.3 distinction again, now on the infinite side. [proved]

### 7.4 Three things that must not be conflated

- **Constant stream `1,1,…` [example]**: every prefix is producible, but `P_N = N` has no finite real limit.
- **Alternating stream `1,-1,1,-1,…` [example]**: every prefix is producible, but the partial sums `1,0,1,0,…` do not converge.
- **From the two above [proved]**: computable prefixes do not imply convergent partial sums. The geometric series' convergence comes from that **independent** proof, not from "the generator can still produce the next item".

Productivity of an infinite process, the mathematical limit of partial sums, and error control in a finite-precision program are three different problems. This section establishes only the correspondence between state unfolding and finite recursive partial sums; it does not address the general coinduction question, and it does not interpret every infinite recursion as a series. [open]

### 7.5 Aligning with the finite case

| Finite (§3–§6) | Infinite (§7) | Status |
|---|---|---|
| termination returns `c` | seed `s₀ ∈ S` unfolds via `ana(γ)` into a stream | established framework [L2] |
| chain shape = list `foldr` | unfold = `ana` / `unfold` producing a stream | established framework [L1] |
| `F(n) = c + Σ_{k=1}^{n} a_k` | partial sums `P_N`; take the limit as `N → ∞` | convergence must be proved **separately** (§7.3) [proved] |
| the value of the finite sum is the result | each producible prefix allows continuation, but **no guarantee** of convergent partial sums | `[proved]` (§7.4) |
| memoisation changes the execution graph, not the value (Prop. 3) | the generator in this demo does not explicitly cache history; other implementations may share or memoise tails, and the mathematical definition of `ana` specifies no caching strategy | structural contrast, not a theorem [open] |

### 7.6 Runnable check

```text
$ python3 essay/productive_series_checks.py
Geometric: N=0..20, lazy partial sum = finite recursive sum = 1-2^(-N); exact checks passed
N=0: partial=0, error=1
N=1: partial=1/2, error=1/2
N=2: partial=3/4, error=1/4
N=4: partial=15/16, error=1/16
N=8: partial=255/256, error=1/256
Constant ones partial sums: [1, 2, 3, 4, 5, 6]
Alternating signs partial sums: [1, 0, 1, 0, 1, 0]
All checks passed; productivity and convergence arguments are in productive_series.md.
```

The script uses `Fraction` for exact prefixes, keeping floating-point rounding apart from mathematical convergence; for `N = 0..20` the lazy partial sum, the finite recursive sum and `1 - 2^{-N}` agree term by term. [example]

The earlier `productivity_checks.py` has been superseded by `productive_series_checks.py`, which includes the exact-error and convergence-separation comparisons. Finite output cannot prove general productivity or convergence; proofs are in §7.1–§7.4 and `productive_series.md`.

### 7.7 Three levels that must not be conflated

Summarising §7.1–§7.4: **productivity of an infinite process, the mathematical limit of partial sums, and error control in a finite-precision program are three different problems.**

- **Productivity** is an **execution** property: can the program hand over the next prefix in finitely many steps? It depends on the implementation (whether data have arrived, whether computation is possible), not on any convergence condition.
- **Convergence** is a **mathematical** property: does the partial-sum sequence have a limit? It is determined by the terms, independently of how the program is written. The constant and alternating streams show the two can separate.
- **Precision** is an **implementation** property: how far a finite-precision partial sum is from the true value. It is the same phenomenon as the floating-point error of §3.5 and has nothing to do with convergence.

A typical consequence of conflating them is discussing "how large the error is" for a sequence that **does not converge at all** — that is not error, that is divergence — or mistaking a finite float deviation for evidence about the rate of convergence of a very slowly converging series. §7.3 chooses the geometric series precisely because its convergence can be **proved independently** and the error `2^{-N}` is an exact expression, independent of any numerical experiment. [open]

---

## 8 Conclusion

The result is a three-layer structure, and the three layers have quite different degrees of rigour, which must be stated.

**Layer one: the methodological framework, not a contribution.** "Recursion is a finite sum" is wrong; "recursion is unfold-then-fold" is right, but in the corner where it can be stated rigorously (list–monoid) it is only a restatement. This is **our view, not a theorem**: it claims only that the restatement yields no new falsifiable proposition, not that every recursion is a fold, and nothing follows from it for other recursion types. [open]

**Layer two: the classification table, our presentational contribution.** Table 1 is organised not by "four types of recursion" but by "which invariant is given up when going from a recursive computation to a linear aggregate": order, brackets (nesting), multiplicity. Together with Props. 1–3 it gives a line-by-line discussion list. It is not grander than "recursion is folding", but it is more precise and harder to cite loosely — which is why it is worth writing down. [proved] (the propositions), [example] (the in-table checks)

**Layer three: a bounded correspondence to productivity.** §7 gives precise definitions, a runnable example and one prohibition: producible prefixes do not imply convergent partial sums; the geometric series' convergence comes from an independent proof, not from the generator still producing terms. This layer is only a side-by-side contrast within existing recursion-scheme and coinduction frameworks [L1, L2, L5]; it establishes no new theory. [open]

**One sentence for all three layers**: recursion is not a series; certain recursions may be safely written as series, with conditions listed in Prop. 1; once those conditions are left, what is lost is not the label "series-ness" but three concrete pieces of information — **order, brackets, or multiplicity**. Knowing which one is lost is more useful than arguing whether the essence of recursion is folding.

We do **not** claim: that fold/catamorphism equivalence is our contribution; that we solve the general coinduction problem; or anything about originality beyond the literature check (see §10 and `lit-check.md`).

---

## 9 Discussion: what this work means for people who write code

The essay is conceptual, but it reduces to a few operational lessons. None is a discovery; each is an engineering reading of one of the three threads.

**First: ask what the combining operation is.** Faced with a recursion, do not first ask whether it is "recurrence or divide-and-conquer"; ask with which operation it combines the sub-results on return. Addition, multiplication, concatenation, maximum, or a stateful update? That answer determines compressibility far more than the syntactic shape. Props. 1 and 2 translate "can be compressed" into "which axioms the combining operation satisfies".

**Second: rearrangement is an expensive capability, not a free one.** Letting a compiler reorder, letting a sum be vectorised, letting `sum` run faster in a parallel library — all depend on commutativity and associativity. Documenting "the result depends on order" in a floating-point summation routine is therefore not pedantry; it says this passage does not satisfy Prop. 1's hypotheses, so do not perform that rearrangement on my behalf. [example]

**Third: caching changes execution, not mathematics.** Memoisation evaluates repeated subproblems once — a huge engineering gain — but it does not change "how many times a contribution is counted in `V(r)`". Confusing the two yields dependency-graph code that looks faster but silently under-computes a subset sum or a path sum. [example]

**Fourth (methodology): a good explanation should say where it stops.** §2 already noted that restating adds no knowledge. The same holds in engineering: if a refactoring changes only the organisation of the code and not its algebraic structure, its benefit should be reported as readability or a constant-factor improvement, not as "a smarter algorithm". Stating that clearly is more useful than adopting a prettier term. [open]

### 9.1 What this work implies about "how to study an analogy"

Abstracting the skeleton, one workflow emerges that is more portable than any single proposition:

**Step one: turn the intuition into a proposition.** "Recursion is like a series" is not a proposition because it cannot be refuted; "the value of a chain-shaped additive recursion equals a finite sum" is one. The difference is that the latter carries testable conditions (chain shape, addition, termination, exact arithmetic).

**Step two: find every failure and give it a name.** We found four classes: broken chain (structure), changed operation (algebra), lost property (implementation), input outside the domain (input). Classifying failures turns "the analogy is imprecise" into "imprecise under which conditions", which is something a reader can use.

**Step three: shrink the similarity to a provable range.** §7 does not say "infinite recursion is a series"; it says "partial sums and finite recursion align on finite prefixes". Shrinking is not retreat; it is what lets the remaining sentence stand.

**Step four: write down what you do not claim.** The "cannot claim" list in `lit-check.md` is itself a deliverable: it tells those who come next where to look when someone claims something in this direction is new.

**Step five: put experiments beside proofs, not in their place.** Our scripts catch implementation errors and exhibit boundaries; the proofs stand independently. The order cannot be reversed: first the proposition, then the check — not a pile of checks followed by "therefore it holds".

This workflow applies to any "A is really B" analogy. It does not guarantee new theorems, but it makes the **boundary visible** — and in conceptual writing a visible boundary is often more useful than a grand conclusion. [open]

---

## 10 What remains unverified, and limitations

- Propositions labelled [proved] come with **complete proofs given here**, but they have not been peer-reviewed or machine-checked by a proof assistant (Lean/Coq); readers should treat them as documented derivations, not certified theorems. [open]
- [example] items are illustration only; `fold_checks.py`, `propositions_checks.py` and `productive_series_checks.py` are all reproducible but none is a formal verification. The exhaustiveness figures (23 tree shapes / 75 DAGs / 5421 weight assignments) describe sampling strength, not proof. [example]
- The literature check is complete: see [`lit-check.md`](lit-check.md). L1–L5 have verifiable DOIs plus a "cannot claim" list of seven items. Accordingly we do **not** claim: recursion = folding as a new discovery (L1, L3); the finite/infinite duality as ours (L2); the productivity/coinduction framework as ours (L5); left/right fold differences or tail-recursion rewriting as ours (L4); tree sum = preorder fold as a new result (L1). [open]
- The whole essay assumes exact arithmetic; floating-point cases are handled in §3.4–§3.5. [example]
- **Tail recursion is not stack safety.** "No pending combination on return" refers to the **semantic** level; it does not mean Python optimises tail calls to constant stack. In CPython tail recursion still occupies the interpreter stack and deep recursion raises `RecursionError`. This does not affect Table 1, but readers should not treat tail recursion as a "constant-space" rewrite.
- **Floating-point special values are outside our model.** `NaN`, `±inf` and signed zero violate the monoid axioms required by Props. 1 and 3 (`NaN` breaks reflexivity of equality, `inf - inf` is undefined); our derivations do not apply and such values need separate analysis. [open]
- **"Stream unfolding does not memoise" is not a general claim.** The corresponding row of the §7.5 table describes only the unfolding in our demo; whether lazy unfolding caches produced prefixes depends on language and implementation strategy (some lazy languages retain references by default). [open]

---

## Appendix A: experiments and reproduction

All numbers are reproducible. Three independent scripts, one per thread:

```text
$ python3 essay/fold_checks.py
right: 2 lfold: 0
fib(20) naive calls: 6765 21891
fib(20) memo calls: 6765 21
tail: 10
visit order: ['a', 'b', 'c']
ack(2,3): 9
float: (0.1+0.2)+0.3 = 0.6000000000000001  0.1+(0.2+0.3) = 0.6
DAG: V(r)=7  sum_v m_r(v)*b(v)=7  m_r(c)=2
productive prefixes [1, 1, 1, 1, 1]: all producible; partial sums [1, 2, 3, 4, 5] diverge
v0.2 checks: OK

$ python3 essay/propositions_checks.py
A: 23 ordered tree shapes passed; concatenation rab != rba
Parentheses: same leaves [1, 1, 1], values -1 and 1
B diamond: value=16, paths=[1, 1, 1, 2], unweighted=11, evaluated=4
B parallel-edge diamond: value=21, paths=[1, 1, 1, 3], unweighted=11, evaluated=4
B exhaustive: 75 topologically numbered DAGs, 5421 weight assignments passed
All checks passed (finite examples; proofs are in propositions_ab.md).

$ python3 essay/productive_series_checks.py
Geometric: N=0..20, lazy partial sum = finite recursive sum = 1-2^(-N); exact checks passed
N=0: partial=0, error=1
N=1: partial=1/2, error=1/2
N=2: partial=3/4, error=1/4
N=4: partial=15/16, error=1/16
N=8: partial=255/256, error=1/256
Constant ones partial sums: [1, 2, 3, 4, 5, 6]
Alternating signs partial sums: [1, 0, 1, 0, 1, 0]
All checks passed; productivity and convergence arguments are in productive_series.md.
```

All three use the Python standard library only; `productive_series_checks.py` uses `fractions.Fraction` for exact rational arithmetic. Environment: CPython 3.9.

**How the numbers are used**: every number in the text states which script produced it and under what conditions. Numbers marked `[example]` illustrate; they never replace proofs, which are in §3, §5, §6 and §7. Propositions marked `[proved]` do not depend on any script output.

---

## Appendix B: propositions at a glance

| No. | Statement | Hypotheses | Conclusion | Rigour |
|---|---|---|---|---|
| Prop. 1 | finite-sum representation of chain + additive recursion | `(M, +, 0)` commutative additive monoid; `F(0)=c`, `F(n)=a_n+F(n-1)` | `F(n) = c + Σ_{k=1}^{n} a_k` | sufficient only, not a characterisation; no floats, no infinite |
| Prop. 2 | ordered-tree aggregate = preorder ordered product | `(M, ⊗, e)` monoid | `S(T) = fold(pre(T))` | values only; not evaluation order, cost or effects |
| Prop. 3 | weighted aggregation over a DAG | finite acyclic multigraph; commutative monoid; `V(v)=b(v)+Σ V(u)` | `V(r) = Σ m(v)·b(v)` | requires commutativity; not for cycles/infinite graphs/floats |

**Common boundary of the three**: they state **values** only — not execution structure, complexity, or effects. Any claim of "faster" or "less memory" is classified here as an engineering observation, not a corollary. [open]

---

## Appendix C: the five worked examples running through the essay

| # | Example | Combining operation | Structure | Prop. 1 applies? | What is lost |
|---|---|---|---|---|---|
| 1 | `sum_to(n)` | `+` (integers) | chain | yes | nothing (over exact integers) |
| 2 | `factorial(n)` | `×` | chain | no (operation is not `+`) | additive structure; multiplication is still commutative |
| 3 | `repeat(text, n)` | string concatenation | chain | no | commutativity: `"ab"+"ba" ≠ "ba"+"ab"` |
| 4 | `tree_sum(node)` | `+` | tree | no (chain broken), yet the conclusion is a sum | nesting position |
| 5 | memoised `fibonacci(n)` | `+` | DAG | no | execution count; the value still counts by path multiplicity |

All five share one sentence: **whether a computation can be written as "a sum of a queue of terms" depends on the combining operation and the structure, not on whether it is recursive.** Example 1 shows where the intuition is right; examples 2–5 show where and how it is not. The seven rows of Table 1 are that sentence unfolded.

**An extra reminder on example 5**: the memoised version's computation graph differs from the naive one (tree vs DAG), yet both return the same value. If someone explains memoisation as "removing the repeated terms", ask at once why `fib(20)` has not changed. The answer is Prop. 3: what is deduplicated is **execution**, not **value**. [example]

---

## References

1. Haskell `base` 4.22.0.0 — `Data.Foldable` (`foldr` type, right associativity, initial value). [literature]
2. SICP, Comparison Edition — §1.2.2 Tree Recursion. [literature]
3. OpenStax *Calculus Volume 2* — §6.3 Taylor and Maclaurin Series. [literature]
4. *Recursion and Series* source repository — `README.md`, `README.en.md`. [literature]
5. **[L1]** Meijer, E., Fokkinga, M., Paterson, R. *Functional Programming with Bananas, Lenses, Envelopes and Barbed Wire*. FPCA 1991, LNCS 523, pp. 124–144. DOI [10.1007/3540543961_7](https://doi.org/10.1007/3540543961_7). [literature] — recursion schemes generated from datatype definitions; unfold-then-fold is not our discovery.
6. **[L2]** Hagino, T. *A Categorical Programming Language*. PhD thesis, University of Edinburgh, 1987; reissued arXiv [2010.05167](https://arxiv.org/abs/2010.05167). [literature] — F,G-dialgebras unify initial and terminal algebras; finite/infinite duality is established, so §7 claims no new theory.
7. **[L3]** Hutton, G. *A tutorial on the universality and expressiveness of fold*. J. Functional Programming 9(4), 1999. DOI [10.1017/S0956796899003500](https://doi.org/10.1017/S0956796899003500). [literature] — fold is uniquely determined by its recursive equation; §2 can only be a methodological statement.
8. **[L4]** Danvy, O. *Folding left and right matters: Direct style, accumulators, and continuations*. J. Functional Programming 33, e2, 2023. DOI [10.1017/S0956796822000156](https://doi.org/10.1017/S0956796822000156). [literature] — left/right fold equivalence modulo left-permutativity (more general than associativity/commutativity) and accumulator rewriting; the bracket-order and tail-recursion rows are not new.
9. **[L5]** Jacobs, B., Rutten, J. *An introduction to (co)algebra and (co)induction*. In *Advanced Topics in Bisimulation and Coinduction* (Sangiorgi & Rutten, eds.), CUP, 2011. DOI [10.1017/CBO9780511792588.003](https://doi.org/10.1017/CBO9780511792588.003). [literature] — rigorous frameworks for coalgebra, coinduction and corecursion already exist; §7 only brings the reader to the door.

The literature check and the "cannot claim" list are in [`lit-check.md`](lit-check.md).
