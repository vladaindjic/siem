import mimetypes
import os
import platform
import tarfile
import zipfile

import yaml
from binaryornot.check import is_binary
from windows_agent import WinAgent
from linux_binary_agent import *
from parse_log import LinuxStandardSyslogParser, SyslogRFC5424Parser, DummyParser

from http_communication import sec_channel

# da oprobamo redirekciju u fajl
# import sys
# sys.stdout = open('probica.txt', 'a')


def initialize_parser(parser_type, file_path=""):
    if parser_type == 'SyslogRFC5424Parser':
        print('SyslogRFC5424Parser')
        return SyslogRFC5424Parser("")
    elif parser_type == 'LinuxStandardSyslogParser':
        print('LinuxStandardSyslogParser')
        return LinuxStandardSyslogParser("")
    else:
        print('DummyParser')
        return DummyParser(full_line="", file_path=file_path)


def read_configuration(config_path):
    with open(config_path, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def run_agents(file_agents):
    for file, agent in file_agents.items():
        agent.run()


def is_file_linux(file_path):
    if not os.access(file_path, os.R_OK):
        print("Permission denied: %s" % file_path)
        return False
        # os.chmod(file_path, 0o644)

    if file_path.endswith('.gz'):
        return False

    # provera da li je direktorijum
    if os.path.isdir(file_path):
        return False
    # kompresovan file
    elif tarfile.is_tarfile(file_path) and ('lastlog' not in file_path) and ('btmp' not in file_path) and \
            ('faillog' not in file_path) and ('tallylog' not in file_path):
        return False
    elif zipfile.is_zipfile(file_path) and ('btmp' not in file_path):
        return False
    elif mimetypes.guess_type(file_path)[1] == 'gzip' and ('btmp' not in file_path):
        return False

    return True


def run_linux_agents(file_agents):
    # print(file_agents)
    for file_path, lin_agent in file_agents.items():
        if is_file_linux(file_path):
            # u pitanju je tekstualni parser
            if not is_binary(file_path) and ('btmp' not in file_path) and ('tallylog' not in file_path)\
                    and ('wtmp' not in file_path) and ('utmp' not in file_path) and ('lastlog' not in file_path):
                lin_agent.run()
            else:
                # da li je za lastlog
                if 'lastlog' in file_path:
                    LastlogAgent(lin_agent).run()
                # faillog
                elif 'faillog' in file_path:
                    FailLogAgent(lin_agent).run()
                # tallylog
                elif 'tallylog' in file_path:
                    TallyLogAgent(lin_agent).run()
                # utmp, wtmp, btmp
                else:
                    type = 'wtmp'
                    if 'utmp' in file_path:
                        type = 'utmp'
                    elif 'btmp' in file_path:
                        type = 'btmp'
                    UWBTmpAgent(lin_agent, type).run()


def get_value_or_default_from_dict(dictionary, key, default_value):
    return dictionary[key] if key in dictionary else default_value


def read_linux_configuration(linux_conf, patterns, interval, read_all, only_specified_files):
    print("Reading linux configuration")
    if not 'linux' in linux_conf:
        return
    linux_conf = linux_conf['linux']
    linux_interval = get_value_or_default_from_dict(linux_conf, 'interval', interval)
    linux_patterns = get_value_or_default_from_dict(linux_conf, 'patterns', patterns)
    linux_read_all = get_value_or_default_from_dict(linux_conf, 'read_all', read_all)
    linux_only_specified_files = get_value_or_default_from_dict(linux_conf, 'only_specified_files', only_specified_files)
    if 'directories' not in linux_conf or linux_conf['directories'] is None:
        return

    for directory in linux_conf['directories']:
        directory = directory['directory']
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
                file_agents[full_path] = Agent(os.path.join(dir_path, file_path), [].extend(dir_patterns), dir_interval,
                                               dir_read_all, log_parser=LinuxStandardSyslogParser(""))

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
                    agent = Agent(os.path.join(dir_path, file_path), file_patterns, file_interval, file_read_all,
                                  log_parser=LinuxStandardSyslogParser(""))
                    file_agents[full_path] = agent

                # eventualna promena parsera
                parser_type = get_value_or_default_from_dict(file, 'parser_type', None)
                if parser_type:
                    print("OVAJ TIP PARSERA ZA LINUX file %s: %s" % (os.path.join(dir_path, file_path), parser_type))
                    agent.syslog_parser = initialize_parser(parser_type, os.path.join(dir_path, file_path))

        run_linux_agents(file_agents)

    # print(linux_conf)


def run_windows_agents(windows_agents):
    for agent in windows_agents:
        print("Windows agent,pratim log: ",agent._name)
        agent.run()


def read_windows_configuration(windows_conf, patterns, interval, read_all, only_specified_files):
    print("Reading windows configuration configuration")
    windows_conf = windows_conf['windows']
    windows_agents = []

    if (windows_conf['logs'] == None):
        raise Exception("Mora postojati bar jedan log koji zelimo da pratimo")

        # prolazimo kroz sve logove koje zelimo da pratimo
    for log_config in windows_conf['logs']:
        # print(log_config)
        patterns = log_config['log']['patterns'] if 'patterns' in log_config['log'] else []
        agent = WinAgent(log_config['log']['name'], log_config['log']['interval'], patterns)
        windows_agents.append(agent)

    run_windows_agents(windows_agents)
    # print(windows_conf)


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
        dir_patterns = get_value_or_default_from_dict(directory, 'patterns', [])
        dir_patterns.extend(patterns)
        dir_interval = get_value_or_default_from_dict(directory, 'interval', interval)
        dir_only_specified_files = get_value_or_default_from_dict(directory, 'only_specified_files', only_specified_files)
        dir_read_all =get_value_or_default_from_dict(directory, 'read_all', read_all)
        # recnik koji sadrzi parove (putanja_do_fajla, agent_koji_fajl_obradjuje
        file_agents = {}
        # ako nije naznaceno da se citaju samo specificirani fajlovi
        if not dir_only_specified_files:
            # prolazak kroz sve fajlove direktorijuma i pravljenje agenta za svaki od fajlova
            for file_path in os.listdir(dir_path):
                file_agents[file_path] = Agent(os.path.join(dir_path, file_path), [].extend(dir_patterns), dir_interval, dir_read_all)

        # prolazak kroz sve eksplicitno specificirane fajlove
        for file in get_value_or_default_from_dict(directory, 'files', []):
            file = file['file']
            file_path = file['path']
            file_patterns = get_value_or_default_from_dict(file, 'patterns', [])
            file_patterns.extend(dir_patterns)
            file_interval = get_value_or_default_from_dict(file, 'interval', dir_interval)
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

            parser_type = get_value_or_default_from_dict(file, 'parser_type', None)
            if parser_type:
                print("OVAJ TIP PARSERA ZA SPECIFIC file %s: %s" % (os.path.join(dir_path, file_path), parser_type))
                agent.syslog_parser = initialize_parser(parser_type, os.path.join(dir_path, file_path))

        run_agents(file_agents)


def read_security_config(sec_config):
    key_path = sec_config['key']
    cert_path = sec_config['cert']
    ca_path = sec_config['ca']
    API_ENDPOINT = sec_config['API_ENDPOINT']
    HOST = sec_config['HOST']
    PORT = sec_config['PORT']
    communication_protocol = sec_config['communication_protocol']
    interval = sec_config['interval']
    # inicijalizacija komunikacija i pokretanje niti
    sec_channel.initialize_communication(key_path, cert_path, ca_path, API_ENDPOINT, interval, HOST, PORT, communication_protocol)


def main():
    configuration = read_configuration('config.yaml')
    # provo citamo security configuration
    read_security_config(configuration['security'])
    general_conf = get_value_or_default_from_dict(configuration, 'general', {})
    patterns = get_value_or_default_from_dict(general_conf, 'patterns', [])
    interval = get_value_or_default_from_dict(general_conf, 'interval', [])
    read_all = get_value_or_default_from_dict(general_conf, 'read_all', False)
    only_specified_files = get_value_or_default_from_dict(general_conf, 'only_specified_files', False)

    specific_conf = configuration['specific']
    # prolazimo kroz sve direktorijume
    read_specific_configuration(specific_conf, patterns, interval, read_all, only_specified_files)
    read_os_configuration(configuration, patterns, interval, read_all, only_specified_files)


if __name__ == '__main__':
    main()