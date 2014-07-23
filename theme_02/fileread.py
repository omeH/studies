"""The module read the file contents.

USsage:
    fileread.py [filename ...]

Description:
    In the absence of input file, reading comes from the standart input.
    Display the contents of the files produced on standart output.
"""

import sys
import os


def main():
    """Function to read files
    """
    if len(sys.argv) == 1:
        sys.stdout.write(sys.stdin.read())
        return
    files = sys.argv[1:]
    for file_ in files:
        if os.access(file_, os.F_OK):
            if os.access(file_, os.R_OK):
                file_ = open(file_)
                sys.stdout.write(file_.read())
                file_.close()
                # sys.stdout.write(open(file_).read())
            else:
                sys.stderr.write('Error: access deniad \'{}\'\n'.format(file_))
        else:
            sys.stderr.write('Error: file \'{}\' not found\n'.format(file_))


if __name__ == '__main__':
    main()
