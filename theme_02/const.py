import os
import sys
import signal

BUFFER_SIZE = 2**20

STDOUT = sys.stdout
STDIN = sys.stdin
STDERR = sys.stderr
EXIT = sys.exit


def setmode(stdfiles):
    """Function sets BINARY mode to file STANDARD I/O if OS Windows
    """
    if 'win' in sys.platform:
        import msvcrt
    else:
        return

    for file_ in stdfiles:
        msvcrt.setmode(file_.fileno(), os.O_BINARY)


def sigint_handler(error, stack):
    """Handler keystrokes CTRL+C
    """
    STDERR.write('\n')
    EXIT(1)


def init_options():
    signal.signal(signal.SIGINT, sigint_handler)
    setmode([sys.stdin, sys.stdout])


def print_help(doc):
    if sys.argv[1] == '-h':
        STDOUT.write(doc)
        EXIT(0)


def get_file_names():
    file_names = sys.argv[1:]
    return file_names if file_names else None
