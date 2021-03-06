from django.conf.urls import url
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^center/login$', obtain_jwt_token),
    url(r'^center/change_password$', views.UpdatePassword.as_view(), name="change_password"),
    url(r'^center/find_logs$', views.find_logs, name='find_logs'),
    url(r'^center/create_alarm$', views.create_alarm, name='create_alarm'),
    url(r'^center/update_alarm/(?P<idA>\w{0,50})', views.update_alarm, name='update_alarm'),
    url(r'^center/delete_alarm/(?P<idA>\w{0,50})', views.delete_alarm, name='delete_alarm'),
    url(r'^center/get_alarms', views.get_alarms, name='get_alarms'),
    url(r'^center/get_log_analytics', views.get_log_analytics, name='get_log_analytics'),
    url(r'^center/get_alarm_analytics', views.get_alarm_analytics, name='get_alarm_analytics'),
    url(r'^center/get_hosts', views.get_hosts, name='get_hosts'),
    url(r'^center/alarm_fire_details/(?P<idA>\w{0,50})', views.alarm_fire_details, name='alarm_fire_details')
]

