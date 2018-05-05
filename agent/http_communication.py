import requests
import json
from security_communication import SecurityChannel

sec_channel = SecurityChannel()

API_ENDPOINT = "https://localhost:8443/logger"

line_num = 0
lines = set()


def send_log_line(line):
    # data = line
    pass
    # r = requests.post(API_ENDPOINT, data=line.encode('utf-8'), headers={'content-type': 'text/plain'})
    # if r.status_code != 200:
    #     print("Ova linija ne valja: %s" % line)


def send_json_log(json_log):
    sec_channel.send_message(json.dumps(json_log).encode('utf-8'))

    # Debug info
    # global line_num
    # line_num +=1
    # lines.add(json_log['line'])
    #
    # if line_num >= 50:
    #     print("Line number: %d and set size: %d" % (line_num, len(lines)))
    # print("Salje se: %s" % json_log)
    # r = requests.post(API_ENDPOINT, data=json.dumps(json_log).encode('utf-8'), headers={'content-type': 'application/json'},
    #                   cert=('certs/agent.vlada.crt', 'certs/agent.vlada.key'), verify='certs/myCA.pem')
    # if r.status_code != 201:
    #     print(r)
    #     print("Ova linija ne valja: %s" % json_log)
    # pass