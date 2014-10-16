"""This module parses the log-files of connections to the
nginx server.

Description:
    The module can work both directly with log-file and
    archive gzip containing log-file. If the module
    receives input multiple files, they are processed
    and the information is incorporated into a single
    output.

Usage:
    parse_nginx_log.py [-o] [--out-format {print, csv}]
                       [-m] [--mode {request_by_ip, request_by_hour}]
                       [-h] [--help]
                       FILENAME [...]

Parameters:
    FILENAME
        Gets the name or names of the files to be processed.

Options:
    -h
        Print help on the module and exit.

    --help
        Print detailed help on the modulw and exit.

    -o, --out-format {print, csv}
        Switches the output format of the print or to csv.
        Take the value 'print' or 'csv'.The default value
        is 'print'.

    -m, --mode {requests_by_ip, requests_by_hour}
        Sets the processing mode of the log-file:
            - requests_by_ip: counts the number of HTTP-
              requests from each ip;
            - requests_by_hour: counts the number of
              requests on the cock;
        Take the value 'requests_by_ip' or 'requests_by_hour'.
        The default value is 'requests_by_ip'

Examples:
    To run module is necessary for it to pass parameter
    FILENAME:
        parse_nginx_log.py FILENAME

    To run the module and output information to file csv:
        parse_nginx_log.py FILENAME --out-format csv
"""


import re
import argparse
import gzip
import pprint
import sys
import signal

# import timer

################
# Regex format #
################
REGEX_IP = re.compile(
    r'(((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?))( )'
)
REGEX_HTTP = re.compile(r'[httpHTTP]{4}')
REGEX_DATE_TIME = re.compile(r'(\d{2})/(\w{3})/(\d{4}):(2[0-3]|[01]\d)')
IS_GZIP = re.compile(r'(.gz)$')
################


##################
# Module classes #
##################
class ModuleHelpAction(argparse._HelpAction):
    """The class for overriding method __call__
    """
    def __call__(self, parser, namespace, values, option_string=None):
        if 'help' in option_string:
            parser.print_help_detailed()
            parser.exit()
        parser.print_help()
        parser.exit()


class ModuleParser(argparse.ArgumentParser):
    """The class add method print_help_detailed
    """
    @classmethod
    def print_help_detailed(cls):
        """Print help documentation
        """
        sys.stdout.write(__doc__)
##################


def sigint_handler(error, stack):
    sys.stderr.write('\n')
    sys.exit(1)


def print_csv(result):
    for line in result:
        sys.stdout.write('{0},{1}\n'.format(*line))


def run_function(function, options):
    result = function(options.files)
    if options.out_format == 'print':
        pprint.pprint(result)
    else:
        print_csv(result)


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


#######################
# Processing function #
#######################
def requests_by_ip(log_file):
    result = {}
    group_ip = 1
    for line in read_files(log_file):
        obj = REGEX_IP.search(line)
        if obj:
            ip_address = obj.group(group_ip)
        if REGEX_HTTP.search(line):
            add_item(result, ip_address)
    return sorted(result.items(), cmp=cmp_http, reverse=True)


def requests_by_hour(log_file):
    result = {}
    for line in read_files(log_file):
        obj = REGEX_DATE_TIME.search(line)
        if obj:
            key = format_date_time(obj.groups())
            add_item(result, key)
    return sorted(result.items(), cmp=cmp_date_time)


def read_files(file_list):
    for name_file in file_list:
        if IS_GZIP.search(name_file):
            function_open = gzip.open
        else:
            function_open = open

        with function_open(name_file) as log_file:
            for line in log_file:
                yield line
#######################


CHOICES = {
    'requests_by_ip': requests_by_ip,
    'requests_by_hour': requests_by_hour
}


def parse_args():
    """parse command line parameters passed to the module.
    """
    parser = ModuleParser(add_help=False)

    parser.add_argument(
        '-o', '--out-format', type=str, default='print',
        choices=['print', 'csv'], help='Selecting the output result'
    )
    parser.add_argument(
        '-h', '--help', action=ModuleHelpAction,
        help='Show help message and exit'
    )
    parser.add_argument(
        '-m', '--mode', type=str, choices=CHOICES.keys(),
        default='requests_by_ip',
        help='Selecting the mode processing log-files'
    )
    parser.add_argument(
        'files', nargs='+', metavar='FILENAME',
        help='The names of files to process'
    )

    return parser.parse_args()


def main():
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    signal.signal(signal.SIGINT, sigint_handler)

    options = parse_args()

    if not options.mode:
        sys.stderr.write('--> Search mode unknown <--\n')
        sys.exit(1)

    if options.mode in CHOICES:
        run_function(CHOICES[options.mode], options)


if __name__ == '__main__':
    main()
    # timer.print_time(main)
