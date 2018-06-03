from threading import Lock


class AlarmDto(object):
    counter = 0
    lock = Lock()

    @staticmethod
    def new_id():
        AlarmDto.lock.acquire()
        AlarmDto.counter += 1
        new_id = AlarmDto.counter
        AlarmDto.lock.release()
        return new_id

    @staticmethod
    def create_instance(query):
        # FIXME: da li je ok da koristimo Object, zbog getera
        # return AlarmDto(AlarmDto.new_id(), query)
        return AlarmDto(query=query)

    def __init__(self, id=None, query=None):
        self._id = id
        self.query = query