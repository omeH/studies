"""Module defines and describes the objects:
    Exam, Consultation, AccessDenied

Function:
    today, timedelta
"""


import datetime


def today():
    """
    """
    return datetime.date.today()


def timedelta(term):
    """
    """
    return datetime.timedelta(days=term)


class AccessDenied(Exception):
    """
    """

    pass


class Consultation(object):
    """Class describes some of the attributes and behavior of the
    object consultation.
    """

    # --------------
    # Message format
    # --------------
    CONSULTATION = 'Lesson - {0}; room - {1}; date - {2}'
    # --------------

    def __init__(self, lesson, room, date):
        """
        >>> consultation = Consultation('OPIP', '501-5', today())
        >>> consultation.lesson, consultation.room
        ('OPIP', '501-5')
        """
        self.lesson = lesson
        self.room = room
        self.date = date

    def __str__(self):
        """
        >>> consultation = Consultation('OPIP', '501-5', today())
        >>> msg = Consultation.CONSULTATION.format('OPIP', '501-5', today())
        >>> str(consultation) == msg
        True
        """
        return self.CONSULTATION.format(
            self.lesson, self.room, self.date
        )

    def __eq__(self, other):
        """
        >>> consultation = Consultation('OPIP', '501-5', today())
        >>> consultation == 'OPIP'
        True
        >>> consultation == 'VKSIS'
        False
        """
        return self.lesson == other


class Exam(object):
    """Class describes some of the attributes and behavior of the
    object exam.
    """

    # --------------
    # Message format
    # --------------
    EXAM = 'Lesson - {0}; rating - {1}'
    # --------------

    def __init__(self, lesson, rating, teacher):
        """
        >>> d_evm = Department('EVM', {})
        >>> teacher = Teacher('Ivanov Ivan', 4000, d_evm, age=40)
        >>> exam = Exam('OPIP', 4, teacher)
        >>> exam.lesson, exam.rating, teacher.name
        ('OPIP', 4, 'Ivanov Ivan')
        """
        self.lesson = lesson
        self.rating = rating
        self.teacher = teacher

    def __str__(self):
        """
        >>> d_evm = Department('EVM', {})
        >>> teacher = Teacher('Ivanov Ivan', 4000, d_evm, age=40)
        >>> exam = Exam('OPIP', 4, teacher)
        >>> print(exam)
        Lesson - OPIP; rating - 4
        """
        return self.EXAM.format(self.lesson, self.rating)

    def __eq__(self, other):
        """
        >>> d_evm = Department('EVM', {})
        >>> teacher = Teacher('Ivanov Ivan', 4000, d_evm, age=40)
        >>> exam = Exam('OPIP', 4, teacher)
        >>> exam == 'OPIP'
        True
        >>> exam == 'VKSIS'
        False
        """
        return self.lesson == other

    def __lt__(self, other):
        """
        >>> d_evm = Department('EVM', {})
        >>> teacher = Teacher('Ivanov Ivan', 4000, d_evm, age=40)
        >>> exam = Exam('OPIP', 4, teacher)
        >>> exam < 7
        True
        >>> exam < 3
        False
        """
        return self.rating < other
