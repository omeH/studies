import datetime


YEAR = 365

VIOLATIONS = {
    '001': 'drinking alcohol',
    '002': 'smoked in the room',
    '003': 'absent from work'
}

TAB = '    '


def today():
    return datetime.date.today()


def timedelta(term):
    return datetime.timedelta(days=term)


class Unit(object):
    """
    >>> unit = Unit('rectorate', {})
    >>> print(unit)
    Unit: rectorate
    >>> print(unit.consist)
    {}
    >>> emp_1 = Employee('Ivanov Ivan Ivanovich', age=25)
    >>> emp_1.get_job('secretary', 1000, unit)
    >>> emp_1.sign_contract(1)
    >>> emp_2 = Employee('Semenov Semen Semenovich', age=20)
    >>> emp_2.get_job('secretary', 1000, unit)
    >>> emp_2.sign_contract(1)
    >>> emp_3 = Employee('Sidorov Ivan Ivanovich', age=45)
    >>> emp_3.get_job('rector', 5000, unit)
    >>> emp_3.sign_contract(1)
    >>> print(unit.consist['rector'][0])
    Employee: Sidorov Ivan Ivanovich
    >>> unit.celebrate('new year')
    From the department rectorate to celebrate the new year present:
        rector:
            Employee: Sidorov Ivan Ivanovich
        secretary:
            Employee: Ivanov Ivan Ivanovich
            Employee: Semenov Semen Semenovich
    >>> emp_1.leave_job()
    Employee Ivanov Ivan Ivanovich leave 365 days before the completion of the contract
    >>> unit.dismiss(emp_2)
    Employee Semenov Semen Semenovich leave 365 days before the completion of the contract
    >>> unit.celebrate('8 march')
    From the department rectorate to celebrate the 8 march present:
        rector:
            Employee: Sidorov Ivan Ivanovich
    """

    # --------------
    # Message format
    # --------------
    UNIT = 'Unit: {0}'
    UNIT_CELEBRATE = 'From the department {0} to celebrate the {1} present:'
    # --------------

    name = None

    def __init__(self, name, consist):
        self.name = name
        self.consist = consist

    def __str__(self):
        return self. UNIT.format(self.name)

    def recruit(self, position, person):
        if self.consist.has_key(position):
            self.consist[position].append(person)
        else:
            self.consist[position] = [person]

    def exclude(self, person):
        if self.consist.has_key(person.position):
            self.consist[person.position].remove(person)

    def dismiss(self, person):
        person.leave_job()

    def celebrate(self, what):
        print(self.UNIT_CELEBRATE.format(self.name, what))
        for position, persons in self.consist.iteritems():
            if not persons:
                continue
            print('{0}{1}:'.format(TAB, position))
            for person in persons:
                print('{0}{1}'.format(TAB * 2, person))


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
    A person Ivanov Ivan Ivanovich talk to a Semenov Semen Semenovich about cars
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

    position = None
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
        """
        self.position = position
        self.pay = pay
        self.unit = unit
        self.unit.recruit(self.position, self)

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
        >>> emp.sign_contract(1)
        >>> emp.unit == unit, unit.consist['secretary'][0] == emp
        (True, True)
        >>> emp.leave_job()
        Employee Ivanov Ivan leave 365 days before the completion of the contract
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


if __name__ == '__main__':
    import doctest
    doctest.testmod()
