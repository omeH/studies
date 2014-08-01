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
    Module mast be passed two mandatory parameters: PATTERN - the string
    to search for in the file; REPLACE - the string which substitutions
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
        Set the suffix included in the file.The list of values with ','.

    -h
        Print help on the module and exit.

    --help
        Print detailed help on the module and exit.

    -v, --verbose
        Print detailed information about the implementation.

    -q, --quiet
        Suppresses information about the implementation.When combined
        with -v or --verbose, priority is -q or --quiet.

Examples:
    To rum the replacement PATTERN to REPLACE in files in current
    directory and show default information:
        replacer.py PATTERN REPLACE

    To rum the replacement PATTERN to REPLACE in files in the other
    directory and show default information:
        replacer.py PATTERN REPLACE -d [--directory=] DIRECTORY

    To rum the replacement PATTERN to REPLACE and show detail
    information:
        replacer.py PATTERN REPLACE -v [--verbose]

    To rum the replacement PATTERN to REPLACE and disable  show
    information:
        replacer.py PATTERN REPLACE -q [--quiet]

    To rum the replacement PATTERN to REPLACE whit certain suffix:
        replacer.py PATTERN REPLACE -i [--include-ext] TEMPLATE [,TEMPLATE,...]

"""

import os
import sys
import argparse


# Status of file
STATUS_ERROR = 1
STATUS_OMITTED = 2
STATUS_PROCESSED = 3
STATUS_FILTERED = 4
FILE_ERROR = -1
FILE_FILTERED = -2

MODE = {
    STATUS_ERROR: 'error',
    STATUS_OMITTED: 'omitted',
    STATUS_PROCESSED: 'processed',
    STATUS_FILTERED: 'filtered'
}

OPTIONS = None


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
        sys.stdout.write(__doc__)


def print_info_total(info):
    """This function formats the output of total information
    """
    if not OPTIONS.quiet:
        sys.stdout.write('Total processed: ' +
                         'directories - {}, '.format(len(info['directories'])) +
                         'files - {}, '.format(info['files']) +
                         'changes - {}, '.format(info['replaces']) +
                         'errors - {}.\n'.format(info['errors']))


def print_info_directory(directory=None):
    """This function formats the output of information about directory
    """
    if OPTIONS.quiet:
        print_info_directory.current_directory = directory
        return

    if OPTIONS.verbose:
        print_info_directory.current_directory = directory
        sys.stdout.write('Processing directory - {}\n'.format(directory))
        return

    print_info_directory.current_directory = directory


def print_info_file(file_name=None, count=0,
                    status=None, start=True):
    """This function formats the output modes of information about file
    """
    # Enable option -q or --quiet
    if OPTIONS.quiet:
        return

    # Enable option -i or --include-ext
    if OPTIONS.verbose:

        if start:
            sys.stdout.write('\tProcessing file - {}, '.format(file_name) +
                             'status: {}\n'.format(MODE[status]))
            return

        sys.stdout.write('\tProcessed file - {}, '.format(file_name) +
                         '{} - replacements\n\n'.format(count))
        return

    # Standard format output information
    if count > 0:
        sys.stdout.write('\tProcessed file - {}, '.format(file_name) +
                         '{} - replacements\n'.format(count))
        return


def parse_args():
    """Parse command line parameters passed to the module
    """
    parser = ModuleParser(add_help=False)

    parser.add_argument('pattern', type=str, help='Source string')
    parser.add_argument('replace', type=str, help='Replace string')
    parser.add_argument('-d', '--directory', type=str, default=os.getcwd(),
                        help='Target directory')
    parser.add_argument('-i', '--include-ext', type=str,
                        help='Sets the suffix included in file name')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Print details information')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Suppress information')
    parser.add_argument('-e', '--hide-errors', action='store_false',
                        help='Disable print error')
    parser.add_argument('-h', '--help', action=ModuleHelpAction,
                        help='Show help message and exit')

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

    # print information about the filtered file
    if not suffix_filter(file_name):
        print_info_file(file_name=full_file_name, status=STATUS_FILTERED)
        print_info_file(file_name=full_file_name, start=False)
        return FILE_FILTERED

    # Print information about the error while reading the file
    file_ = file_error(full_file_name, 'r')
    if file_ is None:
        print_info_file(file_name=full_file_name, status=STATUS_ERROR)
        print_info_file(file_name=full_file_name, start=False)
        return FILE_ERROR

    buffer_ = file_.read()
    file_.close()

    # Print information about the missing file
    count_ = buffer_.count(OPTIONS.pattern)
    if not count_:
        print_info_file(file_name=full_file_name, status=STATUS_OMITTED)
        print_info_file(file_name=full_file_name, count=count_, start=False)
        return count_

    # Print information about the error while writing the file
    file_ = file_error(full_file_name, 'w')
    if file_ is None:
        print_info_file(file_name=full_file_name, status=STATUS_ERROR)
        print_info_file(file_name=full_file_name, start=False)
        return FILE_ERROR

    # Print information about the processed file
    print_info_file(file_name=full_file_name, status=STATUS_PROCESSED)
    print_info_file(file_name=full_file_name, count=count_, start=False)

    file_.write(buffer_.replace(OPTIONS.pattern, OPTIONS.replace))
    file_.close()

    return count_


def main():
    """This main function
    """
    global OPTIONS
    OPTIONS = parse_args()

    if not OPTIONS.quiet:
        sys.stdout.write('List of changes: \n')

    info = {
        'directories': set(),
        'files': 0,
        'replaces': 0,
        'errors': 0
    }

    print_info_directory(OPTIONS.directory)

    for current, file_name in parse_dir():

        if current != print_info_directory.current_directory:
            print_info_directory(current)
        count = replace_str(current, file_name)

        info['files'] += 1
        info['directories'].add(current)
        if count > 0:
            info['replaces'] += count
        elif count == -1:
            info['errors'] += 1

    print_info_total(info)


if __name__ == '__main__':
    main()
