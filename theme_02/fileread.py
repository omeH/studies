"""The module read the file contents.
In the absence of input file, reading comes from the standart input.
--------------------------------------------------------------------
Format:
    fileread [filename...]
--------------------------------------------------------------------
Display the contents of the files produced on standart output.
"""

import sys

def main():
    """Function to read files
    """
    if len(sys.argv) == 1:
        sys.stdout.write(sys.stdin.read())
        return
    files = sys.argv[1:]
    for file_ in files:
        try:
            sys.stdout.write(open(file_).read())
        except IOError:
            sys.stderr.write('File \'{}\' not found\n'.format(file_))


if __name__ == '__main__':
    main()
