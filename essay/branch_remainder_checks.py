"""Exact path-frontier remainder experiments, standard library only."""
from fractions import Fraction as Q
from itertools import product


def solve(a, edges):
    f = [Q(0)] * len(a)
    for u in reversed(range(len(a))):
        f[u] = a[u] + sum(c * f[v] for v, c in edges[u])
    return f


def frontier(a, edges, depth):
    k = [Q(0)] * len(a)
    absolute = [Q(0)] * len(a)
    k[0] = absolute[0] = Q(1)
    partial = Q(0)
    for _ in range(depth):
        partial += sum(x * y for x, y in zip(k, a))
        next_k, next_abs = [Q(0)] * len(a), [Q(0)] * len(a)
        for u, row in enumerate(edges):
            for v, c in row:
                next_k[v] += k[u] * c
                next_abs[v] += absolute[u] * abs(c)
        k, absolute = next_k, next_abs
    return partial, k, absolute


def full_binary(depth, c):
    n = 2 ** (depth + 1) - 1
    first_leaf = 2 ** depth - 1
    a = [Q(int(i >= first_leaf)) for i in range(n)]
    edges = [[(2*i+1,c),(2*i+2,c)] if i < first_leaf else [] for i in range(n)]
    return a, edges


def main():
    count = 0
    positions = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
    for coefficients in product((Q(-1,4),Q(0),Q(1,4)), repeat=6):
        edges = [[] for _ in range(4)]
        for (u,v), c in zip(positions, coefficients):
            if c:
                edges[u].append((v,c))
        q = max(sum(abs(c) for _,c in row) for row in edges)
        assert q <= Q(3,4)
        for a in product((Q(-1),Q(1)), repeat=4):
            f = solve(a,edges)
            m = 1/(1-q)
            for d in range(5):
                s,k,h = frontier(a,edges,d)
                assert f[0] == s + sum(x*y for x,y in zip(k,f))
                t = [Q(1,3)]*4
                delta = [abs(x-y) for x,y in zip(f,t)]
                estimate = s + sum(x*y for x,y in zip(k,t))
                actual = abs(f[0]-estimate)
                tight = sum(abs(x)*y for x,y in zip(k,delta))
                loose = sum(x*y for x,y in zip(h,delta))
                assert actual <= tight <= loose
                assert sum(h) <= q**d
                assert abs(f[0]-s) <= m*q**d
                count += 1
    print(f'Exact frontier identity, signed/absolute error bounds and contraction bound: {count} cases passed')
    for c in (Q(3,4),Q(1,2),Q(1,4)):
        results=[]
        for d in (1,2,4,8):
            a,edges=full_binary(d,c)
            f=solve(a,edges)
            s,k,h=frontier(a,edges,d)
            error=abs(f[0]-s)
            assert error==(2*c)**d
            assert sum(h)==error
            results.append(str(error))
        print(f'Binary leaf-frontier errors, edge={c}, depths=1,2,4,8: '+', '.join(results))
    a=[Q(0),Q(0),Q(0),Q(7)]
    edges=[[(1,Q(1)),(2,Q(-1))],[(3,Q(1))],[(3,Q(1))],[]]
    f=solve(a,edges)
    s,k,h=frontier(a,edges,2)
    assert f[0]==s==0 and k[3]==0 and h[3]==2
    print(f'Shared cancellation: actual=0, merged bound={abs(k[3])*7}, path-absolute bound={h[3]*7}')
    q=Q(1,2)
    m=Q(2)
    eps=Q(1,100)
    depth=0
    while m*q**depth>eps:
        depth+=1
    assert depth==8
    print(f'Certified stop: A=1, q=1/2, epsilon=1/100 -> depth={depth}, bound={m*q**depth}')
    print('All branch remainder checks passed.')


if __name__=='__main__':
    main()
