from theme_09.university.test.imports import *
# from university.test.imports import *


if __name__ == '__main__':
    import doctest
    gl = globals()
    doctest.testmod(m=person, globs=gl)
    doctest.testmod(m=unit, globs=gl)
    doctest.testmod(m=other, globs=gl)
