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
    if len(sys.argv) == 1:
        sys.stdout.write(sys.stdin.read())
        return


if __name__ == '__main__':
    main()
