import re
from timestamp_formatters import RFC3164_TIMESTAMP, RFC3339_TIMESTAMP
import json
from rfc3339 import rfc3339
import datetime
import time
import socket
from dateutil import parser


class SyslogParser(object):
    # FIXME: izgleda da postoji jos jedan fazon da se oznaci casovna zova za RFC339
    timestamp_formats = r"((%s)|(%s))" % (RFC3164_TIMESTAMP, RFC3339_TIMESTAMP)
    '''
    
        SYSLOG-MSG      = HEADER SP STRUCTURED-DATA [SP MSG]

        HEADER          = PRI VERSION SP TIMESTAMP SP HOSTNAME
                            SP APP-NAME SP PROCID SP MSGID
        PRI             = "<" PRIVAL ">"
        PRIVAL          = 1*3DIGIT ; range 0 .. 191
        VERSION         = NONZERO-DIGIT 0*2DIGIT
        HOSTNAME        = NILVALUE / 1*255PRINTUSASCII
    
        APP-NAME        = NILVALUE / 1*48PRINTUSASCII
        PROCID          = NILVALUE / 1*128PRINTUSASCII
        MSGID           = NILVALUE / 1*32PRINTUSASCII
    
        TIMESTAMP       = NILVALUE / FULL-DATE "T" FULL-TIME
        FULL-DATE       = DATE-FULLYEAR "-" DATE-MONTH "-" DATE-MDAY
        DATE-FULLYEAR   = 4DIGIT
        DATE-MONTH      = 2DIGIT  ; 01-12
        DATE-MDAY       = 2DIGIT  ; 01-28, 01-29, 01-30, 01-31 based on
                                    ; month/year
        FULL-TIME       = PARTIAL-TIME TIME-OFFSET
        PARTIAL-TIME    = TIME-HOUR ":" TIME-MINUTE ":" TIME-SECOND
                            [TIME-SECFRAC]
        TIME-HOUR       = 2DIGIT  ; 00-23
        TIME-MINUTE     = 2DIGIT  ; 00-59
        TIME-SECOND     = 2DIGIT  ; 00-59
        TIME-SECFRAC    = "." 1*6DIGIT
        TIME-OFFSET     = "Z" / TIME-NUMOFFSET
        TIME-NUMOFFSET  = ("+" / "-") TIME-HOUR ":" TIME-MINUTE
    
    
        STRUCTURED-DATA = NILVALUE / 1*SD-ELEMENT
        SD-ELEMENT      = "[" SD-ID *(SP SD-PARAM) "]"
        SD-PARAM        = PARAM-NAME "=" %d34 PARAM-VALUE %d34
        SD-ID           = SD-NAME
        PARAM-NAME      = SD-NAME
        PARAM-VALUE     = UTF-8-STRING ; characters '"', '\' and
                                         ; ']' MUST be escaped.
        SD-NAME         = 1*32PRINTUSASCII
                            ; except '=', SP, ']', %d34 (")
    
        MSG             = MSG-ANY / MSG-UTF8
        MSG-ANY         = *OCTET ; not starting with BOM
        MSG-UTF8        = BOM UTF-8-STRING
        BOM             = %xEF.BB.BF
           
        UTF-8-STRING    = *OCTET ; UTF-8 string as specified
                            ; in RFC 3629
    
        OCTET           = %d00-255
        SP              = %d32
        PRINTUSASCII    = %d33-126
        NONZERO-DIGIT   = %d49-57
        DIGIT           = %d48 / NONZERO-DIGIT
        NILVALUE        = "-"
        
    
        ------------------------------HEADER
        Ovoga nema nigde
        PRI = <PRIVAL> = <0-192> Prriority value = facility * 20 + severity
        VERSION - Verzija syslog protokola koja se koristi
        
        Ovo ima, ali ne sve
        TIMESTAMP - trebalo bi da se koristi RFC standard
        HOST - pise u nekim Fully Qualified Domain Name
        APP-NAME - aplikacija koja salje log
        PROCID - id procesa
        MSGID - id poruke
        
        ----------------------------- Structured Data
        SD-ELEMENT = [SD-ID (PARAM_NAME="PARAM_VALUE")+]*
        
        
        znak - moze da se koristi za odsustvo necega u poruci (nillvalue)
        
        
        
        --------------------------------- MSG
        Poruka moze biti bilo sta
        ako pocinje sa BOM, onda se odnosi na UTF-8 encodovanje
        
        
    '''
    def __init__(self, full_line):
        self.line = re.sub(r"\s+", " ", full_line.strip())
        self.timestamp = None
        self.facility_code = None
        self.severity_code = None
        self.syslog_version = None
        self.rest_line = self.line
        self.hostname = None
        self.app_name = None
        self.process_id = None
        self.process_id_str = None
        self.message_id = None
        self.message = None
        self.linux_system_time = None
        self.severity_symbol = None

    def set_line(self, full_line):
        self.line = re.sub(r"\s+", " ", full_line.strip())
        self.rest_line = self.line

    def parse(self):
        self.parse_header()

    def find_timestamp(self):
        m = re.search(SyslogParser.timestamp_formats, self.line)
        if m:
            self.timestamp = m.group(0)
        else:
            self.timestamp = self.provide_timestamp()
        return self.timestamp

    def provide_timestamp(self):
        timestamp = time.time()
        dt = datetime.datetime.fromtimestamp(timestamp)
        self.timestamp = rfc3339(dt)
        return self.timestamp

    def convert_timestamp(self):
        dt = parser.parse(self.timestamp)
        self.timestamp = rfc3339(dt)
        return self.timestamp

    def provide_hostname(self):
        self.hostname = socket.gethostname()
        return self.hostname

    def parse_header(self):
        self.parse_pri()
        self.parse_syslog_version()
        self.parse_timestamp()
        self.parse_hostname()
        self.parse_app_name()
        self.parse_process_id()

    def cut_beginning(self, length):
        self.rest_line = self.rest_line[length:].strip()
        if self.rest_line.startswith(":"):
            self.rest_line = self.rest_line[1:]

    def add_nil(self, pattern):
        return r"(%s|-)" % pattern

    def is_nil(self, match):
        return match.group(0) == "-" if match else False

    def parse_pri(self):
        # facility and severity
        pri_pattern = self.add_nil(r"<\d{1,3}>")
        m = re.match(pri_pattern, self.rest_line)
        if not m:
            return
        elif self.is_nil(m):
            print("PRIAAAAAAAA NEMA: " + m.group(0))
            self.cut_beginning(len(m.group(0)))
            return
        pri_code = int(re.search(r"\d{1,3}", m.group(0)).group(0))
        self.facility_code = pri_code // 8
        self.severity_code = pri_code % 8
        print("Facility code: %d\nSeverity code:%d" % (self.facility_code, self.severity_code))
        self.cut_beginning(len(m.group(0)))

    def parse_syslog_version(self):
        syslog_version_pattern = self.add_nil(r"\d+")
        m = re.match(syslog_version_pattern, self.rest_line)
        if not m:
            return
        elif self.is_nil(m):
            print("SYSLOG VERSION NEMA: " + m.group(0))
            self.cut_beginning(len(m.group(0)))
            return
        self.syslog_version = int(m.group(0))
        self.cut_beginning(len(m.group(0)))
        print("Syslog version: %d" % self.syslog_version)

    def parse_timestamp(self):
        m = re.match(self.add_nil(SyslogParser.timestamp_formats), self.rest_line)
        if not m or self.is_nil(m):
            # TODO: provide the date
            self.provide_timestamp()
            # da secnemo -
            if self.is_nil(m):
                self.cut_beginning(len(m.group(0)))
            return
        self.timestamp = m.group(0)
        self.cut_beginning(len(m.group(0)))
        self.convert_timestamp()
        print("Time stamp: %s" % self.timestamp)

    def parse_hostname(self):
        m = re.match(self.add_nil(r"[!-~]+"), self.rest_line)
        if not m or self.is_nil(m):
            # TODO: provide hostmachine
            self.provide_hostname()
            if self.is_nil(m):
                self.cut_beginning(len(m.group(0)))
                return
            raise Exception("Format error, no hostname %s &&& and %s" % (self.line, self.rest_line))
        self.hostname = m.group(0)
        print("Hostname: %s" % self.hostname)
        self.cut_beginning(len(self.hostname))

    def parse_app_name(self):
        m = re.match(self.add_nil(r"[!-~]+"), self.rest_line)
        if not m:
            raise Exception("Format error, no process id")
        elif self.is_nil(m):
            self.cut_beginning(len(m.group(0)))
            return
        self.app_name = m.group(0)
        self.cut_beginning(len(self.app_name))
        print("Application name: %s" % self.app_name)

    def parse_message(self):
        self.message = self.rest_line[:]
        self.cut_beginning(len(self.message))
        print("Message: %s" % self.message)

    def parse_process_id(self):
        pass

    def to_json(self):
        from build_and_crypt import build_json_dto
        return build_json_dto(self)


class SyslogRFC5424Parser(SyslogParser):
    def __init__(self, full_line):
        super().__init__(full_line)
        self.sd_elements = []

    def parse(self):
        super().parse()
        self.parse_sd_elements()
        self.parse_message()

    def parse_header(self):
        super().parse_header()
        self.parse_message_id()

    def parse_process_id(self):
        m = re.match(self.add_nil(r"[!-~]+"), self.rest_line)
        if not m:
            raise Exception("Format error, no process id")
        elif self.is_nil(m):
            self.cut_beginning(len(m.group(0)))
            return
        self.process_id_str = m.group(0)
        print("Process id str: %s" % self.process_id_str)
        self.cut_beginning(len(m.group(0)))
        # da li je integer, trebalo bi da bude
        m = re.search("\d+", self.process_id_str)
        if not m:
            # FIXME is process id always number
            self.process_id = None
            return
        self.process_id = int(m.group(0))
        print("Process id: %d" % self.process_id)

    def parse_message_id(self):
        m = re.match(self.add_nil(r"[!-~]+"), self.rest_line)
        if not m:
            raise Exception("Format error, no message id")
        elif self.is_nil(m):
            self.cut_beginning(len(m.group(0)))
            return
        self.message_id = m.group(0)
        self.cut_beginning(len(self.message_id))
        print("Message id: %s" % self.message_id)

    def parse_sd_elements(self):
        while True:
            m = re.match(self.add_nil("\[[^\[\]]+\]"), self.rest_line)
            if not m:
                break
            elif self.is_nil(m):
                self.cut_beginning(len(m.group(0)))
                break
            self.sd_elements.append(m.group(0))
            self.cut_beginning(len(m.group(0)))
        print("SD Elements: %s" % self.sd_elements)


class LinuxStandardSyslogParser(SyslogParser):
    def __init__(self, full_line):
        super().__init__(full_line)

    def parse(self):
        super().parse()
        self.parse_severity()
        self.parse_system_time()
        self.parse_message()

    def parse_app_name(self):
        super().parse_app_name()
        m = re.match("[^\[\]:]+", self.app_name)
        self.process_id_str = self.app_name[m.end():]
        self.app_name = self.app_name[:m.end()]
        print("App-name: %s" % self.app_name)

    def parse_process_id(self):
        m = re.search("\d+", self.process_id_str)
        if not m:
            self.process_id_str = None
            self.process_id = None
            return
        self.process_id_str = m.group(0)
        self.process_id = int(self.process_id_str)
        print("Process id str: %s" % self.process_id_str)
        print("Process id: %d" % self.process_id)

    def parse_severity(self):
        m = re.match("<[^<>]+>", self.rest_line)
        if not m:
            return
        self.severity_symbol = m.group(0)[1:-1]
        self.cut_beginning(len(m.group(0)))
        print("Severity symbol: %s" % self.severity_symbol)

    def parse_system_time(self):
        m = re.match("\[\s*\d+\.\d+\s*\]", self.rest_line)
        if not m:
            return
        self.linux_system_time = m.group(0)[1:-1].strip()
        self.cut_beginning(len(m.group(0)))
        print("Linux system time: %s" % self.linux_system_time)


class UWBTmpParser(SyslogParser):
    def __init__(self, full_line, type="wtmp"):
        super().__init__(full_line)
        self.type = type

    def parse(self):
        self.find_timestamp()
        self.hostname = self.provide_hostname()
        self.message = "%s: %s" % (self.type, self.line)


class FaillogParser(SyslogParser):
    def __init__(self, full_line):
        super().__init__(full_line)

    def parse(self):
        # ima 5 kolona, u 4 se nalazi timestamp
        temp = re.sub('\s+', ' ', self.line)
        temp = temp.split(' ')
        # TODO: sredit eventualno format
        self.timestamp = " ".join(temp[3:6])
        self.hostname = self.provide_hostname()
        self.message = 'faillog: %s' % self.line


class LastlogParser(SyslogParser):
    def __init__(self, full_line):
        super().__init__(full_line)

    def parse(self):
        # ima 5 kolona, u 4 se nalazi timestamp
        if 'NEVER' in self.line.upper():
            self.timestamp = self.provide_timestamp()
        else:
            temp = re.sub('\s+', ' ', self.line)
            temp = temp.split(' ')
            # TODO: ako mozes na neki nacin sa latinice u cirilicu da promenis i onda promenis format
            self.timestamp = " ".join(temp[3:])
        self.hostname = self.provide_hostname()
        self.message = 'lastlog: %s' % self.line


class DummyParser(SyslogParser):
    def __init__(self, full_line):
        super().__init__(full_line)

    def parse(self):
        self.find_timestamp()
        self.hostname = self.provide_hostname()
        self.message = self.line

# TODO: resi sa Tallylog, ali prvo skontaj kako izgleda

def main():
    line1 = "Apr 19 00:47:57 vi3-Inspiron-5737 dbus[846]: [system] Activating via systemd: service name='org.freedesktop.PolicyKit1' unit='polkitd.service'"
    line2 = """
        <165>1 2003-10-11T22:14:15.003Z mymachine.example.com
           evntslog - ID47 [exampleSDID@32473 iut="3" eventSource=
           "Application" eventID="1011"][examplePriority@32473
           class="high"]
    """
    line3 = """
    <165>1 2003-08-24T05:14:15.000003-07:00 192.0.2.1
         myproc 8710 - - %% It's time to make the do-nuts.
    """
    line4 = "Apr 20 22:14:12 vi3-Inspiron-5737 NetworkManager[898]: <info>  [1524255252.7989] dhcp4 (wlp2s0): state changed bound -> bound"
    line5 = "Apr 20 13:31:16 vi3-Inspiron-5737 anacron[7918]: Job `cron.daily' terminated"
    logic = SyslogRFC5424Parser(line3)
    logic.parse()
    print("\n")
    lin_log = LinuxStandardSyslogParser(line5)
    lin_log.parse()
    print(lin_log.to_json())
    print(lin_log.provide_timestamp())
    print(lin_log.provide_hostname())

    print("GLEDAJ MEEEEEEEEEEE\n\n\n")
    line10 = """
        <165>1 2003-08-24T05:14:15.000003-07:00 192.0.2.1
         myproc 8710 MSG123 - %% It's time to make the do-nuts.
    """

    log = SyslogRFC5424Parser(line10)
    log.parse()
    print(log.to_json())

    print("A SADA MENE\n\n\n")
    line11 = """
        -- - -
         - - - - %% It's time to make the do-nuts.
    """
    log = SyslogRFC5424Parser(line11)
    log.parse()
    print(log.to_json())


if __name__ == '__main__':
    main()
    # TODO: add date if missing
    # TODO: add hostname if missing
