"""This module generates a natural number multiples of the divisors.
"""


def generate_natural_divisibles(limit, *divisors):
    """Generation a natural number multiples of the divisors.
    Numbers are generated up to the limit.
    """
    if limit < 0:
        return
    for number in range(1, limit):
        if filter((lambda divider: number % divider == 0), divisors):
            yield number
