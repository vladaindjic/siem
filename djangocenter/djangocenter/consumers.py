
from channels import Group

from center.mini_parser.alarm_util import convert_alarm_fire_to_dict
from center.mini_parser.log_util import convert_log_to_dict
import json
from bson import json_util


def send_message_alarm_fire(alarm_fire):
    af_dict = convert_alarm_fire_to_dict(alarm_fire)
    # saljemo id alarm-fire
    af_json = json.dumps(af_dict, default=json_util.default)

    Group('alarm-fire').send({'text': af_json})
    # print('Rezultat je: %s' % ret)
    print("Poslat alarm u socket")


# otvaranje socketa
def ws_connect_alarm_fire(message):
    Group('alarm-fire').add(message.reply_channel)
    print("Konektovao si se")
    Group('alarm-fire').send({'text': 'connected'})


# zatvaranje socketa
def ws_disconnect_alarm_fire(message):
    Group('alarm-fire').send({'text': 'disconnected'})
    Group('alarm-fire').discard(message.reply_channel)
    print('Diskonektovao si se')


# socketi za logove
def send_message_log(log):
    log_dict = convert_log_to_dict(log)
    log_json = json.dumps(log_dict, default=json_util.default)
    # print('Evo kod je tipa log_json: %s' % type(log_json))
    # saljemo json loga
    Group('log').send({'text': log_json})
    # print("Poslat log u socket")


# otvaranje socketa
def ws_connect_log(message):
    Group('log').add(message.reply_channel)
    print("Konektovao si se da slusas logove")
    Group('log').send({'text': 'connected'})


# zatvaranje socketa
def ws_disconnect_log(message):
    Group('log').send({'text': 'disconnected'})
    Group('log').discard(message.reply_channel)
    print('Diskonektovao si se')

