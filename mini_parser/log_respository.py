import pymongo
from .log_util import convert_log_to_dict
from .mongo_util import MongoUtil


class LogRepository(object):
    instance = None

    @staticmethod
    def get_instance():
        if LogRepository.instance is None:
            LogRepository.instance = LogRepository()
        return LogRepository.instance

    def __init__(self):
        self.log_collection = MongoUtil.get_log_collection()
        self._create_indexes()

    def _create_indexes(self):
        self.log_collection.create_index([("timestamp", pymongo.DESCENDING),
                                          ("hostname", pymongo.ASCENDING),
                                          ("appname", pymongo.ASCENDING)],
                                         name="time_host_appname_ind", background=True)
        self.log_collection.create_index([("hostname", pymongo.ASCENDING)],
                                         name="hostname_ind", background=True)
        self.log_collection.create_index([("appname", pymongo.ASCENDING)],
                                         name="appname_ind", background=True)
        self.log_collection.create_index([("msg", pymongo.TEXT)])

    def add_log(self, log):
        log_dict = convert_log_to_dict(log)
        # FIXME: ovde izbaci : iz datuma
        return self.log_collection.insert_one(log_dict).inserted_id

    def find(self, query, limit=None, page=None, sort=None):
        from json import loads
        print(query)
        # print(loads(query))
        print("Ima li te?")
        for l in self.log_collection.find(filter=query):
            print(l)
        # self.log_collection.find(filter=loads(query), limit=limit, skip=limit*page, sort=sort)
        pass


if __name__ == '__main__':
    l = LogRepository.get_instance()
    id = l.log_collection.insert_one({"vlada": "doktor"}).inserted_id
    print(id)