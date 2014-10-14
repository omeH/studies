import re
import argparse
import gzip
import pprint
import sys
import signal

# import timer


REGEX_IP = re.compile(
    r'(((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?))( )'
)
REGEX_HTTP = re.compile(r'[httpHTTP]{4}')
REGEX_DATE_TIME = re.compile(r'(\d{2})/(\w{3})/(\d{4}):(2[0-3]|[01]\d)')
IS_GZIP = re.compile(r'(.gz)$')


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--mode', type=str)
    parser.add_argument('files', nargs='+')

    return parser.parse_args()


def run_function(function, file_list):
    for file_name in file_list:
        if IS_GZIP.search(file_name):
            function_open = gzip.open
        else:
            function_open = open

        with function_open(file_name) as file_log:
            result = function(file_log)

        print('Result for file - {0}:'.format(file_name))
        pprint.pprint(result)
        print


def cmp_http(x, y):
    return cmp(x[1], y[1])


def cmp_date_time(x, y):
    return cmp(x[0], y[0])


def format_date_time(date_time):
    return '{2}-{1}-{0}_{3}'.format(*date_time)


def add_item(dict_, key):
    if key in dict_:
        dict_[key] += 1
    else:
        dict_[key] = 1


def requests_by_ip(log_file):
    result = {}
    group_ip = 1
    for line in log_file:
        obj = REGEX_IP.search(line)
        if obj:
            ip_address = obj.group(group_ip)
        if REGEX_HTTP.search(line):
            add_item(result, ip_address)
    return sorted(result.items(), cmp=cmp_http, reverse=True)


def requests_by_hour(log_file):
    result = {}
    for line in log_file:
        obj = REGEX_DATE_TIME.search(line)
        if obj:
            key = format_date_time(obj.groups())
            add_item(result, key)
    return sorted(result.items(), cmp=cmp_date_time)


CHOICE = {
    'requests_by_ip': requests_by_ip,
    'requests_by_hour': requests_by_hour
}


def main():
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    options = parse_args()
    # file_list = options.file_list.split(',')

    if not options.mode:
        sys.stderr.write('--> Search mode unknown <--\n')
        sys.exit(1)

    if options.mode in CHOICE:
        run_function(CHOICE[options.mode], options.files)


if __name__ == '__main__':
    main()
    # timer.print_time(main)
