import datetime


YEAR = 365
VIOLATIONS = {
    '001': 'drinking alcohol',
    '002': 'smoked in the room',
    '003': 'absent from work'
}


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
        return 'Person: {0}'.format(self.name)

    def go_to(self, to):
        print('Person {0} goes to {1}'.format(self.name, to))

    def run_to(self, to):
        print('Person {0} running to {1}'.format(self.name, to))

    def celebrate(self, what, with_whom):
        print('Person {0} celebration the {1} with:'.format(self.name, what))
        for person in with_whom:
            print('    {0}'.format(person))

    def commit_violation(self, view):
        self.violations.append((view, str(datetime.date.today())))

    def talk(self, person, about):
        print('A person {0}'.format(self.name) +
              ' talk to a {0}'.format(person.name) +
              ' about {0}'.format(about))


class Employee(Person):

    position = None
    unit = None
    pay = None
    start_work = None
    end_work = None

    def __init__(self, name, **info):
        Person.__init__(self, name, **info)

    def __str__(self):
        pass

    def get_job(self, position, pay, unit):
        self.position = position
        self.pay = pay
        self.unit = unit

    def sign_contract(self, term):
        self.start_work = str(datetime.date.today())
        self.end_work = str(self.start_work +
                            datetime.timedelta(days=term*YEAR))

    def leave_job(self):
        print('Employee {0}'.format(self.name) +
              ' leaves {1}'.format(self.end_work - datetime.date.today()) +
              ' days before the completion of the contract')
        self.unit.composition.remove(self)

    def receive_award(self, percent):
        return self.pay * percent

    def receive_increment(self, percent):
        self.pay *= percent


if __name__ == '__main__':
    import doctest
    doctest.testmod()
