"""This module performs a counting the sum of digits in the number of n!.

Usage:
    factorial.py [-h] n [...]

Description:
    factorial.py receivers one or more values n. For each values of n is n!
    and calculated the sum of digits in the number n! Value of n! is only
    natural numbers.

Options:
    -h Print help on the module and exit.

"""

import sys


def factorial(n):
    """This function finds the value of n!
    """
    if n < 0:
        return None
    res = 1
    for i in range(1, n+1):
        res *= i
    return res


def sumDigits(number):
    """This function calculates the sum of the digits for number
    """
    return sum([int(i) for i in str(number)]) if number else None


def main():
    """The main function
    """
    errorstr = 'factorial.py: missing operand specifiels the file.\n' + \
        'Get more information on the command: factorial.py -h\n'
    if len(sys.argv) == 1:
        sys.stderr.write(errorstr)
        sys.exit(1)
    if sys.argv[1] == '-h':
        sys.stdout.write(__doc__)
        sys.exit(0)
    numbers = sys.argv[1:]
    for number in numbers:
        try:
            sum_ = sumDigits(factorial(int(number)))
            sys.stdout.write('Sum of digits {}!: {}\n'.format(number, sum_))
        except ValueError as error:
            sys.stderr.write('Parameter {}: {}\n'.format(number, error))


if __name__ == '__main__':
    main()
