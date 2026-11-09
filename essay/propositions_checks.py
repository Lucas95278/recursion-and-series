"""Exact finite examples for propositions_ab.md; standard library only."""
from functools import lru_cache
from itertools import product


@lru_cache(None)
def shapes(n):
    if n == 0:
        return (None,)
    return tuple((left, right) for k in range(n)
                 for left in shapes(k) for right in shapes(n - 1 - k))


def label(shape, counter):
    if shape is None:
        return None
    value = str(next(counter)) + ':'
    return value, label(shape[0], counter), label(shape[1], counter)


def tree_fold(tree):
    if tree is None:
        return ''
    value, left, right = tree
    return value + (tree_fold(left) + tree_fold(right))


def preorder(tree):
    if tree is None:
        return []
    value, left, right = tree
    return [value] + preorder(left) + preorder(right)


def dag_values(children, weights):
    # Vertices are numbered in topological order; duplicate edges are retained.
    assert len(children) == len(weights) and len(weights) > 0
    assert all(i < j < len(children) for i, row in enumerate(children) for j in row)
    evaluations = 0

    @lru_cache(None)
    def value(i):
        nonlocal evaluations
        evaluations += 1
        return weights[i] + sum(value(j) for j in children[i])

    result = value(0)
    multiplicities = [0] * len(children)
    multiplicities[0] = 1
    for i, row in enumerate(children):
        for j in row:
            multiplicities[j] += multiplicities[i]
    weighted = sum(m * b for m, b in zip(multiplicities, weights))
    unweighted = sum(b for m, b in zip(multiplicities, weights) if m)
    assert result == weighted
    assert evaluations == sum(m > 0 for m in multiplicities)
    return result, multiplicities, unweighted, evaluations


def main():
    tree_count = 0
    for n in range(5):
        for shape in shapes(n):
            tree = label(shape, iter(range(n)))
            assert tree_fold(tree) == ''.join(preorder(tree))
            tree_count += 1
    tree = ('r', ('a', None, None), ('b', None, None))
    swapped = ('r', tree[2], tree[1])
    assert tree_fold(tree) == 'rab' and tree_fold(swapped) == 'rba'
    print(f'A: {tree_count} ordered tree shapes passed; concatenation rab != rba')
    left, right = (1 - 1) - 1, 1 - (1 - 1)
    assert left == -1 and right == 1
    print(f'Parentheses: same leaves [1, 1, 1], values {left} and {right}')
    for name, edges, expected in (
        ('diamond', [[1, 2], [3], [3], []], 16),
        ('parallel-edge diamond', [[1, 2], [3, 3], [3], []], 21),
    ):
        value, counts, naive, evaluations = dag_values(edges, [1, 2, 3, 5])
        assert value == expected and naive == 11
        print(f'B {name}: value={value}, paths={counts}, unweighted={naive}, evaluated={evaluations}')
    graph_count = 0
    case_count = 0
    for n in range(1, 5):
        possible = [(i, j) for i in range(n) for j in range(i + 1, n)]
        for mask in product((0, 1), repeat=len(possible)):
            children = [[] for _ in range(n)]
            for present, (i, j) in zip(mask, possible):
                if present:
                    children[i].append(j)
            graph_count += 1
            for weights in product((-1, 0, 1), repeat=n):
                dag_values(children, weights)
                case_count += 1
    print(f'B exhaustive: {graph_count} topologically numbered DAGs, {case_count} weight assignments passed')
    print('All checks passed (finite examples; proofs are in propositions_ab.md).')


if __name__ == '__main__':
    main()
