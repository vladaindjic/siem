from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):

    def create_users(self):
        admins, created = Group.objects.get_or_create(name='admins')
        operators, created = Group.objects.get_or_create(name='operators')

        if not User.objects.filter(username='user1').exists():
            user1 = User(
                first_name='Nikola',
                is_staff=False,
                is_superuser=False,
                last_name='Tesla',
                username='user1',
            )
            user1.set_password('asdf1234')
            user1.save()
            admins.user_set.add(user1)

        if not User.objects.filter(username='user2').exists():
            user2 = User(
                first_name='Marko',
                is_staff=False,
                is_superuser=False,
                last_name='Markovic',
                username='user2',
            )
            user2.set_password('asdf1234')
            user2.save()
            operators.user_set.add(user2)

        if not User.objects.filter(username='user3').exists():
            user3 = User(
                first_name='Milos',
                is_staff=False,
                is_superuser=False,
                last_name='Milosevic',
                username='user3',
            )
            user3.set_password('asdf1234')
            user3.save()
            operators.user_set.add(user3)

        get_logs = Permission.objects.get(name="Get Logs")
        create_alarm = Permission.objects.get(name="Create Alarm")
        update_alarm = Permission.objects.get(name="Update Alarm")
        delete_alarm = Permission.objects.get(name="Delete Alarm")
        get_alarms = Permission.objects.get(name="Get Alarms")
        get_alarm_details = Permission.objects.get(name="Get Alarm Details")
        get_log_analytics = Permission.objects.get(name="Get Log Analytics")
        get_alarm_analytics = Permission.objects.get(name="Get Alarm Analytics")
        get_hosts = Permission.objects.get(name="Get Hosts")

        admins.permissions.add(get_logs, create_alarm, update_alarm, delete_alarm, get_alarms, get_alarm_details,
                               get_alarm_analytics, get_log_analytics, get_hosts)

        operators.permissions.add(get_logs, get_alarms, get_alarm_details,
                                  get_alarm_analytics, get_log_analytics, get_hosts)

    def handle(self, *args, **options):
        self.create_users()
