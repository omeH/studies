# -*- coding: utf-8 -*-
"""
This module iterates through the replacement of one line to another
in all underlying directories.

Usage:
    replacer.py  PATTERN REPLACE [-d DIRECTORY] [--directory=DIRECTORY]
                [-i TEMPLATE] [--include-ext=TEMPLATE] [-h] [--help]
                [-e] [--hide-errors] [-v] [--verbose] [-q] [--quiet]

Description:
    If you specify directory, the bypass is performed for this directory.
    In the absence of this parameter is performed to bypass the current
    directory.
    Module mast be passed two mandatory parameters: pattern - the string
    to search for in the file; replace - the string which substitutions
    are made.

Parameters:
    PATTERN
        Search string in the file.

    REPLACE
        Replacement string in the file.

Options:
    -d DIRECTORY, --directory=DIRECTORY
        Parameter takes the initial directory.

    -e, --hide-errors
        Disable errors output.

    -i TEMPLATE, --include-ext=TEMPLATE
        Set the suffix included in the file.
        The list of values with ','.

    -h
        Print help on the module and exit.

    --help
        Print detailed help on the module and exit.

    -v, --verbose
        Print detailed information about the implementation.

    -q, --quiet
        Suppresses information about the implementation.

"""

import os
import sys
import argparse


STATUS_ERROR = 1
STATUS_OMITTED = 2
STATUS_PROCESSED = 3
STATUS_FILTERED = 4

FILE_ERROR = 0

OPTIONS = None


class ModuleBaseException(BaseException):
    """The base class for all exceptions in this module
    """
    pass


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
    """The class add method print_help
    """
    def print_help_detailed(self):
        """Print help documentation
        """
        sys.stdout.write(__doc__ + '\n')


def print_info(directory=None, file_name=None, count=0,
               status=None, start=True):
    """This function formats the output modes of information
    """
    # Enable option -q or --quiet
    if OPTIONS.quiet:
        print_info.first = True
        return

    mode = {
        1: 'error',
        2: 'omitted',
        3: 'processed',
        4: 'filtered'
    }
    # Enable option -i or --include-ext
    if OPTIONS.verbose and status:
        if directory:
            print_info.first = False
            print_info.current_directory = directory
            sys.stdout.write('Processing directory - {}\n'.format(directory))
            return

        if start:
            sys.stdout.write('\tProcessing file - {}, '.format(file_name) +
                             'status: {}\n'.format(mode[status]))
            return

        sys.stdout.write('\tProcessed file - {}, '.format(file_name) +
                         '{} - replacements\n\n'.format(count))
        return

    # Standard format output information
    if count > 0:
        sys.stdout.write('\tProcessed file - {}, '.format(file_name) +
                         '{} - replacements\n'.format(count))
        return
    print_info.first = True


def parse_args():
    """Parse command line parameters passed to the module
    """
    parser = ModuleParser(add_help=False)

    parser.add_argument('pattern', type=str, help='Source string')
    parser.add_argument('replace', type=str, help='Replace string')
    parser.add_argument('-d', '--directory', type=str, default=os.getcwd(),
                        help='Directory traversal')
    parser.add_argument('-i', '--include-ext', type=str,
                        help='Sets the suffix included in file name')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Print details information')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Suppress information')
    parser.add_argument('-e', '--hide-errors', action='store_false',
                        help='Print error')
    parser.add_argument('-h', '--help', action=ModuleHelpAction)

    return parser.parse_args()


def file_error(file_name, mode):
    """This function intercepts exceptions to the function open
    """
    res = None
    try:
        res = open(file_name, mode)
    except IOError as error:
        if OPTIONS.hide_errors:
            sys.stderr.write('->>{}\n'.format(error))

    return res


def suffix_filter(file_name):
    """This function filters files on a specified suffix
    """
    if not OPTIONS.include_ext:
        return True

    suffix = file_name.split('.')
    if len(suffix) == 1:
        return False

    ext = OPTIONS.include_ext.split(',')

    if suffix[-1] in ext:
        return True

    return False


def parse_dir():
    """This function returns the full name all files of the current
    and subdirectories.
    """
    for current, dirs, files in os.walk(OPTIONS.directory):
        for file_ in files:
            yield current, file_


def replace_str(directory_, file_name):
    """This function searches the string source_line in the file and
    change it to replace_line.
    """
    full_file_name = os.path.join(directory_, file_name)

    if OPTIONS.verbose:
        if directory_ != print_info.__dict__['current_directory']:
            print_info(directory=directory_, status=True)

    # print information about the filtered file
    if not suffix_filter(file_name):
        # Print information to processing
        print_info(file_name=full_file_name, status=STATUS_FILTERED)
        # Print information to processed
        print_info(file_name=full_file_name, status=True, start=False)
        return FILE_ERROR

    # Print information about the error while reading the file
    file_ = file_error(full_file_name, 'r')
    if file_ is None:
        # Print information to processing
        print_info(file_name=full_file_name, status=STATUS_ERROR)
        # Print information to processed
        print_info(file_name=full_file_name, status=True, start=False)
        return FILE_ERROR

    buffer_ = file_.read()
    file_.close()

    # Print information about the missing file
    count_ = buffer_.count(OPTIONS.pattern)
    if not count_:
        # Print information to processing
        print_info(file_name=full_file_name, status=STATUS_OMITTED)
        # Print information to processed
        print_info(file_name=full_file_name, count=count_,
                   status=True, start=False)
        return count_

    # Print information about the error while writing the file
    file_ = file_error(full_file_name, 'w')
    if file_ is None:
        # Print information to processing
        print_info(file_name=full_file_name, status=STATUS_ERROR)
        # Print information to processed
        print_info(file_name=full_file_name, status=True, start=False)
        return FILE_ERROR

    # Print information about the processed file
    # Print information to processing
    print_info(file_name=full_file_name, status=STATUS_PROCESSED)
    # Print information to processed
    print_info(file_name=full_file_name, count=count_, status=True, start=False)

    file_.write(buffer_.replace(OPTIONS.pattern, OPTIONS.replace))
    file_.close()

    return count_


def main():
    """This main function
    """
    global OPTIONS
    OPTIONS = parse_args()
    print_info()

    if not OPTIONS.quiet:
        sys.stdout.write('List of changes: \n')
        # print_info()

    info = {
        'dirs': set(),
        'files': 0,
        'replaces': 0
    }
    count = 0

    for current, file_name in parse_dir():
        info['dirs'].add(current)
        if print_info.first:
            print_info(
                directory=current,
                status=True
            )
        info['files'] += 1
        count = replace_str(current, file_name)
        if count:
            info['replaces'] += count

    if not OPTIONS.quiet:
        sys.stdout.write('Total processed: ' +
                         'directories - {}, '.format(len(info['dirs'])) +
                         'files - {}, '.format(info['files']) +
                         'changes - {}.\n'.format(info['replaces']))


if __name__ == '__main__':
    main()
