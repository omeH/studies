import re
import argparse


RE = r'<({0})?>(.*)</\1>'

ATTR = 1
VALUE = 2


def parse_arg():
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '---file', type=str)
    parser.add_argument('-l', '--list-attrs', type=str)

    return parser.parse_args()


def format_regex(list_attrs):
    attrs = '|'.join(list_attrs)
    return RE.format(attrs)


def find_attrs(regex, xml_file):
    result = {}
    for line in xml_file:
        obj = regex.search(line)
        if obj:
            result[obj.group(ATTR)] = obj.group(VALUE)
    return result


def main():
    options = parse_arg()
    list_attrs = options.list_attrs.split(',')
    regex = re.compile(format_regex(list_attrs))

    with open(options.file) as xml_file:
        attrs = find_attrs(regex, xml_file)

    print(attrs)


if __name__ == '__main__':
    main()
