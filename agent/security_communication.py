from threading import Thread
from threading import Lock
from time import sleep
from requests import Session


class SecurityChannel(object):
    def __init__(self, key_path=None, cert_path=None, ca_path=None, API_ENDPOINT=None, interval=1):
        self.key_path = key_path
        self.cert_path = cert_path
        self.ca_path = ca_path
        self.interval = interval

        self.session = None
        self.messages = []
        self.thread = Thread(target=self.center_communication)
        self.lock = Lock()
        self.API_ENDPOINT = API_ENDPOINT

    def initialize_communication(self, key_path, cert_path, ca_path, API_ENDPOINT, interval):
        # postavljanje parametara
        self.set_key_path(key_path)
        self.set_cert_path(cert_path)
        self.set_ca_path(ca_path)
        self.set_API_ENDPOINT(API_ENDPOINT)
        self.set_interval(interval)
        # incijalizacija sesije
        self._initialize_session()
        # pokretanje background niti
        self.thread.start()

    def _initialize_session(self):
        self.session = Session()
        self.session.cert = (self.cert_path, self.key_path)
        self.session.verify = self.ca_path
        self.session.headers = {'content-type': 'application/json'}

    def set_key_path(self, key_path):
        self.key_path = key_path

    def set_cert_path(self, cert_path):
        self.cert_path = cert_path

    def set_ca_path(self, ca_path):
        self.ca_path = ca_path

    def set_interval(self, interval):
        self.interval = interval

    def set_API_ENDPOINT(self, API_ENDPOINT):
        self.API_ENDPOINT = API_ENDPOINT

    def _acquire_lock(self):
        self.lock.acquire(blocking=True)

    def _release_lock(self):
        self.lock.release()

    def send_message(self, message):
        self._acquire_lock()
        self.messages.append(message)
        self._release_lock()

    def take_message(self):
        self._acquire_lock()
        msgs = self.messages[:]
        self.messages.clear()
        self._release_lock()
        return msgs

    def send_messages(self, messages):
        # requests.post(API_ENDPOINT, data=json.dumps(json_log).encode('utf-8'),
        #               headers={'content-type': 'application/json'},
        #                   cert=('certs/agent.vlada.crt', 'certs/agent.vlada.key'), verify='certs/myCA.pem')
        for m in messages:
            r = self.session.post(self.API_ENDPOINT, data=m)
            if r.status_code != 201:
                print("Ovo ne valja: %s" % m)
            else:
                print("Sve ok")

    def center_communication(self):
        while True:
            msgs = self.take_message()
            if not msgs:
                print("Nema nista da se salje")
                sleep(self.interval)
                continue
            self.send_messages(msgs)