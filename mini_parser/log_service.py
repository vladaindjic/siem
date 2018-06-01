from .log_util import convert_json_to_log
from .log_respository import LogRepository
from .alarm_engine import AlarmEngine
from .sysql import SysqlMongoCompiler


class LogService(object):
    instance = None

    @staticmethod
    def get_instance():
        if LogService.instance is None:
            LogService.instance = LogService()
        return LogService.instance

    def __init__(self):
        self.log_repository = LogRepository.get_instance()
        self.alarm_engine = AlarmEngine.get_instance()
        self.sysql_compiler = SysqlMongoCompiler.get_instance()

    def add_log(self, log_str):
        log = convert_json_to_log(log_str)
        self.log_repository.add_log(log)
        self.alarm_engine.add_log(log)

    def find(self, syslog_query):
        print("Trazimo: %s" % syslog_query)
        compiled_query = self.sysql_compiler.compile(syslog_query)
        print("Posle kompajliranja: %s" % compiled_query)
        self.log_repository.find(compiled_query['mongo_query'], compiled_query['limit'],
                                 compiled_query['page'], compiled_query['sort'])


if __name__ == '__main__':
    # query = "severity > 1 and severity < 3 ; limit(10), page(2), sort(hostname:asc, appname:desc)"
    query = "severity > 1 and facility!=1; limit(10), page(2), sort(hostname:asc, appname:desc)"
    # query = 'last(1Y) and severity > 3 and msg=/.*/ and hostname="192.168.1.1"'

    query = 'last(1h) and appname="FakeWebApp"'
    ls = LogService.get_instance()
    ls.find(query)

    # FIXME: Regex ne radi
