
# Mmm dd hh:mm:ss
day = '(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
RFC3164_TIMESTAMP = r"%s\s+\d+\s+\d{2}\:\d{2}\:\d{2}" % day
wrap_RFC3164_TIMESTAMP = r".*%s.*" % RFC3164_TIMESTAMP
# print(RFC3164_TIMESTAMP)

# 1985-04-12T23:20:50.52Z - this one is real
# 2018-03-31 15:15:45
RFC3339_TIMESTAMP = r'\d{4}\-\d{2}\-\d{2}(T|\s+)\d{2}\:\d{2}\:\d{2}(\.\d+Z)?'
wrap_RFC3339_TIMESTAMP = r".*%s.*" % RFC3339_TIMESTAMP
# print(RFC3339_TIMESTAMP)


# koji fajlovi imaju ovaj timestamp
RFC3164_log_files = [r'apport', r'kern\.log', r'syslog', r'ufw\.log']
RFC3164_logs_path_patterns = [r'.*%s.*' % file_name for file_name in RFC3164_log_files]
# koji fajlovi imaju ovaj timestamp
RFC3339_log_files = [r'alternatives', r'apport', r'kern\.log', r'syslog', r'dpkg\.log']
RFC3339_logs_path_patterns = [r'.*%s.*' % file_name for file_name in RFC3339_log_files]

# print(RFC3164_logs_path_patterns)
# print(RFC3339_logs_path_patterns)


NO_WHITESPACE_AT_BEGINNING = '^[^\s+]'


def get_new_line_patterns(file_path):
    if contains_RFC3164(file_path):
        return wrap_RFC3164_TIMESTAMP
    elif contains_RFC3339(file_path):
        return wrap_RFC3339_TIMESTAMP
    else:
        return NO_WHITESPACE_AT_BEGINNING


def contains_RFC3164(file_path):
    return any(re.match(pattern, file_path) for pattern in RFC3164_logs_path_patterns)


def contains_RFC3339(file_path):
    return any(re.match(pattern, file_path) for pattern in RFC3339_logs_path_patterns)


def is_new_log_line(line, pattern_matcher):
    # print(line)
    # print(pattern_matcher)
    # print(re.match(pattern_matcher, line))
    return re.match(pattern_matcher, line) is not None


"""
    RFC3164_TIMESTAMP:
        - apport - Apr  1 19:47:52
        - kern.log - Apr  1 02:55:51
        - syslog - Apr  2 16:29:50
    
    RFC3339_TIMESTAMP:
        - dpkg.log 2018-04-01 23:08:42
        - alternatives - Apr  2 01:24:42 2018

        
        
    Sta cemo za:
        - boot.log [^[][][][][][][
        - bootstrap.log - ako pocinje \s+
        - dmesg    
        - fontconfig.log
        - gpu-manager.log
        - Xorg (pocinje sa tabom)
        
    Binarno za:
        - faillog
        
"""

import re
# print(re.match(wrap_RFC3339_TIMESTAMP, "update-alternatives 2018-03-31 15:15:39: run with --install /usr/bin/x-www-browser x-www-browser /usr/bin/chromium-browser 40"))
# print(re.match(NO_WHITESPACE_AT_BEGINNING, "\n     asdas    asdasdas"))
# print(is_new_log_line("update-alternatives 2018-03-31 15:15:39: run with --install /usr/bin/x-www-browser x-www-browser /usr/bin/chromium-browser 40", wrap_RFC3339_TIMESTAMP))


# print(is_new_log_line('Apr  2 16:12:10 vi3-Inspiron-5737 anacron[828]: Job `cron.daily\' terminated', wrap_RFC3164_TIMESTAMP))