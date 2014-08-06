import argparse
import random


def parse_arg():
    parser = argparse.ArgumentParser()

    parser.add_argument('limit', type=int)

    return parser.parse_args()


def sort_bubble(list_):
    for i in range(len(list_) - 1):
        for j in range(len(list_) - i - 1):
            if list_[j] > list_[j + 1]:
                list_[j], list_[j + 1] = list_[j + 1], list_[j]


def init_list(limit):
    return [random.randrange(limit) for i in range(limit)]


def main():
    options = parse_arg()

    list_ = init_list(options.limit)
    sort_bubble(list_)


if __name__ == '__main__':
    main()
