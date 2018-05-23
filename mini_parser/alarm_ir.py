from collections import OrderedDict
from sysqo_time_util import *

from ir import *


class TimeOffsetVal(Val):
    def __init__(self, timedelta_value):
        super().__init__(timedelta_value)

    def eval(self, log=None):
        # value je timedelta value
        return get_current_local_time() - self.value

    def has_timestamp(self):
        return True


# Deo koji se tice alarma
class Alarm(IRObject):
    def __init__(self, query, count=None):
        self.query = query
        self.count = count

    def init(self):
        self.num_logs = self.count.count.eval() if self.count is not None else 0
        # TODO: ovde ostaje da se razresi kako cemo da hendlamo korisnicka imena i ip adrese
        self.queue = [] if self.num_logs > 1 else None
        self.timestamp_prop_exist = self.has_timestamp()
        self.categorical = self.find_category_resolver()
        self.category_queues = {}

    def check_log(self, log):
        try:
            if self.query.eval(log):
                self._add_log(log)
        except:
            pass

    def _add_log(self, log):
        queue = self.queue
        if queue is not None:
            if self.categorical:
                category = self.categorical.find_category(log)
                if category not in self.category_queues:
                    print("Nova kategorija: %s" % category)
                    self.category_queues[category] = []
                queue = self.category_queues[category]

            queue.append(log)
            # da li treba da se sortira mozda po vremenu
            if self.timestamp_prop_exist:
                queue.sort(key=lambda l: convert_rfc3339str_to_datetime(l.timestamp), reverse=True)
        self._check_fire_alarm(log, queue)

    def _check_fire_alarm(self, log, queue):
        # ako timestamp postoji, proveri da nije istekao iduci od nazad
        # ako je istekao, brisi taj log iz reda
        if self.timestamp_prop_exist:
            while queue:
                last = queue[-1]
                # ako log zadovoljava uslov, ostaje u redu cekanje
                if self.query.eval(last):
                    break
                # inace se brise
                del queue[-1]

        # ako je broj logova manji, nikom nista
        if queue is not None:
            if len(queue) < self.num_logs:
                    return
        # alarm se pali ako je potreban samo jedan log ili ako imamo dovoljan broj logova
        self._fire_alarm(log, queue)

    def _fire_alarm(self, log, queue):
        if queue is not None:
            print("ALARMS: %s" % queue)
            queue.clear()
        else:
            print("ALARM: %s" % log)

    def has_timestamp(self):
        return self.query.has_timestamp()

    def find_category_resolver(self):
        return self.query.find_category_resolver()


class CountExpr(IRObject):
    def __init__(self, count):
        self.count = count


alarm_ir_actions = {
    "Alarm": [
        lambda _, nodes: Alarm(nodes[0]),
        lambda _, nodes: Alarm(nodes[0], nodes[2])
    ],
    "CountExpr": lambda _, nodes: CountExpr(nodes[2]),
    "Query": [
        lambda _, nodes: nodes[0],
        lambda _, nodes: Or(nodes[0], nodes[2])
    ],
    "Expr": [
        lambda _, nodes: nodes[0],
        lambda _, nodes: And(nodes[0], nodes[2])
    ],
    "NonTerm": [
        lambda _, nodes: nodes[0],
        lambda _, nodes: Not(nodes[1])
    ],

    "Term": [
        lambda _, nodes: nodes[0],
        lambda _, nodes:  nodes[1]
    ],
    "SysExpr": lambda _, nodes: nodes[0],
    "RelExpr": [
        lambda _, nodes: nodes[1].set_param(nodes[0], nodes[2])
    ],
    "StrExpr": [
        lambda _, nodes: Eq(nodes[0], nodes[2])
    ],
    "RHSStrExpr": lambda _, nodes: nodes[0],
    "TimestampExpr": lambda _, nodes: nodes[0],
    "Property": lambda _, nodes: Property(nodes[0]),
    "RelProperty": lambda _, nodes: nodes[0],
    "StrProperty": lambda _, nodes: nodes[0],
    "TimeProperty": lambda _, nodes: nodes[0],
    "BeforeExpr": lambda _, nodes: Lt(Property("timestamp"), DateVal(nodes[2][0])),
    "AfterExpr": lambda _, nodes: Gt(Property("timestamp"), DateVal(nodes[2][0])),
    "AtExpr": lambda _, nodes: And(
                                    Gte(Property("timestamp"), DateVal(nodes[2][0])),
                                    Lt(Property("timestamp"), DateVal(nodes[2][1]))
                                  ),
    "LastExpr": lambda _, nodes: Gte(Property("timestamp"), TimeOffsetVal(nodes[2])),
    "datetime": lambda _, nodes: nodes[0],
    "rel_op": lambda _, nodes: nodes[0],
    "eq_op": lambda _, value: Eq(),
    "ne_op": lambda _, value: Ne(),
    "lt_op": lambda _, value: Lt(),
    "lte_op": lambda _, value: Lte(),
    "gt_op": lambda _, value: Gt(),
    "gte_op": lambda _, value: Gte(),
    # int property
    "FACILITY": lambda _, value: Property(value),
    "SEVERITY": lambda _, value: Property(value),
    "VERSION": lambda _, value: Property(value),
    # string property
    "HOSTNAME": lambda _, value: Property(value),
    "APPNAME": lambda _, value: Property(value),
    "PROCID": lambda _, value: Property(value),
    "MSGID": lambda _, value: Property(value),
    "MSG": lambda _, value: Property(value),
    # types:
    "INT": lambda _, value: IntVal(value),
    "STRING": lambda _, value: StrVal(value),
    "REG_EXPR": lambda _, value: RegVal(value),
    # datetime
    "YEAR": lambda _, value: YearInterval("%s-01-01T00:00:00%s" % (value, get_local_timezone())),
    "YEAR_MONTH": lambda _, value: MonthInterval("%s-01T00:00:00%s" % (value, get_local_timezone())),
    "YEAR_MONTH_DAY": lambda _, value: DayInterval("%sT00:00:00%s" % (value, get_local_timezone())),
    "YEAR_MONTH_DAY_HOUR": lambda _, value: MonthInterval("%s:00:00%s" % (re.sub("\s+", "T", value), get_local_timezone())),
    "YEAR_MONTH_DAY_HOUR_MINUTE": lambda _, value: MinuteInterval("%s:00%s" % (re.sub("\s+", "T", value), get_local_timezone())),
    "YEAR_MONTH_DAY_HOUR_MINUTE_SECOND": lambda _, value: SecondInterval("%s%s" % (re.sub("\s+", "T", value), get_local_timezone())),
    "TIME_OFFSET": lambda _, value: calculate_timedelta_offset(value),
    "ASC": lambda _, value: 1,
    "DESC": lambda _, value: -1
}


