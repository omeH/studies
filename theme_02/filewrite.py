"""The module writes the data in file.

Usage:
    filewrite.py filename

Description:
    The module receives data from the standard input and writes
    them to the specified file.
"""

import const


def copy_stdin_to_file(file_):
    """Thia function reads data from a standard input blocks and
    writes to file.
    """
    while True:
        block = const.STDIN.read(const.BUFFER_SIZE)
        if not block:
            break
        file_.write(block)


def main():
    """The main function
    """
    const.init_options()
    file_name = const.get_file_names()
    error_message = 'Filewrite.py: missing operand specifiers the file.\n' + \
        'Get more information on the command: "filewrite.py -h\n'

    if file_name is None:
        const.STDERR.write(error_message)
        const.EXIT(1)

    const.print_help(__doc__)

    try:
        file_ = open(file_name[0], 'wb')
        copy_stdin_to_file(file_)
        file_.close()
    except IOError as error:
        const.STDERR.write('filewrite.py: {}\n'.format(error))
    else:
        const.EXIT(0)


if __name__ == '__main__':
    main()
