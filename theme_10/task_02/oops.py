INDEXERROR_MESSAGE = 'Oops! IndexError'
OOPSERROR_MESAAGE = 'Oops! OopsError'


class OopsError(Exception):

    pass


def oops_indexerror():
    raise IndexError(INDEXERROR_MESSAGE)


def oops_oopserror():
    raise OopsError(OOPSERROR_MESAAGE)


def main(oops):
    try:
        oops()
    except (IndexError, OopsError) as exc:
        print(exc)


def main_2(oops):
    try:
        oops()
    except IndexError as exc:
        print(exc)
    except OopsError as exc:
        print(OopsError, exc)


if __name__ == '__main__':
    for oops in (oops_indexerror, oops_oopserror):
        main(oops)
