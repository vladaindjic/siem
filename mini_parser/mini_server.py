# import socket programming library
import socket
import threading
# import thread module
from _thread import *
from sysql import SysqlMongoCompiler
import ssl

print_lock = threading.Lock()

sysql_mongo_compiler = SysqlMongoCompiler()
MAX_MESSAGE_SIZE = 4096


def threaded(c):
    try:
        # data received from client
        sysql_bytes = c.recv(MAX_MESSAGE_SIZE)
        sysql_str = sysql_bytes.decode('utf-8')
        print("Parse: %s" % sysql_str)
        mongo_query = sysql_mongo_compiler.compile(sysql_str)
        print("Mongo query: %s" % mongo_query)
        mongo_query_bytes = mongo_query.encode("utf-8")
        # send back reversed string to client
        c.send(mongo_query_bytes)
    except:
        c.send("failed".encode('utf-8'))
    finally:
        print_lock.release()
        c.close()


def start_server():
    host = ""

    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 33333
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s = ssl.wrap_socket(s, keyfile="certs/sysqo.key", certfile="certs/sysqo.crt",
                        server_side=True, cert_reqs=ssl.CERT_REQUIRED, ca_certs="certs/ca.crt")
    s.bind((host, port))
    print("socket binded to post", port)

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        c, addr = s.accept()

        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))
    s.close()


def main():
    start_server()


if __name__ == '__main__':
    main()

