from collections import OrderedDict
from sysqo_time_util import *


class IRObject(object):
    def inv(self):
        return self

    def remove_not(self):
        return self

    def optimize(self):
        return self

    def str_mongo(self):
        return ""


class Not(IRObject):
    def __init__(self, term):
        self.term = term

    def __str__(self):
        return "Not(%s)" % str(self.term)

    def inv(self):
        return self.term.inv()

    def remove_not(self):
        return self.inv()


class And(IRObject):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "And(%s, %s)" % (str(self.left), str(self.right))

    def inv(self):
        return Or(self.left.inv(), self.right.inv())

    def remove_not(self):
        self.left = self.left.remove_not()
        self.right = self.right.remove_not()
        return self

    def optimize(self):
        self.left = self.left.optimize()
        self.right = self.right.optimize()

        transformed = self.simple_simple_optimization()
        if transformed:
            return transformed

        transformed = self.compound_simple_optimization()
        if transformed:
            return transformed

        transformed = self.compound_compound_optimization()
        if transformed:
            return transformed

        return self

    def simple_simple_optimization(self):
        # da li su oba jednostavno
        simple_1, simple_2 = self._find_simple_and_simple()
        if simple_1 and simple_2:
            # da li su im razlicite promenljive
            if simple_1.property.name != simple_2.property.name:
                ce = CompoundExpr()
                ce[simple_1.property.name] = simple_1
                ce[simple_2.property.name] = simple_2
                return ce
            return self
        return None

    def compound_simple_optimization(self):
        # da li je jedan compund
        simple, compound = self._find_compound_and_simple()
        if simple and compound:
            if simple.property.name not in compound:
                compound[simple.property.name] = simple
                return compound
            return self
        return None

    def compound_compound_optimization(self):
        # da li su oba compound
        compound_1, compound_2 = self._find_compound_and_compound()
        if compound_1 and compound_2:
            exchanged = []
            for prop in compound_2:
                if prop not in compound_1:
                    compound_1[prop] = compound_2[prop]
                    exchanged.append(prop)
            for prop in exchanged:
                del compound_2[prop]

            if len(compound_2) <= 0:
                return compound_1
            else:
                return self
        return None

    def _find_simple_and_simple(self):
        if isinstance(self.left, RelExp) and isinstance(self.right, RelExp):
            return self.left, self.right
        else:
            return None, None

    def _find_compound_and_simple(self):
        if isinstance(self.left, RelExp) and isinstance(self.right, CompoundExpr):
            return self.left, self.right
        elif isinstance(self.left, CompoundExpr) and isinstance(self.right, RelExp):
            return self.right, self.left
        else:
            return None, None

    def _find_compound_and_compound(self):
        if isinstance(self.left, CompoundExpr) and isinstance(self.right, CompoundExpr):
            return self.left, self.right
        else:
            return None, None

    def str_mongo(self):
        return "{$and: [%s, %s]}" % (self.left.str_mongo(), self.right.str_mongo())


class Or(IRObject):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "Or(%s, %s)" % (str(self.left), str(self.right))

    def inv(self):
        return And(self.left.inv(), self.right.inv())

    def remove_not(self):
        self.left = self.left.remove_not()
        self.right = self.right.remove_not()
        return self

    def optimize(self):
        self.left = self.left.optimize()
        self.right = self.right.optimize()
        return self

    def str_mongo(self):
        return "{$or: [%s, %s]}" % (self.left.str_mongo(), self.right.str_mongo())


class RelExp(IRObject):
    def __init__(self, property, value):
        self.property = property
        self.value = value

    def set_param(self, property, value):
        self.property = property
        self.value = value
        return self

    def __str__(self):
        return "(%s, %s)" % (str(self.property), str(self.value))

    def str_mongo(self):
        return "{%s: {%s: %s}}" % (self.property, self.str_op(), self.value)

    def str_op(self):
        return ""

    def str_mongo_inside(self):
        # uklonicemo { i }
        return self.str_mongo()[1:-1]


class Lt(RelExp):
    def __init__(self, property=None, value=None):
        super().__init__(property, value)

    def __str__(self):
        return "Lt%s" % super().__str__()

    def inv(self):
        return Gte(self.property, self.value)

    def str_op(self):
        return "$lt"


class Lte(RelExp):
    def __init__(self, property=None, value=None):
        super().__init__(property, value)

    def __str__(self):
        return "Lte%s" % super().__str__()

    def inv(self):
        return Gt(self.property, self.value)

    def str_op(self):
        return "$lte"


class Gt(RelExp):
    def __init__(self, property=None, value=None):
        super().__init__(property, value)

    def __str__(self):
        return "Gt%s" % super().__str__()

    def inv(self):
        return Lte(self.property, self.value)

    def str_op(self):
        return "$gt"


class Gte(RelExp):
    def __init__(self, property=None, value=None):
        super().__init__(property, value)

    def __str__(self):
        return "Gte%s" % super().__str__()

    def inv(self):
        return Lt(self.property, self.value)

    def str_op(self):
        return "$gte"


class Eq(RelExp):
    def __init__(self, property=None, value=None):
        super().__init__(property, value)

    def __str__(self):
        return "Eq%s" % super().__str__()

    def inv(self):
        return Ne(self.property, self.value)

    def str_mongo(self):
        return "{%s: %s}" % (self.property, self.value)


class Ne(RelExp):
    def __init__(self, property=None, value=None):
        super().__init__(property, value)

    def __str__(self):
        return "Ne%s" % super().__str__()

    def inv(self):
        return Eq(self.property, self.value)

    def str_op(self):
        return "$ne"

    def str_mongo(self):
        if isinstance(self.value, RegVal):
            return "{%s: {$not: %s}}" % (self.property, self.value)
        else:
            # klasicno ponasanje
            return super().str_mongo()
# FIXME: vidi sta ces za NotEqual da odradis


class IntVal(object):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "%s" % str(self.value)


class StrVal(object):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "%s" % str(self.value)


class RegVal(object):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "%s" % str(self.value)


class DateVal(object):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "ISODate(\"%s\")" % self.value


class Property(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "%s" % self.name


class CompoundExpr(IRObject):
    def __init__(self):
        self.prop_expressions = OrderedDict()

    def __len__(self):
        return len(self.prop_expressions)

    def __contains__(self, item):
        if item in self.prop_expressions:
            return True
        return False

    def __setitem__(self, key, value):
        if key not in self.prop_expressions:
            self.prop_expressions[key] = value
        else:
            raise KeyError

    def __getitem__(self, item):
        if item in self.prop_expressions:
            return self.prop_expressions[item]
        else:
            raise KeyError

    def __delitem__(self, key):
        if key in self.prop_expressions:
            del self.prop_expressions[key]
        else:
            raise KeyError

    def __iter__(self):
        for i in self.prop_expressions:
            yield i
        raise StopIteration

    def __str__(self):
        string = "{"
        for k, v in self.prop_expressions.items():
            string += str(v)
            string += ", "
        if len(string) > 1:
            string = string[:-2]
        string += "}"
        return string

    def str_mongo(self):
        string = "{"
        for k, v in self.prop_expressions.items():
            string += v.str_mongo_inside()
            string += ", "
        if len(string) > 1:
            string = string[:-2]
        string += "}"
        return string


ir_actions = {
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
    "RelProperty": lambda _, nodes: nodes[0],
    "StrProperty": lambda _, nodes: nodes[0],
    "BeforeExpr": lambda _, nodes: Lt(Property("timestamp"), DateVal(nodes[2][0])),
    "AfterExpr": lambda _, nodes: Gt(Property("timestamp"), DateVal(nodes[2][0])),
    "AtExpr": lambda _, nodes: And(
                                    Gte(Property("timestamp"), DateVal(nodes[2][0])),
                                    Lt(Property("timestamp"), DateVal(nodes[2][1]))
                                  ),
    "LastExpr": lambda _, nodes: Gte(Property("timestamp"), DateVal(nodes[2])),
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
    "TIME_OFFSET": lambda _, value: calculate_offset(value)
}


