"""Module defines and describes the objects:
    Unit, Rectorate, Department, Faculty, Group
"""


import theme_09.university2.person as mperson
import theme_09.university2.const as const
import theme_09.university2.other as other


Rector = mperson.Rector
Dean = mperson.Dean


class Unit(object):
    """Class describes some of the attributes and behavior of the
    object unit.
    """

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
        >>> unit_1.consist[Rector.__name__][0].name
        'Ivanov Ivan'
        >>> unit_2.consist[Dean.__name__][0].name
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
        >>> rectorate = Rectorate({}, {})
        >>> rector_1 = Rector('Ivanov Ivan', 5000, rectorate, age=50)
        >>> rector_2 = Rector('Semenov Semen', 4500, rectorate, age=45)
        >>> rectorate.consist[Rector.__name__][0].name
        'Ivanov Ivan'
        >>> rectorate.exclude(rector_2)
        >>> rectorate.consist[Rector.__name__][0].name
        'Ivanov Ivan'
        >>> rectorate.exclude(rector_1)
        >>> rectorate.consist[Rector.__name__]
        []
        >>> f_fzo = Faculty('FZO', {})
        >>> dean_1 = Dean('Ivanov Ivan', 5000, f_fzo, age=50)
        >>> dean_2 = Dean('Semenov Semen', 4500, f_fzo, age=45)
        >>> f_fzo.consist[Dean.__name__][0].name
        'Ivanov Ivan'
        >>> f_fzo.exclude(dean_2)
        >>> f_fzo.consist[Dean.__name__][0].name
        'Ivanov Ivan'
        >>> f_fzo.exclude(dean_1)
        >>> f_fzo.consist[Dean.__name__]
        []
        """
        if self.consist.has_key(person.position):
            self.consist[person.position].remove(person)
            if isinstance(person, Rector):
                self.restrictions['Rector'] = None
            if isinstance(person, Dean):
                self.restrictions['Dean'] = None

    @classmethod
    def dismiss(cls, person):
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
        >>> rectorate = Rectorate({}, {})
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

        if person.__class__ is Rector and self.restrictions['Rector']:
            check.append(True)

        if person.__class__ is Dean and self.restrictions['Dean']:
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
            Dean:
                Dean: Semenov Semen
            teacher:
                Employee: Ivanov Ivan
        """
        print(self.UNIT_CELEBRATE.format(self.name, what))
        for position, persons in self.consist.iteritems():
            if not persons:
                continue
            print('{0}{1}:'.format(const.TAB, position))
            for person in persons:
                print('{0}{1}'.format(const.TAB * 2, person))

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
    """Class describes some of the attributes and behavior of the
    object rectorate.
    """

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
        >>> rectorate = Rectorate({}, {})
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
    """Class describes some of the attributes and behavior of the
    object faculty.
    """

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
            order = ''.join([order, '\n', const.TAB, str(student)])
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
    """Class describes some of the attributes and behavior of the
    object department.
    """

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
            self.consultation[teacher].append(
                other.Consultation(lesson, room, date)
            )
        else:
            self.consultation[teacher] = [
                other.Consultation(lesson, room, date)
            ]

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
            msg = ''.join([msg, '\n', const.TAB, str(student)])
        return msg


class Group(Unit):
    """Class describes some of the attributes and behavior of the
    object group.
    """

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

    def recruit(self, position, student):
        Unit.recruit(self, position, student)
        if student.info.has_key('elder'):
            if student.info['elder']:
                self.elder = student
