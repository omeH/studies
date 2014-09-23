import random

from .variables import *
from .other import today, timedelta, AccessDenied
from .other import Exam


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
    A Person Ivanov Ivan Ivanovich talk to a Person Semenov Semen Semenovich \
about cars
    """

    # --------------
    # Message format
    # --------------
    PERSON = 'Person: {0}'
    PERSON_GO = '{0} {1} goes to {2}'
    PERSON_RUN = '{0} {1} running to {2}'
    PERSON_CELEBRATE = '{0} {1} celebration the {2} with:'
    PERSON_TALK = 'A {0} {1} talk to a {2} {3} about {4}'
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
        print(self.PERSON_GO.format(self.__class__.__name__, self.name, to))

    def run_to(self, to):
        print(self.PERSON_RUN.format(self.__class__.__name__, self.name, to))

    def celebrate(self, what, with_whom):
        print(self.PERSON_CELEBRATE.format(self.__class__.__name__,
                                           self.name, what))
        for person in with_whom:
            print('{0}{1}'.format(TAB, person))

    def commit_violation(self, view):
        self.violations.append((view, str(today())))

    def talk(self, person, about):
        print(self.PERSON_TALK.format(self.__class__.__name__, self.name,
                                      person.__class__.__name__, person.name,
                                      about))


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
        self.commit_violation(VIOLATIONS[ABSENT_FROM_WORK])

    def score_work(self, days):
        """
        >>> emp = Employee('Ivanov Ivan')
        >>> emp.score_work(5)
        >>> emp.violations[0][0]
        '5 days absent from work'
        """
        self.commit_violation(VIOLATIONS[N_DAYS_ABSENT_FROM_WORK].format(days))


class Rector(Employee):

    # --------------
    # Message format
    # --------------
    RECTOR = 'Rector: {0}'
    RECTOR_TO_ORDER = 'Rector {0} ordered the {1} on the {2}'
    RECTOR_ISSUE_ORDER = 'Rector {0} issued an order {1}'
    RECTOR_SIGN_ORDER = 'Rector {0} signed an order {1} of {2}'
    RECTOR_REPORT = 'Rector {0} reported to the Ministry of the {1}'
    RECTOR_NO_REPORT = 'Object {0} class access is denied'
    # --------------

    def __init__(self, name, pay, unit, **info):
        """
        >>> rectorate = Rectorate({}, {})
        >>> rector = Rector('Ivanov Ivan', 5000, rectorate, age=40)
        >>> rector.name, rector.info['age'], rector.unit.name
        ('Ivanov Ivan', 40, 'Rectorate')
        """
        Employee.__init__(self, name, **info)
        self.get_job('rector', pay, unit)

    def __str__(self):
        """
        >>> rectorate = Rectorate({}, {})
        >>> rector = Rector('Ivanov Ivan', 5000, rectorate, age=40)
        >>> print(rector)
        Rector: Ivanov Ivan
        """
        return self.RECTOR.format(self.name)

    def to_order(self, order, unit):
        """
        >>> rectorate = Rectorate({}, {})
        >>> rector = Rector('Ivanov Ivan', 5000, rectorate, age=40)
        >>> rector.to_order('preparation of reports', rectorate)
        Rector Ivanov Ivan ordered the Rectorate on the preparation of reports
        """
        print(self.RECTOR_TO_ORDER.format(self.name, unit.__class__.__name__,
                                          order))

    def issue_order(self, about):
        """
        >>> rectorate = Rectorate({}, {})
        >>> rector = Rector('Ivanov Ivan', 5000, rectorate, age=40)
        >>> emp = Employee('Semenov Semen')
        >>> rector.issue_order('banning smoking in university')
        Rector Ivanov Ivan issued an order banning smoking in university
        """
        print(self.RECTOR_ISSUE_ORDER.format(self.name, about))

    def sign_order(self, about):
        """
        >>> rectorate = Rectorate({}, {})
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
        >>> rectorate = Rectorate({}, {})
        >>> rector = Rector('Ivanov Ivan', 5000, rectorate, age=40)
        >>> emp = Employee('Semenov Semen')
        >>> rector.punish(emp, 'smoking in university')
        >>> emp.violations[0][0]
        'smoking in university'
        """
        person.commit_violation(what)

    def promote(self, person, award):
        """
        >>> rectorate = Rectorate({}, {})
        >>> rector = Rector('Ivanov Ivan', 5000, rectorate, age=40)
        >>> rector.promote(rector, .1)
        500
        """
        print(person.receive_award(award))

    def report_for_ministry(self, cause):
        """
        >>> rectorate = Rectorate({}, {})
        >>> rector = Rector('Ivanov Ivan', 5000, rectorate, age=40)
        >>> rector.report_for_ministry('execution of the order #01')
        Rector Ivanov Ivan reported to the Ministry of the execution of the \
order #01
        >>> v_rector = ViceRector('Semenov Semen',3000,rectorate,'study',age=30)
        >>> v_rector.report_for_ministry('execution of the order #01')
        Traceback (most recent call last):
            ...
        AccessDenied: Object ViceRector class access is denied
        """
        if self.__class__ is not Rector:
            raise AccessDenied(
                self.RECTOR_NO_REPORT.format(self.__class__.__name__)
            )
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
        >>> rectorate = Rectorate({}, {})
        >>> v_rector = ViceRector('Ivanov Ivan', 4000, rectorate,'study',age=40)
        >>> v_rector.name, v_rector.direction, v_rector.pay,v_rector.info['age']
        ('Ivanov Ivan', 'study', 4000, 40)
        """
        Employee.__init__(self, name, **info)
        self.direction = direction
        self.get_job('vicerector', pay, unit)

    def __str__(self):
        """
        >>> rectorate = Rectorate({}, {})
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
            if lesson not in student.exam:
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
        self.unit = group
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
        self.violations.append(
            (VIOLATIONS[ABSENT_FROM_LESSON].format(lesson), today())
        )

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
        self.violations.append(
            VIOLATIONS[N_DAYS_ABSENT_FRON_LESSON].format(days)
        )

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
