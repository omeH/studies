"""Testing the module sudigits
"""

from sumdigits import factorial, sumDigits


def main():
    """The main function
    """
    # Data 0, expected value 1
    sum_1 = sumDigits(factorial(0))
    if sum_1 != 1:
        print('Expected value is {}, actual is {}'.format(0, sum_1))
    # Data 5, expected value 3
    sum_2 = sumDigits(factorial(5))
    if sum_2 != 3:
        print('Expected value is {}, actual is {}'.format(0, sum_2))
    # Data 10, expected value 27
    sum_3 = sumDigits(factorial(10))
    if sum_3 != 27:
        print('Expected value is {}, actual is {}'.format(0, sum_3))
    # Data -10, expected value None
    sum_4 = sumDigits(factorial(-10))
    if sum_4 is not None:
        print('Expected value is {}, actual is {}'.format(0, sum_4))
    # Data 'str', expected value <exception>
    try:
        sumDigits(factorial('str'))
    except TypeError:
        pass
    else:
        print('Error: excepted TypeError, but got no exception')
    # Data [], expected value <exception>
    try:
        sumDigits(factorial([]))
    except TypeError:
        pass
    else:
        print('Error: excepted TypeError, but got no exception')


if __name__ == '__main__':
    main()

