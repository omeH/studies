"""Testing the module naturalnambers
"""
# from sys import argv

from naturalnumbers import multiples


def main():
    """Function main
    """
    values = [0, 1, 10, 100, -1, 'spam', []]
    for i in values:
        try:
            sum_ = sum(multiples(i))
        except:
            print('Bad value: {}'.format(i))
        else:
            if sum_ != 0:
                print('Expected value is {}, actual is {}'.format(i, sum_))


if __name__ == '__main__':
    main()

