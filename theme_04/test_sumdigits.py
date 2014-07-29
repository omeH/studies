"""Testing the module sudigits
"""

from sumdigits import factorial, sum_digits, FactorialException


def test_positive(data, value):
    """Testing the factorial() with value positive and 0
    """
    sum_ = sum_digits(factorial(data))
    if sum_ != value:
        print('Test_positive: Expected value is {}, '.format(value) +
              'actual is {}'.format(sum_))


def test_exception(data, msg):
    """Testing the factorial() to exception
    """
    try:
        sum_digits(factorial(data))
    except FactorialException:
        pass
    else:
        print('Test exception: excepted \'{}\', '.format(msg) +
              'but got no exception\n')


def main():
    """The main function
    """
    # Data 0, expected value 1
    test_positive(0, 1)
    # Data 5, expected value 3
    test_positive(5, 3)
    # Data 10, expected value 27
    test_positive(10, 27)
    # Data -10, expected value <exception>
    test_exception(-10, 'negative int')
    # Data 'str', expected value <exception>
    test_exception('str', 'not int')
    # Data [], expected value <exception>
    test_exception([], 'not int')


if __name__ == '__main__':
    main()

