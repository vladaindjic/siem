from ir import Log
from json import loads
from json import dumps
from sysqo_time_util import convert_rfc3339str_to_datetime


def convert_json_to_log(json_str):
    log = loads(json_str, object_hook=Log)
    if hasattr(log, 'timestamp'):
        log.timestamp = convert_rfc3339str_to_datetime(log.timestamp)
    return log


def convert_log_to_dict(log):
    return log.__dict__


if __name__ == '__main__':
    l = Log({'severity': 1, 'msg': "porukica"})
    print(convert_log_to_dict(l))
    print(convert_json_to_log('{"timestamp": "2018-05-30T22:58:16+02:00"}'))