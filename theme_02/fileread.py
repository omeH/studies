"""The module read the file contents.

Usage:
    fileread.py [filename ...]

Description:
    In the absence of input file, reading comes from the standard input.
    Display the contents of the files produced on standard output.
"""
import signal

import sys


def hundler(error, stack):
    """Handler keystriles CTRL+C
    """
    sys.stderr.write(': {}\n'.format(error))
    sys.exit(1)


def transfer(file_):
    """This function reads data from a file blocks and writes them to
    standard output.
    """
    buffer_size = 256
    while True:
        line = file_.read(buffer_size)
        if not line:
            break
        sys.stdout.write(line)


def main():
    """The main function
    """
    signal.signal(signal.SIGINT, hundler)
    if len(sys.argv) == 1:
        transfer(sys.stdin)
        sys.exit(0)
    if sys.argv[1] == '-h':
        print(__doc__)
        sys.exit(0)
    file_names = sys.argv[1:]
    for name in file_names:
        try:
            file_ = open(name)
            transfer(file_)
            file_.close()
            # sys.stdout.write(open(file_).read())
        except IOError as error:
            sys.stderr.write('fileread.py: {}\n'.format(error.strerror))
            sys.exit(1)


if __name__ == '__main__':
    main()
