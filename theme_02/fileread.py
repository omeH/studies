"""The module read the file contents.

USsage:
    fileread.py [filename ...]

Description:
    In the absence of input file, reading comes from the standart input.
    Display the contents of the files produced on standart output.
"""

import sys
import os


def write(arg):
    """FUnction writes content to standart output
    """
    while True:
        line = arg.read(256)
        if not  line:
            break
        sys.stdout.write(line)


def main():
    """Function to read files
    """
    if len(sys.argv) == 1:
        write(sys.stdin)
        return
    namefiles = sys.argv[1:]
    for name in namefiles:
        if os.access(file_, os.F_OK):
            if os.access(file_, os.R_OK):
                file_ = open(name)
                write(file_)
                file_.close()
                # sys.stdout.write(open(file_).read())
            else:
                sys.stderr.write('Error: access deniad \'{}\'\n'.format(file_))
        else:
            sys.stderr.write('Error: file \'{}\' not found\n'.format(file_))


if __name__ == '__main__':
    main()
