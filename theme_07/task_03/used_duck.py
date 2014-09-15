import sys

import theme_07.task_02.linkedlist as ll
import duck

if len(sys.argv) >= 2:
    List = ll.List
else:
    List = list

# Duck actions
FLY = 1
GO = 2
SWIM = 3
QUACK = 4

NAMES_DUCK = [
    'Donald', 'Sam', 'Max', 'Dan', 'Tom'
]

COLORS_DUCK = [
    'black', 'red', 'green', 'yellow', 'purple'
]

CLASS_DUCK = [
    duck.Duck, duck.MuteDuck, duck.FlightlessDuck,
    duck.AlbinoDuck, duck.FlightlessBlueDuck
]
LEN_CLASS_DUCK = len(CLASS_DUCK)


class DuckAction(object):

    actions = None

    def __init__(self, duck):
        self.duck = duck
        self.actions = {
            FLY: self.duck.fly,
            GO: self.duck.go,
            SWIM: self.duck.swim,
            QUACK: self.duck.quack
        }

    def run_action(self):
        for action in self.actions:
            print(self.actions[action]())


def init_ducks():
    list_ducks = List()
    for index in range(LEN_CLASS_DUCK):
        list_ducks.append(
            CLASS_DUCK[index](
                name=NAMES_DUCK[index], color=COLORS_DUCK[index]
            )
        )
    return list_ducks


def run_actions(ducks):
    for duck_ in ducks:
        print(duck_)
        DuckAction(duck_).run_action()


def main():
    print(List)
    list_ducks = init_ducks()
    run_actions(list_ducks)


if __name__ == '__main__':
    main()
