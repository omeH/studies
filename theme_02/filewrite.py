"""The module writes the data in file.

Usage:
    filewrite.py filename

Description:
    The module receives data from the standard input and writes
    them to the specified file.
"""

import signal
import sys

import const


def sigint_handler(error, stack):
    """Handler keystrokes CTRL+C
    """
    sys.stdout.write('\n')
    sys.exit(1)


def transfer(file_):
    """Thia function reads data from a standard input blocks and
    writes to file.
    """
    while True:
        block = sys.stdin.read(const.BUFFER_SIZE)
        if not block:
            break
        file_.write(block)


def main():
    """The main function
    """
    signal.signal(signal.SIGINT, sigint_handler)
    const.setmode([sys.stdin, sys.stdout])
    errorstr = 'Filewrite.py: missing operand specifiels the file.\n' + \
        'Get more informaition on the command: "filewrite.py -h\n'
    if len(sys.argv) == 1:
        sys.stderr.write(errorstr)
        sys.exit(1)
    if sys.argv[1] == '-h':
        print(__doc__)
        sys.exit(0)
    try:
        file_ = open(sys.argv[1], 'wb')
        transfer(file_)
        file_.close()
    except IOError as error:
        sys.stderr.write('filewrite.py: {}\n'.format(error))
    else:
        sys.exit(0)
    sys.exit(1)


if __name__ == '__main__':
    main()
