import sys
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

THEME_FOR_TALK = [
    'music', 'car',
    'girls', 'boys',
    'study', 'games',
    'sport', 'news',
    'exam', 'books'
]

PLACE = [
    'lesson', 'work',
    'clinic', 'dining',
    'library', 'shop',
    'casino', 'bank'
]

VIOLATIONS = [
    'drinking alcohol',
    'smoked in room',
    'absent from work',
    'sleep on the lesson',
    'absent from lesson',
    'put up a fight'
]

OOPS_GROUPS = 'Oops! {0} and then no groups'
OOPS_DEPARTMENTS = 'Oops! {0} and then no departments'

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
    'Nikovai', 'Mihail',
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

    def __init__(self, person):
        self.person = person
        self.actions = {
            GO_TO: self.go_to,
            RUN_TO: self.run_to,
            COMIT_VIOLATION: self.comit_violation,
            TALK: self.talk
        }

    def go_to(self):
        place = PLACE[random.randrange(len(PLACE))]
        self.person.go_to(place)

    def run_to(self):
        place = PLACE[random.randrange(len(PLACE))]
        self.person.run_to(place)

    def comit_violation(self):
        violation = VIOLATIONS[random.randrange(len(VIOLATIONS))]
        self.person.commit_violation(violation)

    def talk(self):
        theme = THEME_FOR_TALK[random.randrange(len(THEME_FOR_TALK))]
        self.person.talk(self.person, theme)

    def random_key(self):
        len_k = len(self.actions)
        return self.actions.keys()[random.randrange(len_k)]

    def rundom_action(self):
        self.actions[self.random_key()]()


def random_count(endpoint):
    return random.randrange(LOWER_LIMIT, endpoint)


def random_name_person():
    return ''.join([
        SURNAME[random.randrange(LEN_SURNAME)], ' ',
        NAME[random.randrange(LEN_NAME)], ' ',
        PATRONYMIC[random.randrange(LEN_PATRONYMIC)]
    ])


def random_faculty(faculties):
    len_f = len(faculties)
    return faculties[random.randrange(len_f)]


def random_department(departments):
    len_d = len(departments)
    return departments[random.randrange(len_d)]


def random_unit(units):
    return units[random.randrange(len(units))]


def random_curator(faculties):
    while True:
        faculty = random_unit(faculties)
        if len(faculty.departments) == 0:
            continue
        department = random_unit(faculty.departments)
        if department.consist.has_key('teacher'):
            break
    len_t = len(department.consist['teacher'])
    return department.consist['teacher'][random.randrange(len_t)]


def random_person(persons):
    return persons[random.randrange(len(persons))]


def structure_or_consisct():
    return random.randint(False, True)


def department_or_group():
    return random.randint(False, True)


def random_key(keys):
    return keys[random.randrange(len(keys))]


def is_rectorate(unit):
    if unit.__class__ is not u.Rectorate:
        return None
    if structure_or_consisct():
        key = random_key(unit.consist.keys())
        return random_person(unit.consist[key])
    else:
        key = random_key(unit.structure.keys())
        len_u = len(unit.structure[key])
        return unit.structure[key][random.randrange(len_u)]


def is_faculty(unit):
    if unit.__class__ is not u.Faculty:
        return None
    if structure_or_consisct():
        key = random_key(unit.consist.keys())
        return random_person(unit.consist[key])
    else:
        if department_or_group():
            if len(unit.groups) == 0:
                return OOPS_GROUPS.format(unit)
            return random_unit(unit.groups)
        else:
            if len(unit.departments) == 0:
                return OOPS_DEPARTMENTS.format(unit)
            return random_unit(unit.departments)


def is_person(obj):
    return isinstance(obj, u.Person)


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
    employee = u.Employee(
        random_name_person(),
        age=random.randrange(MIN_AGE, MAX_AGE)
    ).get_job(
        POSITIONS[random.randrange(LEN_POSITIONS)],
        random.randrange(MIN_SALARY, MAX_SALARY),
        unit
    )
    return employee


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
    for _ in range(random_count(MAX_TEACHER)):
        init_teacher(departments[random.randrange(len_d)])
    for _ in range(random_count(MAX_EMPLOYEE)):
        init_employee(departments[random.randrange(len_d)])

    # Init faculties consist
    faculties = [init_faculty(name) for name in NAME_FACULTY]
    len_f = len(faculties)
    for faculty in faculties:
        init_dean(faculty)
    for _ in range(random_count(MAX_EMPLOYEE)):
        init_employee(random_unit(faculties))

    # Set faculty for departments
    set_faculty_for_department(faculties, len_f, departments)

    # Init groups
    groups = \
        [init_group(name, random_curator(faculties)) for name in NAME_GROUPS]
    len_g = len(groups)
    for _ in range(random_count(MAX_STUDENT)):
        init_student(groups[random.randrange(len_g)])

    # Set faculty for groups
    set_faculty_for_group(faculties, len_f, groups)

    # Init rectorate
    rectorate = u.Rectorate({}, {})
    rector = init_rector(rectorate)
    for faculty in faculties:
        rectorate.add_unit(faculty)
    for _ in range(random_count(MAX_EMPLOYEE)):
        init_employee(rectorate)
    for direction in VICERECTOR_DIRECTION:
        init_vicerector(rectorate, direction)

    return rectorate


def run(unit, count):
    for _ in range(count):
        faculty_or_person = is_rectorate(unit)
        if is_person(faculty_or_person):
            PersonAction(faculty_or_person).rundom_action()
            continue
        unit_or_person = is_faculty(faculty_or_person)
        if is_person(unit_or_person):
            PersonAction(unit_or_person).rundom_action()
            continue
        if isinstance(unit_or_person, str):
            print(unit_or_person)
        else:
            key = random_key(unit_or_person.consist.keys())
            person = random_person(unit_or_person.consist[key])
            PersonAction(person).rundom_action()


def main():
    rectorate = init_structure()
    run(rectorate, int(sys.argv[1]))


if __name__ == '__main__':
    main()
