import datetime
import random


YEAR = 365
MIN_RATING = 1
POSITIVE_RATING = 4
MAX_RATING = 10

VIOLATIONS = {
    '001': 'drinking alcohol',
    '002': 'smoked in the room',
    '003': 'absent from work',
    '004': '{0} days absent from work',
    '005': 'absent from lesson {0}',
    '006': '{0} days absent from lessons'
}

TAB = '    '


def today():
    return datetime.date.today()


def timedelta(term):
    return datetime.timedelta(days=term)


class Unit(object):

    # --------------
    # Message format
    # --------------
    UNIT = 'Unit: {0}'
    UNIT_CELEBRATE = 'From the department {0} to celebrate the {1} present:'
    UNIT_MONITOR = \
        '{0} {1} was assigned to monitor the execution of the order on {2}'
    UNIT_NO_MONITOR = '{0} {1} is not an employee unit {2}'
    # --------------

    name = None

    def __init__(self, name, consist):
        """
        >>> unit = Unit('FZO', {})
        >>> unit.name, unit.consist
        ('FZO', {})
        """
        self.restrictions = {}
        self.name = name
        self.consist = consist
        self.restrictions['age'] = 17
        self.restrictions['Rector'] = None
        self.restrictions['Dean'] = None

    def __str__(self):
        """
        >>> unit = Unit('FZO', {})
        >>> print(unit)
        Unit: FZO
        """
        return self. UNIT.format(self.name)

    def recruit(self, position, person):
        """
        >>> unit_1 = Unit('FZO', {})
        >>> emp = Employee('Ivanov Ivan', age=20)
        >>> unit_1.recruit('teacher', emp)
        True
        >>> unit_1.consist['teacher'][0].name
        'Ivanov Ivan'
        >>> rector = Rector('Ivanov Ivan', 5000, unit_1, age=50)
        >>> unit_2 = Unit('FZO', {})
        >>> dean = Dean('Semenov Semen', 4500, unit_2, age=45)
        >>> unit_1.consist['rector'][0].name
        'Ivanov Ivan'
        >>> unit_2.consist['dean'][0].name
        'Semenov Semen'
        >>> isinstance(unit_1.restrictions['Rector'], Rector)
        True
        >>> isinstance(unit_2.restrictions['Dean'], Dean)
        True
        """
        if self.refuse(person):
            return False
        if self.consist.has_key(position):
            self.consist[position].append(person)
        else:
            if person.__class__ is Rector:
                self.restrictions['Rector'] = person
            if person.__class__ is Dean:
                self.restrictions['Dean'] = person
            self.consist[position] = [person]
        return True

    def exclude(self, person):
        """
        >>> rectorate = Rectorate('Rectorate', {})
        >>> rector_1 = Rector('Ivanov Ivan', 5000, rectorate, age=50)
        >>> rector_2 = Rector('Semenov Semen', 4500, rectorate, age=45)
        >>> rectorate.consist['rector'][0].name
        'Ivanov Ivan'
        >>> rectorate.exclude(rector_2)
        >>> rectorate.consist['rector'][0].name
        'Ivanov Ivan'
        >>> rectorate.exclude(rector_1)
        >>> rectorate.consist['rector']
        []
        >>> f_fzo = Faculty('FZO', {})
        >>> dean_1 = Dean('Ivanov Ivan', 5000, f_fzo, age=50)
        >>> dean_2 = Dean('Semenov Semen', 4500, f_fzo, age=45)
        >>> f_fzo.consist['dean'][0].name
        'Ivanov Ivan'
        >>> f_fzo.exclude(dean_2)
        >>> f_fzo.consist['dean'][0].name
        'Ivanov Ivan'
        >>> f_fzo.exclude(dean_1)
        >>> f_fzo.consist['dean']
        []
        """
        if self.consist.has_key(person.position):
            self.consist[person.position].remove(person)
            if isinstance(person, Rector):
                self.restrictions['Rector'] = None
            if isinstance(person, Dean):
                self.restrictions['Dean'] = None

    def dismiss(self, person):
        """
        >>> unit = Unit('FZO', {})
        >>> emp = Employee('Ivanov Ivan', age=20)
        >>> emp.get_job('Teacher', 1000, unit)
        True
        >>> emp.sign_contract(days=1)
        >>> isinstance(unit.consist['Teacher'][0], Employee)
        True
        >>> unit.dismiss(emp)
        Employee Ivanov Ivan leave 1 days before the completion of the contract
        >>> unit.consist
        {'Teacher': []}
        """
        person.leave_job()

    def refuse(self, person):
        """
        >>> f_fzo = Faculty('FZO', {})
        >>> emp_1 = Employee('Ivanov Ivan', age=25)
        >>> f_fzo.refuse(emp_1)
        False
        >>> emp_2 = Employee('Semenov Semen', age=16)
        >>> f_fzo.refuse(emp_2)
        True
        >>> rectorate = Rectorate('Rectorate', {})
        >>> rector_1 = Rector('Ivanov Ivan', 5000, rectorate, age=50)
        >>> rector_2 = Rector('Semenov Semen', 4500, rectorate, age=45)
        >>> rectorate.refuse(rector_2)
        True
        >>> f_fzo = Faculty('FZO', {})
        >>> dean_1 = Dean('Ivanov Ivan', 5000, f_fzo, age=50)
        >>> dean_2 = Dean('Semenov Semen', 4500, f_fzo, age=45)
        >>> f_fzo.refuse(dean_2)
        True
        """
        check = []
        if person.info.has_key('age'):
            check.append(False if person.info['age'] >=
                         self.restrictions['age'] else True)

        if self.restrictions['Rector']:
            check.append(True)

        if self.restrictions['Dean']:
            check.append(True)

        return True if True in check else False

    def celebrate(self, what):
        """
        >>> unit = Unit('FZO', {})
        >>> emp = Employee('Ivanov Ivan', age=25)
        >>> emp.get_job('teacher', 1000, unit)
        True
        >>> dean = Dean('Semenov Semen', 5000, unit, age=25)
        >>> unit.celebrate('new year')
        From the department FZO to celebrate the new year present:
            dean:
                Dean: Semenov Semen
            teacher:
                Employee: Ivanov Ivan
        """
        print(self.UNIT_CELEBRATE.format(self.name, what))
        for position, persons in self.consist.iteritems():
            if not persons:
                continue
            print('{0}{1}:'.format(TAB, position))
            for person in persons:
                print('{0}{1}'.format(TAB * 2, person))

    def monitor_execution_of_order(self, order, person):
        """
        >>> f_fzo = Faculty('FZO', {})
        >>> emp = Employee('Ivanov Ivan', age=25)
        >>> emp.get_job('secretary', 1000, f_fzo)
        True
        >>> order = 'banning smoking in university'
        >>> f_fzo.monitor_execution_of_order(order, emp)
        Employee Ivanov Ivan was assigned to monitor the execution of the \
order on banning smoking in university
        """
        if self.consist.has_key(person.position):
            print(self.UNIT_MONITOR.format(person.__class__.__name__,
                                           person.name, order))
        else:
            print(self.UNIT_NO_MONITOR.format(person.__class__.__name__,
                                              person.name, self.name))


class Rectorate(Unit):

    # --------------
    # Message format
    # --------------
    RECTORATE = 'Rectorate: {0}'
    # --------------

    def __init__(self, structure, consist):
        """
        >>> f_fzo = Faculty('FZO', {})
        >>> f_fkp = Faculty('FKP', {})
        >>> d_evm = Department('EVM', {})
        >>> structure = {'Faculty': [f_fzo, f_fkp], 'Department': [d_evm]}
        >>> rectorate = Rectorate(structure, {})
        >>> rectorate.structure['Faculty'][0] == f_fzo
        True
        >>> rectorate.consist == {}
        True
        """
        Unit.__init__(self, 'Rectorate', consist)
        self.structure = structure

    def __str__(self):
        """
        >>> rectorate = Rectorate('Rectorate', {})
        >>> print(rectorate)
        Rectorate: Rectorate
        """
        return self.RECTORATE.format(self.name)

    def add_unit(self, unit):
        """
        >>> f_fzo = Faculty('FZO', {})
        >>> f_fkp = Faculty('FKP', {})
        >>> d_evm = Department('EVM', {})
        >>> structure = {'Faculty': [f_fzo, f_fkp], 'Department': [d_evm]}
        >>> rectorate = Rectorate(structure, {})
        >>> len(rectorate.structure['Faculty'])
        2
        >>> f_ftk = Faculty('FTK', {})
        >>> rectorate.add_unit(f_ftk)
        >>> len(rectorate.structure['Faculty'])
        3
        >>> unit = Unit('Guard', {})
        >>> rectorate.add_unit(unit)
        >>> len(rectorate.structure['Unit'])
        1
        """
        if self.structure.has_key(unit.__class__.__name__):
            self.structure[unit.__class__.__name__].append(unit)
        else:
            self.structure[unit.__class__.__name__] = [unit]

    def del_unit(self, unit):
        """
        >>> f_fzo = Faculty('FZO', {})
        >>> f_fkp = Faculty('FKP', {})
        >>> structure = {'Faculty': [f_fzo, f_fkp]}
        >>> rectorate = Rectorate(structure, {})
        >>> len(rectorate.structure['Faculty'])
        2
        >>> rectorate.del_unit(f_fkp)
        >>> len(rectorate.structure['Faculty'])
        1
        >>> rectorate.del_unit(f_fkp)
        Traceback (most recent call last):
            ...
        ValueError: list.remove(x): x not in list
        >>> d_evm = Department('EVM', {})
        >>> rectorate.del_unit(d_evm)
        """
        if self.structure.has_key(unit.__class__.__name__):
            self.structure[unit.__class__.__name__].remove(unit)


class Faculty(Unit):

    # --------------
    # Message format
    # --------------
    FACULTY = 'Faculty: {0}'
    FACULTY_ORDER = 'Order No.{0} on the expulsion of students:'
    # --------------

    departments = None
    groups = None
    training_plan = None

    def __init__(self, name, consist):
        """
        >>> f_fzo = Faculty('FZO', {})
        >>> f_fzo.name, f_fzo.consist, f_fzo.departments, f_fzo.groups
        ('FZO', {}, [], [])
        """
        Unit.__init__(self, name, consist)
        self.departments = []
        self.groups = []
        self.training_plan = {}

    def __str__(self):
        """
        >>> f_fzo = Faculty('FZO', {})
        >>> print(f_fzo)
        Faculty: FZO
        """
        return self.FACULTY.format(self.name)

    def add_unit(self, unit):
        """
        >>> f_fzo = Faculty('FZO', {})
        >>> d_evm = Department('EVM', {})
        >>> teacher  = Teacher('Sidorov Semen', 3000, d_evm, age=30)
        >>> g_900502 = Group('900502', {}, teacher)
        >>> f_fzo.add_unit(d_evm)
        >>> f_fzo.add_unit(g_900502)
        >>> len(f_fzo.departments), len(f_fzo.groups)
        (1, 1)
        >>> g_900502.faculty is f_fzo
        True
        """
        if isinstance(unit, Department):
            self.departments.append(unit)
        elif isinstance(unit, Group):
            self.groups.append(unit)
            unit.faculty = self

    def del_unit(self, unit):
        """
        >>> f_fzo = Faculty('FZO', {})
        >>> d_evm = Department('EVM', {})
        >>> teacher  = Teacher('Sidorov Semen', 3000, d_evm, age=30)
        >>> g_900502 = Group('900502', {}, teacher)
        >>> f_fzo.add_unit(d_evm)
        >>> f_fzo.add_unit(g_900502)
        >>> len(f_fzo.departments), len(f_fzo.groups)
        (1, 1)
        >>> f_fzo.del_unit(d_evm)
        >>> f_fzo.del_unit(g_900502)
        >>> f_fzo.departments, f_fzo.groups
        ([], [])
        >>> g_900502 is f_fzo
        False
        >>> f_fzo.del_unit(g_900502)
        Traceback (most recent call last):
            ...
        ValueError: list.remove(x): x not in list
        """
        if isinstance(unit, Department):
            self.departments.remove(unit)
        elif isinstance(unit, Group):
            self.groups.remove(unit)
            unit.faculty = None

    def order_for_expulsion(self, act, students):
        """
        >>> f_fzo = Faculty('FZO', {})
        >>> teacher  = Teacher('Sidorov Semen', 3000, f_fzo, age=30)
        >>> g_900502 = Group('Gr900502', {}, teacher)
        >>> st_1 = Student('Ivanov Ivan', g_900502, age=19)
        >>> st_2 = Student('Semenov Semen', g_900502, age=20)
        >>> order = f_fzo.order_for_expulsion('12', [st_1, st_2])
        >>> print(order)
        Order No.12 on the expulsion of students:
            Student: Ivanov Ivan
            Student: Semenov Semen
        """
        order = self.FACULTY_ORDER.format(act)
        for student in students:
            order = ''.join([order, '\n', TAB, str(student)])
        return order

    def develop_training_plan(self, lesson, data):
        """
        >>> f_fzo = Faculty('FZO', {})
        >>> theme_1 = 'Familiarity with the language Python'
        >>> theme_2 = 'Data types Python language'
        >>> f_fzo.develop_training_plan('OPIP', [theme_1, theme_2])
        >>> f_fzo.training_plan['OPIP'] == ([theme_1, theme_2], 2)
        True
        """
        self.training_plan[lesson] = (data, len(data))


class Department(Unit):

    # --------------
    # Message format
    # --------------
    DEPARTMENT = 'Department: {0}'
    DEPARTMENT_GRADUATE = 'Department - {0}; group - {1}; graduates:'
    # --------------

    lessons = None
    consultation = None

    def __init__(self, name, consist):
        """
        >>> d_evm = Department('EVM', {})
        >>> d_evm.name, d_evm.consist, d_evm.lessons
        ('EVM', {}, [])
        """
        Unit.__init__(self, name, consist)
        self.lessons = []
        self.consultation = {}

    def __str__(self):
        """
        >>> d_evm = Department('EVM', {})
        >>> print(d_evm)
        Department: EVM
        """
        return self.DEPARTMENT.format(self.name)

    def add_consultation(self, teacher, lesson, room, date):
        """
        >>> d_evm = Department('EVM', {})
        >>> teacher = Teacher('Ivanov Ivan', 2500, d_evm, age=25)
        >>> d_evm.add_consultation(teacher, 'OPIP', '501-5', today())
        >>> len(d_evm.consultation[teacher])
        1
        >>> d_evm.add_consultation(teacher, 'VKSIS', '501-5', today())
        >>> len(d_evm.consultation[teacher])
        2
        """
        if self.consultation.has_key(teacher):
            self.consultation[teacher].append(Consultation(lesson, room, date))
        else:
            self.consultation[teacher] = [Consultation(lesson, room, date)]

    def del_consultation(self, teacher, lesson):
        """
        >>> d_evm = Department('EVM', {})
        >>> teacher = Teacher('Ivanov Ivan', 2500, d_evm, age=25)
        >>> d_evm.add_consultation(teacher, 'OPIP', '501-5', today())
        >>> len(d_evm.consultation[teacher])
        1
        >>> d_evm.add_consultation(teacher, 'VKSIS', '501-5', today())
        >>> len(d_evm.consultation[teacher])
        2
        >>> d_evm.del_consultation(teacher, 'OPIP')
        >>> len(d_evm.consultation[teacher])
        1
        >>> d_evm.del_consultation(teacher, 'VKSIS')
        >>> d_evm.consultation.has_key(teacher)
        False
        """
        if self.consultation.has_key(teacher):
            self.consultation[teacher].remove(lesson)
            if not self.consultation[teacher]:
                self.consultation.pop(teacher)

    def issue_graduate(self, group):
        """
        >>> d_evm = Department('EVM', {})
        >>> teacher  = Teacher('Sidorov Semen', 3000, d_evm, age=30)
        >>> g_900502 = Group('Gr900502', {}, teacher)
        >>> st_1 = Student('Ivanov Ivan', g_900502, age=20)
        >>> st_2 = Student('Semenov Semen', g_900502, age=20)
        >>> print(d_evm.issue_graduate(g_900502))
        Department - EVM; group - 900502; graduates:
            Student: Ivanov Ivan
            Student: Semenov Semen
        """
        msg = self.DEPARTMENT_GRADUATE.format(self.name, group.number)
        for student in group.consist['student']:
            msg = ''.join([msg, '\n', TAB, str(student)])
        return msg


class Consultation(object):

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


class Group(Unit):

    # --------------
    # Message format
    # --------------
    GROUP = 'Group: {0}'
    # --------------

    faculty = None
    number = None
    curator = None
    elder = None

    def __init__(self, name, consist, curator):
        Unit.__init__(self, name, consist)
        self.number = name[-6:]
        self.curator = curator

    def __str__(self):
        return self.GROUP.format(self.name)

    def recruit(self, position, student, elder=False):
        Unit.recruit(self, position, student)
        if elder:
            self.elder = student


class Person(object):
    """
    >>> person_1 = Person('Ivanov Ivan Ivanovich', age=20)
    >>> person_2 = Person('Semenov Semen Semenovich', age=20)
    >>> person_3 = Person('Sidorov Ivan Ivanovich', age=20)
    >>> print(person_1)
    Person: Ivanov Ivan Ivanovich
    >>> print(person_1.info['age'])
    20
    >>> person_1.go_to('shop')
    Person Ivanov Ivan Ivanovich goes to shop
    >>> person_2.run_to('work')
    Person Semenov Semen Semenovich running to work
    >>> person_3.celebrate('new year', [person_1, person_2])
    Person Sidorov Ivan Ivanovich celebration the new year with:
        Person: Ivanov Ivan Ivanovich
        Person: Semenov Semen Semenovich
    >>> person_1.violations
    []
    >>> person_1.commit_violation('smoked in the room')
    >>> person_1.violations[0][0]
    'smoked in the room'
    >>> person_1.talk(person_2, 'cars')
    A person Ivanov Ivan Ivanovich talk to a Semenov Semen Semenovich \
about cars
    """

    # --------------
    # Message format
    # --------------
    PERSON = 'Person: {0}'
    PERSON_GO = 'Person {0} goes to {1}'
    PERSON_RUN = 'Person {0} running to {1}'
    PERSON_CELEBRATE = 'Person {0} celebration the {1} with:'
    PERSON_TALK = 'A person {0} talk to a {1} about {2}'
    # --------------

    name_key = ['Surname', 'Name', 'Patronymic']
    name = 'Incognito'
    _name = {key: 'Incognito' for key in name_key}
    position = None

    def __init__(self, name=None, **info):
        self.info = {}
        self.violations = []
        if name:
            self.name = name
            self._name = dict(zip(self.name_key, name.split()))
        if info:
            for key in info:
                self.info[key] = info[key]

    def __str__(self):
        return self.PERSON.format(self.name)

    def go_to(self, to):
        print(self.PERSON_GO.format(self.name, to))

    def run_to(self, to):
        print(self.PERSON_RUN.format(self.name, to))

    def celebrate(self, what, with_whom):
        print(self.PERSON_CELEBRATE.format(self.name, what))
        for person in with_whom:
            print('{0}{1}'.format(TAB, person))

    def commit_violation(self, view):
        self.violations.append((view, str(today())))

    def talk(self, person, about):
        print(self.PERSON_TALK.format(self.name, person.name, about))


class Employee(Person):

    # --------------
    # Message format
    # --------------
    EMPLOYEE = 'Employee: {0}'
    EMPLOYEE_LEAVE = \
        'Employee {0} leave {1} days before the completion of the contract'
    EMPLOYEE_VACATION = 'For a {0} vacation ends {1}'
    # --------------

    # position = None
    unit = None
    pay = None
    start_work = None
    end_work = None

    def __init__(self, name, **info):
        """
        >>> emp = Employee('Ivanov Ivan', age=20, email='mail@mail.com')
        >>> emp.name, emp.info['age'], emp.info['email']
        ('Ivanov Ivan', 20, 'mail@mail.com')
        """
        Person.__init__(self, name, **info)

    def __str__(self):
        """
        >>> emp = Employee('Ivanov Ivan')
        >>> print(emp)
        Employee: Ivanov Ivan
        """
        return self. EMPLOYEE.format(self.name)

    def get_job(self, position, pay, unit):
        """
        >>> unit = Unit('rectorate', {})
        >>> emp = Employee('Ivanov Ivan')
        >>> emp.get_job('secretary', 1000, unit)
        True
        """
        if unit.recruit(position, self):
            self.position = position
            self.pay = pay
            self.unit = unit
            return True
        return False
        # self.unit.recruit(self.position, self)

    def sign_contract(self, years=False, days=False):
        """
        >>> emp = Employee('Ivanov Ivan')
        >>> emp.sign_contract() == None
        True
        >>> emp.sign_contract(years=3)
        >>> emp.start_work == today()
        True
        >>> emp.end_work == emp.start_work + timedelta(3*YEAR)
        True
        >>> emp.sign_contract(days=30)
        >>> emp.start_work == today()
        True
        >>> emp.end_work == emp.start_work + timedelta(30)
        True
        """
        if years is False and days is False:
            return None
        term = years.real * YEAR + days.real
        self.start_work = today()
        self.end_work = self.start_work + timedelta(term)

    def leave_job(self):
        """
        >>> unit = Unit('rectorate', {})
        >>> emp = Employee('Ivanov Ivan')
        >>> emp.get_job('secretary', 1000, unit)
        True
        >>> emp.sign_contract(1)
        >>> emp.unit == unit, unit.consist['secretary'][0] == emp
        (True, True)
        >>> emp.leave_job()
        Employee Ivanov Ivan leave 365 days before the completion of the \
contract
        >>> emp.unit == None, unit.consist['secretary'] == []
        (True, True)
        """
        if self.unit is None:
            return
        days_left = self.end_work - today()
        print(self.EMPLOYEE_LEAVE.format(self.name, days_left.days))
        self.unit.exclude(self)
        self.unit = None

    def receive_award(self, percent):
        """
        >>> emp = Employee('Ivanov Ivan')
        >>> emp.pay = 1000
        >>> emp.receive_award(.2)
        200
        """
        return int(self.pay * percent)

    def receive_increment(self, percent):
        """
        >>> emp = Employee('Ivanov Ivan')
        >>> emp.pay = 1000
        >>> emp.receive_increment(.2)
        >>> emp.pay
        1200
        """
        self.pay += int(self. pay * percent)

    def go_vacation(self, term):
        """
        >>> emp = Employee('Ivanov Ivan')
        >>> data = today() + timedelta(30)
        >>> msg = emp.EMPLOYEE_VACATION.format(emp.name, data)
        >>> emp.go_vacation(30) == msg
        True
        """
        return self.EMPLOYEE_VACATION.format(
            self.name, today() + timedelta(term)
        )

    def absent_work(self):
        """
        >>> emp = Employee('Ivanov Ivan')
        >>> emp.absent_work()
        >>> emp.violations[0][0]
        'absent from work'
        """
        self.commit_violation(VIOLATIONS['003'])

    def score_work(self, days):
        """
        >>> emp = Employee('Ivanov Ivan')
        >>> emp.score_work(5)
        >>> emp.violations[0][0]
        '5 days absent from work'
        """
        self.commit_violation(VIOLATIONS['004'].format(days))


class Rector(Employee):

    # --------------
    # Message format
    # --------------
    RECTOR = 'Rector: {0}'
    RECTOR_TO_ORDER = 'Rector {0} ordered the {1} on the {2}'
    RECTOR_ISSUE_ORDER = 'Rector {0} issued an order {1}'
    RECTOR_SIGN_ORDER = 'Rector {0} signed an order {1} of {2}'
    RECTOR_REPORT = 'Rector {0} reported to the Ministry of the {1}'
    # --------------

    def __init__(self, name, pay, unit, **info):
        """
        >>> rectorate = Rectorate('Rectorate', {})
        >>> rector = Rector('Ivanov Ivan', 5000, rectorate, age=40)
        >>> rector.name, rector.info['age'], rector.unit.name
        ('Ivanov Ivan', 40, 'Rectorate')
        """
        Employee.__init__(self, name, **info)
        self.get_job('rector', pay, unit)

    def __str__(self):
        """
        >>> rectorate = Rectorate('Rectorate', {})
        >>> rector = Rector('Ivanov Ivan', 5000, rectorate, age=40)
        >>> print(rector)
        Rector: Ivanov Ivan
        """
        return self.RECTOR.format(self.name)

    def to_order(self, order, unit):
        """
        >>> rectorate = Rectorate('Rectorate', {})
        >>> rector = Rector('Ivanov Ivan', 5000, rectorate, age=40)
        >>> rector.to_order('preparation of reports', rectorate)
        Rector Ivanov Ivan ordered the Rectorate on the preparation of reports
        """
        print(self.RECTOR_TO_ORDER.format(self.name, unit.__class__.__name__,
                                          order))

    def issue_order(self, about):
        """
        >>> rectorate = Rectorate('Rectorate', {})
        >>> rector = Rector('Ivanov Ivan', 5000, rectorate, age=40)
        >>> emp = Employee('Semenov Semen')
        >>> rector.issue_order('banning smoking in university')
        Rector Ivanov Ivan issued an order banning smoking in university
        """
        print(self.RECTOR_ISSUE_ORDER.format(self.name, about))

    def sign_order(self, about):
        """
        >>> rectorate = Rectorate('Rectorate', {})
        >>> rector = Rector('Ivanov Ivan', 5000, rectorate, age=40)
        >>> msg = Rector.RECTOR_SIGN_ORDER.format(\
                rector.name,\
                'banning smoking in university',\
                str(today())\
            )
        >>> rector.sign_order('banning smoking in university') == msg
        True
        """
        return(self.RECTOR_SIGN_ORDER.format(self.name, about, str(today())))

    def punish(self, person, what):
        """
        >>> rectorate = Rectorate('Rectorate', {})
        >>> rector = Rector('Ivanov Ivan', 5000, rectorate, age=40)
        >>> emp = Employee('Semenov Semen')
        >>> rector.punish(emp, 'smoking in university')
        >>> emp.violations[0][0]
        'smoking in university'
        """
        person.commit_violation(what)

    def promote(self, person, award):
        """
        >>> rectorate = Rectorate('Rectorate', {})
        >>> rector = Rector('Ivanov Ivan', 5000, rectorate, age=40)
        >>> rector.promote(rector, .1)
        500
        """
        print(person.receive_award(award))

    def _report_for_ministry(self, cause):
        """
        >>> rectorate = Rectorate('Rectorate', {})
        >>> rector = Rector('Ivanov Ivan', 5000, rectorate, age=40)
        >>> rector._report_for_ministry('execution of the order #01')
        Rector Ivanov Ivan reported to the Ministry of the execution of the \
order #01
        """
        print(self.RECTOR_REPORT.format(self.name, cause))


class ViceRector(Rector):

    # --------------
    # Message format
    # --------------
    VICERECTOR = 'ViceRector: {0}'
    # --------------

    direction = None

    def __init__(self, name, pay, unit, direction, **info):
        """
        >>> rectorate = Rectorate('Rectorate', {})
        >>> v_rector = ViceRector('Ivanov Ivan', 4000, rectorate,'study',age=40)
        >>> v_rector.name, v_rector.direction, v_rector.pay,v_rector.info['age']
        ('Ivanov Ivan', 'study', 4000, 40)
        """
        Employee.__init__(self, name, **info)
        self.direction = direction
        self.get_job('vicerector', pay, unit)

    def __str__(self):
        """
        >>> rectorate = Rectorate('Rectorate', {})
        >>> v_rector = ViceRector('Ivanov Ivan', 4000, rectorate,'study',age=40)
        >>> print(v_rector)
        ViceRector: Ivanov Ivan
        """
        return self.VICERECTOR.format(self.name)


class Dean(Rector):

    # --------------
    # Message format
    # --------------
    DEAN = 'Dean: {0}'
    # --------------

    def __init__(self, name, pay, unit, **info):
        """
        >>> f_fzo = Faculty('FZO', {})
        >>> dean = Dean('Ivanov Ivan', 5000, f_fzo, age=40)
        >>> dean.name, dean.info['age'], dean.unit.name
        ('Ivanov Ivan', 40, 'FZO')
        """
        Employee.__init__(self, name, **info)
        self.get_job('dean', pay, unit)

    def __str__(self):
        """
        >>> f_fzo = Faculty('FZO', {})
        >>> dean = Dean('Ivanov Ivan', 5000, f_fzo, age=50)
        >>> print(dean)
        Dean: Ivanov Ivan
        """
        return self.DEAN.format(self.name)


class Teacher(Employee):

    # --------------
    # Message format
    # --------------
    TEACHER = 'Teacher: {0}'
    TEACHER_SESSION = 'Today teacher {0} on lesson {1} said a theme \'{2}\''
    TEACHER_LATE = 'Teacher {0} late the lesson {1} for {2} minutes'
    # --------------

    lessons = None

    def __init__(self, name, pay, unit, **info):
        """
        >>> d_evm = Department('EVM', {})
        >>> teacher = Teacher('Ivanov Ivan', 3000, d_evm, age=30)
        >>> teacher.name, teacher.info['age'], teacher.position
        ('Ivanov Ivan', 30, 'teacher')
        """
        Employee.__init__(self, name, **info)
        self.get_job('teacher', pay, unit)
        self.lessons = {}

    def __str__(self):
        """
        >>> d_evm = Department('EVM', {})
        >>> teacher = Teacher('Ivanov Ivan', 3000, d_evm, age=30)
        >>> print(teacher)
        Teacher: Ivanov Ivan
        """
        return self.TEACHER.format(self.name)

    def conduct_training_session(self, lesson, theme):
        """
        >>> d_evm = Department('EVM', {})
        >>> teacher = Teacher('Ivanov Ivan', 3000, d_evm, age=30)
        >>> data = 'Data types Python language'
        >>> teacher.conduct_training_session('OPIP', data)
        Today teacher Ivanov Ivan on lesson OPIP said a theme 'Data types \
Python language'
        """
        print(self.TEACHER_SESSION.format(self.name, lesson, theme))

    def punish_student(self, student, violation):
        """
        >>> d_evm = Department('EVM', {})
        >>> teacher = Teacher('Ivanov Ivan', 3000, d_evm, age=30)
        >>> g_900502 = Group('Gr900502', {}, teacher)
        >>> student = Student('Semenov Semen', g_900502, age=20)
        >>> teacher.punish_student(student, 'smoking in room')
        >>> student.violations[0][0]
        'smoking in room'
        """
        student.commit_violation(violation)

    def develop_training_program(self, lesson, data):
        """
        >>> d_evm = Department('EVM', {})
        >>> teacher = Teacher('Ivanov Ivan', 3000, d_evm, age=30)
        >>> data = 'Familiarity with the language Python. Data types Python \
language'
        >>> teacher.develop_training_program('OPIP', data)
        >>> teacher.lessons['OPIP'][0]
        'Familiarity with the language Python'
        """
        self.lessons[lesson] = [string.strip() for string in data.split('.')]

    def conduct_exam(self, lesson, group, limit=MAX_RATING):
        """
        >>> d_evm = Department('EVM', {})
        >>> teacher = Teacher('Ivanov Ivan', 3000, d_evm, age=30)
        >>> g_900502 = Group('Gr900502', {}, teacher)
        >>> st_1 = Student('Semenov Semen', g_900502, age=20)
        >>> st_2 = Student('Sidorov Ivan', g_900502, age=19)
        >>> teacher.conduct_exam('OPIP', g_900502)
        >>> len(st_1.exam), len(st_2.exam)
        (1, 1)
        >>> 'OPIP' in st_1.exam, 'OPIP' in st_2.exam
        (True, True)
        """
        for student in group.consist['student']:
            if not lesson in student.exam:
                student.exam.append(Exam(
                    lesson, random.randrange(MIN_RATING, limit), self))

    def conduct_retake(self, exam):
        """
        >>> d_evm = Department('EVM', {})
        >>> teacher = Teacher('Ivanov Ivan', 3000, d_evm, age=30)
        >>> exam = Exam('OPIP', 3, teacher)
        >>> teacher.conduct_retake(exam)
        >>> exam.rating >= 4
        True
        """
        exam.rating = random.randrange(POSITIVE_RATING, MAX_RATING)

    def set_automatic_rating(self, student, lesson):
        """
        >>> d_evm = Department('EVM', {})
        >>> teacher = Teacher('Ivanov Ivan', 3000, d_evm, age=30)
        >>> g_900502 = Group('Gr900502', {}, teacher)
        >>> st = Student('Semenov Semen', g_900502, age=20)
        >>> teacher.set_automatic_rating(st, 'OPIP')
        >>> st.exam[0].rating
        10
        """
        student.exam.append(Exam(lesson, MAX_RATING, self))

    def late_on_lesson(self, lesson, minutes):
        """
        >>> d_evm = Department('EVM', {})
        >>> teacher = Teacher('Ivanov Ivan', 4000, d_evm, age=40)
        >>> teacher.late_on_lesson('OPIP', 5)
        Teacher Ivanov Ivan late the lesson OPIP for 5 minutes
        """
        print self.TEACHER_LATE.format(self.name, lesson, minutes)


class Exam(object):

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


class Student(Person):

    # --------------
    # Message format
    # --------------
    STUDENT = 'Student: {0}'
    STUDENT_ATTEND_LESSONS = 'Student {0} attend today lessons:'
    STUDENT_LATE = 'Student {0} late the lesson {1} for {2} minutes'
    # --------------

    rate = 1

    def __init__(self, name, group, **info):
        """
        >>> d_evm = Department('EVM', {})
        >>> teacher = Teacher('Ivanov Ivan', 4000, d_evm, age=40)
        >>> g_900502 = Group('Gr900502', {}, teacher)
        >>> st_1 = Student('Semenov Semen', g_900502, age=20)
        >>> st_2 = Student('Sidorov Ivan', g_900502, age=19, elder=True)
        >>> st_1.name, st_2.name
        ('Semenov Semen', 'Sidorov Ivan')
        >>> g_900502.elder.name
        'Sidorov Ivan'
        """
        Person.__init__(self, name, **info)
        self.position = 'student'
        if info.has_key('elder'):
            group.recruit('student', self, elder=True)
        else:
            group.recruit('student', self)
        self.group = group
        self.exam = []

    def __str__(self):
        """
        >>> d_evm = Department('EVM', {})
        >>> teacher = Teacher('Ivanov Ivan', 4000, d_evm, age=40)
        >>> g_900502 = Group('Gr900502', {}, teacher)
        >>> st = Student('Semenov Semen', g_900502, age=20)
        >>> print(st)
        Student: Semenov Semen
        """
        return self.STUDENT.format(self.name)

    def attend_lessons(self, lessons):
        """
        >>> d_evm = Department('EVM', {})
        >>> teacher = Teacher('Ivanov Ivan', 4000, d_evm, age=40)
        >>> g_900502 = Group('Gr900502', {}, teacher)
        >>> st = Student('Semenov Semen', g_900502, age=20)
        >>> lessons_today = ['OPIP', 'MG', 'VKSIS']
        >>> print(st.attend_lessons(lessons_today))
        Student Semenov Semen attend today lessons:
            OPIP
            MG
            VKSIS
        """
        msg = self.STUDENT_ATTEND_LESSONS.format(self.name)
        for lesson in lessons:
            msg = ''.join([msg, '\n', TAB, lesson])
        return msg

    def absent_lesson(self, lesson):
        """
        >>> d_evm = Department('EVM', {})
        >>> teacher = Teacher('Ivanov Ivan', 4000, d_evm, age=40)
        >>> g_900502 = Group('Gr900502', {}, teacher)
        >>> st = Student('Semenov Semen', g_900502, age=20)
        >>> st.absent_lesson('OPIP')
        >>> st.violations[0][0]
        'absent from lesson OPIP'
        """
        self.violations.append((VIOLATIONS['005'].format(lesson), today()))

    def late_on_lesson(self, lesson, minutes):
        """
        >>> d_evm = Department('EVM', {})
        >>> teacher = Teacher('Ivanov Ivan', 4000, d_evm, age=40)
        >>> g_900502 = Group('Gr900502', {}, teacher)
        >>> st = Student('Semenov Semen', g_900502, age=20)
        >>> st.late_on_lesson('OPIP', 10)
        Student Semenov Semen late the lesson OPIP for 10 minutes
        """
        print(self.STUDENT_LATE.format(self.name, lesson, minutes))

    def score_lessons(self, days):
        """
        >>> d_evm = Department('EVM', {})
        >>> teacher = Teacher('Ivanov Ivan', 4000, d_evm, age=40)
        >>> g_900502 = Group('Gr900502', {}, teacher)
        >>> st = Student('Semenov Semen', g_900502, age=20)
        >>> st.score_lessons(5)
        >>> st.violations[0]
        '5 days absent from lessons'
        """
        self.violations.append(VIOLATIONS['006'].format(days))

    def go_retake(self):
        """
        >>> d_evm = Department('EVM', {})
        >>> teacher = Teacher('Ivanov Ivan', 3000, d_evm, age=30)
        >>> g_900502 = Group('Gr900502', {}, teacher)
        >>> st_1 = Student('Semenov Semen', g_900502, age=20)
        >>> st_2 = Student('Sidorov Ivan', g_900502, age=19)
        >>> teacher.conduct_exam('OPIP', g_900502, limit=3)
        >>> st_1.exam[0] < 4, st_2.exam[0] < 4
        (True, True)
        >>> st_1.go_retake(); st_2.go_retake()
        >>> st_1.exam[0] < 4, st_2.exam[0] < 4
        (False, False)
        """
        for exam in self.exam:
            if exam < POSITIVE_RATING:
                exam.teacher.conduct_retake(exam)

    def get_automatic_rating(self, teacher, lesson):
        """
        >>> d_evm = Department('EVM', {})
        >>> teacher = Teacher('Ivanov Ivan', 3000, d_evm, age=30)
        >>> g_900502 = Group('Gr900502', {}, teacher)
        >>> st = Student('Semenov Semen', g_900502, age=20)
        >>> st.get_automatic_rating(teacher, 'OPIP')
        >>> st.exam[0].rating
        10
        """
        teacher.set_automatic_rating(self, lesson)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
