"""This module generates a number multiples of 3 or 5.
"""


def natural_numbers(limit):
    """Generation of the multiples 3 or 5
    """
    if limit < 0:
        return
    for number in range(1, limit):
        if number % 3 == 0 or number % 5 == 0:
            yield number
