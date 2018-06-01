from parglare import Grammar, Parser
from .alarm_ir import alarm_ir_actions


class AlarmCompiler(object):
    def __init__(self):
        self.grammar = self.build_grammar('/home/zarko/Fax/Bezbednost/Siem/siem/mini_parser/alarm.pg')
        self.parser = self.build_parser(self.grammar, alarm_ir_actions)

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

    def prepare_header(self, header):
        if header is None:
            return ""
        return header.str_mongo()

    def compile(self, query):
        # print("Alarm query      : %s" % query)
        alarm = self.parse(query)
        # print("IR reprezentation: %s" % alarm.query)
        alarm.query = self.remove_not(alarm.query)
        # print("Not removed      : %s" % without_not_ir)
        alarm.query = self.optimize(alarm.query)
        # print("Optimized IR     : %s" % alarm.query)
        # alarm.query = self.str_mongo(alarm.query)
        # str_header = self.prepare_header(header)
        # print("Mongo query      : %s" % str_mongo_query)
        # full_query = str_mongo_query + ";" + str_header if str_header else str_mongo_query
        # print("Response: %s" % full_query)
        return alarm


if __name__ == '__main__':
    sysqo = AlarmCompiler()
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
    # query = 'appname=/nivica/ and not (appname=/nivica/); limit(3), page(2), sort(hostname:asc, appname:desc)'
    # query = "before(2014-11-12) and not severity<10; page(3), limit(5), sort(hostname:asc, appname:desc)"

    # query = "last(1s) and appname=/.*Fa.*/; limit(5), page(0)"
    # query = "msg=/$from.*/"
    # query =
    # r'appname="asda\"sd\"asd" and hostname="cao \" kako si" and appname=/\/\/asdasd\// and hostname=/ovo ide\/ovo ne ide/'
    # query = r'not(severity!=1 or facility!=2) and hostname="machine1" and appname="app3"'
    #
    # mongo_query = sysqo.compile(query)


    from ir import Log
    import json
    json_str = r'{"severity": 5, "msgid": "porukica", "timestamp":"2018-05-22T01:27:17+02:00"}'

    l = json.loads(json_str, object_hook=Log)

    # query = "severity = 5"
    # query = r'not msgid="porukica"'
    # query = "msgid=/porukica/"
    # query = r'at(2018)'
    # query = r'severity>3 and msgid="porukica" and before(2017) or after(2016)'
    query = r'severity>3 and msgid="porukica" and last(1d)'


    alarm = sysqo.compile(query)
    print(alarm.query.eval(l))
    print(alarm.num_logs)
    # import datetime
    # print(type(datetime.datetime.now()))

    # from sysqo_time_util import convert_rfc3339str_to_datetime
    # res = convert_rfc3339str_to_datetime("2018-05-22T01:27:17+02:00")
    # print(type(res))
    # print(res)