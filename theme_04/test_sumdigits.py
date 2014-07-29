"""Testing the module sudigits
"""

from sumdigits import factorial, sum_digits
from sumdigits import FactorialException, SumDigitsException


def test_positive(data, value):
    """Testing the factorial() with value positive and 0
    """
    sum_ = sum_digits(factorial(data))
    if sum_ != value:
        print('Test_positive: Expected value is {}, '.format(value) +
              'actual is {}'.format(sum_))


def test_negative(data, value):
    """Testing the sum_digits() with value negative
    """
    sum_ = sum_digits(data)
    if sum_ != value:
        print('Test_negative: Expected value is {}, '.format(value) +
              'actual is {}'.format(sum_))


def test_exception_factorial(data, msg):
    """Testing the factorial() to exception
    """
    try:
        sum_digits(factorial(data))
    except FactorialException:
        pass
    else:
        print('Test exception factorial: excepted \'{}\', '.format(msg) +
              'but got no exception\n')


def test_exception_sum_digits(data, msg):
    """Testing the sum_digits() to exception
    """
    try:
        sum_digits(data)
    except SumDigitsException:
        pass
    else:
        print('Test exception sum_digits: excepted \'{}\', '.format(msg) +
              'but got no exception\n')


def main():
    """The main function
    """
    # Test factorial()
    # Data 0, expected value 1
    test_positive(0, 1)
    # Data 5, expected value 3
    test_positive(5, 3)
    # Data 10, expected value 27
    test_positive(10, 27)
    # Data -10, expected value <exception>
    test_exception_factorial(-10, 'negative int')
    # Data 'str', expected value <exception>
    test_exception_factorial('str', 'not int')
    # Data [], expected value <exception>
    test_exception_factorial([], 'not int')

    # Test sum_digits()
    # Data -10, excepted value 1
    test_negative(-10, 1)
    # Data 'str', expected value <exception>
    test_exception_sum_digits('str', 'not int')
    # Data [], expected value <exception>
    test_exception_sum_digits([], 'not int')


if __name__ == '__main__':
    main()

