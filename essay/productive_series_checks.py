"""Lazy unfold and exact finite sums; no third-party dependencies."""
from fractions import Fraction
from itertools import islice


def unfold(step, state):
    while True:
        item, state = step(state)
        yield item


def geometric_step(n):
    return Fraction(1, 2 ** (n + 1)), n + 1


def with_partial_sums(step):
    def extended(state):
        source_state, total = state
        item, next_state = step(source_state)
        total = total + item
        return (item, total), (next_state, total)
    return extended


def finite_recursive_sum(count, items):
    if count == 0:
        return Fraction(0)
    if count < 0:
        raise ValueError('count must be nonnegative')
    previous = finite_recursive_sum(count - 1, items)
    return previous + next(items)


def main():
    pairs = list(islice(unfold(with_partial_sums(geometric_step), (0, Fraction(0))), 20))
    for count in range(21):
        partial = Fraction(0) if count == 0 else pairs[count - 1][1]
        recursive = finite_recursive_sum(count, unfold(geometric_step, 0))
        expected = 1 - Fraction(1, 2 ** count)
        assert partial == recursive == expected
        assert 1 - partial == Fraction(1, 2 ** count)
    print('Geometric: N=0..20, lazy partial sum = finite recursive sum = 1-2^(-N); exact checks passed')
    for count in (0, 1, 2, 4, 8):
        partial = Fraction(0) if count == 0 else pairs[count - 1][1]
        print(f'N={count}: partial={partial}, error={1-partial}')
    constant = list(islice(unfold(with_partial_sums(lambda n: (Fraction(1), n + 1)), (0, Fraction(0))), 6))
    alternating = list(islice(unfold(with_partial_sums(lambda n: (Fraction((-1) ** n), n + 1)), (0, Fraction(0))), 6))
    constant_sums = [int(total) for _, total in constant]
    alternating_sums = [int(total) for _, total in alternating]
    assert constant_sums == [1, 2, 3, 4, 5, 6]
    assert alternating_sums == [1, 0, 1, 0, 1, 0]
    print(f'Constant ones partial sums: {constant_sums}')
    print(f'Alternating signs partial sums: {alternating_sums}')
    print('All checks passed; productivity and convergence arguments are in productive_series.md.')


if __name__ == '__main__':
    main()
