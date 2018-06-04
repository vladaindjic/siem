# sa tackama
from .mongo_util import MongoUtil
from .alarm_util import convert_alarm_to_dict, convert_alarm_fire_to_dict

# bez tacaka
# from mongo_util import MongoUtil
# from alarm_util import convert_alarm_to_dict, convert_alarm_fire_to_dict

from bson.objectid import ObjectId


class AlarmRepository(object):
    instance = None

    @staticmethod
    def get_instance():
        if AlarmRepository.instance is None:
            AlarmRepository.instance = AlarmRepository()
        return AlarmRepository.instance

    def __init__(self):
        self.alarm_collection = MongoUtil.get_alarm_collection()
        self.alarm_fire_collection = MongoUtil.get_alarm_fire_collection()

    def add_alarm(self, alarm_dto):
        return self.alarm_collection.insert_one(convert_alarm_to_dict(alarm_dto))

    def get_alarm(self, alarm_id):
        # FIXME: da li moze iz Angulara samo string da se vrati za ObjectId
        return self.alarm_collection.find_one(filter={'_id': ObjectId(alarm_id)})

    def get_alarms(self):
        cursor = self.alarm_collection.find({})
        return list(cursor)

    def delete_alarm(self, alarm_id):
        """
            Brisanje alarma i vracanje stare vrednosti
        :param alarm_id:
        :return:
        """
        old_val = self.get_alarm(alarm_id)
        ret = self.alarm_collection.remove(ObjectId(alarm_id))
        if ret['n'] <= 0:
            raise ValueError('Alarm with: %s id does not exist' % alarm_id)
        return old_val

    def update_alarm(self, alarm_id, alarm_dto):
        """
            Update vrednosti i vracanje stare
        :param alarm_id:
        :param alarm_dto:
        :return:
        """
        alarm_dto_old = self.get_alarm(alarm_id)
        # radimo update
        alarm_dto._id = ObjectId(alarm_id)
        self.alarm_collection.replace_one({'_id': alarm_dto._id}, convert_alarm_to_dict(alarm_dto))
        # vracamo stari
        return alarm_dto_old, alarm_dto

    def find_alarm_by_str(self, alarm_str):
        return self.alarm_collection.find_one(filter={'query': alarm_str})

    def fire_alarm(self, alarm_fire):
        return self.alarm_fire_collection.insert_one(convert_alarm_fire_to_dict(alarm_fire))

    def alarm_analytics(self, start_time, end_time, all_system, hosts):
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
            "alarm_fires": {"$push": "$$ROOT"},
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
        aggregations = list(self.alarm_fire_collection.aggregate(aggregate_list))
        count = 0
        for ag_item in aggregations:
            count += ag_item['count']
        return {
            'aggregations': aggregations,
            'count': count
        }