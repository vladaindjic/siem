import os
import re
from threading import Thread
from time import sleep

import http_communication
import timestamp_formatters
from parse_log import SyslogRFC5424Parser, LinuxStandardSyslogParser


class Agent(object):
    # cp855
    def __init__(self, file_path, patterns, interval=1, read_all=True, encoding='cp855',
                 log_parser=SyslogRFC5424Parser("")):
        self.file_path = file_path
        self.patterns = patterns
        self.file = None
        self.interval = interval
        self.read_all = read_all
        self.encoding = encoding

        self.thread = Thread(target=self.monitor_log)
        self.new_line_pattern = timestamp_formatters.get_new_line_patterns(self.file_path)

        self.current_line = ""
        self.line_num = 0
        self.syslog_parser = log_parser
        print("File path: %s and parser: %s" % (self.file_path, type(self.syslog_parser)))

    def __del__(self):
        if self.file is not None:
            print("Closing file")
            self.file.close()

    def get_new_line(self):
        """
            Returns next line
        :return:
        """
        return self.file.readline()

    def send_line(self, line):
        if line.strip() == "":
            return

        # da li ima poklapanja sa nekim regularnim izrazom
        if self.read_all or any([re.match(pattern, line) for pattern in self.patterns]):
            self.syslog_parser.set_line(line)
            self.syslog_parser.parse()
            http_communication.send_json_log(self.syslog_parser.to_json())
            # udp_communication.send_log_line(line)
            # print("Sending: %s" % line)
            self.line_num += 1

    def check_and_send(self, line):
        # da li je nova linija loga
        if timestamp_formatters.is_new_log_line(line, self.new_line_pattern):
            # ako trenutna linija nije prazna, saljemo je
            if self.current_line != "" and self.current_line != line:
                self.send_line(self.current_line)
            # postavljamo novu trenutnu liniju
            self.current_line = line
        # ako nije nova linija loga
        else:
            # dodajemo je na trenutnu
            self.current_line += line
        # da li smo stigli do kraja file-a
        new_read = self.get_new_line()
        if not new_read:
            if self.current_line != "":
                self.send_line(self.current_line)
        return new_read

    def run(self):
        print("Pratimo log: %s putem klase: %s" % (self.file_path, self.__class__.__name__))
        self.thread.start()

    def monitor_log(self):
        if not os.path.exists(self.file_path):
            raise FileExistsError("File: {} not exist: ".format(self.file_path))
        self.file = open(self.file_path, 'r', encoding=self.encoding)
        # pozicioniramo se na kraj fajla
        self.file.readlines()
        while True:
            line = self.file.readline()
            while line:
                line = self.check_and_send(line)
            # kada ih nema, sacekaj odredjeni interval
            sleep(self.interval)
            self.current_line = ""
