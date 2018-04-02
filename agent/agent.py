import re
from time import sleep
from threading import Thread
import http_communication
import yaml
import sys
import os
import udp_communication
import platform
import tarfile
import zipfile
import mimetypes
from binaryornot.check import is_binary
import subprocess
import timestamp_formatters


class Agent(object):
    # cp855
    def __init__(self, file_path, patterns, interval=1, read_all=True, encoding='cp855'):
        self.file_path = file_path
        self.patterns = patterns
        self.file = None
        self.interval = interval
        self.read_all = read_all
        self.encoding = encoding

        self.thread = Thread(target=self.monitor_log)
        self.new_line_pattern = timestamp_formatters.get_new_line_patterns(self.file_path)
        print("File path: %s\t New line pattern: %s" % (self.file_path, self.new_line_pattern))

        self.current_line = ""

        self.line_num = 0
        # self.file_position = 0

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

        # cpy_line = "%s" % line
        #
        # cpy_line = cpy_line.replace('\s+', ' ')

        # print(line)
        # da li ima poklapanja sa nekim regularnim izrazom
        if self.read_all or any([re.match(pattern, line) for pattern in self.patterns]):
            http_communication.send_log_line(line)
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
            print("KRAJ")
        return new_read

    def run(self):
        self.thread.start()

    def monitor_log(self):
        if not os.path.exists(self.file_path):
            raise FileExistsError("File: {} not exist: ".format(self.file_path))
        self.file = open(self.file_path, 'r', encoding=self.encoding)
        while True:
            # ucitaj liniju
            # line = self.check_and_send(self.current_line)
            # dokle god ih ima iscitavaj linije
            line = self.file.readline()
            while line:
                # try:
                    line = self.check_and_send(line)
                    # line = self.file.readline()
                # except Exception as e:
                #     print("Greska u fileu: %s\t%s\t%s" % (self.file_path, line, str(e)))
                #     self.file.close()
                #     return
            # kada ih nema, sacekaj odredjeni interval
            sleep(self.interval)
            self.current_line = ""
            # print(self.line_num)
            # print(len(self.current_line.encode(self.encoding)))


class LinuxBinaryAgent(Agent):
    def __init__(self, agent):
        super().__init__(agent.file_path, agent.patterns, agent.interval, agent.read_all, agent.encoding)
        self.current_line = -1  # nista nije procitano
        self.cmd = ""
        self.footer_lines_num = 0  # kod poziva last programa poslednje dve linije ne nose informaciju
        self.header_lines_num = 0  # kod poziva lastlog, prva linija nije bitna

    def next_line(self, table):
        """
            Postavlja liniju koju treba procitati.

        :param table:
        :return: 1 ako je uspesno procitana linija, 0 ako nema nista novo da se procita
        """
        lines = table.strip().split('\n')
        # nema nista da se cita
        if len(lines) <= self.header_lines_num:
            self.current_line = -1
            return False

        if self.current_line == -1:
            if len(lines) >= self.footer_lines_num:
                self.current_line = lines[self.header_lines_num]
                return True
            # nema nista da se cita
            return False

        # treba naci poslednje procitanu liniju
        current_line_index = -1
        for i, l in enumerate(lines):
            if l == self.current_line:
                current_line_index = i
                break

        # ako nije pronadjeno nista, prva linija se vraca
        if current_line_index == -1:
            self.current_line = lines[self.header_lines_num]
            return True
        # poslednja dva reda su prazna kod UTMP, dok kod lastloga nije tako,
        # tako da ako zelimo novu liniju da gledamo, onda trenutna linija
        # mora biti na indeksu manjem od len(lines) - footer_lines_num - 1
        elif current_line_index < len(lines) - self.footer_lines_num - 1:
            self.current_line = lines[current_line_index+1]
            return True

        return False

    # check and send
    def check_and_send(self, line):
        line = line.strip()
        if line == "":
            return
        # print(line)
        # da li ima poklapanja sa nekim regularnim izrazom
        if self.read_all or any([re.match(pattern, line) for pattern in self.patterns]):
            http_communication.send_log_line(line)
            # udp_communication.send_log_line(line)

    def monitor_log(self):
        while True:
            table = self.call_bash()
            while self.next_line(table):
                self.check_and_send(self.current_line)
            sleep(self.interval)

    def call_bash(self):
        process = subprocess.Popen(self.cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        process.kill()
        return output.decode('utf-8')


class UWBTmpAgent(LinuxBinaryAgent):
    def __init__(self, agent):
        super().__init__(agent)
        self.cmd = "last -F -f {}".format(self.file_path)
        self.footer_lines_num = 2
        self.header_lines_num = 0


class LastlogAgent(LinuxBinaryAgent):
    def __init__(self, agent):
        super().__init__(agent)
        self.cmd = "lastlog".format(self.file_path)
        self.footer_lines_num = 0
        self.header_lines_num = 1


class FailLogAgent(LinuxBinaryAgent):
    def __init__(self, agent):
        super().__init__(agent)
        self.cmd = "faillog -a"
        self.footer_lines_num = 0
        self.header_lines_num = 2


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


def is_file_linux(file_path):
    # FIXME: resi sta ces kada nemas prava pristupa
    if not os.access(file_path, os.R_OK):
        print("Permission denied: %s" % file_path)
        return False
        # os.chmod(file_path, 0o644)

    # FIXME: vidi sta ces za lastlog i faillog

    # FIXME: vidi za utmp, wtmp, btmp
    if 'btmp' in file_path:
        print("********************************" + file_path)
    # provera da li je direktorijum
    if os.path.isdir(file_path):
        print("Ovo je direktorijum" + file_path)
        return False
    elif tarfile.is_tarfile(file_path) and ('lastlog' not in file_path) and ('btmp' not in file_path) and ('faillog' not in file_path):
        print('STA JE SVE TARFILE: %s' % file_path)
        # print("Ovo je Tar file")
        return False
    elif zipfile.is_zipfile(file_path) and ('btmp' not in file_path):
        print('STA JE SVE ZIPFILE: %s' % file_path)
        # print("Ovo je zip file")
        return False
    elif mimetypes.guess_type(file_path)[1] == 'gzip' and ('btmp' not in file_path):
        print('STA JE SVE GZIPFILE: %s' % file_path)
        # print("Gzip file")
        return False

    return True
    # provera da li je neki kompresovan file
    # da li je binaran file


def run_linux_agents(file_agents):
    print(file_agents)
    for file_path, lin_agent in file_agents.items():
        if is_file_linux(file_path):
            # u pitanju je tekstualni parser
            if not is_binary(file_path) and 'btmp' not in file_path:
                lin_agent.run()
            else:
                print("Binaran fajl: %s" % file_path)
                # da li je za lastlog
                if 'lastlog' in file_path:
                    LastlogAgent(lin_agent).run()
                elif 'faillog' in file_path:
                    FailLogAgent(lin_agent).run()
                else:
                    UWBTmpAgent(lin_agent).run()
                # print("Ovo je tekstualni file: %s" % file_path)
                # pass
            # print("File: %s\t type: %s" % (file_path, str(is_binary(file_path))))


def get_value_or_default_from_dict(dictionary, key, default_value):
    return dictionary[key] if key in dictionary else default_value


def read_linux_configuration(linux_conf, patterns, interval, read_all, only_specified_files):
    print("Reading linux configuration")
    linux_conf = linux_conf['linux']
    linux_interval = get_value_or_default_from_dict(linux_conf, 'interval', interval)
    linux_patterns = get_value_or_default_from_dict(linux_conf, 'patterns', patterns)
    linux_read_all = get_value_or_default_from_dict(linux_conf, 'read_all', read_all)
    linux_only_specified_files = get_value_or_default_from_dict(linux_conf, 'only_specified_files', only_specified_files)
    if 'directories' not in linux_conf or linux_conf['directories'] is None:
        return

    for directory in linux_conf['directories']:
        directory = directory['directory']
        # FIXME: currently support only this folder
        dir_path = directory['path']
        dir_interval = get_value_or_default_from_dict(directory, 'interval', linux_interval)
        dir_patterns = get_value_or_default_from_dict(directory, 'patterns', linux_patterns)
        dir_only_specified_files = get_value_or_default_from_dict(directory, 'only_specified_files',
                                                                  linux_only_specified_files)
        dir_read_all = get_value_or_default_from_dict(directory, 'read_all', linux_read_all)

        file_agents = {}

        if not dir_only_specified_files:
            # prolazak kroz sve fajlove direktorijuma i pravljenje agenta za svaki od fajlova
            for file_path in os.listdir(dir_path):
                full_path = os.path.join(dir_path, file_path)
                # FIXME: za svaki slucaj pravimo novu listu, a mogli smo samo dir_patterns da prosledimo
                file_agents[full_path] = Agent(os.path.join(dir_path, file_path), [].extend(dir_patterns), dir_interval,
                                               dir_read_all)

        if 'files' in directory and directory['files'] is not None:
            # prolazak kroz sve eksplicitno specificirane fajlove
            for file in directory['files']:
                file = file['file']
                file_path = file['path']

                full_path = os.path.join(dir_path, file_path)

                # file_patterns = file['patterns'] if 'patterns' in file else []
                file_patterns = get_value_or_default_from_dict(file, 'patterns', [])
                file_patterns.extend(dir_patterns)
                # file_interval = file['interval'] if 'interval' in file else dir_interval
                file_interval = get_value_or_default_from_dict(file, 'interval', dir_interval)
                # file_read_all = file['read_all'] if 'read_all' in file else dir_read_all
                file_read_all = get_value_or_default_from_dict(file, 'read_all', dir_read_all)

                if full_path in file_agents:
                    agent = file_agents[full_path]
                    agent.file_path = os.path.join(dir_path, file_path)
                    agent.patterns = file_patterns
                    agent.interval = file_interval
                    agent.read_all = file_read_all
                else:
                    agent = Agent(os.path.join(dir_path, file_path), file_patterns, file_interval, file_read_all)
                    file_agents[full_path] = agent

        run_linux_agents(file_agents)

    print(linux_conf)


def read_windows_configuration(windows_conf, patterns, interval, read_all, only_specified_files):
    print("Reading windows configuration configuration")


def read_os_configuration(configuration, patterns, interval, read_all, only_specified_files):
    os_conf = configuration['os'] if 'os' in configuration else {}
    platform_type = platform.platform().upper()
    if 'LINUX' in platform_type:
        read_linux_configuration(os_conf, patterns, interval, read_all, only_specified_files)
    elif 'WINDOWS' in platform_type:
        read_windows_configuration(os_conf, patterns, interval, read_all, only_specified_files)
    else:
        raise Exception("Unssuported platform (os): %s" % platform_type)


def read_specific_configuration(specific_conf, patterns, interval, read_all, only_specified_files):
    if 'directories' not in specific_conf or specific_conf['directories'] is None:
        return
    for directory in specific_conf['directories']:
        directory = directory['directory']
        dir_path = directory['path']
        # dir_patterns = directory['patterns'] if 'patterns' in directory else []
        dir_patterns = get_value_or_default_from_dict(directory, 'patterns', [])
        dir_patterns.extend(patterns)
        # dir_interval = directory['interval'] if 'interval' in directory else interval
        dir_interval = get_value_or_default_from_dict(directory, 'interval', interval)
        # dir_only_specified_files = directory['only_specified_files'] if 'only_specified_files' in directory else False
        dir_only_specified_files = get_value_or_default_from_dict(directory, 'only_specified_files', only_specified_files)
        # dir_read_all = directory['read_all'] if 'read_all' in directory else read_all
        dir_read_all =get_value_or_default_from_dict(directory, 'read_all', read_all)
        # recnik koji sadrzi parove (putanja_do_fajla, agent_koji_fajl_obradjuje
        file_agents = {}
        # ako nije naznaceno da se citaju samo specificirani fajlovi
        if not dir_only_specified_files:
            # prolazak kroz sve fajlove direktorijuma i pravljenje agenta za svaki od fajlova
            for file_path in os.listdir(dir_path):
                # FIXME: za svaki slucaj pravimo novu listu, a mogli smo samo dir_patterns da prosledimo
                file_agents[file_path] = Agent(os.path.join(dir_path, file_path), [].extend(dir_patterns), dir_interval, dir_read_all)

        # prolazak kroz sve eksplicitno specificirane fajlove
        for file in get_value_or_default_from_dict(directory, 'files', []):
            file = file['file']
            file_path = file['path']
            # file_patterns = file['patterns'] if 'patterns' in file else []
            file_patterns = get_value_or_default_from_dict(file, 'patterns', [])
            file_patterns.extend(dir_patterns)
            # file_interval = file['interval'] if 'interval' in file else dir_interval
            file_interval = get_value_or_default_from_dict(file, 'interval', dir_interval)
            # file_read_all = file['read_all'] if 'read_all' in file else dir_read_all
            file_read_all = get_value_or_default_from_dict(file, 'read_all', dir_read_all)

            if file_path in file_agents:
                agent = file_agents[file_path]
                agent.file_path = os.path.join(dir_path, file_path)
                agent.patterns = file_patterns
                agent.interval = file_interval
                agent.read_all = file_read_all
            else:
                agent = Agent(os.path.join(dir_path, file_path), file_patterns, file_interval, file_read_all)
                file_agents[file_path] = agent

        run_agents(file_agents)


def main():
    configuration = read_configuration('config.yaml')
    # general_conf = configuration['general'] if 'general' in configuration else {}
    general_conf = get_value_or_default_from_dict(configuration, 'general', {})
    # patterns = general_conf['patterns'] if 'patterns' in general_conf else []
    patterns = get_value_or_default_from_dict(general_conf, 'patterns', [])
    # interval = general_conf['interval'] if 'interval' in general_conf else []
    interval = get_value_or_default_from_dict(general_conf, 'interval', [])
    # read_all = general_conf['read_all'] if 'read_all' in general_conf else False
    read_all = get_value_or_default_from_dict(general_conf, 'read_all', False)
    only_specified_files = get_value_or_default_from_dict(general_conf, 'only_specified_files', False)

    specific_conf = configuration['specific']
    # prolazimo kroz sve direktorijume
    read_specific_configuration(specific_conf, patterns, interval, read_all, only_specified_files)
    read_os_configuration(configuration, patterns, interval, read_all, only_specified_files)


if __name__ == '__main__':
    # reg_list = [
    #     r'^a',
    #     r'.*b$',
    #     r'.*c.*'
    #
    # ]
    # a = Agent('log.txt', reg_list, interval=2)
    # a.do_something()
    import sys
    print(sys.getdefaultencoding())
    main()