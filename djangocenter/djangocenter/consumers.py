# # consumers.py
# def websocket_receive(message):
#     text = message.content.get('text')
#     if text:
#         message.reply_channel.send({"text": "You said: {}".format(text)})
#
#
#
#



import json
from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
import threading
import random

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

# zatvaranje socketa
def ws_disconnect_alarm_fire(message):
    Group('alarm-fire').discard(message.reply_channel)
