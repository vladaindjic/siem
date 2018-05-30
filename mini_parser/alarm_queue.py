from threading import Lock
from sysqo_time_util import convert_rfc3339str_to_datetime


class AlarmQueue(object):
    def __init__(self, alarm, num_logs, has_timestamp):
        self.alarm = alarm
        self.num_logs = num_logs
        self.has_timestamp = has_timestamp
        self.logs = []
        self.lock = Lock()

    def add_log(self, log):
        fired_logs = []
        self.lock.acquire()
        self._add(log)
        self._sort()
        self._clean()
        if self._is_full():
            fired_logs = self._clear()
        self.lock.release()
        return fired_logs

    def _add(self, log):
        self.logs.append(log)

    def _sort(self):
        # ako ima timestamp, onda treba sortirati po njemu u opadajucem redosledu
        if self.has_timestamp:
            self.logs.sort(key=lambda l: convert_rfc3339str_to_datetime(l.timestamp), reverse=True)

    def _clean(self):
        # ako nema timestampa, nema potrebe da se cisti
        if not self.has_timestamp:
            return

        while self.logs:
            last = self.logs[-1]
            # ako log zadovoljava uslov, ostaje u redu cekanje
            if self.alarm.eval(last):
                break
            print(last)
            # inace se brise
            del self.logs[-1]

    def _is_full(self):
        return len(self.logs) >= self.num_logs

    def _clear(self):
        old_logs = self.logs.copy()
        self.logs.clear()
        return old_logs
