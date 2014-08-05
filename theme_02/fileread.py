"""The module read the file contents.

Usage:
    fileread.py [filename ...]

Description:
    In the absence of input file, reading comes from the standard input.
    Display the contents of the files produced on standard output.
"""
import signal
import sys

import const


def sigint_handler(error, stack):
    """Handler keystrokes CTRL+C
    """
    sys.stderr.write('\n')
    sys.exit(1)


def transfer(file_):
    """This function reads data from a file blocks and writes them to
    standard output.
    """
    while True:
        block = file_.read(const.BUFFER_SIZE)
        if not block:
            break
        sys.stdout.write(block)


def main():
    """The main function
    """
    signal.signal(signal.SIGINT, sigint_handler)
    const.setmode([sys.stdin, sys.stdout])

    if len(sys.argv) == 1:
        transfer(sys.stdin)
        sys.exit(0)

    if sys.argv[1] == '-h':
        print(__doc__)
        sys.exit(0)

    file_names = sys.argv[1:]
    for file_name in file_names:
        try:
            file_ = open(file_name, 'rb')
            transfer(file_)
            file_.close()
            # sys.stdout.write(open(file_).read())
        except IOError as error:
            sys.stderr.write('fileread.py: {}\n'.format(error))


if __name__ == '__main__':
    main()
