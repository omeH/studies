"""Testing the module naturalnambers
"""

from naturalnumbers import generate_natural_divisibles


def main():
    """Function main
    """
    # Data 0, divisors 3 and 5, expected value 0
    sum_1 = sum(generate_natural_divisibles(0, 3, 5))
    if sum_1 != 0:
        print('Expected value is {}, actual is {}'.format(0, sum_1))
    # Data 1, divisors 3 and 5, expected value 0
    sum_2 = sum(generate_natural_divisibles(1, 3, 5))
    if sum_2 != 0:
        print('Expected value is {}, actual is {}'.format(0, sum_2))
    # Data 10, divisors 3 and 5, expected value 23
    sum_3 = sum(generate_natural_divisibles(10, 3, 5))
    if sum_3 != 23:
        print('Expected value is {}, actual is {}'.format(23, sum_3))
    # Data -1, divisors 3 and 5, expected value None
    sum_4 = sum(generate_natural_divisibles(-1, 3, 5))
    if sum_4:
        print('Expected value is {}, actual is {}'.format(None, sum_4))
    # Data -10, expected value None
    sum_5 = sum(generate_natural_divisibles(-10))
    if sum_5:
        print('Expected value is {}, actual is {}'.format(None, sum_5))
    # Data 'spam', expected value <exception>
    try:
        sum(generate_natural_divisibles('spam'))
    except TypeError:
        pass
    else:
        print('ERROR: excepted TypeError, but got no exception')
    # Data [], expected value <exception>
    try:
        sum(generate_natural_divisibles([]))
    except TypeError:
        pass
    else:
        print('ERROR: excepted TypeError, but got no exception')
    # Data 10, divisors 'spam', expected value <exception>
    try:
        sum(generate_natural_divisibles(10, 'spam'))
    except TypeError:
        pass
    else:
        print('ERROR: excepted TypeError, but got no exception')


if __name__ == '__main__':
    main()
