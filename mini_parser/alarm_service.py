class AlarmService(object):
    instance = None

    @staticmethod
    def get_instance():
        if AlarmService.instance is None:
            AlarmService.instance = AlarmService()
        return AlarmService.instance

    def __init__(self):
        pass