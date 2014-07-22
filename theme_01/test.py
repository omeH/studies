"""Testing the module naturalnambers
"""
from sys import argv

from naturalnumbers import sum_


def main():
    """Function main
    """
    arglist = argv
    if len(arglist) == 1:
        sum_(1000)
    else:
        for i in arglist[1:]:
            sum_(int(i))


if __name__ == '__main__':
    main()

