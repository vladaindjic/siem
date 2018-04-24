from agent import Agent
import http_communication
import re
from time import sleep, time
import subprocess
from parse_log import UWBTmpParser, FaillogParser, LastlogParser
import datetime


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
            self.syslog_parser.set_line(line)
            self.syslog_parser.parse()
            http_communication.send_json_log(self.syslog_parser.to_json())
            # http_communication.send_log_line(line)
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
    def __init__(self, agent, type='wtmp'):
        super().__init__(agent)
        # FIXME: privremeno resenje, trazimo samo odavde da ti prikazuje, s obzirom na to da ga ima malo, nece biti problema
        current_time = time()
        self.start_time = current_time
        print(current_time)

        # YYYY-MM-DD hh: mm:ss
        current_time = datetime.datetime.strftime(datetime.datetime.fromtimestamp(current_time), "%Y%m%d%H%M%S")
        print(current_time)

        self.cmd = "last -f %s --time-format=iso -s %s" % (self.file_path, current_time)
        print(self.cmd)
        self.footer_lines_num = 2
        self.header_lines_num = 0
        self.syslog_parser = UWBTmpParser("", type)


class LastlogAgent(LinuxBinaryAgent):
    def __init__(self, agent):
        super().__init__(agent)
        self.cmd = "lastlog -t +1".format(self.file_path)
        self.footer_lines_num = 0
        self.header_lines_num = 1
        self.syslog_parser = LastlogParser("")


class FailLogAgent(LinuxBinaryAgent):
    def __init__(self, agent):
        super().__init__(agent)
        self.cmd = "faillog -a -t +1"
        self.footer_lines_num = 0
        self.header_lines_num = 2
        self.syslog_parser = FaillogParser("")


class TallyLogAgent(LinuxBinaryAgent):
    def __init__(self, agent):
        super().__init__(agent)
        self.cmd = "sudo pam_tally2"
        self.footer_lines_num = 0
        self.header_lines_num = 0


# TODO: wtmp i btmp imaju neki normalan format (user, terminal, from, timestamp pocetka - timestamp kraja,
        # uzrok, trajanje)
# TODO: faillog (username, failures, maximum, timestamp-latest)
# TODO: lastlog (username, port, from, timestamp-latest)
# TODO: ufw log ima identican format kao standardan linuxov syslog
# TODO: tallylog (broj neuspesne pokusaje, prazan mi je i nemam format)

# TODO: provide hostname if missing to all binary format
# TODO: provide hostname where needed