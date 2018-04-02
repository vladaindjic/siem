import subprocess, sys
import re
from threading import Thread
import time
import datetime
import yaml
import platform
from event import Event
# from udp_communication import send_log_line
from http_communication import send_log_line


class WinAgent(object):

    def __init__(self,name,interval,patterns):
        self._name = name
        self._interval = interval
        self._date = ""
        self._patterns = patterns
        self._thread = Thread(target=self.monitor_log)

    def run(self):
        self._thread.start()

    def monitor_log(self):
        self._date = get_date()
        while True:
            # print("##############################################################")
            p = subprocess.Popen(["powershell.exe","./getEvents.ps1","-logFile",self._name,"-datum",self._date],
                      stdout=subprocess.PIPE) #PIPE za cuvanje u stringu /sys.stdout

            out = p.communicate()[0]
            self._date = get_date()
            out = out.decode('utf-8')
            # print(out)
            out = re.sub(r'\s+', ' ', out)
            events = get_events(parse(out),out)
            print(len(events))
            #Ako postoje patterni za filtriranje onda cemo da fltriramo listu eventa inace saljemo citavu
            if self._patterns:
                send_events(self._filter_events(events))
            else:
                send_events(events)
            # print("##############################################################")
            p.kill()
            time.sleep(60*self._interval)

    def _filter_events(self,events_list):
        events = []
        for pattern in self._patterns:
            for event in events_list:
                if(re.match(pattern,str(event))):
                    events.append(event)
        #
        # for event in events_list:
        #     if any([[re.match(pattern, str(event)) for pattern in self._patterns]]):
        #         events.append(event)

        # print("ovdije sam",len(events))
        return events


def get_date():
    now  = datetime.datetime.now()
    now_str = now.strftime("%d%m%Y_%H%M%S")
    return now_str

def read_configuration(config_path):
    with open(config_path, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)

def run_agents(agents_list):
    for agent in agents_list:
        agent.run()


def send_events(events):
    for event in events:
        print("Poslan log:",event)
        send_log_line(str(event))


def parse(string):
    ret_val = {}
    ret_val['EventID']=[m.start() for m in re.finditer('EventID :', string)]
    ret_val['MachineName'] = [m.start() for m in re.finditer('MachineName :', string)]
    ret_val['Data'] = [m.start() for m in re.finditer('Data :', string)]
    ret_val['Index'] = [m.start() for m in re.finditer('Index :', string)]
    ret_val['Category'] = [m.start() for m in re.finditer('Category :', string)]
    ret_val['CategoryNumber'] = [m.start() for m in re.finditer('CategoryNumber :', string)]
    ret_val['EntryType'] = [m.start() for m in re.finditer('EntryType :', string)]
    ret_val['Message'] = [m.start() for m in re.finditer('Message :', string)]
    ret_val['Source'] = [m.start() for m in re.finditer('Source :', string)]
    ret_val['ReplacementStrings'] = [m.start() for m in re.finditer('ReplacementStrings :', string)]
    ret_val['InstanceId'] = [m.start() for m in re.finditer('InstanceId :', string)]
    ret_val['TimeGenerated'] = [m.start() for m in re.finditer('TimeGenerated :', string)]
    ret_val['TimeWritten'] = [m.start() for m in re.finditer('TimeWritten :', string)]
    ret_val['UserName'] = [m.start() for m in re.finditer('UserName :', string)]
    ret_val['Site'] = [m.start() for m in re.finditer('Site :', string)]
    ret_val['Container'] = [m.start() for m in re.finditer('Container :', string)]

    return ret_val


def get_events(index,string):
    ret_val = []
    for i in range(0,len(index['EventID'])):
        event_id = string[index['EventID'][i]+9:index['MachineName'][i]]
        machine_name = string[index['MachineName'][i] + 13:index['Data'][i]]
        data = string[index['Data'][i] + 6:index['Index'][i]]
        indexx = string[index['Index'][i] + 7:index['Category'][i]]
        Category = string[index['Category'][i]+10:index['CategoryNumber'][i]]
        CategoryNumber = string[index['CategoryNumber'][i] + 16:index['EntryType'][i]]
        EntryType = string[index['EntryType'][i] + 11:index['Message'][i]]
        Message = string[index['Message'][i] + 9:index['Source'][i]]
        Source = string[index['Source'][i] + 8:index['ReplacementStrings'][i]]
        ReplacementStrings = string[index['ReplacementStrings'][i] + 20:index['InstanceId'][i]]
        InstanceId = string[index['InstanceId'][i] + 12:index['TimeGenerated'][i]]
        TimeGenerated = string[index['TimeGenerated'][i] + 15:index['TimeWritten'][i]]
        TimeWritten = string[index['TimeWritten'][i] + 13:index['UserName'][i]]
        UserName = string[index['UserName'][i] + 10:index['Site'][i]]
        Site = string[index['Site'][i] + 6:index['Container'][i]]
        if(i==len(index['EventID'])-1):
            Container = string[index['Container'][i] + 11:len(string)]
        else:
            Container = string[index['Container'][i] + 11:index['EventID'][i+1]]
        #print(i,"          ",event_id,machine_name,data,indexx,Category,CategoryNumber,EntryType,Message,Source,ReplacementStrings,InstanceId,TimeGenerated,TimeWritten,UserName,Site,Container)
        e = Event(event_id,machine_name,data,indexx,Category,CategoryNumber,EntryType,Message,Source,ReplacementStrings,InstanceId,TimeGenerated,TimeWritten,UserName,Site,Container)
        ret_val.append(e)

    return ret_val

def check_os():
    if(platform.system()!="Windows"):
        return False
    return True

def main():

    if(not check_os()):
        raise Exception("Ovaj agent radi samo na Windowsu")
        exit(-1)

    log_agents =[]
    config = read_configuration("./windowsAgentConfig.yaml")
    if(config['logs']==None):
        raise Exception("Mora postojati bar jedan log koji zelimo da pratimo")

    #prolazimo kroz sve logove koje zelimo da pratimo
    for log_config in config['logs']:
        # print(log_config)
        patterns = log_config['log']['patterns'] if 'patterns' in log_config['log'] else []
        agent = WinAgent(log_config['log']['name'],log_config['log']['interval'],patterns)
        log_agents.append(agent)

    run_agents(log_agents)

if __name__ == '__main__':
    main()