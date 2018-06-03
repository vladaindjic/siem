import sys
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK
)

from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

)

sys.path.append("..")
from mini_parser.log_service import LogService

log_service = LogService.get_instance()


@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def funkcija(request):
    content = {
        'user': str(request.user),  # `django.contrib.auth.User` instance.
        'auth': str(request.auth),  # None
    }
    return Response(content)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def find_logs(request):
    print("**************************")
    print(request)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    logs = log_service.find(syslog_query="severity=3")
    print(logs)
    return Response(logs)


@api_view(['POST'])
@permission_classes((IsAuthenticated, IsAdminUser))
def create_alarm(request):
    log_service.alarm_engine.add_alarm(alarm_str="")
    return Response("")


@api_view(['PUT'])
@permission_classes((IsAuthenticated, IsAdminUser))
def update_alarm(request):
    return Response("")


@api_view(['DELETE'])
@permission_classes((IsAuthenticated, IsAdminUser))
def delete_alarm(request):
    log_service.alarm_engine.remove_alarm(alarm_str="")
    return Response("")


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_alarms(request):
    alarms = log_service.alarm_engine.alarms.items()
    return


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_alarm_details(request):
    alarms = log_service.alarm_engine.alarms.get(kwargs="pk")
    return


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_report_list(request):
    return


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_report(request):
    return

#
# if __name__ == '__main__':
#     print("Ovde sam 1")
#     log_service_instance = LogService.get_instance()
#     print("Ovde sam")
#     print(log_service_instance)
#     print("OVO JE TO")
#     print(log_service_instance.find("severity=3"))


#
# # Create your views here.
# class HomePageView(TemplateView):
#     def get(self, request, **kwargs):
#         return render(request, 'index.html', context=None)
#
#
# class LinksPageView(TemplateView):
#     def get(self, request, **kwargs):
#         return render(request, 'links.html', context=None)
