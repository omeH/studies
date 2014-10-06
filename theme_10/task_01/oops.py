INDEXERROR_MESSAGE = 'Oops! IndexError'
KEYERROR_MESSAGE = 'Oops! KeyError'


def oops_indexerror():
    raise IndexError(INDEXERROR_MESSAGE)


def oops_keyerror():
    raise KeyError(KEYERROR_MESSAGE)


def main(oops):
    try:
        oops()
    except IndexError as exc:
        print(exc)


if __name__ == '__main__':
    for oops in (oops_indexerror, oops_keyerror):
        main(oops)
