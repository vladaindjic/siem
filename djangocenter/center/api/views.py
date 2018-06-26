import json
import sys

from bson import json_util
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,

)
from rest_framework.views import APIView

from ..permissions import *

sys.path.append("..")

from center.mini_parser.log_service import LogService
from center.mini_parser.alarm_service import AlarmService
from center.mini_parser.alarm_fire_service import AlarmFireService

log_service = LogService.get_instance()
alarm_service = AlarmService.get_instance()
alarm_fire_service = AlarmFireService.get_instance()

decorator_with_arguments = lambda decorator: lambda *args, **kwargs: lambda func: decorator(func, *args, **kwargs)


@decorator_with_arguments
def custom_permission_required(function, perm):
    def _function(request, *args, **kwargs):
        print(request.user.get_group_permissions())
        if "center." + perm in request.user.get_group_permissions():
            return function(request, *args, **kwargs)
        else:
            return Response(status=HTTP_401_UNAUTHORIZED)
            # Return a response or redirect to referrer or some page of your choice

    return _function


@api_view(['PUT'])
@custom_permission_required("find_logs")
@permission_classes((IsAuthenticated, HasGroupPermission,))
def find_logs(request):
    logs = log_service.find(syslog_query=request.data['query'])
    return Response(json.dumps(logs, default=json_util.default))


@api_view(['POST'])
@custom_permission_required("create_alarm")
@permission_classes((IsAuthenticated, HasGroupPermission,))
def create_alarm(request):
    from center.mini_parser.alarm_util import convert_alarm_to_dict
    alarm = alarm_service.add_alarm(alarm_str=request.data['query'])
    return Response(json.dumps(convert_alarm_to_dict(alarm), default=json_util.default), HTTP_200_OK)


@api_view(['PUT'])
@custom_permission_required("update_alarm")
@permission_classes((IsAuthenticated, HasGroupPermission,))
def update_alarm(request, idA):
    from center.mini_parser.dto.alarm_dto import AlarmDto
    from center.mini_parser.alarm_util import convert_alarm_to_dict
    alarm = alarm_service.update_alarm(alarm_dto=AlarmDto(query=request.data['query']), alarm_id=idA)
    return Response(json.dumps(convert_alarm_to_dict(alarm), default=json_util.default), HTTP_200_OK)


@api_view(['DELETE'])
@custom_permission_required("delete_alarm")
@permission_classes((IsAuthenticated, HasGroupPermission,))
def delete_alarm(request, idA):
    alarm_service.delete_alarm(alarm_id=idA)
    return Response('', HTTP_204_NO_CONTENT)


@api_view(['GET'])
@custom_permission_required("get_alarms")
@permission_classes((IsAuthenticated, HasGroupPermission,))
def get_alarms(request):
    return Response(json.dumps(alarm_service.get_alarms(), default=json_util.default), HTTP_200_OK)


@api_view(['PUT'])
@custom_permission_required("get_alarm_analytics")
@permission_classes((IsAuthenticated, HasGroupPermission,))
def get_alarm_analytics(request):
    data = request.data
    startTime = data['startTime']
    endTime = data['endTime']
    all = data['all']
    hosts = data['hosts']
    print(startTime)
    return Response(json.dumps(alarm_service.alarm_analytics(startTime,endTime,all,hosts), default=json_util.default),HTTP_200_OK)


@api_view(['PUT'])
@custom_permission_required("get_log_analytics")
@permission_classes((IsAuthenticated, HasGroupPermission,))
def get_log_analytics(request):
    data = request.data
    startTime = data['startTime']
    endTime = data['endTime']
    all = data['all']
    hosts = data['hosts']
    # print(data)
    return Response(json.dumps(log_service.log_analytics(startTime, endTime, all, hosts), default=json_util.default),HTTP_200_OK)

@api_view(['GET'])
@custom_permission_required("get_hosts")
@permission_classes((IsAuthenticated, HasGroupPermission,))
def get_hosts(request):
    return Response(log_service.get_hostnames())

@api_view(['GET'])
def funkcija(request):
    print("ovdi sam")
    return Response(status=HTTP_200_OK)


@api_view(['GET'])
@custom_permission_required("get_alarms")
@permission_classes((IsAuthenticated, HasGroupPermission,))
def alarm_fire_details(request, idA):
    return Response(json.dumps(alarm_fire_service.get_alarm_fire_details(idA), default=json_util.default), HTTP_200_OK)



class UpdatePassword(APIView):
    """
    An endpoint for changing password.
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()

        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        repeated_password = request.data.get("repeat_new_password")
        if not self.object.check_password(old_password):
            return Response({"old_password": ["Wrong password."]},
                            status=HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get

        if not new_password == repeated_password:
            return Response({"old_password": ["Repeated Password doesn't match."]},
                            status=HTTP_400_BAD_REQUEST)

        self.object.set_password(new_password)
        self.object.save()
        return Response('', status=HTTP_204_NO_CONTENT)


# ajde da pokrenemo i mini server
from threading import Thread
from center.mini_parser.log_server import LogServer
Thread(target=LogServer.get_instance().start_server).start()