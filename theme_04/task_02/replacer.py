# -*- coding: utf-8 -*-
"""
This module iterates through the raplacement of one line to another
in all underluing directories.

Usage:
    scandir.py  PATTERN REPLACE [-d DIRECTORY] [--directory=DIRECTORY]
                [-i FILTER] [--include-ext=FILTER] [-h] [--help]
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

    -i FILTER, --include-ext=FILTER
        Set the file type to change.

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


STATUS_ERROR = 0
STATUS_OMITTED = 1
STATUS_PROCESSED = 2

FILE_ERROR = -1


class ModuleBaseException(BaseException):
    """The base class for all exceptions in this module
    """
    pass


class FileIOException(IOError):
    """Exceptions generates by the IO error
    """
    pass


def print_help():
    """Print help docementation
    """
    sys.stdout.write(__doc__)
    sys.exit(0)


def print_info_2(directory, file_name=None,
                 count=0, status=None, include_ext=False, start=True):
    # Enable option -i or --include-ext
    if include_ext:
        if directory:
            print_info_2.current_directory = directory
            sys.stdout.write('Processing directory - {}'.format(directory))
            return

        if start:
            sys.stdout.write('\tProcesseing file - {}, '.format(file_name) +
                             'status: {}\n'.format(status))
            return

        sys.stdout.write('\tProcessed file - {}, '.format(file_name) +
                         '{} - replacements\n'.format(count))
        return

    # Standart format output information
    if count > 0:
        sys.stdout.write('\tProcessed file - {}, '.format(file_name) +
                         '{} - replacements\n'.format(count))


def print_info(info, files, verbose, quiet):
    """This function formats the output modes of information
    """
    # Enable option -q or --quiet
    if quiet:
        sys.exit(0)

    count = 0
    status = {
        0: 'error',
        1: 'omitted',
        2: 'processed'
    }
    sys.stdout.write('List of changes:\n')

    # Enable option -v or --verbose
    if verbose:
        tmp = files[0][0]
        sys.stdout.write('{}\n'.format(tmp))
        for file_ in files:
            if tmp != file_[0]:
                tmp = file_[0]
                sys.stdout.write('\n{}\n'.format(tmp))

            sys.stdout.write('\tIn file ->{}<- '.format(file_[1]) +
                             'is entered {}'.format(file_[2]) +
                             ' changes; ' +
                             'status: {}\n'.format(status[file_[-1]]))
            count += file_[2] if file_[2] > 0 else 0

    # Standart format output information
    if not verbose:
        for file_ in files:
            if file_[2] > 0:
                sys.stdout.write('\tIn file ->{}<- '.format(file_[1]) +
                                 'is entered {}'.format(file_[2]) +
                                 ' changes\n')
                count += file_[2]

    sys.stdout.write('\nTotal find: ' +
                     'directorys - {}, '.format(len(info['dirs'])) +
                     'files - {}, '.format(info['files']) +
                     'in {} files is entered '.format(info['replaces']) +
                     '{} changes.\n'.format(count))
    sys.exit(0)


def parse_args():
    """Parse command line parameters passed to the module
    """
    parser = argparse.ArgumentParser()

    # Overriding
    # parser.print_help = print_help

    parser.add_argument('pattern', type=str, help='Source srting')
    parser.add_argument('replace', type=str, help='Replace string')
    parser.add_argument('-d', '--directory', type=str, default=os.getcwd(),
                        help='Directory traversal')
    parser.add_argument('-i', '--include-ext', type=str,
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
    except FileIOException as error:
        if print_:
            sys.stderr.write('scandir.py: {}\n'.format(error))

    return res


def file_filter(file_name, filter_):
    """Thia function filtres files on a specified type
    """
    if not filter_:
        return True

    res = file_name.split('.')
    '''
    if not res[0] and secret:
        return True
    '''

    if res[-1] == filter_:
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
        if directory != print_info_2.__dict__['current_directory']:
            print_info_2(directory, include_ext=data.include_ext)

    file_ = file_error(full_file_name, 'r', data.error)
    if file_ is None:
        return FILE_ERROR, STATUS_ERROR
    buffer_ = file_.read()
    file_.close()

    count = buffer_.count(data.pattern)
    if not count:
        return count, STATUS_OMITTED

    file_ = file_error(full_file_name, 'w', data.error)
    if file_ is None:
        return FILE_ERROR, STATUS_ERROR
    file_.write(buffer_.replace(data.pattern, data.replace))
    file_.close()

    return count, STATUS_PROCESSED


def main():
    """This main function
    """
    opt = parse_args()
    sys.stdout.write('List of changes: \n')
    print_info_2(opt._directory, opt.include_ext)
    info = {
        'dirs': set(),
        'files': 0,
        'replaces': 0
    }
    files = []

    print(opt)
    for current, file_name in parse_dir(opt.directory):
        info['dirs'].add(current)
        info['files'] += 1
        if not file_filter(file_name, opt.include_ext):
            continue
        count, status = replace_str(current, file_name, opt)
        files.append((current, file_name, count, status))
        if count > 0:
            info['replaces'] += 1
    # print(info)
    # print(files)
    print_info(info, files, opt.verbose, opt.quiet)


if __name__ == '__main__':
    main()
