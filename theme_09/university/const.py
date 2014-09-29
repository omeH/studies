"""Module defines and describes the variables:
    YEAR, MIN_RATING, MAX_RATING, POSITIVE_RATING,
    DRINKING_ALCOHOL, SMOKED_IN_ROOM, ABSENT_FRON_WORK,
    ABSENT_FROM_LESSON, N_DAYS_ABSENT_FROM_WORK,
    N_DAYS_ABSENT_FROM_LESSON, VIOLATIONS
"""


YEAR = 365
MIN_RATING = 1
POSITIVE_RATING = 4
MAX_RATING = 10

DRINKING_ALCOHOL = 1
SMOKED_IN_ROOM = 2
ABSENT_FROM_WORK = 3
N_DAYS_ABSENT_FROM_WORK = 4
ABSENT_FROM_LESSON = 5
N_DAYS_ABSENT_FRON_LESSON = 6

VIOLATIONS = {
    DRINKING_ALCOHOL: 'drinking alcohol',
    SMOKED_IN_ROOM: 'smoked in the room',
    ABSENT_FROM_WORK: 'absent from work',
    N_DAYS_ABSENT_FROM_WORK: '{0} days absent from work',
    ABSENT_FROM_LESSON: 'absent from lesson {0}',
    N_DAYS_ABSENT_FRON_LESSON: '{0} days absent from lessons'
}

TAB = '    '