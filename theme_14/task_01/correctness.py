import re


PATTERN = ''.join([
    r'^(\d{4})-',               # Format year YYYY
    r'(0[1-9]|1[012])-',        # Format month MM
    r'([0-2][0-9]|3[01]) ',     # Format day DD
    r'([01][0-9]|2[0-3])',      # Format hour HH
    r'(:[0-5][0-9]){2,2}$'      # Format minute MM and second SS
])

RE_DATE_TIME = re.compile(PATTERN)


def is_date_time(str_date_time):
    """Function check for the string str_date_time to the
    correct template 'YYYY-MM-DD HH:MM:SS'.
    """
    if RE_DATE_TIME.match(str_date_time):
        return True
    return False
