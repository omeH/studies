"""Testing the module naturalnambers
"""
# from sys import argv

from naturalnumbers import multiples


def main():
    """Function main
    """
    # Data 0, expected value 0
    sum_1 = sum(multiples(0))
    if sum_1 != 0:
        print('Expected value is {}, actual is {}'.format(0, sum_1))
    # Data 1, expected value 0
    sum_2 = sum(multiples(1))
    if sum_2 != 0:
        print('Expected value is {}, actual is {}'.format(0, sum_2))
    # Data 10, expected value 23
    sum_3 = sum(multiples(10))
    if sum_3 != 23:
        print('Expected value is {}, actual is {}'.format(23, sum_3))
    # Data -1, expected value 0
    sum_4 = sum(multiples(-1))
    if sum_4 != 0:
        print('Expected value is {}, actual is {}'.format(0, sum_4))
    # Data -10, expected value 23
    sum_5 = sum(multiples(-10))
    if sum_5 != -23:
        print('Expected value is {}, actual is {}'.format(-23, sum_5))
    # Data 'spam', expected value <exception>
    try:
        sum_spam = sum(multiples('spam'))
    except TypeError:
        print('ERROR: value is {}'.format('spam'))
    # Data [], expected value <exception>
    try:
        sum_list = sum(multiples([]))
    except TypeError:
        print('ERROR: value is {}'.format([]))


if __name__ == '__main__':
    main()

