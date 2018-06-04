from threading import Lock


class AlarmFireDto(object):
    counter = 0
    lock = Lock()

    @staticmethod
    def new_id():
        AlarmFireDto.lock.acquire()
        AlarmFireDto.counter += 1
        new_id = AlarmFireDto.counter
        AlarmFireDto.lock.release()
        return new_id

    @staticmethod
    def create_instance(alarm_id, alarm_str, timestamp, logs, hostname):
        # FIXME: da li je ok da koristimo Object, zbog getera
        # return AlarmDto(AlarmDto.new_id(), query)
        return AlarmFireDto(id=None, alarm_id=alarm_id, alarm_str=alarm_str, timestamp=timestamp, logs=logs, hostname=hostname)

    def __init__(self, id=None, alarm_id=None, alarm_str=None, timestamp=None, logs=None, hostname=None):
        self._id = id
        self.alarm_id = alarm_id
        self.alarm_str = alarm_str
        self.timestamp = timestamp
        self.logs = logs
        self.hostname = hostname
