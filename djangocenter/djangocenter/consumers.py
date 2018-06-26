
from channels import Group

from center.mini_parser.alarm_util import convert_alarm_fire_to_dict


def send_message_alarm_fire(alarm_fire):
    af_dict = convert_alarm_fire_to_dict(alarm_fire)
    # saljemo id alarm-fire
    Group('alarm-fire').send({'text': str(alarm_fire._id)})
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
