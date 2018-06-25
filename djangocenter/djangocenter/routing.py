# routing.py
from channels.routing import route
# from .consumers import websocket_receive
from .consumers import *

# channel_routing = [
#     route("websocket.receive", websocket_receive, path=r"^/chat/"),
# ]



channel_routing = [
    route('websocket.connect', ws_connect_alarm_fire, path=r"^/alarm-fire/"),
    route('websocket.disconnect', ws_disconnect_alarm_fire, path=r"^/alarm-fire/"),
]