from parglare import Grammar, Parser
from ir import ir_actions


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


# class SysqlMongoParser(object):
#     def __init__(self, actions=mongo_actions):
#         self.grammar = build_grammar('sysql.pg')
#         self.parser = build_parser(self.grammar, actions)
#
#     def parse(self, sysql_str):
#         try:
#             return self.parser.parse(sysql_str)
#         except:
#             return None


class SysqlMongoCompiler(object):
    def __init__(self):
        self.grammar = self.build_grammar('sysql.pg')
        self.parser = build_parser(self.grammar, ir_actions)

    def build_grammar(self, grammar_file_path):
        grammar = Grammar.from_file(grammar_file_path)
        return grammar

    def build_parser(self, grammar, actions):
        parser = Parser(grammar, actions=actions)
        return parser

    def parse(self, query):
        return self.parser.parse(query)

    def remove_not(self, ir_representation):
        return ir_representation.remove_not()

    def optimize(self, without_not_ir):
        return without_not_ir.optimize()

    def str_mongo(self, optimized_ir):
        return optimized_ir.str_mongo()

    def compile(self, query):
        print("Sysql query      : %s" % query)
        ir_representation = self.parse(query)
        print("IR reprezentation: %s" % ir_representation)
        without_not_ir = self.remove_not(ir_representation)
        print("Not removed      : %s" % without_not_ir)
        optimized_ir = self.optimize(without_not_ir)
        print("Optimized IR     : %s" % optimized_ir)
        str_mongo_query = self.str_mongo(optimized_ir)
        print("Mongo query      : %s" % str_mongo_query)
        return str_mongo_query

# sysqo = SysqlMongoCompiler()
# # result = sysqo.parse('not (last(1Y 2M 3D 1h 2m 3s)) or last(1Y)')
# # result = sysqo.parse('severity > 10')
# # result = sysqo.parse('severity >= 10 and facility = 15')
#
# # query = "version = 1 and (severity=2 and not(facility=3 or (appname=\"nivica\" and hostname=\"vlada\")))"
#
# # query = 'appname=/nivica/ and hostname ="vlada"'
# #
# query = 'appname = "nivica" or hostname="vlada" and (severity=3 and facility=4)'
#
# # query = 'appname=/nivica/ and not (appname=/nivica/)'
#
# result = sysqo.parse(query)
# print("With Not          : %s" % result)
# result = result.find_not()
# print("without not       : %s" % result)
# result = result.optimize()
# print("After otpimization: %s" % result)
# result = result.str_mongo()
# print("Mongo query       : %s" % result)

# query = "not (last(1Y 2M 3D 1h 2m 3s)) or last(1Y)"
# query = "version = 1 and (severity=2 and not(facility=3 or (appname=\"nivica\" and hostname=\"vlada\")))"
# query = 'appname=/nivica/ and hostname ="vlada"'
# query = 'appname = "nivica" or hostname="vlada" and (severity=3 and facility=4)'
# query = 'appname=/nivica/ and not (appname=/nivica/)'

# mongo_query = sysqo.compile(query)
