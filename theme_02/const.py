import os
import sys

BUFFER_SIZE = 2**20


def setmode(stdfiles):
    """Function sets BINARY mode to file STANDARD I/O if OS Windows
    """
    if 'win' in sys.platform:
        import msvcrt
    else:
        return

    for file_ in stdfiles:
        msvcrt.setmode(file_.fileno(), os.O_BINARY)
