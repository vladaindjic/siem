import pymongo
# sa tackama
# from .log_util import convert_log_to_dict
# from .mongo_util import MongoUtil
# bez tacaka
from log_util import convert_log_to_dict
from mongo_util import MongoUtil


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
        limit = limit if limit is not None else 0
        page = page if page is not None else 0
        sort = sort if sort is not None else None
        res = self.log_collection.find(filter=query, limit=limit, skip=limit*page, sort=sort)
        return {
            'logs': list(res),
            'count': res.count()
        }

    def log_analytics(self, start_time, end_time, all_system, hosts):

        # db.log.aggregate(
        #     [
        #
        #         {
        #           $match: {$ or: [{hostname: "192.168.1.1"}, {hostname: "123"}]}
        #          },
        #
        #        {
        #           $group:
        #           {
        #               _id: {hostname: '$hostname'},
        #               logs: { $push: "$$ROOT"},
        #               count: {$sum: 1}
        #           }
        #        }
        #      ]
        # ).pretty()

        match_time = {"timestamp": {"$gte": start_time, "$lte": end_time}}
        if all_system:
            match = match_time
        else:
            or_list_hostnames = []
            for hostname in hosts:
                or_list_hostnames.append({"hostname": hostname})
            match_hostnames = {"$or": or_list_hostnames}
            match = {"$and": [match_time, match_hostnames]}


        group = {
            "_id": {"hostname": "$hostname"},
            "logs": {"$push": "$$ROOT"},
            "count": {"$sum": 1}
        }

        aggregate_list = [
            {
                "$match": match
            },
            {
                "$group": group
            }
        ]

        print(aggregate_list)
        aggregations = list(self.log_collection.aggregate(aggregate_list))
        count = 0
        for ag_item in aggregations:
            count += ag_item['count']
        return {
            'agregations': aggregations,
            'count': count
        }


if __name__ == '__main__':
    l = LogRepository.get_instance()
    id = l.log_collection.insert_one({"vlada": "doktor"}).inserted_id
    print(id)