import random

import university as u


MIN_SALARY = 1000
MAX_SALARY = 5000

MIN_AGE = 18
MAX_AGE = 60

MAX_EMPLOYEE = 10
MAX_TEACHER = 10
MAX_STUDENT = 40

LOWER_LIMIT = 5

# Person action
GO_TO = 1
RUN_TO = 2
COMIT_VIOLATION = 3
TALK = 4

# Name Person
SURNAME = [
    'Smirnov', 'Smirnova',
    'Ivanov', 'Ivanova',
    'Sokolov', 'Sokolova',
    'Popov', 'Popova',
    'Petrov', 'Petrova',
    'Volkov', 'Volkova'
]
LEN_SURNAME = len(SURNAME)

NAME = [
    'Aleksandor', 'Maxim',
    'Ivan', 'Dmitrii',
    'Nikovai', 'Mihail'
    'Anastasia', 'Elizaveta',
    'Victiria', 'Ekaterina'
]
LEN_NAME = len(NAME)

PATRONYMIC = [
    'Aleksandrovich', 'Aleksandrovna',
    'Maximovich', 'Maximovna',
    'Ivanovich', 'Ivanovna',
    'Dmitrievich', 'Dmitrievna',
    'Nikolaevich', 'Nicolaevna',
    'Mihailovich', 'Mihailovna'
]
LEN_PATRONYMIC = len(PATRONYMIC)

# Name Unit
NAME_DEPARTMENT = ['EVM', 'EVS', 'ETiT']
NAME_FACULTY = ['FZO', 'FKP']
NAME_GROUPS = ['Gr940501', 'Gr980502', 'Gr900501', 'Gr900502']

VICERECTOR_DIRECTION = [
    'study', 'education',
    'development', 'marketing',
    'science'
]

POSITIONS = [
    'secretary', 'manager',
    'guard', 'driver',
    'methodist', 'librarian'
]
LEN_POSITIONS = len(POSITIONS)


class PersonAction(object):

    actions = {}

    def __init__(self, person, action):
        self.person = person
        self.action = action
        self.actions = {
            GO_TO: self.go_to,
            RUN_TO: self.run_to,
            COMIT_VIOLATION: self.comit_violation,
            TALK: self.talk
        }

    def go_to(self):
        return self.person.go_to

    def run_to(self):
        return self.person

    def comit_violation(self):
        return self.person.comit_violation

    def talk(self):
        return self.person.talk

    def run(self):
        return self.actions[self.action]


def random_name_person():
    return ''.join([
        NAME[random.randrange(LEN_NAME)], ' ',
        SURNAME[random.randrange(LEN_SURNAME)], ' ',
        PATRONYMIC[random.randrange(LEN_PATRONYMIC)]
    ])


def random_department(faculties):
    len_f = len(faculties)
    len_d = 0
    while len_d == 0:
        faculty = faculties[random.randrange(len_f)]
        len_d = len(faculty.departments)
    return faculty.departments[random.randrange(len_d)]


def random_curator(faculties):
    while True:
        department = random_department(faculties)
        if department.consist.has_key('teacher'):
            break
    len_t = len(department.consist['teacher'])
    return department.consist['teacher'][random.randrange(len_t)]


def set_faculty_for_department(faculties, len_f, departments):
    for department in departments:
        faculties[random.randrange(len_f)].add_unit(department)


def set_faculty_for_group(faculties, len_f, groups):
    for group in groups:
        faculties[random.randrange(len_f)].add_unit(group)


def init_department(name):
    return u.Department(name, {})


def init_faculty(name):
    return u.Faculty(name, {})


def init_group(name, curator):
    return u.Group(name, {}, curator)


def init_employee(unit):
    return u.Employee(
        random_name_person(),
        age=random.randrange(MIN_AGE, MAX_AGE)
    ).get_job(
        POSITIONS[random.randrange(LEN_POSITIONS)],
        random.randrange(MIN_SALARY, MAX_SALARY),
        unit
    )


def init_rector(rectorate):
    return u.Rector(
        random_name_person(),
        random.randrange(MIN_SALARY, MAX_SALARY),
        rectorate,
        age=random.randrange(MIN_AGE, MAX_AGE)
    )


def init_vicerector(rectorate, direction):
    return u.ViceRector(
        random_name_person(),
        random.randrange(MIN_SALARY, MAX_SALARY),
        rectorate,
        direction,
        age=random.randrange(MIN_AGE, MAX_AGE)
    )


def init_dean(faculty):
    return u.Dean(
        random_name_person(),
        random.randrange(MIN_SALARY, MAX_SALARY),
        faculty,
        age=random.randrange(MIN_AGE, MAX_AGE)
    )


def init_teacher(department):
    return u.Teacher(
        random_name_person(),
        random.randrange(MIN_SALARY, MAX_SALARY),
        department,
        age=random.randrange(MIN_AGE, MAX_AGE)
    )


def init_student(group):
    return u.Student(
        random_name_person(),
        group,
        age=random.randrange(MIN_AGE, MAX_AGE)
    )


def init_structure():
    # Init departments consist
    departments = [init_department(name) for name in NAME_DEPARTMENT]
    len_d = len(departments)
    for _ in range(LOWER_LIMIT, MAX_TEACHER):
        init_teacher(departments[random.randrange(len_d)])
    for _ in range(LOWER_LIMIT, MAX_EMPLOYEE):
        init_employee(departments[random.randrange(len_d)])

    # Init faculties consist
    faculties = [init_faculty(name) for name in NAME_FACULTY]
    len_f = len(faculties)
    for faculty in faculties:
        init_dean(faculty)
    for _ in range(LOWER_LIMIT, MAX_EMPLOYEE):
        init_employee(faculties[random.randrange(len_f)])

    # Set faculty for departments
    set_faculty_for_department(faculties, len_f, departments)

    # Init groups
    groups = \
        [init_group(name, random_curator(faculties)) for name in NAME_GROUPS]
    len_g = len(groups)
    for _ in range(LOWER_LIMIT, MAX_STUDENT):
        init_student(groups[random.randrange(len_g)])

    # Set faculty for groups
    set_faculty_for_group(faculties, len_f, groups)

    # Init rectorate
    rectorate = u.Rectorate({}, {})
    rector = init_rector(rectorate)
    for faculty in faculties:
        rectorate.add_unit(faculty)
    for _ in range(LOWER_LIMIT, MAX_EMPLOYEE):
        init_employee(rectorate)
    for direction in VICERECTOR_DIRECTION:
        init_vicerector(rectorate, direction)

    return rectorate


def main():
    init_structure()


if __name__ == '__main__':
    main()
