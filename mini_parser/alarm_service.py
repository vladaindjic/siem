# sa tackama
from .alarm_engine import AlarmEngine
from .dto.alarm_dto import AlarmDto
from .dto.alarm_fire import AlarmFireDto
from .alarm_repository import AlarmRepository


# bez tacaka
# from alarm_engine import AlarmEngine
# from dto.alarm_dto import AlarmDto
# from dto.alarm_fire import AlarmFireDto
# from alarm_repository import AlarmRepository


import re


class AlarmService(object):
    instance = None

    @staticmethod
    def get_instance():
        if AlarmService.instance is None:
            AlarmService.instance = AlarmService()
        return AlarmService.instance

    def __init__(self):
        self.alarm_engine = AlarmEngine.get_instance()
        self.alarm_repository = AlarmRepository.get_instance()

    def add_alarm(self, alarm_str):
        # izbaciti vise whitespaceova na jedan
        alarm_str = re.sub("\s+", " ", alarm_str)
        alarm_in_engine = self.alarm_engine.add_alarm(alarm_str)
        alarm_dto = AlarmDto.create_instance(alarm_str)
        alarm_in_db = self.alarm_repository.add_alarm(alarm_dto)
        alarm_in_engine.set_alarm_str(alarm_str)
        alarm_in_engine.set_alarm_id(alarm_in_db.inserted_id)
        return alarm_in_db

    def get_alarm(self, alarm_id):
        return self.alarm_repository.get_alarm(alarm_id)

    def get_alarms(self):
        return self.alarm_repository.get_alarms()

    def find_alarm_by_str(self, alarm_str):
        return self.alarm_repository.find_alarm_by_str(alarm_str)

    def delete_alarm(self, alarm_id):
        old_alarm_dict = self.alarm_repository.delete_alarm(alarm_id)
        # brisemo i iz engine-a
        self.alarm_engine.remove_alarm(old_alarm_dict['query'])

    def update_alarm(self, alarm_id, alarm_dto):
        # update alarma bi znacilo njegovo brisanje, pa ponovno dodavanjem
        # dodamo novi u engine
        self.alarm_engine.add_alarm(alarm_dto.query)
        # ako je uspesno proslo, onda radimo update
        old_alarm_dict, updated_value = self.alarm_repository.update_alarm(alarm_id, alarm_dto)
        self.alarm_engine.remove_alarm(old_alarm_dict['query'])
        # updated_value je AlarmDto
        return updated_value

    def check_log(self, log):
        # ubacujemo log u engine ako treba
        self.alarm_engine.add_log(log)

    def fire_alarm(self, alarm_id, alarm_str, time, logs):
        # FIXME: ako kojim slucajem alarm_id nije postavljen zbog konkurentnosti, jako retko
        # vraticemo ga iz baze
        if alarm_id is None:
            print("Sta me koji kurac jebes?: %s" % alarm_str)
            # FIXME: da li moze ikada da bude None ovde
            alarm_id = self.find_alarm_by_str(alarm_str)['_id']

        # da li su svi isti hostname-ovi logova koji su izazvali alarm
        # FIXME: Da li moze da se desi da log nema hostname?
        hostname = logs[0].hostname
        for i in range(1, len(logs)):
            # razlicit hostname
            if hostname != logs[i].hostname:
                hostname = None
                break
        if hostname is None:
            hostname = 'multiple_hosts'

        alarm_fire = AlarmFireDto.create_instance(alarm_id, alarm_str, time, logs, hostname)
        return self.alarm_repository.fire_alarm(alarm_fire)

    def alarm_analytics(self, start_time=None, end_time=None, all_system=True, hosts=[]):
        from sysqo_time_util import convert_rfc3339str_to_datetime
        from datetime import datetime
        # start_time i end_time su u rfc3339 formatu
        start_time = convert_rfc3339str_to_datetime(start_time) if start_time is not None else datetime(1970, 1, 1)
        end_time = convert_rfc3339str_to_datetime(end_time) if end_time is not None else datetime.now()
        return self.alarm_repository.alarm_analytics(start_time, end_time, all_system, hosts)


if __name__ == '__main__':
    als = AlarmService.get_instance()
    # new = als.add_alarm("severity=1")
    # print("New: %s" % new.inserted_id)
    # print(type(new.inserted_id))
    # print(als.get_alarm("5b132b95ece47a0af32d9e46"))
    # print(als.get_alarms())
    # updated = als.update_alarm(new.inserted_id, AlarmDto(query="facility=1"))
    # print(updated._id)
    # print(als.find_alarm_by_str('facility=1')['_id'])

    # import datetime
    # from dto.log_dto import Log
    # als.fire_alarm(None, 'severity=1', datetime.datetime.now(), [Log({'severity':1, 'hostname': 'asd'})])

    print(als.alarm_analytics())