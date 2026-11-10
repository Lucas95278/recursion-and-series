"""Small exact operation-count comparison; not a wall-clock benchmark.

Run: python3 research/expansion_cost_comparison.py
Counts include one-query macro construction; selection/certificate scans are
reported separately. This intentionally does not assume cached preprocessing.
"""

from fractions import Fraction as Q
import json

from adaptive_expansion_checks import matrix, vector, dot, ratios, potential, solve, system_matrix


def layer(c, a, estimate, coefficients):
    n = len(c)
    updated = [Q(0)] * n
    operations = 0
    for u, alpha in enumerate(coefficients):
        if not alpha:
            continue
        estimate += alpha * a[u]
        operations += 1
        for v, coefficient in enumerate(c[u]):
            if coefficient:
                updated[v] += alpha * coefficient
                operations += 1
    return estimate, updated, operations


def construct(c, a, h, target=Q(1, 2), max_length=8):
    n = len(c)
    rows, local, lengths = [], [], []
    operations = scans = 0
    for u in range(n):
        current = [Q(i == u) for i in range(n)]
        b = Q(0)
        for length in range(1, max_length + 1):
            b, current, cost = layer(c, a, b, current)
            operations += cost
            scans += n
            q = dot([abs(x) for x in current], h) / h[u]
            if q <= target:
                break
        else:
            raise ValueError('no certificate within the configured exploratory depth')
        rows.append(current)
        local.append(b)
        lengths.append(length)
    return rows, local, lengths, operations, scans


def zero_frontier(k):
    return all(x == 0 for x in k)


def synchronous(c, a, h, epsilon):
    n = len(c)
    k, estimate = [Q(i == 0) for i in range(n)], Q(0)
    q = max(ratios(c, h))
    bound = max(abs(a[i]) / h[i] for i in range(n)) / (1 - q) if q < 1 else None
    operations = layers = 0
    while not zero_frontier(k):
        if bound is not None and bound * potential(k, h) <= epsilon:
            break
        assert layers < 100
        estimate, k, cost = layer(c, a, estimate, k)
        operations += cost
        layers += 1
    return estimate, operations, layers


def adaptive(c, a, h, epsilon):
    n = len(c)
    rows, local, lengths, preprocessing, certificate_scans = construct(c, a, h)
    q = ratios(rows, h)
    certificate_scans += n * n + n  # Final row verification and local-value bound.
    bound = max(abs(local[i]) / h[i] for i in range(n)) / (1 - max(q))
    costs = [1 + sum(x != 0 for x in row) for row in rows]
    k, estimate = [Q(i == 0) for i in range(n)], Q(0)
    operations = updates = selection_scans = 0
    while bound * potential(k, h) > epsilon:
        assert updates < 100
        scores = [(1 - q[i]) * abs(k[i]) * h[i] / costs[i] for i in range(n)]
        selection_scans += n
        u = max(range(n), key=lambda i: scores[i])
        alpha = k[u]
        estimate += alpha * local[u]
        k[u] = Q(0)
        for v, coefficient in enumerate(rows[u]):
            if coefficient:
                k[v] += alpha * coefficient
        operations += costs[u]
        updates += 1
    return estimate, {
        'lengths': lengths,
        'precompute_multiply_adds': preprocessing,
        'online_multiply_adds': operations,
        'total_multiply_adds': preprocessing + operations,
        'certificate_entries_examined': certificate_scans,
        'selection_candidates_examined': selection_scans,
        'completed_macro_updates': updates,
    }


def main():
    chain = [[Q(0)] * 8 for _ in range(8)]
    for i in range(7):
        chain[i][i + 1] = Q(1, 2)
    examples = [
        ('weighted_positive_cycle', matrix([[0, 2], [Q(1, 8), 0]]), vector([1, 1]), vector([4, 1])),
        ('signed_nilpotent', matrix([[2, 1], [-4, -2]]), vector([-1, 4]), vector([1, 1])),
        ('shared_cancellation_diamond', matrix([[0, 1, -1, 0], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 0]]), vector([0, 0, 0, 1]), vector([1, 1, 1, 1])),
        ('eight_node_chain', chain, vector([1] * 8), vector([1] * 8)),
    ]
    results = []
    epsilon = Q(1, 1000)
    for name, c, a, h in examples:
        exact = solve(system_matrix(c), a)[0]
        baseline, baseline_cost, depth = synchronous(c, a, h, epsilon)
        approximate, report = adaptive(c, a, h, epsilon)
        assert abs(exact - baseline) <= epsilon
        assert abs(exact - approximate) <= epsilon
        results.append({
            'example': name,
            'root_tolerance': str(epsilon),
            'synchronous_multiply_adds': baseline_cost,
            'synchronous_layers': depth,
            'macro': report,
            'synchronous_actual_error': str(abs(exact - baseline)),
            'macro_actual_error': str(abs(exact - approximate)),
        })
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
