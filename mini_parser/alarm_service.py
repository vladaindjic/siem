from alarm_engine import AlarmEngine


class AlarmService(object):
    instance = None

    @staticmethod
    def get_instance():
        if AlarmService.instance is None:
            AlarmService.instance = AlarmService()
        return AlarmService.instance

    def __init__(self):
        self.alarm_engine = AlarmEngine.get_instance()

    def add_alarm(self, alarm):
        pass

    def get_alarm(self, alarm_id):
        pass

    def get_alarms(self):
        pass

    def delete_alarm(self, alarm_id):
        pass

    def update_alarm(self, alarm_id, alarm):
        pass

    def check_log(self, log):
        pass