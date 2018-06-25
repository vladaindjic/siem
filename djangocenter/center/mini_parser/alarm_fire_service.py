# sa tackama
from djangocenter.consumers import send_message_alarm_fire
from .alarm_repository import AlarmRepository
from .dto.alarm_fire import AlarmFireDto


# bez tacaka
# from alarm_engine import AlarmEngine
# from dto.alarm_dto import AlarmDto
# from dto.alarm_fire import AlarmFireDto
# from alarm_repository import AlarmRepository


class AlarmFireService(object):
    instance = None

    @staticmethod
    def get_instance():
        if AlarmFireService.instance is None:
            AlarmFireService.instance = AlarmFireService()
        return AlarmFireService.instance

    def __init__(self):
        self.alarm_repository = AlarmRepository.get_instance()

    def find_alarm_by_str(self, alarm_str):
        return self.alarm_repository.find_alarm_by_str(alarm_str)

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
        af = self.alarm_repository.fire_alarm(alarm_fire)
        # TODO: ovde pozivamo socket
        # print("Iz servisa se salje u socket alarm fire " + af)
        print("VRACAMO REZULTAT NAKON PUCANJA ALARMA %s" % af)
        send_message_alarm_fire(af)
        return af


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
    als.fire_alarm(None, 'severity=1', datetime.datetime.now(), [Log({'severity':1, 'hostname': 'asd'})])

    print(als.alarm_analytics())