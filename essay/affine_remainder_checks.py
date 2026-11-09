"""Exact affine-recurrence remainder checks; standard library only."""
from fractions import Fraction as Q
from itertools import product


def values(a, b, c):
    out = [Q(c)]
    for ak, bk in zip(a, b):
        out.append(Q(ak) + Q(bk) * out[-1])
    return out


def expand(a, b, n, r):
    total, coefficient = Q(0), Q(1)
    for j in range(r):
        k = n - j - 1
        total += coefficient * a[k]
        coefficient *= b[k]
    return total, coefficient


def main():
    checked = 0
    for a in product((-1, 0, 2), repeat=3):
        for b in product((Q(-1), Q(0), Q(1, 2), Q(2)), repeat=3):
            for c in (-2, 0, 3):
                f = values(a, b, c)
                for n in range(4):
                    for r in range(n + 1):
                        partial, p = expand(a, b, n, r)
                        assert f[n] == partial + p * f[n-r]
                        t = Q(3, 2)
                        assert f[n] - (partial + p*t) == p*(f[n-r]-t)
                        low, high = f[n-r]-2, f[n-r]+3
                        assert partial+min(p*low,p*high) <= f[n] <= partial+max(p*low,p*high)
                        checked += 1
    print(f'Exact expansion, replacement error and signed intervals: {checked} cases passed')
    a, b = [1,2,3,4], [2,0,-1,3]
    f = values(a,b,7)
    partial,p = expand(a,b,4,3)
    assert f[4] == partial == 7 and p == 0
    print(f'Zero shield: F(4)={f[4]}, r=3 partial={partial}, coefficient={p}')
    f = values([1]*6,[-1]*6,0)
    errors = [abs(f[6]-expand([1]*6,[-1]*6,6,r)[0]) for r in range(7)]
    assert errors == [0,1,0,1,0,1,0]
    print('Negative coefficients: errors at r=0..6:', [int(x) for x in errors])
    f = values([0]*6,[2]*6,1)
    errors = [abs(f[6]-expand([0]*6,[2]*6,6,r)[0]) for r in range(7)]
    assert all(x==64 for x in errors)
    print('Amplifying coefficients: zero-truncation errors at r=0..6:', [int(x) for x in errors])
    contractions = 0
    q, bound = Q(1,2), Q(4)
    for a in product((-2,0,2),repeat=4):
        for b in product((-q,Q(0),q),repeat=4):
            f=values(a,b,3)
            for r in range(5):
                partial,p=expand(a,b,4,r)
                assert abs(f[4]-partial)<=q**r*bound
                contractions+=1
    print(f'Uniform contraction bound q=1/2, A=2, c=3, M=4: {contractions} cases passed')
    for r in (2,4,8):
        n=2*r
        a=[Q(2**k) for k in range(1,n+1)]
        b=[Q(1,2)]*n
        f=values(a,b,0)
        partial,p=expand(a,b,n,r)
        error=f[n]-partial
        assert error==Q(4,3)*(1-Q(1,4)**r)
        print(f'Shrinking product is insufficient: r={r}, product={p}, residual={error}')
    for r in (0,1,4,8):
        residual=Q(1,2)**r*(3*2**r)
        assert residual==3
    print('Infinite boundary counterexample: alpha=0, beta=1/2, x_j=3*2^j; residual=3 at all tested depths')
    print('All affine remainder checks passed.')


if __name__=='__main__':
    main()
