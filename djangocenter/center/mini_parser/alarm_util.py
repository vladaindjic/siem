# sa tackama
from .log_util import convert_log_to_dict

# bez tacaka
# from log_util import convert_log_to_dict


def convert_alarm_to_dict(alarm_dto):
    ret = {'query': alarm_dto.query}
    if alarm_dto._id is not None:
        ret['_id'] = alarm_dto._id
    return ret


def convert_alarm_fire_to_dict(alarm_fire_dto):
    ret = {
        'alarm_id': alarm_fire_dto.alarm_id,
        'alarm_str': alarm_fire_dto.alarm_str,
        'timestamp': alarm_fire_dto.timestamp,
        'logs': [convert_log_to_dict(log) for log in alarm_fire_dto.logs],
        'hostname': alarm_fire_dto.hostname
    }
    if alarm_fire_dto._id is not None:
        ret['_id'] = alarm_fire_dto._id
    print("Udjes li ti ovde ponov")
    return ret


