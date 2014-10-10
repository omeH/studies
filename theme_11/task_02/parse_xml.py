import re
import argparse


GROUP = 1
TAB = '----'

OPEN_TAG_PATTERN = r'<([^/](.*?)[^/])>'
CLOSE_TAG_PATTERN = r'</(.*?)>'
HAS_ID_PATTERN = r'id="(.*?)"[^/]'
GET_TAG_VALUE_PATTERN = r'<(\w*?)( .*)?>(.*)</\1>'


PATTERN = ''.join([
    r''
])


class Person(object):
    pass


class PersonObject(object):
    pass


def parse_arg():
    parser = argparse.ArgumentParser()

    parser.add_argument('-l', '--list-attrs', type=str, default='')
    parser.add_argument('-a', '--all', action='store_true')
    parser.add_argument('-f', '--file', type=str, default='')

    return parser.parse_args()


def add_value(dict_, name, value):
    if dict_.has_key(name):
        dict_[name].append(value)
    else:
        dict_[name] = [value]


def add_attrs(obj, attrs):
    for key, value in attrs.items():
        if len(value) < 2:
            setattr(obj, key, value[0])
        else:
            index = 1
            for item in value:
                setattr(obj, ''.join([key, '_', str(index)]), item)
                index += 1


def init_object(input_file, obj, open_tag=False):
    result = obj()
    attrs = {}
    close_tag = True
    while open_tag != close_tag:
        line = input_file.readline()
        if not line:
            break
        tag = re.search(CLOSE_TAG_PATTERN, line)
        if tag:
            close_tag = tag.group(GROUP)
        tag = re.search(OPEN_TAG_PATTERN, line)
        if tag:
            value = re.search(GET_TAG_VALUE_PATTERN, line)
            if value:
                add_value(attrs, value.group(GROUP), value.group(GROUP + 2))
                continue

            value = re.search(HAS_ID_PATTERN, line)
            if value:
                add_value(attrs, 'id', value.group(GROUP))
                continue

            value = re.search(OPEN_TAG_PATTERN, line)
            if value:
                p_obj = init_object(
                    input_file, PersonObject, value.group(GROUP)
                )
                add_value(attrs, value.group(GROUP), p_obj)
    add_attrs(result, attrs)
    return result


def print_attrs(obj, attrs, tab=''):
    for item in sorted(attrs):
        value = getattr(obj, item)
        if not isinstance(value, PersonObject):
            print(tab + item + ': ' + value)
        else:
            print(tab + item + ':')
            print_attrs(value, value.__dict__.keys(), tab+TAB)


def main():
    options = parse_arg()
    with open(options.file) as f:
        obj = init_object(f, Person)
    if options.all:
        attrs = obj.__dict__.keys()
    else:
        attrs = options.list_attrs.split(',')
    print_attrs(obj, attrs)


if __name__ == '__main__':
    main()
