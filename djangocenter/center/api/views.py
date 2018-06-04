import sys
import json
from bson import json_util
from django.db.models import fields
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import permission_required

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth.models import Permission, Group

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,

)
from ..permissions import *
from rest_framework.serializers import Serializer

from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)

sys.path.append("..")
from mini_parser.log_service import LogService

log_service = LogService.get_instance()

decorator_with_arguments = lambda decorator: lambda *args, **kwargs: lambda func: decorator(func, *args, **kwargs)


@decorator_with_arguments
def custom_permission_required(function, perm):
    def _function(request, *args, **kwargs):
        if "center." + perm in request.user.get_group_permissions():
            return function(request, *args, **kwargs)
        else:
            return Response(status=HTTP_401_UNAUTHORIZED)
            # Return a response or redirect to referrer or some page of your choice

    return _function


@api_view(['GET'])
@custom_permission_required("find_logs")
@permission_classes((IsAuthenticated, HasGroupPermission,))
def find_logs(request):
    logs = log_service.find(syslog_query=request.query_params['query'])
    print(logs)

    return Response(json.dumps(logs, default=json_util.default))


@api_view(['POST'])
@permission_required("create_alarm")
@permission_classes((IsAuthenticated, HasGroupPermission,))
def create_alarm(request):
    log_service.alarm_engine.add_alarm(alarm_str="")
    return Response("")


@api_view(['PUT'])
@custom_permission_required("update_alarm")
@permission_classes((IsAuthenticated, HasGroupPermission,))
def update_alarm(request):
    return Response("")


@api_view(['DELETE'])
@custom_permission_required("delete_alarm")
@permission_classes((IsAuthenticated, HasGroupPermission,))
def delete_alarm(request):
    log_service.alarm_engine.remove_alarm(alarm_str="")
    return Response("")


@api_view(['GET'])
@custom_permission_required("get_alarms")
@permission_classes((IsAuthenticated, HasGroupPermission,))
def get_alarms(request):
    alarms = log_service.alarm_engine.alarms.items()
    return


@api_view(['GET'])
@custom_permission_required("get_alarm_details")
@permission_classes((IsAuthenticated, HasGroupPermission,))
def get_alarm_details(request):
    alarms = log_service.alarm_engine.alarms.get(kwargs="pk")
    return


@api_view(['GET'])
@custom_permission_required("get_alarm_analytics")
@permission_classes((IsAuthenticated, HasGroupPermission,))
def get_alarm_analytics(request):
    return


@api_view(['GET'])
@custom_permission_required("get_log_analytics")
@permission_classes((IsAuthenticated, HasGroupPermission,))
def get_log_analytics(request):
    return


@api_view(['GET'])
def funkcija(request):
    print("ovdi sam")
    return Response(status=HTTP_200_OK)


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
