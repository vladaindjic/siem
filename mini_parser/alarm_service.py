from alarm_engine import AlarmEngine
from dto.alarm_dto import AlarmDto
from dto.alarm_fire import AlarmFireDto
from alarm_repository import AlarmRepository
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
            alarm_id = self.find_alarm_by_str(alarm_str)['_id']

        alarm_fire = AlarmFireDto.create_instance(alarm_id, alarm_str, time, logs)
        return self.alarm_repository.fire_alarm(alarm_fire)



if __name__ == '__main__':
    als = AlarmService.get_instance()
    new = als.add_alarm("severity=1")
    print("New: %s" % new.inserted_id)
    # print(type(new.inserted_id))
    # print(als.get_alarm("5b132b95ece47a0af32d9e46"))
    # print(als.get_alarms())
    updated = als.update_alarm(new.inserted_id, AlarmDto(query="facility=1"))
    print(updated._id)
    print(als.find_alarm_by_str('facility=1')['_id'])

    import datetime
    from dto.log_dto import Log
    als.fire_alarm(None, 'facility=1', datetime.datetime.now(), [Log({'facility':1})])

