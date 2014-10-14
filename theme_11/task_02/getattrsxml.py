import re
import argparse
import sys


RE = r'<({0})?>(.*)</\1>'


def parse_arg():
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--file', type=str,
                        help='Get the name of the file being processed')
    parser.add_argument('-l', '--list-attrs', type=str,
                        help='Get a list of attributes, separated by commas')

    return parser.parse_args()


def format_regex(list_attrs):
    attrs = '|'.join(list_attrs)
    return RE.format(attrs)


def find_attrs(regex, xml_file):
    result = {}
    group_attr = 1
    group_value = 2
    for line in xml_file:
        obj = regex.search(line)
        if obj:
            result[obj.group(group_attr)] = obj.group(group_value)
    return result


def main():
    options = parse_arg()
    if not options.file:
        sys.stderr.write('--> No file name specified <--\n')
        sys.exit(1)
    if options.list_attrs:
        list_attrs = options.list_attrs.split(',')
    else:
        list_attrs = []
    regex = re.compile(format_regex(list_attrs))

    with open(options.file) as xml_file:
        attrs = find_attrs(regex, xml_file)

    print(attrs)


if __name__ == '__main__':
    main()
