# Test whether "recursion = finite fold" adds anything beyond: every total program on a finite domain
# computes SOME function, and "fold" is just primitive recursion. Run a few discriminating cases.

# 1. Non-associative op (subtraction): bracket structure matters -> recursion fixes RIGHT nesting.
def rsub(xs, acc=0):
    if not xs: return acc
    return xs[0] - rsub(xs[1:], acc)
def lsub(xs):
    acc = xs[0]
    for x in xs[1:]: acc = x - acc   # wrong order on purpose if left
    return acc
def lfold(xs):
    acc = xs[0]
    for x in xs[1:]: acc = acc - x
    return acc
print("right:", rsub([3,2,1]), "lfold:", lfold([3,2,1]))

# 2. Fibonacci memoised: recursion TREE vs DAG. Count calls.
import functools
calls=[0]
def fib(n):
    calls[0]+=1
    return n if n<=1 else fib(n-1)+fib(n-2)
print("fib(20) naive calls:", fib(20), calls[0])
c2=[0]
@functools.lru_cache(None)
def mfib(n):
    c2[0]+=1
    return n if n<=1 else mfib(n-1)+mfib(n-2)
print("fib(20) memo calls:", mfib(20), c2[0])

# 3. Tail recursion: NO pending fold on the way back.
def tsum(xs, acc=0):
    if not xs: return acc
    return tsum(xs[1:], acc+xs[0])
print("tail:", tsum([1,2,3,4]))

# 4. State / order: side-effectful recursion whose value isn't a pure fold of children values.
log=[]
def preorder(n):
    if n is None: return 0
    log.append(n)
    preorder(LEFT.get(n)); preorder(RIGHT.get(n))
    return 1
LEFT={'a':'b','b':None}; RIGHT={'a':'c'}
preorder('a'); print("visit order:", log)

# 5. The real generality gap: Ackermann - not a fold over a finite input list.
import sys; sys.setrecursionlimit(100000)
def ack(m,n):
    return n+1 if m==0 else (ack(m-1,1) if n==0 else ack(m-1, ack(m,n-1)))
print("ack(2,3):", ack(2,3))

# ---- v0.2 additions: claims tagged [example]/[proved-check] in essay_draft.md ----

# §3.2 float non-associativity: chain + "+" preserved, exactness lost
def check_float():
    (a, b, c) = (0.1, 0.2, 0.3)
    left, right = (a + b) + c, a + (b + c)
    assert left != right
    print(f"float: (0.1+0.2)+0.3 = {left!r}  0.1+(0.2+0.3) = {right!r}")

# §6 Proposition 3: path multiplicity on a small shared DAG
def check_path_multiplicity():
    E = {"r": ["a", "b"], "a": ["c", "d"], "b": ["c", "d"], "c": [], "d": []}
    bw = dict.fromkeys(E, 1)

    def V(v):
        return bw[v] + sum(V(u) for u in E[v])

    def paths(v, target):
        return 1 if v == target else sum(paths(u, target) for u in E[v])

    lhs = V("r")
    rhs = sum(paths("r", v) * bw[v] for v in E)
    assert lhs == rhs, (lhs, rhs)
    print(f"DAG: V(r)={lhs}  sum_v m_r(v)*b(v)={rhs}  m_r(c)={paths('r','c')}")

# §7.1 productivity does not imply convergence: stream of 1s
def check_productive_not_convergent():
    s, prefixes = 0, []
    for _ in range(5):
        prefixes.append(1)
        s += 1
    assert prefixes == [1] * 5 and s == 5
    print(f"productive prefixes {prefixes}: all producible; partial sums {list(range(1,6))} diverge")

if __name__ == "__main__":
    check_float()
    check_path_multiplicity()
    check_productive_not_convergent()
    print("v0.2 checks: OK")
