"""This module parses the contents of the file '/etc/passwd' and
returns a list whose elements are dictionaries with keys.

Examples:
    import passwdparser

    lines = read_passwd()
    res = parser_paswwd(lines)

"""
import sys


FILE_NAME = '/etc/passwd'
LIST_KEYS = [
    'login',
    'passwd',
    'id_user',
    'id_group',
    'comment',
    'home',
    'interpreter'
]

FILE_ERROR = -1


def file_error(file_name, mode):
    """This function intercepts exceptions to the function open
    """
    res = None
    try:
        res = open(file_name, mode)
    except IOError as error:
        sys.stdout.write('passwdparser.py: {}\n'.format(error))
    return res


def parser_passwd(passwd_lines):
    """This function parses the contents of strings based on a
    delimiter ':' and returns a list whose elements are
    dictionaries with keys:
        login, passwd, id_user, id_group, comment, home, interpreter

    >>> lines = read_passwd()
    >>> res = parser_passwd(lines)
    >>> isinstance(res, list)
    True
    >>> len(res) == len(lines)
    True
    >>> res[0]['login'] == 'root'
    True
    >>> parser_passwd(-1)
    Traceback (most recent call last):
        ...
    ValueError: passwd_lines must be list
    >>> parser_passwd({})
    Traceback (most recent call last):
        ...
    ValueError: passwd_lines must be list
    """
    if not isinstance(passwd_lines, list):
        raise ValueError('passwd_lines must be list')

    return [dict(zip(LIST_KEYS, line.split(':'))) for line in passwd_lines]


def read_passwd():
    """ This function reads the contents of file '/etc/passwd' and
    returns the contents as a list of string.If can't open the file,
    it returns -1.
    """
    file_ = file_error(FILE_NAME, 'r')
    if file_ is None:
        return FILE_ERROR

    passwd_lines = file_.readlines()
    file_.close()

    return [line.strip() for line in passwd_lines]


if __name__ == '__main__':
    import doctest
    doctest.testmod()
