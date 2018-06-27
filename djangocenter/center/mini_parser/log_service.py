# sa tackama
from .log_util import convert_json_to_log
from .log_respository import LogRepository
from .alarm_engine import AlarmEngine
from .sysql import SysqlMongoCompiler
from .alarm_service import AlarmService

# bez tacaka
# from log_util import convert_json_to_log
# from log_respository import LogRepository
# from alarm_engine import AlarmEngine
# from sysql import SysqlMongoCompiler
# from alarm_service import AlarmService

from djangocenter.consumers import send_message_log


class LogService(object):
    instance = None

    @staticmethod
    def get_instance():
        if LogService.instance is None:
            LogService.instance = LogService()
        return LogService.instance

    def __init__(self):
        self.log_repository = LogRepository.get_instance()
        self.sysql_compiler = SysqlMongoCompiler.get_instance()
        self.alarm_service = AlarmService.get_instance()

    def add_log(self, log_str):
        log = convert_json_to_log(log_str)

        log = self.log_repository.add_log(log)
        print("Pre cekiranja")
        self.alarm_service.check_log(log)
        print("POSLE CEKIRANJA")
        # poslati log kroz socket
        send_message_log(log)

    def find(self, syslog_query):
        print("Trazimo: %s" % syslog_query)
        compiled_query = self.sysql_compiler.compile(syslog_query)
        print("Posle kompajliranja: %s" % compiled_query)
        res = self.log_repository.find(compiled_query['mongo_query'], compiled_query['limit'],
                                 compiled_query['page'], compiled_query['sort'])
        return res

    def log_analytics(self, start_time=None, end_time=None, all_system=True, hosts=[]):
        from .sysqo_time_util import convert_rfc3339str_to_datetime
        from datetime import datetime
        # start_time i end_time su u rfc3339 formatu
        start_time = convert_rfc3339str_to_datetime(start_time) if start_time is not None else datetime(1970, 1, 1)
        end_time = convert_rfc3339str_to_datetime(end_time) if end_time is not None else datetime.now()
        # FIXME: nadji pametniji nacin da ovo sredis
        return self.log_repository.log_analytics(start_time, end_time, all_system, hosts)

    def get_hostnames(self):
        return self.log_repository.get_hostnames()


if __name__ == '__main__':
    # query = "severity > 1 and severity < 3 ; limit(10), page(2), sort(hostname:asc, appname:desc)"
    # query = "severity > 1 and facility!=1; limit(10), page(2), sort(hostname:asc, appname:desc)"
    # query = 'last(1Y) and severity > 3 and msg=/.*/ and hostname="192.168.1.1"'

    query = 'last(1Y) and appname="FakeWebApp"; limit(100), page(0), sort(severity:desc)'
    ls = LogService.get_instance()
    # res = ls.find(query)
    # print(res)
    res = ls.log_analytics(all_system=False, hosts=['fake', '192.168.1.1'])
    print(res)
    # FIXME: Regex ne radi
