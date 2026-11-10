"""Exact research experiments for adaptive signed recursive expansion.

Exploratory verification, not a production solver or a proof assistant.
Run from the repository root: python3 research/adaptive_expansion_checks.py
All arithmetic uses fractions.Fraction; no third-party packages are required.
"""

from fractions import Fraction as Q
from itertools import combinations, product
import json


def vector(values):
    return [Q(x) for x in values]


def matrix(rows):
    return [vector(row) for row in rows]


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), Q(0))


def identity(n):
    return [[Q(i == j) for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(column) for column in zip(*a)]


def matvec(a, x):
    return [dot(row, x) for row in a]


def matmul(a, b):
    columns = transpose(b)
    return [[dot(row, column) for column in columns] for row in a]


def power(a, degree):
    result = identity(len(a))
    for _ in range(degree):
        result = matmul(result, a)
    return result


def solve(a, rhs):
    """Independent rational Gaussian elimination for the exact reference value."""
    n = len(rhs)
    work = [list(row) + [value] for row, value in zip(a, rhs)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if work[i][j]), None)
        if pivot is None:
            raise ValueError('singular matrix')
        work[j], work[pivot] = work[pivot], work[j]
        scale = work[j][j]
        work[j] = [x / scale for x in work[j]]
        for i in range(n):
            if i != j:
                scale = work[i][j]
                work[i] = [x - scale * y for x, y in zip(work[i], work[j])]
    return [row[-1] for row in work]


def system_matrix(c):
    return [[Q(i == j) - x for j, x in enumerate(row)]
            for i, row in enumerate(c)]


def macros(c, a, lengths):
    """Keep each row's finite signed expansion before applying absolute values."""
    n = len(c)
    result, local = [], []
    for u, length in enumerate(lengths):
        assert length >= 1
        row = identity(n)[u]
        value = Q(0)
        for _ in range(length):
            value += dot(row, a)
            row = [dot(row, column) for column in transpose(c)]
        result.append(row)
        local.append(value)
    return result, local


def push(rows, local, estimate, coefficients, u):
    alpha = coefficients[u]
    updated = list(coefficients)
    updated[u] = Q(0)
    for v, value in enumerate(rows[u]):
        updated[v] += alpha * value
    return estimate + alpha * local[u], updated


def potential(coefficients, h):
    return sum((abs(x) * y for x, y in zip(coefficients, h)), Q(0))


def ratios(rows, h):
    return [dot([abs(x) for x in row], h) / h[u]
            for u, row in enumerate(rows)]


def scalar_series_sum(initial, beta):
    denominator = 1 - sum(beta, Q(0))
    if not denominator:
        raise ValueError('the candidate recurrence has a unit root')
    numerator = sum(initial, Q(0)) - sum(
        (beta[i] * sum(initial[:i], Q(0)) for i in range(len(beta))), Q(0))
    return numerator / denominator


def main():
    summary = {}

    # False generalization: spectral stability alone does not protect local greed.
    c = matrix([[2, 1], [-4, -2]])
    a = vector([-1, 4])
    exact = solve(system_matrix(c), a)
    assert exact == vector([1, 0])
    assert power(c, 2) == matrix([[0, 0], [0, 0]])
    estimate, k = Q(0), vector([1, 0])
    trace = []
    for t in range(13):
        assert k == vector([2 ** t, 2 ** t - 1])
        assert estimate == 1 - 2 ** t
        assert exact[0] == estimate + dot(k, exact)
        assert abs(exact[0] - estimate) == 2 ** t
        trace.append({'step': t, 'error': str(abs(exact[0] - estimate))})
        u = max(range(2), key=lambda i: abs(k[i]))
        assert u == 0
        estimate, k = push(c, a, estimate, k, u)
    rows, local = macros(c, a, [2, 2])
    estimate, k = push(rows, local, Q(0), vector([1, 0]), 0)
    assert estimate == exact[0] and k == vector([0, 0])
    summary['nilpotent_greedy_counterexample'] = trace

    # Parallel edges must be merged before the matrix |C| is defined.
    parallel_coefficients = vector([1, -1])
    aggregate = sum(parallel_coefficients)
    edge_absolute = sum(abs(x) for x in parallel_coefficients)
    assert aggregate == 0 and edge_absolute == 2
    summary['parallel_edges'] = {'C': str(aggregate), 'B': str(edge_absolute)}

    # A weighted certificate succeeds although the ordinary maximum row sum is 2.
    c = matrix([[0, 2], [Q(1, 8), 0]])
    h = vector([4, 1])
    assert max(sum(abs(x) for x in row) for row in c) == 2
    assert ratios(c, h) == vector([Q(1, 2), Q(1, 2)])
    summary['weighted_certificate'] = {'h': ['4', '1'], 'q': '1/2'}

    # An unstable global matrix can have a stable, specified source direction.
    c = matrix([[Q(5, 4), Q(3, 4)], [Q(3, 4), Q(5, 4)]])
    a = vector([1, -1])
    assert matvec(c, a) == [x / 2 for x in a]
    assert matvec(c, vector([1, 1])) == vector([2, 2])
    assert solve(system_matrix(c), a) == vector([2, -2])
    summary['source_specific_modes'] = {'unstable_mode': '2', 'source_mode': '1/2'}

    # Root-visible cancellation: the root reaches both unstable coordinates.
    c = matrix([[Q(1, 2), 1, -1], [0, 2, 0], [0, 0, 2]])
    a = vector([1, 1, 1])
    exact = solve(system_matrix(c), a)
    assert exact == vector([2, -1, -1])
    defect = [x - y / 2 for x, y in zip(matvec(c, a), a)]
    assert defect == vector([0, Q(3, 2), Q(3, 2)])
    witness = list(defect)
    for _ in range(3):
        assert witness[0] == 0
        witness = matvec(c, witness)
    terms = list(a)
    perturbed = vector([1, Q(101, 100), 1])
    visible_count = 0
    for j in range(13):
        assert terms[0] == Q(1, 2) ** j
        expected = Q(1, 2) ** j + Q(1, 150) * (2 ** j - Q(1, 2) ** j)
        assert perturbed[0] == expected
        terms, perturbed = matvec(c, terms), matvec(c, perturbed)
        visible_count += 1
    summary['root_visible_certificate'] = {
        'checked_annihilation_moments': 3,
        'exact_terms_and_perturbed_terms': visible_count,
        'root_sum': '2',
        'global_unstable_eigenvalue': '2',
    }
    assert scalar_series_sum(vector([1]), vector([Q(1, 2)])) == 2
    c = matrix([[0, Q(-1, 4)], [1, Q(1, 2)]])
    a = vector([1, 0])
    beta = vector([Q(-1, 4), Q(1, 2)])
    initial = [a[0], matvec(c, a)[0]]
    assert scalar_series_sum(initial, beta) == solve(system_matrix(c), a)[0] == Q(2, 3)
    terms = []
    current = list(a)
    for _ in range(12):
        terms.append(current[0])
        current = matvec(c, current)
    assert all(terms[j + 2] == beta[0] * terms[j] + beta[1] * terms[j + 1]
               for j in range(10))
    summary['scalar_sum_formula_checks'] = 2

    # A mixed row-length certificate need not use the same depth at every node.
    c = matrix([[Q(1, 2), Q(1, 4)], [-1, Q(-1, 2)]])
    a = vector([2, -1])
    rows, local = macros(c, a, [1, 2])
    assert rows == matrix([[Q(1, 2), Q(1, 4)], [0, 0]])
    exact = solve(system_matrix(c), a)
    assert exact == [b + dot(row, exact) for b, row in zip(local, rows)]
    summary['variable_depths'] = {'lengths': [1, 2], 'ratios': ['3/4', '0']}

    # Exhaust finite rational matrices with certified one-step row contraction.
    # Check macro invariants, certificates, and per-completed-cost progress.
    entries = (Q(-1, 2), Q(-1, 4), Q(0), Q(1, 4), Q(1, 2))
    h = vector([1, 1])
    costs = vector([1, 3])
    trajectories = steps = 0
    for values in product(entries, repeat=4):
        c = [list(values[:2]), list(values[2:])]
        original_q = ratios(c, h)
        if max(original_q) >= 1:
            continue
        for signs in product((-1, 1), repeat=2):
            a = vector(signs)
            exact = solve(system_matrix(c), a)
            rows, local = macros(c, a, [1, 2])
            q = ratios(rows, h)
            assert max(q) < 1
            total_k = sum(costs[i] / (1 - q[i]) for i in range(2))
            bound = max(abs(x) for x in a) / (1 - max(original_q))
            estimate, k = Q(0), vector([1, 0])
            completed_cost = Q(0)
            for _ in range(8):
                old = potential(k, h)
                assert exact[0] == estimate + dot(k, exact)
                assert abs(exact[0] - estimate) <= bound * old
                if not old:
                    break
                gains = [(1 - q[i]) * abs(k[i]) * h[i] for i in range(2)]
                u = max(range(2), key=lambda i: gains[i] / costs[i])
                assert gains[u] / costs[u] >= old / total_k
                estimate, k = push(rows, local, estimate, k, u)
                new = potential(k, h)
                assert new <= old - gains[u]
                assert new <= old * (1 - costs[u] / total_k)
                completed_cost += costs[u]
                assert exact[0] == estimate + dot(k, exact)
                steps += 1
            trajectories += 1
    summary['cost_certificate_checks'] = {'trajectories': trajectories, 'completed_updates': steps}

    # Adjoint identity and certified approximate-adjoint correction.
    c = matrix([[0, 2], [Q(1, 8), 0]])
    a = vector([1, -2])
    h = vector([4, 1])
    q = Q(1, 2)
    m = system_matrix(c)
    exact = solve(m, a)
    z = solve(transpose(m), vector([1, 0]))
    adjoint_cases = 0
    for vals in product((Q(-1), Q(0), Q(1)), repeat=4):
        approx, z_approx = list(vals[:2]), list(vals[2:])
        residual = [b - x for b, x in zip(a, matvec(m, approx))]
        error = [x - y for x, y in zip(exact, approx)]
        assert error[0] == dot(z, residual)
        dual_residual = [b - x for b, x in zip(vector([1, 0]), matvec(transpose(m), z_approx))]
        correction = dot(z_approx, residual)
        primal_bound = max(abs(residual[i]) / h[i] for i in range(2)) / (1 - q)
        correction_bound = potential(dual_residual, h) * primal_bound
        assert abs(error[0] - correction) <= correction_bound
        adjoint_cases += 1
    summary['adjoint_checks'] = adjoint_cases

    # Fixed-frontier independent intervals: exact information radius and query cost.
    k, delta = vector([2, -3, 0]), vector([1, 2, 5])
    radius = dot([abs(x) for x in k], delta)
    endpoints = [dot(k, [s * d for s, d in zip(signs, delta)])
                 for signs in product((-1, 1), repeat=3)]
    assert min(endpoints) == -radius and max(endpoints) == radius == 8
    benefits, query_costs, budget = [6, 10, 12], [1, 2, 3], 5
    ranked = sorted(range(3), key=lambda i: Q(benefits[i], query_costs[i]), reverse=True)
    chosen, spent = [], 0
    for i in ranked:
        if spent + query_costs[i] <= budget:
            chosen.append(i)
            spent += query_costs[i]
    best = max((sum(benefits[i] for i in subset), subset)
               for size in range(4) for subset in combinations(range(3), size)
               if sum(query_costs[i] for i in subset) <= budget)
    assert sum(benefits[i] for i in chosen) == 16 and best[0] == 22
    summary['fixed_frontier_information_radius'] = str(radius)
    summary['query_ratio_counterexample'] = {'ratio_greedy_benefit': 16, 'optimal_benefit': 22}

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print('All exact adaptive-expansion research checks passed.')


if __name__ == '__main__':
    main()
