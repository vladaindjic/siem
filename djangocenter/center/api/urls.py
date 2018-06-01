from django.conf.urls import url
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^center/$', views.funkcija, name="funkcija"),
    url(r'^center/login$', obtain_jwt_token),
    url(r'^center/find_logs', views.find_logs, name='find_logs'),
    url(r'^center/create_alarm', views.create_alarm, name='create_alarm'),
    url(r'^center/update_alarm', views.update_alarm, name='update_alarm'),
    url(r'^center/delete_alarm', views.delete_alarm, name='delete_alarm'),
    url(r'^center/get_alarms', views.get_alarms, name='get_alarms'),
    url(r'^center/get_alarm_details', views.get_alarm_details, name='get_alarm_details'),
    url(r'^center/get_report_list', views.get_report_list, name='get_report_list'),
    url(r'^center/get_report', views.get_report, name='get_report'),
]
