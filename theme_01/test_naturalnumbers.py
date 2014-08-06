"""Testing the module naturalnambers
"""

from naturalnumbers import natural_numbers


def main():
    """Function main
    """
    # Data 0, expected value 0
    sum_1 = sum(natural_numbers(0))
    if sum_1 != 0:
        print('Expected value is {}, actual is {}'.format(0, sum_1))
    # Data 1, expected value 0
    sum_2 = sum(natural_numbers(1))
    if sum_2 != 0:
        print('Expected value is {}, actual is {}'.format(0, sum_2))
    # Data 10, expected value 23
    sum_3 = sum(natural_numbers(10))
    if sum_3 != 23:
        print('Expected value is {}, actual is {}'.format(23, sum_3))
    # Data -1, expected value None
    sum_4 = sum(natural_numbers(-1))
    if sum_4:
        print('Expected value is {}, actual is {}'.format(None, sum_4))
    # Data -10, expected value None
    sum_5 = sum(natural_numbers(-10))
    if sum_5:
        print('Expected value is {}, actual is {}'.format(None, sum_5))
    # Data 'spam', expected value <exception>
    try:
        sum(natural_numbers('spam'))
    except TypeError:
        pass
    else:
        print('ERROR: excepted TypeError, but got no exception')
    # Data [], expected value <exception>
    try:
        sum(natural_numbers([]))
    except TypeError:
        pass
    else:
        print('ERROR: excepted TypeError, but got no exception')


if __name__ == '__main__':
    main()

