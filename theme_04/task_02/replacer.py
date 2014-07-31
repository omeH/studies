# -*- coding: utf-8 -*-
"""
This module iterates through the raplacement of one line to another
in all underluing directories.

Usage:
    scandir.py  PATTERN REPLACE [-d DIRECTORY] [--directory=DIRECTORY]
                [-t TEMPLATE] [--type-file=TEMPLATE] [-h] [--help]
                [-s] [--secret]

Description:
    If you specify derictory, the bypass is perfoemed for this derictory.
    In the absence of this parameter is performed to bypass the current
    directory.
    Module mast be passed two mandatory parametrs: pattern - the string
    to search for in the file; replace - the string which subsitutions
    are made.

Parametrs:
    PATTERN
        Search string in the file.

    REPLACE
        Replacement string in the file.

Options:
    -d DIRECTORY, --directory=DIRECTORY
        Parametr takes the initial directory.

    -e, --error
        Includes error output.

    -t TEMPLATE, --type-file=TAMPLATE
        Set the file type to change. The list of values with ','.

    -i TEMPLATE, --include-ext=TAMPLATE
        Set the suffix included in the file name.
        The list of values with ','.

    -h, --help
        Print help on the module and exit.

    -v, --verbose
        Print detailed information about the implementation.

    -q, --quiet
        Suppresses information about the implementaion.

"""

import os
import sys
import argparse


STATUS_ERROR = 1
STATUS_OMITTED = 2
STATUS_PROCESSED = 3

FILE_ERROR = 0

OPTIONS = None


class ModuleBaseException(BaseException):
    """The base class for all exceptions in this module
    """
    pass


class ModuleParser(argparse.ArgumentParser):
    """The class for overriding method print_help
    """
    def print_help(self, file_=None):
        """Print help documentation
        """
        sys.stdout.write(__doc__ + '\n')
        sys.exit(0)


def print_info(directory=None, file_name=None, count=0,
               status=None, verbose=False, quiet=False, start=True):
    """This function formats the output modes of information
    """
    # Enable option -q or --quiet
    if quiet:
        return

    mode = {
        1: 'error',
        2: 'omitted',
        3: 'processed'
    }
    # Enable option -i or --include-ext
    if verbose:
        if directory:
            print_info.current_directory = directory
            sys.stdout.write('Processing directory - {}\n'.format(directory))
            return

        if start:
            sys.stdout.write('\tProcesseing file - {}, '.format(file_name) +
                             'status: {}\n'.format(mode[status]))
            return

        sys.stdout.write('\tProcessed file - {}, '.format(file_name) +
                         '{} - replacements\n\n'.format(count))
        return

    # Standart format output information
    if count > 0:
        sys.stdout.write('\tProcessed file - {}, '.format(file_name) +
                         '{} - replacements\n'.format(count))


def parse_args():
    """Parse command line parameters passed to the module
    """
    parser = ModuleParser()

    parser.add_argument('pattern', type=str, help='Source srting')
    parser.add_argument('replace', type=str, help='Replace string')
    parser.add_argument('-d', '--directory', type=str, default=os.getcwd(),
                        help='Directory traversal')
    parser.add_argument('-i', '--include-ext', type=str,
                        help='Sets the suffix included in file name')
    parser.add_argument('-t', '--type-file', type=str,
                        help='Sets the file type')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Print details information')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Suppress information')
    parser.add_argument('-e', '--error', action='store_true',
                        help='Print error')

    return parser.parse_args()


def file_error(file_name, mode, print_):
    """This function intercepts exceptions to the function open
    """
    res = None
    try:
        res = open(file_name, mode)
    except IOError as error:
        if print_:
            sys.stderr.write('scandir.py: {}\n'.format(error))

    return res


def type_filter(file_name, filter_):
    """This function filtres files on a specified type
    """
    if not filter_:
        return True

    res = file_name.split('.')
    ext = filter_.split(',')

    if res[-1] in ext:
        return True

    return False


def suffix_filter(file_name, filter_):
    """This function filtres files on a specified suffix
    """
    if not filter_:
        return True

    suffix = file_name.split('.')
    if len(suffix) == 1:
        return False

    ext = filter_.split(',')

    if suffix[-1] in ext:
        return True

    return False


def parse_dir(directory):
    """This function returns the full name all files of the current
    and subdirectories.
    """
    for current, dirs, files in os.walk(directory):
        for file_ in files:
            yield current, file_


def replace_str(directory, file_name, data):
    """This function searches the string source_line in the file and
    change it to reolace_line.
    """
    full_file_name = os.path.join(directory, file_name)
    if data.verbose:
        if directory != print_info.__dict__['current_directory']:
            print_info(directory=directory, verbose=data.verbose)

    file_ = file_error(full_file_name, 'r', data.error)
    if file_ is None:
        # Print information to processing
        print_info(
            file_name=full_file_name,
            status=STATUS_ERROR,
            verbose=data.verbose,
            quiet=data.quiet
        )
        # Print information to processed
        print_info(
            file_name=full_file_name,
            verbose=data.verbose,
            start=False,
            quiet=data.quiet
        )
        return FILE_ERROR

    buffer_ = file_.read()
    file_.close()

    count_ = buffer_.count(data.pattern)
    if not count_:
        # Print information to processing
        print_info(
            file_name=full_file_name,
            status=STATUS_OMITTED,
            verbose=data.verbose
        )
        # Print information to processed
        print_info(
            file_name=full_file_name,
            count=count_,
            verbose=data.verbose,
            start=False,
            quiet=data.quiet
        )
        return count_

    file_ = file_error(full_file_name, 'w', data.error)
    if file_ is None:
        # Print information to processing
        print_info(
            file_name=full_file_name,
            status=STATUS_ERROR,
            verbose=data.verbose
        )
        # Print information to processed
        print_info(
            file_name=full_file_name,
            verbose=data.verbose,
            start=False,
            quiet=data.quiet
        )
        return FILE_ERROR
    # Print information to processing
    print_info(
        file_name=full_file_name,
        status=STATUS_PROCESSED,
        verbose=data.verbose
    )
    # Print information to processed
    print_info(
        file_name=full_file_name,
        count=count_,
        verbose=data.verbose,
        start=False,
        quiet=data.quiet
    )
    file_.write(buffer_.replace(data.pattern, data.replace))
    file_.close()

    return count_


def main():
    """This main function
    """
    OPTIONS = parse_args()

    if not OPTIONS.quiet:
        sys.stdout.write('List of changes: \n')
        print_info(
            directory=OPTIONS.directory,
            verbose=OPTIONS.verbose
        )

    info = {
        'dirs': set(),
        'files': 0,
        'replaces': 0
    }
    count = 0

    # print(opt)
    for current, file_name in parse_dir(OPTIONS.directory):
        info['dirs'].add(current)
        if not type_filter(file_name, OPTIONS.type_file):
            continue
        if not suffix_filter(file_name, OPTIONS.include_ext):
            continue
        info['files'] += 1
        count = replace_str(current, file_name, OPTIONS)
        if count:
            info['replaces'] += 1
    # print(info)
    # print(files)
    if not OPTIONS.quiet:
        sys.stdout.write('Total processed: ' +
                         'directorys - {}, '.format(len(info['dirs'])) +
                         'files - {}, '.format(info['files']) +
                         'changes - {}.\n'.format(info['replaces']))


if __name__ == '__main__':
    main()
