# sa tackama
from .alarm import AlarmCompiler
from .dto.log_dto import Log

# bez tacaka
# from alarm import AlarmCompiler
# from dto.log_dto import Log


from json import loads


class AlarmEngine(object):
    instance = None

    @staticmethod
    def get_instance():
        if AlarmEngine.instance is None:
            AlarmEngine.instance = AlarmEngine()
        return AlarmEngine.instance

    def __init__(self):
        self.alarms = {}
        self.compiler = AlarmCompiler()

    def add_alarm(self, alarm_str):
        if alarm_str in self.alarms:
            raise KeyError("The same alaram already exists")
        alarm = self.compiler.compile(alarm_str)
        alarm.set_alarm_str(alarm_str)
        # alarm.init()
        self.alarms[alarm_str] = alarm
        print("Trenutno imamo: %d" % len(self.alarms))
        return alarm

    def remove_alarm(self, alarm_str):
        if alarm_str in self.alarms:
            del self.alarms[alarm_str]
        else:
            raise KeyError("Alarm does not exist")
        print("Trenutno imamo: %d" % len(self.alarms))

    def add_log(self, log):
        # FIXME: trenutno se jako glupo resava
        for al in self.alarms.values():
            al.check_log(log)
        return log


def build_log():
    import rfc3339
    import sysqo_time_util
    from json import dumps
    log = {
        'timestamp': sysqo_time_util.removo_colon_from_rfc3339_time_format(
            rfc3339.rfc3339(sysqo_time_util.get_current_local_time())),
        'msg': 'cao, kako si, user:vlada  asd'
    }
    return dumps(log)


if __name__ == '__main__':
    ae = AlarmEngine()
    ae.add_alarm('severity = 1')
    # ae.add_alarm('severity = 2; count(2)')
    ae.add_alarm('last(10s) and msg=/.*cao.*/; count(3)')
    ae.add_alarm('last(10s) and msg=/.*user:${\w+}.*/; count(3)')

    log1 = r'{"severity": 1}'
    # log2 = r'{"severity": 2}'
    # log3 = r'{"severity": 3}'
    # log4 = r'{"severity": 2}'
    # log5 = r'{"severity": 2}'
    # log6 = r'{"severity": 2}'
    #
    # log7 = r'{"timestamp":"2018-05-22T01:27:17+02:00", "msg":"cao, kako si"}'
    # log8 = r'{"timestamp":"2018-05-22T01:27:17+02:00", "msg":"cao, kako si"}'
    # log9 = r'{"timestamp":"2018-05-22T01:27:17+02:00", "msg":"cao, kako si"}'
    # log10 = r'{"timestamp":"2018-05-22T01:27:17+02:00", "msg":"cao, kako si"}'
    #
    ae.add_log(log1)
    # ae.add_log(log2)
    # ae.add_log(log3)
    # ae.add_log(log4)
    # ae.add_log(log5)
    # ae.add_log(log6)
    # ae.add_log(log7)
    # ae.add_log(log8)
    # ae.add_log(log9)

    from time import sleep
    from sysqo_time_util import convert_rfc3339str_to_datetime
    logs = []
    for i in range(10):
        l = build_log()
        # sleep(3)
        print("Adding: %s" % l)
        l = ae.add_log(l)
        logs.append(l)
    logs.sort(key=lambda l: convert_rfc3339str_to_datetime(l.timestamp), reverse=True)
