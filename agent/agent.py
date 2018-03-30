import re
from time import sleep
from http_communication import send_log_line


class Agent(object):
    def __init__(self, file_path, patterns, interval=1):
        self.file_path = file_path
        self.patterns = patterns
        self.file = None
        self.interval = interval
        # self.file_position = 0

    def __del__(self):
        if self.file is not None:
            self.file.close()

    def check_and_send(self, line):
        # da li ima poklapanja sa nekim regularnim izrazom
        if any([re.match(pattern, line) for pattern in self.patterns]):
            print("Sending line to server: %s" % line)
            send_log_line(line)

    def do_something(self):
        self.file = open(self.file_path, 'r')
        while True:
            # ucitaj liniju
            line = self.file.readline()
            # dokle god ih ima iscitavaj linije
            while line:
                self.check_and_send(line)
                line = self.file.readline()
            # kada ih nema, sacekaj odredjeni interval
            sleep(self.interval)


if __name__ == '__main__':
    reg_list = [
        r'^a',
        r'.*b$',
        r'.*c.*'

    ]
    a = Agent('log.txt', reg_list, interval=2)
    a.do_something()



