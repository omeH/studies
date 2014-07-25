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

BUFFER_SIZE = const.BUFFER_SIZE
STDIN = sys.stdin
STDOUT = sys.stdout

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
        line = file_.read(BUFFER_SIZE)
        if not line:
            break
        sys.stdout.write(line)


def main():
    """The main function
    """
    signal.signal(signal.SIGINT, sigint_handler)
    const.setmode([STDIN, STDOUT])
    if len(sys.argv) == 1:
        transfer(STDIN)
        sys.exit(0)
    if sys.argv[1] == '-h':
        print(__doc__)
        sys.exit(0)
    file_names = sys.argv[1:]
    error = 0
    for name in file_names:
        try:
            file_ = open(name, 'rb')
            transfer(file_)
            file_.close()
            # sys.stdout.write(open(file_).read())
        except IOError as error:
            sys.stderr.write('fileread.py: {}\n'.format(error))
    if error:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
