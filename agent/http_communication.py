import requests


API_ENDPOINT = "http://192.168.0.18:8080/logger"


def send_log_line(line):
    # data = line
    pass
    # r = requests.post(API_ENDPOINT, data=line.encode('utf-8'), headers={'content-type': 'text/plain'})
    # if r.status_code != 200:
    #     print("Ova linija ne valja: %s" % line)


def send_json_log(json_log):
    print(json_log)
    # pass