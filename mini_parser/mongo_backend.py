from .sysqo_time_util import *

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



