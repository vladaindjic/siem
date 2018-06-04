from django.db import models


class Permisije(models.Model):
    class Meta:
        managed = False  # No database table creation or deletion operations \
        permissions = (
            ('find_logs', 'Get Logs'),
            ('create_alarm', 'Create Alarm'),
            ('update_alarm', 'Update Alarm'),
            ('delete_alarm', 'Delete Alarm'),
            ('get_alarms', 'Get Alarms'),
            ('get_alarm_details', 'Get Alarm Details'),
            ('get_log_analytics', 'Get Log Analytics'),
            ('get_alarm_analytics', 'Get Alarm Analytics'),

        )
