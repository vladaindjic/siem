

class AlarmRepository(object):
    instance = None

    @staticmethod
    def get_instance():
        if AlarmRepository.instance is None:
            AlarmRepository.instance = AlarmRepository()
        return AlarmRepository.instance

    def __init__(self):
        pass
