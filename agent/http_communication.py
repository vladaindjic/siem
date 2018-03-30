import requests


API_ENDPOINT = "http://localhost:8080/logger"


def send_log_line(line):
    # data = line
    r = requests.post(API_ENDPOINT, data=line, headers={'content-type': 'text/plain'})
    print(r)