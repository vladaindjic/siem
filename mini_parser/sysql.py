from parglare import Grammar, Parser
from mongo_backend import mongo_actions


def build_grammar(file_path):
    grammar = Grammar.from_file(file_path)
    return grammar


def build_parser(grammar, actions):
    parser = Parser(grammar, actions=actions)
    return parser


def parse_sysql(sysql):
    g = build_grammar('sysql.pg')
    p = build_parser(g, mongo_actions)
    template = "db.log.find(%s)"
    mongo_query = template % p.parse(sysql)
    return mongo_query

# parser = Parser(g, debug=True)
# result = parser.parse('facility >= 1 or severity<2 and appname=\"Vlado,\" majstore\" or hostname=/cao, vladimire/')
# result = parser.parse('before(2013-01-20 10:11:15) and after(2020-01-25) or before(2015-02)')
# result = parser.parse('at(2013-01-20)')


result = parse_sysql('not (last(1Y 2M 3D 1h 2m 3s)) or last(1Y)')
print(result)

# print("db.log.find(%s)" % result)
#
# t = time_parser.parse("2016-01-01T10:11:15+02:00")
#
# print(t)
# print(t + relativedelta(months=1))


class SysqlMongoParser(object):
    def __init__(self):
        self.grammar = build_grammar('sysql.pg')
        self.parser = build_parser(self.grammar, mongo_actions)

    def parse(self, sysql_str):
        try:
            return self.parser.parse(sysql_str)
        except:
            return None
