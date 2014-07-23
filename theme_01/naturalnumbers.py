"""Find the sum of all the multiples of 3 or 5 below 1000.
"""


def multiples(count):
    """Generation of the multiples 3 or 5
    """
    if count < 0:
        return
    for i in range(1, count):
        if i%3 == 0 or i%5 == 0:
            yield i

