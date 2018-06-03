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
    def create_instance(alarm_id, alarm_str, time, logs):
        # FIXME: da li je ok da koristimo Object, zbog getera
        # return AlarmDto(AlarmDto.new_id(), query)
        return AlarmFireDto(id=None, alarm_id=alarm_id, alarm_str=alarm_str, time=time, logs=logs)

    def __init__(self, id=None, alarm_id=None, alarm_str=None, time=None, logs=None):
        self._id = id
        self.alarm_id = alarm_id
        self.alarm_str = alarm_str
        self.time = time
        self.logs = logs
