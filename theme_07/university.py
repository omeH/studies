import datetime


YEAR = 365
VIOLATIONS = {
    '001': 'drinking alcohol',
    '002': 'smoked in the room',
    '003': 'absent from work'
}

# --------------
# Message format
# --------------
# Person
PERSON = 'Person: {0}'
PERSON_GO = 'Person {0} goes to {1}'
PERSON_RUN = 'Person {0} running to {1}'
PERSON_CELEBRATE = 'Person {0} celebration the {1} with:'
PERSON_TALK = 'A person {0} talk to a {1} about {2}'
# Employee
EMPLOYEE = 'Employee: {0}'
EMPLOYEE_LEAVE = \
    'Employee {0} leave {1} before the completion of the contract'
# Unit
UNIT = 'Unit: {0}'
Unit_CELEBRATE = 'From the department {0} to celebrate the {1} present:'
# Other
TAB = '    '


class Unit:
    """
    >>> unit = Unit('rectorate', {})
    >>> print(unit)
    Unit: rectorate
    >>> print(unit.composition)
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
    >>> print(unit.composition['rector'][0])
    Employee: Sidorov Ivan Ivanovich
    >>> unit.celebrate('new year')
    From the department rectorate to celebrate the new year present:
        rector:
            Employee: Sidorov Ivan Ivanovich
        secretary:
            Employee: Ivanov Ivan Ivanovich
            Employee: Semenov Semen Semenovich
    >>> emp_1.leave_job()
    Employee Ivanov Ivan Ivanovich leave 365 days, 0:00:00 before the completion of the contract
    >>> unit.dismiss(emp_2)
    Employee Semenov Semen Semenovich leave 365 days, 0:00:00 before the completion of the contract
    >>> unit.celebrate('8 march')
    From the department rectorate to celebrate the 8 march present:
        rector:
            Employee: Sidorov Ivan Ivanovich
    """

    name = ''
    composition = {}

    def __init__(self, name, composition):
        self.name = name
        self.composition = composition

    def __str__(self):
        return UNIT.format(self.name)

    def recruit(self, position, person):
        if self.composition.has_key(position):
            self.composition[position].append(person)
        else:
            self.composition[position] = [person]

    def exclude(self, person):
        if self.composition.has_key(person.position):
            self.composition[person.position].remove(person)

    def dismiss(self, person):
        person.leave_job()

    def celebrate(self, what):
        print(Unit_CELEBRATE.format(self.name, what))
        for position in self.composition:
            if self.composition[position]:
                print('{0}{1}:'.format(TAB, position))
                for person in self.composition[position]:
                    print('{0}{1}'.format(TAB * 2, person))


class Person:
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

    name_key = ['Surname', 'Name', 'Patronymic']
    name = 'Incognito'
    _name = {key: 'Incognito' for key in name_key}
    violations = []

    def __init__(self, name=None, **info):
        self.info = {}
        if name:
            self.name = name
            self._name = dict(zip(self.name_key, name.split()))
        if info:
            for key in info:
                self.info[key] = info[key]

    def __str__(self):
        return PERSON.format(self.name)

    def go_to(self, to):
        print(PERSON_GO.format(self.name, to))

    def run_to(self, to):
        print(PERSON_RUN.format(self.name, to))

    def celebrate(self, what, with_whom):
        print(PERSON_CELEBRATE.format(self.name, what))
        for person in with_whom:
            print('{0}{1}'.format(TAB, person))

    def commit_violation(self, view):
        self.violations.append((view, str(datetime.date.today())))

    def talk(self, person, about):
        print(PERSON_TALK.format(self.name, person.name, about))


class Employee(Person):

    position = None
    unit = None
    pay = None
    start_work = None
    end_work = None

    def __init__(self, name, **info):
        Person.__init__(self, name, **info)

    def __str__(self):
        return EMPLOYEE.format(self.name)

    def get_job(self, position, pay, unit):
        self.position = position
        self.pay = pay
        self.unit = unit
        self.unit.recruit(self.position, self)

    def sign_contract(self, term):
        self.start_work = datetime.date.today()
        self.end_work = self.start_work + datetime.timedelta(days=term*YEAR)

    def leave_job(self):
        if self.unit is None:
            return
        print(EMPLOYEE_LEAVE.format(self.name,
                                    self.end_work - datetime.date.today()))
        self.unit.exclude(self)
        self.unit = None

    def receive_award(self, percent):
        return self.pay * percent

    def receive_increment(self, percent):
        self.pay *= percent


if __name__ == '__main__':
    import doctest
    doctest.testmod()
