class Duck(object):

    ##################
    # Message format #
    ##################
    DUCK = 'Duck: name - {0}, color - {1}'
    DUCK_FLY = '{0} duck flying'
    DUCK_GO = '{0} duck goes'
    DUCK_SWIM = '{0} duck swims'
    DUCK_QUACK = '{0} duck quacks'
    ##################

    name = None
    color = None

    def __init__(self, **info):
        self.name = info['name']
        self.color = info['color']

    def __str__(self):
        return self.DUCK.format(self.name, self.color)

    def fly(self):
        return self.DUCK_FLY.format(self.name)

    def go(self):
        return self.DUCK_GO.format(self.name)

    def swim(self):
        return self.DUCK_SWIM.format(self.name)

    def quack(self):
        return self.DUCK_QUACK.format(self.name)


class MuteDuck(Duck):

    def quack(self):
        pass


class FlightlessDuck(Duck):

    def fly(self):
        pass


class AlbinoDuck(Duck):

    color = 'white'

    def __init__(self, **info):
        Duck.__init__(self, name=info['name'], color=self.color)


class FlightlessBlueDuck(FlightlessDuck):

    color = 'blue'

    def __init__(self, **info):
        FlightlessDuck.__init__(self, name=info['name'], color=self.color)
