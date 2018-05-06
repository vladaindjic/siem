from threading import Thread
from threading import Lock
from time import sleep
from requests import Session
import socket
import ssl


class SecurityChannel(object):
    def __init__(self, key_path=None, cert_path=None, ca_path=None, API_ENDPOINT=None, interval=1,
                 HOST=None, PORT=None, communication_protocol=None):
        self.key_path = key_path
        self.cert_path = cert_path
        self.ca_path = ca_path
        self.interval = interval

        self.session = None
        self.messages = []
        self.thread = Thread(target=self.center_communication)
        self.lock = Lock()
        self.API_ENDPOINT = API_ENDPOINT
        self.HOST = HOST
        self.port = PORT
        self.communication_protocol = communication_protocol

    def initialize_communication(self, key_path, cert_path, ca_path, API_ENDPOINT, interval, HOST, PORT, communication_protocol):
        # postavljanje parametara
        self.set_key_path(key_path)
        self.set_cert_path(cert_path)
        self.set_ca_path(ca_path)
        self.set_API_ENDPOINT(API_ENDPOINT)
        self.set_interval(interval)
        self.set_HOST(HOST)
        self.set_PORT(PORT)
        self.set_communication_protocol(communication_protocol)
        # incijalizacija sesije, ako je HTTPS
        if self.communication_protocol == 'HTTPS':
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

    def set_HOST(self, HOST):
        self.HOST = HOST

    def set_PORT(self, PORT):
        self.PORT = PORT

    def set_communication_protocol(self, communication_protocol):
        self.communication_protocol = communication_protocol

    def _acquire_lock(self):
        self.lock.acquire(blocking=True)

    def _release_lock(self):
        self.lock.release()

    def send_message(self, message):
        self._acquire_lock()
        self.messages.append(message)
        # print("TO SEND: %s" % message)
        self._release_lock()

    def take_message(self):
        self._acquire_lock()
        msgs = self.messages[:]
        self.messages.clear()
        self._release_lock()
        return msgs

    def send_messages(self, messages):
        if self.communication_protocol == 'HTTPS':
            self._send_messages_https(messages)
        else:
            self._send_messages_tcp(messages)

    def _send_messages_https(self, messages):
        # requests.post(API_ENDPOINT, data=json.dumps(json_log).encode('utf-8'),
        #               headers={'content-type': 'application/json'},
        #                   cert=('certs/agent.vlada.crt', 'certs/agent.vlada.key'), verify='certs/myCA.pem')
        for m in messages:
            r = self.session.post(self.API_ENDPOINT, data=m.encode('utf-8'))
            if r.status_code != 201:
                print("Ovo ne valja: %s" % m)
            else:
                print("Sve ok")

    def _send_messages_tcp(self, messages):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_TLSv1_2,keyfile=self.key_path, certfile=self.cert_path,
                            server_side=False, cert_reqs=ssl.CERT_REQUIRED, ca_certs=self.ca_path)
        s.connect((self.HOST, self.PORT))
        for m in messages:
            # FIXME: check this new line character
            s.send((m + '\n').encode('utf-8'))
            print('Sve ok!')
        s.close()

    def center_communication(self):
        while True:
            msgs = self.take_message()
            if not msgs:
                print("Nema nista da se salje")
                sleep(self.interval)
                continue
            self.send_messages(msgs)