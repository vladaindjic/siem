import re
from time import sleep
from threading import Thread
import http_communication
import yaml
import sys
import os
import udp_communication


class Agent(object):
    def __init__(self, file_path, patterns, interval=1):
        self.file_path = file_path
        self.patterns = patterns
        self.file = None
        self.interval = interval
        self.thread = Thread(target=self.monitor_log)
        # self.file_position = 0

    def __del__(self):
        if self.file is not None:
            print("Closing file")
            self.file.close()

    def check_and_send(self, line):
        line = line.strip()
        # da li ima poklapanja sa nekim regularnim izrazom
        if any([re.match(pattern, line) for pattern in self.patterns]):
            print("Sending line to server: %s" % line)
            http_communication.send_log_line(line)
            # udp_communication.send_log_line(line)

    def run(self):
        self.thread.start()

    def monitor_log(self):
        if not os.path.exists(self.file_path):
            raise FileExistsError("File: {} not exist: ".format(self.file_path))
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


def read_configuration(config_path):
    with open(config_path, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def run_agents(file_agents):
    for file, agent in file_agents.items():
        print("Run the agent for log file: %s" % agent.file_path)
        agent.run()


def main():
    from collections import defaultdict
    configuration = read_configuration('config.yaml')
    general_conf = configuration['general'] if 'general' in configuration else {}
    patterns = general_conf['patterns'] if 'patterns' in general_conf else []
    interval = general_conf['interval'] if 'interval' in general_conf else []
    specific_conf = configuration['specific']
    # prolazimo kroz sve direktorijume
    for directory in specific_conf['directories']:
        directory = directory['directory']
        dir_path = directory['path']
        dir_patterns = directory['patterns'] if 'patterns' in directory else []
        dir_patterns.extend(patterns)
        dir_interval = directory['interval'] if 'interval' in directory else interval
        dir_only_specified_files = directory['only_specified_files'] if 'only_specified_files' in directory else False

        # recnik koji sadrzi parove (putanja_do_fajla, agent_koji_fajl_obradjuje
        file_agents = {}
        # ako nije naznaceno da se citaju samo specificirani fajlovi
        if not dir_only_specified_files:
            # prolazak kroz sve fajlove direktorijuma i pravljenje agenta za svaki od fajlova
            for file_path in os.listdir(dir_path):
                # FIXME: za svaki slucaj pravimo novu listu, a mogli smo samo dir_patterns da prosledimo
                file_agents[file_path] = Agent(os.path.join(dir_path, file_path), [].extend(dir_patterns), dir_interval)

        # prolazak kroz sve eksplicitno specificirane fajlove
        for file in directory['files']:
            file = file['file']
            file_path = file['path']
            file_patterns = file['patterns'] if 'patterns' in file else []
            file_patterns.extend(dir_patterns)
            file_interval = file['interval'] if 'interval' in file else dir_interval

            if file_path in file_agents:
                agent = file_agents[file_path]
                agent.file_path = os.path.join(dir_path, file_path)
                agent.patterns = file_patterns
                agent.interval = file_interval
            else:
                agent = Agent(os.path.join(dir_path, file_path), file_patterns, file_interval)
                file_agents[file_path] = agent

        run_agents(file_agents)


if __name__ == '__main__':
    # reg_list = [
    #     r'^a',
    #     r'.*b$',
    #     r'.*c.*'
    #
    # ]
    # a = Agent('log.txt', reg_list, interval=2)
    # a.do_something()
    main()