if __name__ == '__main__':
    from djangocenter.center.mini_parser.log_service import LogService
    from djangocenter.center.mini_parser.alarm_service import AlarmService
    from json import dumps
    ls = LogService.get_instance()
    als = AlarmService.get_instance()
    l1 = {"timestamp": "2018-06-05T18:31:15+02:00", "version": 1,
     "severity": 5,
     "msg": "from:218.221.174.2 \"POST /logout HTTP/1.0\" 200 4941 \"Mozilla/5.0 (X11; Linux x86_64; rv:1.9.7.20) Gecko/2016-04-20 13:01:53 Firefox/3.6.1 \"",
     "hostname": "192.168.1.1", "appname": "FakeWebApp", "msgid": "msg8533", "facility": 1}

    l1 = {"timestamp": "2018-06-05T18:31:15+02:00", "version": 1,
          "severity": 5,
          "msg": "from:218.221.174.2 \"POST /logout HTTP/1.0\" 200 4941 \"Mozilla/5.0 (X11; Linux x86_64; rv:1.9.7.20) Gecko/2016-04-20 13:01:53 Firefox/3.6.1 \"",
          "hostname": "192.168.1.1", "appname": "FakeWebApp", "msgid": "msg8533", "facility": 1}

    l2 = {"timestamp": "2018-06-05T18:31:15+02:00", "version": 1,
          "severity": 5,
          "msg": "from:232.221.174.2 \"POST /logout HTTP/1.0\" 200 4941 \"Mozilla/5.0 (X11; Linux x86_64; rv:1.9.7.20) Gecko/2016-04-20 13:01:53 Firefox/3.6.1 \"",
          "hostname": "192.168.1.1", "appname": "FakeWebApp", "msgid": "msg8533", "facility": 1}

    l3 = {"timestamp": "2018-06-05T18:31:15+02:00", "version": 1,
          "severity": 5,
          "msg": "from:218.221.174.2 \"POST /logout HTTP/1.0\" 200 4941 \"Mozilla/5.0 (X11; Linux x86_64; rv:1.9.7.20) Gecko/2016-04-20 13:01:53 Firefox/3.6.1 \"",
          "hostname": "192.168.1.1", "appname": "FakeWebApp", "msgid": "msg8533", "facility": 1}

    l4 = {"timestamp": "2018-06-05T18:31:15+02:00", "version": 1,
          "severity": 5,
          "msg": "from:232.221.174.2 \"POST /logout HTTP/1.0\" 200 4941 \"Mozilla/5.0 (X11; Linux x86_64; rv:1.9.7.20) Gecko/2016-04-20 13:01:53 Firefox/3.6.1 \"",
          "hostname": "192.168.1.1", "appname": "FakeWebApp", "msgid": "msg8533", "facility": 1}

    l5 = {"timestamp": "2018-06-05T18:31:15+02:00", "version": 1,
          "severity": 5,
          "msg": "from:218.221.174.2 \"POST /logout HTTP/1.0\" 200 4941 \"Mozilla/5.0 (X11; Linux x86_64; rv:1.9.7.20) Gecko/2016-04-20 13:01:53 Firefox/3.6.1 \"",
          "hostname": "192.168.1.1", "appname": "FakeWebApp", "msgid": "msg8533", "facility": 1}
    l6 = {"timestamp": "2018-06-05T18:31:15+02:00", "version": 1,
          "severity": 5,
          "msg": "from:232.221.174.2 \"POST /logout HTTP/1.0\" 200 4941 \"Mozilla/5.0 (X11; Linux x86_64; rv:1.9.7.20) Gecko/2016-04-20 13:01:53 Firefox/3.6.1 \"",
          "hostname": "192.168.1.1", "appname": "FakeWebApp", "msgid": "msg8533", "facility": 1}

    l7 = {"timestamp": "2018-06-05T18:31:15+02:00", "version": 1,
          "severity": 5,
          "msg": "from:232.221.174.2 \"POST /logout HTTP/1.0\" 200 4941 \"Mozilla/5.0 (X11; Linux x86_64; rv:1.9.7.20) Gecko/2016-04-20 13:01:53 Firefox/3.6.1 \"",
          "hostname": "192.168.1.1", "appname": "FakeWebApp", "msgid": "msg8533", "facility": 1}

    # als.add_alarm(r'msg=/^from:{{\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}}}.*/; count(3)')
    als.add_alarm(r'msg=/^from:${{\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}}}$.*/; count(3)')

    ls.add_log(dumps(l1))
    ls.add_log(dumps(l2))
    ls.add_log(dumps(l3))
    ls.add_log(dumps(l4))
    ls.add_log(dumps(l5))
    ls.add_log(dumps(l6))
    ls.add_log(dumps(l7))