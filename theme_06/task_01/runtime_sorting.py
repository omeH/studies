"""The module displays information about the runtime to sort a list
of arbitrary length by the bubble and the built-in sorted().

Usage:
    runtime_sorting.py LIMIT ITERATION [-o] [--output-format]
                       [-h] [--help] [-d number] [--drop=number]
                       [-s] [--statistics]

Description:
    The module take one or more LIMIT values. The list of
    values with ','.

Parameters:
    LIMIT
        Sets the maximum number of values in the list.

    ITERATION
       Sets the number of executions of sorts.

Options:
    -d number, --drop=number
        Sets the number of excluded peak values of the algorithm.

    -h
        Print help on the module and exit.

    --help
        Print detailed help on the module and exit.

    -o, --output-format
        Switches the output format of the table to csv. Takes the
        value 'table' or 'csv'. The default value is 'table'.

    -s, --statistics
        Enables print of the calculated average values of the
        algorithm.

Examples:
    To run the module is necessary for it to pass parameters LIMIT
    and ITERATION:
        runtime_sorting.py LIMIT ITERATION

    To run the module and print statistics is necessary:
        runtime_sorting.py LIMIT ITERATION -s

"""

import sys
import argparse
import random
import time


# ------------
# Unit classes
# ------------
class ModuleProfiler(object):
    """This class is necessary to measure the runtime of the
    algorithm and print this values to the stdout.
    """

    def __init__(self, value, run=[]):
        self._value = value
        self._run = run

    def __enter__(self):
        self._start_time = time.time()

    def __exit__(self, type_, value, traceback):
        _end_time = time.time() - self._start_time
        self._run.append(_end_time)

        if self._value == 'table':
            sys.stdout.write('{:<15.5f}|'.format(_end_time))


class ModuleHelpAction(argparse._HelpAction):
    """The class for overriding method __call__
    """
    def __call__(self, parser, namespace, values, option_string=None):
        if 'help' in option_string:
            parser.print_help_detailed()
            parser.exit()
        parser.print_help()
        parser.exit()


class ModuleParser(argparse.ArgumentParser):
    """The class add method print_help_detailed
    """
    def print_help_detailed(self):
        """Print help documentation
        """
        sys.stdout.write(__doc__)


class ModuleBaseException(Exception):
    """The base class for all exceptions in this module
    """
    pass


# --------------------------
# Print function information
# --------------------------
def print_separation_line_info(iteration):
    """The function formation and print the separation line
    for a table total information.
    """
    sys.stdout.write('+{:9}+{:9}+'.format('-'*9, '-'*9))
    for _ in range(iteration):
        sys.stdout.write('{:15}+'.format('-'*15))
    sys.stdout.write('\n')


def print_separation_line_average():
    """The function formation and print the separation line
    for a table average values.
    """
    sys.stdout.write('+{:<9}+{:<9}+{:<15}+\n'.format('-'*9, '-'*9, '-'*15))


def print_cap_info(options):
    """The function formation and print the cap for a table
    total information.
    """
    if options.output_format == 'table':
        print_separation_line_info(options.iteration)
        sys.stdout.write('|{:<9}|{:<9}|'.format('Limit', 'Type'))
        for index in range(options.iteration):
            sys.stdout.write('{:<15}|'.format(index))
    elif options.output_format == 'csv':
        sys.stdout.write('{},{},'.format('Limit', 'Type'))
        for index in range(options.iteration):
            sys.stdout.write('{},'.format(index))

    sys.stdout.write('\n')


def print_cap_average(format_):
    """The function formation and print the cap for a table
    average values.
    """
    if format_ == 'table':
        print_separation_line_average()
        sys.stdout.write('|{:<9}|{:<9}|{:<15}|\n'.format('Limit',
                                                         'Type', 'Average'))
    elif format_ == 'csv':
        sys.stdout.write('{},{},{}\n'.format('Limit', 'Type', 'Average'))


def print_line_table(mode, *data):
    """The function formation and print the data line
    for a table total information.
    """
    if mode == 'table':
        sys.stdout.write('|{:<9}|{:<9}|'.format(*data))


def print_line_csv(info):
    """The function formation and print the data line
    for a csv total information.
    """
    def sort_by_type(input_list):
        """Sort the list by group
        """
        return input_list[1]

    info.sort(key=sort_by_type)

    for line in info:
        sys.stdout.write('{},{},'.format(*line[:2]))
        for item in line[2:]:
            sys.stdout.write('{:.5f},'.format(item))
        sys.stdout.write('\n')


def print_average_values(format_, info):
    """The function formation and print the data for a average
    values.
    """
    if format_ == 'table':
        print_cap_average(format_)
        for index in range(0, len(info), 2):
            print_separation_line_average()
            sys.stdout.write('|{:<9}|{:<9}|'.format(*info[index][:2]))
            sys.stdout.write(
                '{:<15.5f}|\n'.format(average_value(info[index][2:]))
            )
            sys.stdout.write('|{:<9}|{:<9}|'.format('', info[index + 1][1]))
            sys.stdout.write(
                '{:<15.5f}|\n'.format(average_value(info[index + 1][2:]))
            )
        print_separation_line_average()
    elif format_ == 'csv':
        print_cap_average(format_)
        for line in info:
            sys.stdout.write('{},{},'.format(*line[:2]))
            sys.stdout.write('{:.5f}\n'.format(average_value(line[2:])))


def parse_arg():
    """parse command line parameters passed to the module.
    """
    parser = ModuleParser(add_help=False)

    parser.add_argument('limits', type=str, help='Lengths list')
    parser.add_argument('iteration', type=int,
                        help='The number of repetitions.')
    parser.add_argument('-h', '--help', action=ModuleHelpAction,
                        help='Show help message and exit')
    parser.add_argument('-o', '--output-format', type=str, default='table',
                        help='Show help message and exit')
    parser.add_argument('-d', '--drop', type=int, default=0,
                        help='Number of omitted values')
    parser.add_argument('-s', '--statistics', action='store_true',
                        help='Enable print of statistics')

    return parser.parse_args()


def sort_bubble(list_):
    """The function to sort by bubble.
    """
    for i in range(len(list_) - 1):
        for j in range(len(list_) - i - 1):
            if list_[j] > list_[j + 1]:
                list_[j], list_[j + 1] = list_[j + 1], list_[j]


def init_list(limit):
    """The function returns a list of length 'limit' made up of
    random numbers.
    """
    return [random.randrange(limit) for _ in range(limit)]


def runtime(func, list_, format_, run):
    """The function runtime calculates and print it on the stdout.
    """
    with ModuleProfiler(format_, run) as _:
        func(list_)


def dropping(number, list_):
    """The function dropping from the peak values (max and min).
    """
    for line in list_:
        for _ in range(number):
            items = line[2:]
            line.remove(max(items))
            line.remove(min(items))


def average_value(list_):
    """The function calculates the average value.
    """
    return sum(list_) / len(list_)


def main():
    """The main function.
    """
    options = parse_arg()

    drop_min_max_values = 2
    if drop_min_max_values * options.drop >= options.iteration:
        raise ModuleBaseException('option value \'drop\' incorrect')

    limits = [int(limit) for limit in options.limits.split(',')]
    info = []

    print_cap_info(options)

    for limit in limits:
        if options.output_format == 'table':
            print_separation_line_info(options.iteration)
        print_line_table(options.output_format, limit, 'bubble')

        list_ = init_list(limit)
        run = [limit, 'bubble']

        for _ in range(options.iteration):
            runtime(sort_bubble, list_[:], options.output_format, run)
        info.append(run)

        if options.output_format == 'table':
            sys.stdout.write('\n')

        print_line_table(options.output_format, '', 'built-in')
        run = [limit, 'built-in']

        for _ in range(options.iteration):
            runtime(sorted, list_[:], options.output_format, run)
        info.append(run)

        if options.output_format == 'table':
            sys.stdout.write('\n')

    if options.output_format == 'table':
        print_separation_line_info(options.iteration)
    elif options.output_format == 'csv':
        print_line_csv(info)

    dropping(options.drop, info)

    if options.statistics:
        print_average_values(options.output_format, info)


if __name__ == '__main__':
    main()
