# From Finite Sums to Structural Folding

**Language / 语言: [简体中文](README.md) | English**

A research summary on the relationship between recursion and series · Updated October 26, 2026

## The research in three sentences

I initially understood recursion as a series being expanded term by term: each level exposes a current term, while the next call handles the remaining computation.
Derivations and comparisons narrowed this idea: a single-chain additive recursion can be represented exactly as a finite sum, while multiplication, concatenation, and branching recursion require us to retain their respective operations and structures.
I therefore reframed the question as “How does recursion unfold computational dependencies and combine results according to a rule?”, distinguishing remaining computation from the Lagrange remainder and using the established concept of folding to connect the examples.

## 1 Research question and scope

The starting question was: Is a complete recursive computation simply a finite series?

This intuition fits a recursive summation program: the current call contributes a number and delegates a smaller instance of the same problem to the next call; once that call returns, the current level completes its addition. However, a function call is part of a computational process, while a finite sum is a mathematical expression. They should not be treated as identical concepts.

This summary focuses on recursion that terminates on finite inputs and combines results through return values. The mathematical derivations use exact arithmetic; the code uses Python integers and ordinary function calls. Inputs to the numerical examples are nonnegative integers, and the tree example assumes a finite, acyclic binary tree. Actual execution is also subject to the interpreter's recursion limit and available resources.

“Finite sum” is the clearer term here. An infinite series additionally involves the limit and convergence of its partial sums. Termination of a finite recursive computation does not establish convergence of an infinite series.

## 2 A finite-sum representation that can be proved

Suppose a real-valued sequence satisfies:

$$
F(0)=c,\qquad F(n)=a_n+F(n-1),\quad n\geq1.
$$

Repeated substitution gives:

$$
\begin{aligned}
F(n)&=a_n+F(n-1)\\
&=a_n+a_{n-1}+F(n-2)\\
&=\cdots\\
&=a_n+a_{n-1}+\cdots+a_1+c.
\end{aligned}
$$

Therefore:

$$
\boxed{F(n)=c+\sum_{k=1}^{n}a_k}.
$$

**Proof by induction.** For $n=0$, the empty sum is zero, so the formula holds. Assume that $F(m)=c+\sum_{k=1}^{m}a_k$. Then:

$$
F(m+1)=a_{m+1}+F(m)
=c+\sum_{k=1}^{m+1}a_k.
$$

The result therefore holds for every nonnegative integer.

This proves the correspondence between this class of recursion and finite sums. It does not prove that all recursion belongs to this class.

### Example 1 Summation

```python
def sum_to(n):
    if n == 0:
        return 0
    return n + sum_to(n - 1)
```

For `sum_to(4)`:

$$
S(4)=4+(3+(2+(1+S(0))))=10.
$$

Descending calls establish dependencies. After reaching $S(0)=0$, successive levels compute $1,3,6,10$. In this example, the return phase completes the additions that were waiting for the results of their subcalls.

## 3 Why remaining computation is not the Lagrange remainder

For $0\leq r\leq n$, expanding only the first $r$ levels gives:

$$
F(n)=\sum_{j=0}^{r-1}a_{n-j}+F(n-r).
$$

$F(n-r)$ is an unexpanded subproblem and can be called the remaining computation. It is part of an exact equality. If we omit it to form an approximation, its value becomes the error of that approximation. At the base case, this part is evaluated to $c$, which need not be zero.

The Lagrange remainder, by contrast, belongs to Taylor's theorem. For example, assuming $f\in C^{m+1}$ on an interval containing $a$ and $x$, we have:

$$
f(x)=\sum_{k=0}^{m}\frac{f^{(k)}(a)}{k!}(x-a)^k+R_m(x),
$$

$$
R_m(x)=\frac{f^{(m+1)}(\xi)}{(m+1)!}(x-a)^{m+1},
$$

where, for $x\neq a$, $\xi$ lies between $a$ and $x$. These derivative and interval conditions do not follow automatically from an ordinary recursive call. See [OpenStax's chapter on Taylor's theorem](https://openstax.org/books/calculus-volume-2/pages/6-3-taylor-and-maclaurin-series) for the formula and its conditions.

Both expressions have the form “whole equals expanded part plus remaining part,” but this shared form does not make the concepts identical.

## 4 From addition to finite folding

Replace addition with a closed binary operation $\otimes$, and let:

$$
G(0)=e,\qquad G(n)=a_n\otimes G(n-1).
$$

Repeated substitution gives:

$$
G(n)=a_n\otimes\Bigl(a_{n-1}\otimes
\bigl(\cdots\otimes(a_1\otimes e)\bigr)\Bigr).
$$

This expression retains its right-nested parentheses. It follows by successive substitution, or by induction on $n$, without requiring associativity. Here, $e$ is the initial value returned by the base case; it is an identity element only if it separately satisfies the identity laws.

On a finite list, this corresponds to a right fold: the current element is combined with the folded result of the remaining elements. The [Haskell standard library's Data.Foldable documentation](https://hackage-content.haskell.org/package/base-4.22.0.0/docs/Data-Foldable.html) describes the type of `foldr`, its right-associated structure, and the role of the initial value. Folding is therefore an established concept used here to explain the examples.

| Combining operation | Recursive example | Natural form of the direct expansion |
|---|---|---|
| Numerical addition | Summation | Finite sum |
| Numerical multiplication | Factorial | Finite product |
| String concatenation | Repeating text | Ordered concatenation |
| Maximum | Finding the largest element | Successive comparisons |

If the operation is not associative, its parentheses cannot be rearranged. For example:

$$
3-(2-1)=2,\qquad (3-2)-1=0.
$$

Even for addition, mathematical associativity cannot be transferred without qualification to floating-point computations with rounding error. The derivations here assume exact arithmetic.

### Example 2 Factorial

```python
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)
```

It satisfies $P(0)=1$ and $P(n)=nP(n-1)$, and expands directly to:

$$
P(n)=\prod_{k=1}^{n}k=n!.
$$

`factorial(5)` returns `120`. This shows that multiplication can be the natural combining operation of a recursion; it does not rule out other representations of factorial.

## 5 From a single chain to tree-shaped computation

### Example 3 Fibonacci

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

Here, each non-base-case call produces two subcalls:

$$
F(n)=F(n-1)+F(n-2).
$$

For example, $F(4)=F(3)+F(2)=3$, and `fibonacci(6)` returns `8`. The naive implementation recomputes the same subproblems, producing a call tree with repeated subproblems. [SICP's Tree Recursion section](https://sicp.sourceacademy.org/chapters/1.2.2.html) explains this using Fibonacci.

A recursion tree describes the complete calling relationships; the call stack holds unfinished calls along the current execution path. These are different structures. Under ordinary sequential execution, the program finishes one branch before executing the other, so descending calls and returns are interleaved.

### Example 4 Summing a binary tree

```python
def tree_sum(node):
    if node is None:
        return 0
    return (
        node.value
        + tree_sum(node.left)
        + tree_sum(node.right)
    )
```

Each node provides `value`, `left`, and `right` attributes, and `None` represents an empty subtree. The program unfolds along the data structure and combines the current node's value with the results of its left and right subtrees. A tree with root value `1` and two child values `2` and `3` has a sum of `6`.

For a finite tree $T$, let $S(T)$ denote the value returned by `tree_sum(T)`, let $w(v)$ be node $v$'s `value`, and let $V(T)$ be the set of nodes in the tree. Then:

$$
S(T)=\sum_{v\in V(T)}w(v).
$$

For an empty tree, both sides are zero. If the equality holds for the left and right subtrees, adding the root value establishes it for the whole tree. This is a proof by structural induction.

Thus, “single-chain additive recursion can be represented as a finite sum” gives a sufficient condition. It does not mean that only single-chain recursion admits such a representation. Branching recursion may also compute a finite sum. Tree summation and traversal can be understood through structural folding, but a general structural fold over a tree need not be equivalent to first traversing it into a list and then applying a list fold.

## 6 Revised conclusions

| Initial statement | Revised statement |
|---|---|
| Recursion is a series | Some recursion expands directly into a finite sum; recursion can also use other operations and structures |
| The next call is the Lagrange remainder | The next call represents remaining computation; the Lagrange remainder requires the conditions of Taylor's theorem |
| The remainder disappears at the endpoint | The remaining computation is evaluated to the value specified by the base case |
| Returning means summing | Returning completes the operation waiting at the current level, which may be addition, multiplication, concatenation, or something else |
| Tree recursion cannot be expressed as a finite sum | Tree-shaped calls can produce a sum; call structure and result representation must be distinguished |

For the terminating examples in this summary, “unfold computational dependencies, then combine results according to a rule” is a useful explanatory framework. It does not require the program to build a complete call tree first and fold it afterward.

This framework has limits: a tail-recursive call may leave no combining work after it returns; programs that change state or perform input/output also require attention to execution order; general infinite recursion need not return a result. The mathematical nesting of a list `foldr` also does not imply that all languages and evaluation strategies execute it in the same order.

The work completed here consists of conceptual clarification, a proof of the finite-sum proposition, and a comparison of four recursive examples. It connects to established ideas about recurrence relations, folding, and recursion trees. These examples alone do not establish novelty or universal applicability.

## 7 Questions for further investigation

- Record function-entry and return events, and compare the call tree, the current call stack, and the process of combining results.
- Compare ordinary recursion, tail recursion, and loops, checking which pending operations can be replaced by explicit state.
- Compare combining rules and parenthesization, distinguishing mathematical equivalence from differences in concrete numerical computation.
- Add memoization to Fibonacci and compare repeated calls with dependencies that share subproblems.
- Study structural recursion and more general structural folds to clarify the scope of this explanatory framework.

## References

These sources were used to check established concepts and were consulted on October 26, 2026.

1. [Haskell base 4.22.0.0 — Data.Foldable](https://hackage-content.haskell.org/package/base-4.22.0.0/docs/Data-Foldable.html): left and right folds, initial values, and evaluation behavior.
2. [SICP Comparison Edition — 1.2.2 Tree Recursion](https://sicp.sourceacademy.org/chapters/1.2.2.html): tree-recursive Fibonacci and repeated computation.
3. [OpenStax Calculus Volume 2 — 6.3 Taylor and Maclaurin Series](https://openstax.org/books/calculus-volume-2/pages/6-3-taylor-and-maclaurin-series): Taylor polynomials, remainders, and error estimates.

This summary was developed from the original research discussion with AI assistance for checking and source retrieval; it is not a peer-reviewed paper. Publishing the work with references does not replace independent review or third-party recognition.
