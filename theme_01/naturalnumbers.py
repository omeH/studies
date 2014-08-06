"""This module generates a natural number multiples of the divisors.
"""


def check_natural_divisible(number, divisors):
    """This function checks if number multiples of the divisors.
    """
    for divired in divisors:
        if number % divired == 0:
            return True


def generate_natural_divisibles(limit, *divisors):
    """Generation a natural number multiples of the divisors.
    Numbers are generated up to the limit.
    """
    if limit < 0:
        return
    for number in range(1, limit):
        if check_natural_divisible(number, divisors):
            yield number
