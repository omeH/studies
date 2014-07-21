"""Find the sum of all the multiples of 3 or 5 below 1000.
"""


def getgen(count=1000):
    for i in range(1, count):
        if i%3==0 or i%5==0:
            yield i


def main():
    print sum(getgen(10000))


if __name__ == '__main__':
    main()