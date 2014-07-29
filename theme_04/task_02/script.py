import os
import sys


def parse_dir(directory):
    for current, dirs, files in os.walk(directory):
        for file_ in files:
            yield os.path.join(current, file_)


def replace_str(file_name, source_line, replace_line):
    file_ = open(file_name, 'r')
    lines = file_.readlines()
    file_.close()
    file_ = open(file_name, 'w')
    # size = 0
    for line in lines:
        # file_.seek(size)
        # size += len(line)
        file_.write(''.join([line.replace(source_line, replace_line)]))
    file_.close()


def main():
    """This main function
    """
    replace_str(*sys.argv[1:])


if __name__ == '__main__':
    main()
