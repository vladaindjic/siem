# from concurrent.futures import ThreadPoolExecutor
# import threading
# import random
#
# def task():
#     print("Executing our Task")
#     result = 0
#     i = 0
#     for i in range(10):
#         result = result + i
#     print("I: {}".format(result))
#     print("Task Executed {}".format(threading.current_thread()))
#     return "Kurac"
#
# def main():
#     executor = ThreadPoolExecutor(max_workers=3)
#     task1 = executor.submit(task)
#     task2 = executor.submit(task)
#     print(task1.result())
#
#
# if __name__ == '__main__':
#     main()



# import socket programming library
import socket
# import thread module
import ssl
from concurrent.futures import ThreadPoolExecutor
from .log_service import LogService
from .alarm_engine import AlarmEngine

MAX_MESSAGE_SIZE = 4096
MAX_THREAD_IN_POOL = 10


class LogServer(object):
    def __init__(self,  host="", port=55555):
        self.host = host
        self.port = port
        self.accept_logs_executor = ThreadPoolExecutor(MAX_THREAD_IN_POOL)
        self.alarm_engine = AlarmEngine.get_instance()
        self.log_service = LogService.get_instance()

        self.add_alarm('severity=2')
        self.add_alarm('severity=3')

    def accept_logs(self, c):
        while True:
            log_bytes = c.recv(MAX_MESSAGE_SIZE)
            if len(log_bytes) <= 0:
                break
            log_str = log_bytes.decode('utf-8')
            self.log_service.add_log(log_str)

        c.close()

    def start_server(self):
        # reverse a port on your computer
        # in our case it is 12345 but it
        # can be anything
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s = ssl.wrap_socket(s, keyfile="certs/sysqo2.key", certfile="certs/sysqo.crt",
                            server_side=True, cert_reqs=ssl.CERT_REQUIRED, ca_certs="certs/ca.crt",
                            ssl_version=ssl.PROTOCOL_TLSv1_2)
        s.bind((self.host, self.port))
        print("socket binded to post", self.port)

        # put the socket into listening mode
        s.listen(5)
        print("socket is listening")

        # a forever loop until client wants to exit
        while True:
            print("Samo jednom")
            # establish connection with client
            c, addr = s.accept()

            # lock acquired by client
            print('Connected to :', addr[0], ':', addr[1])

            # Start a new thread and return its identifier
            # start_new_thread(radis_li, (c,))
            self.accept_logs_executor.submit(self.accept_logs, c)
        s.close()

    def add_alarm(self, alarm_str):
        return self.alarm_engine.add_alarm(alarm_str)


def main():
    ls = LogServer()
    ls.start_server()


if __name__ == '__main__':
    main()

