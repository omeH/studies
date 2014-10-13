import re
import argparse
import gzip
import pprint
import sys

# import timer


REGEX_IP = re.compile(
    r'(((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?))( )'
)
REGEX_HTTP = re.compile(r'[httpHTTP]{4}')
REGEX_DATE_TIME = re.compile(r'(\d{2})/(\w{3})/(\d{4}):(2[0-3]|[01]\d)')

GROUP_IP = 1
GROUP_DAY = 1
GROUP_MONTH = 2
GROUP_YEAR = 3
GROUP_HOUR = 4


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--file', type=str)
    parser.add_argument('-r', '--requests', action='store_true')
    parser.add_argument('-s', '--statistics', action='store_true')

    return parser.parse_args()


def run_function(function, file_name):
    with gzip.open(file_name) as file_log:
        result = function(file_log)
    pprint.pprint(result)
    print()


def cmp_http(x, y):
    return cmp(x[1], y[1])


def cmp_date_time(x, y):
    return cmp(x[0], y[0])


def format_date_time(date_time):
    return '{2}-{1}-{0}_{3}'.format(*date_time)


def add_item(dict_, key):
    if dict_.has_key(key):
        dict_[key] += 1
    else:
        dict_[key] = 1


def requests_http(log_file):
    result = {}
    for line in log_file:
        obj = REGEX_IP.search(line)
        if obj:
            ip_address = obj.group(GROUP_IP)
        if REGEX_HTTP.search(line):
            add_item(result, ip_address)
    return sorted(result.items(), cmp=cmp_http, reverse=True)


def query_statistics(log_file):
    result = {}
    for line in log_file:
        obj = REGEX_DATE_TIME.search(line)
        if obj:
            key = format_date_time(obj.groups())
            add_item(result, key)
    return sorted(result.items(), cmp=cmp_date_time)


RUN_DICT = {
    'requests': requests_http,
    'statistics': query_statistics
}


def main():
    options = parse_args()

    if not options.requests and not options.statistics:
        sys.stderr.write('--> Search mode unknown <--\n')
        sys.exit(1)

    for key in RUN_DICT:
        if options.__dict__[key]:
            run_function(RUN_DICT[key], options.file)


if __name__ == '__main__':
    main()
    # timer.print_time(main)
