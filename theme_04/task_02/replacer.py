# -*- coding: utf-8 -*-
"""
This module iterates through the raplacement of one line to another
in all underluing directories.

Usage:
    scandir.py  [-d DIRECTORY] -p PATTERN -r REPLACE
                [--directory=DIRECTORY] --pattern=PATTERN --replace=REPLACE
                [-f FILTER] [--Filter-type=FILTER] [-h] [--help]
                [-s] [--secret]

Description:
    If you specify derictory, the bypass is perfoemed for this derictory.
    In the absence of this parameter is performed to bypass the current
    directory.
    Module mast be passed two mandatory parametrs: pattern - the string
    to search for in the file; replace - the string which subsitutions
    are made.

Options:
    -d DIRECTORY, --directory=DIRECTORY
        Parametr takes the initial directory.

    -f FILTER, --filter=FILTER
        Set the file type to change.

    -h, --help
        Print help on the module and exit.

    -p PATTERT, --pattern=PATTERN
        Search string in the file.

    -r REPLACE, --replace=REPLACE
        Replacement string in the file.

"""

import os
import sys
import argparse


class ModuleBaseException(BaseException):
    """The base class for all exceptions in this module
    """
    pass


class FileIOException(ModuleBaseException):
    """Exceptions generates by the IO error
    """
    pass


def print_help():
    """Print help docementation
    """
    sys.stdout.write(__doc__)


def parse_args():
    """Parse command line parameters passed to the module
    """
    parser = argparse.ArgumentParser()

    # Overriding
    parser.print_help = print_help

    parser.add_argument('pattern', type=str, help='Source srting')
    parser.add_argument('replace', type=str, help='Replace string')
    parser.add_argument('-d', '--directory', type=str, default=os.getcwd(),
                        help='Directory traversal')
    parser.add_argument('-f', '--Filter', type=str,
                        help='Sets the file type')
    parser.add_argument('-s', '--secret', action='store_true',
                        help='Type file')

    return parser.parse_args()


def file_error(file_name, mode):
    """This function intercepts exceptions to the function open
    """
    res = None
    try:
        res = open(file_name, mode)
    except IOError as error:
        sys.stderr.write('scandir.py: {}\n'.format(error))

    return res


def file_filter(file_name, filter_, secret):
    if not filter_:
        return True

    res = file_name.split('/')[-1].split('.')

    if not res[0] and secret:
        return True

    if res[-1] == filter_:
        return True

    return False


def parse_dir(directory):
    """This function returns the full name all files of the current
    and subdirectories.
    """
    for current, dirs, files in os.walk(directory):
        for file_ in files:
            yield os.path.join(current, file_)


def replace_str(file_name, source_line, replace_line):
    """This function searches the string source_line in the file and
    change it to reolace_line.
    """
    file_ = file_error(file_name, 'r')
    if file_ is None:
        return
    buffer_ = file_.read()
    file_.close()

    count = buffer_.count(source_line)
    if not count:
        return

    file_ = file_error(file_name, 'w')
    if file_ is None:
        return
    file_.write(buffer_.replace(source_line, replace_line))
    file_.close()


def main():
    """This main function
    """
    opt = parse_args()
    print(opt)
    for file_name in parse_dir(opt.directory):
        if not file_filter(file_name, opt.Filter, opt.secret):
            continue
        replace_str(file_name, opt.pattern, opt.replace)


if __name__ == '__main__':
    main()
