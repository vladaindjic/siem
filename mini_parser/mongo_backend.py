from tzlocal import get_localzone
import datetime
import re
from dateutil import parser as time_parser
import rfc3339
from dateutil.relativedelta import relativedelta


def get_current_local_time():
    local = get_localzone()
    return datetime.datetime.now(local)


def get_local_timezone():
    local = get_localzone()
    tz = get_current_local_time().strftime('%z')
    tz = "%s:%s" % (tz[:3], tz[3:])
    return tz


def get_numeric_offset(offset_str, offset_pattern):
    m = re.search(offset_pattern, offset_str)
    if m:
        return int(m.group(0)[:-1])
    return 0


def calculate_offset(offset_str):
    current_time = get_current_local_time()

    year_offset = get_numeric_offset(offset_str, "\d+(y|Y)")
    # print("Year: %d" % year_offset)
    month_offset = get_numeric_offset(offset_str, "\d+M")
    # print("Month: %d" % month_offset)
    day_offset = get_numeric_offset(offset_str, "\d+(d|D)")
    # print("Day: %d" % day_offset)

    hour_offset = get_numeric_offset(offset_str, "\d+(h|H)")
    # print("Hour: %d" % hour_offset)
    minute_offset = get_numeric_offset(offset_str, "\d+m")
    # print("Minute: %d" % minute_offset)
    second_offset = get_numeric_offset(offset_str, "\d+(s|S)")
    # print("Second: %d" % second_offset)

    offset_delta = relativedelta(years=year_offset, months=month_offset, days=day_offset,
                                 hours=hour_offset, minutes=minute_offset, seconds=second_offset)

    offset_time = current_time - offset_delta
    return rfc3339.rfc3339(offset_time)


mongo_operators = {
    "=": "$eq",
    "!=": "$ne",
    "<": "$lt",
    "<=": "$lte",
    ">": "$gt",
    ">=": "$gte"
}


mongo_actions = {
    "Query": [
        lambda _, nodes: "%s" % nodes[0],
        lambda _, nodes: "{$or: [%s, %s]}" % (nodes[0], nodes[2])
    ],
    "Expr": [
        lambda _, nodes: "%s" % nodes[0],
        lambda _, nodes: "{$and: [%s, %s]}" % (nodes[0], nodes[2])
    ],
    "NonTerm": [
        lambda _, nodes: "%s" % nodes[0],
        lambda _, nodes: "{$nor: [%s]}" % nodes[1]
    ],

    "Term": [
        lambda _, nodes: "%s" % nodes[0],
        lambda _, nodes: "%s" % nodes[1]
    ],
    "SysExpr": lambda _, nodes: "%s" % nodes[0],
    "RelExpr": [
        lambda _, nodes:
        "{%s: {%s: %s}}" % (nodes[0], mongo_operators[nodes[1]], nodes[2]) if nodes[1] != "="
        else "{%s: %s}" % (nodes[0], nodes[2])
    ],
    "StrExpr": [
        lambda _, nodes: "{%s: %s}" % (nodes[0], nodes[2])  # potential extension if use in
    ],
    "RHSStrExpr": lambda _, nodes: "%s" % nodes[0],
    "TimestampExpr": lambda _, nodes: "%s" % nodes[0],
    "RelProperty": lambda _, nodes: "%s" % nodes[0],
    "StrProperty": lambda _, nodes: "%s" % nodes[0],
    "BeforeExpr": lambda _, nodes: "{timestamp: {$lt: ISODate(\"%s\")}}" % nodes[2][0],
    "AfterExpr": lambda _, nodes: "{timestamp: {$gt: ISODate(\"%s\")}}" % nodes[2][0],
    "AtExpr": lambda _, nodes: "{$and: [{timestamp: {$gte: ISODate(\"%s\")}}, {timestamp: {$lt: ISODate(\"%s\")}}]}"
                               % (nodes[2][0], nodes[2][1]),
    "LastExpr": lambda _, nodes: "{timestamp: {$gte: ISODate(\"%s\")}}" % nodes[2],
    "datetime": lambda _, nodes: nodes[0],
    "rel_op": lambda _, nodes: "%s" % nodes[0],
    "eq_op": lambda _, value: "%s" % value,
    "ne_op": lambda _, value: "%s" % value,
    "lt_op": lambda _, value: "%s" % value,
    "lte_op": lambda _, value: "%s" % value,
    "gt_op": lambda _, value: "%s" % value,
    "gte_op": lambda _, value: "%s" % value,
    # int property
    "FACILITY": lambda _, value: "%s" % value,
    "SEVERITY": lambda _, value: "%s" % value,
    "VERSION": lambda _, value: "%s" % value,
    # string property
    "HOSTNAME": lambda _, value: "%s" % value,
    "APPNAME": lambda _, value: "%s" % value,
    "PROCID": lambda _, value: "%s" % value,
    "MSGID": lambda _, value: "%s" % value,
    "MSG": lambda _, value: "%s" % value,
    # types:
    "INT": lambda _, value: "%s" % value,
    "STRING": lambda _, value: "%s" % value,
    "REG_EXPR": lambda _, value: "%s" % value,
    # datetime
    "YEAR": lambda _, value: YearInterval("%s-01-01T00:00:00%s" % (value, get_local_timezone())),
    "YEAR_MONTH": lambda _, value: MonthInterval("%s-01T00:00:00%s" % (value, get_local_timezone())),
    "YEAR_MONTH_DAY": lambda _, value: DayInterval("%sT00:00:00%s" % (value, get_local_timezone())),
    "YEAR_MONTH_DAY_HOUR": lambda _, value: MonthInterval("%s:00:00%s" % (re.sub("\s+", "T", value), get_local_timezone())),
    "YEAR_MONTH_DAY_HOUR_MINUTE": lambda _, value: MinuteInterval("%s:00%s" % (re.sub("\s+", "T", value), get_local_timezone())),
    "YEAR_MONTH_DAY_HOUR_MINUTE_SECOND": lambda _, value: SecondInterval("%s%s" % (re.sub("\s+", "T", value), get_local_timezone())),
    "TIME_OFFSET": lambda _, value: calculate_offset(value)
}


class DateTimeInterval(object):
    def __init__(self, datetime_str):
        self.start_time = time_parser.parse(datetime_str)
        self.end_time = None

    def __getitem__(self, item):
        if item == 0:
            return rfc3339.rfc3339(self.start_time)
        elif item == 1:
            return rfc3339.rfc3339(self.end_time)
        else:
            return None


class SecondInterval(DateTimeInterval):
    def __init__(self, datetime_str):
        super().__init__(datetime_str)
        self.end_time = self.start_time + relativedelta(seconds=1)


class MinuteInterval(DateTimeInterval):
    def __init__(self, datetime_str):
        super().__init__(datetime_str)
        self.end_time = self.start_time + relativedelta(minutes=1)


class HourInterval(DateTimeInterval):
    def __init__(self, datetime_str):
        super().__init__(datetime_str)
        self.end_time = self.start_time + relativedelta(hours=1)


class DayInterval(DateTimeInterval):
    def __init__(self, datetime_str):
        super().__init__(datetime_str)
        self.end_time = self.start_time + relativedelta(days=1)


class MonthInterval(DateTimeInterval):
    def __init__(self, datetime_str):
        super().__init__(datetime_str)
        self.end_time = self.start_time + relativedelta(months=1)


class YearInterval(DateTimeInterval):
    def __init__(self, datetime_str):
        super().__init__(datetime_str)
        self.end_time = self.start_time + relativedelta(years=1)
