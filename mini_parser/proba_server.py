# import socket programming library
import socket

# import thread module
from _thread import *
import threading
import ssl

print_lock = threading.Lock()


# thread fuction
def threaded(c):
    while True:

        # data received from client
        data_bytes = c.recv(1024)
        header = data_bytes[0:2]
        data = data_bytes[2:].decode('utf-8')
        if not data:
            print('Bye')

            # lock released on exit
            print_lock.release()
            break
        print("Stigli podaci: %s" % data)
        # reverse the given string from client
        poruka = "Ovo saljemo!"
        poruka_bytes = poruka.encode("utf-8")

        # send back reversed string to client
        c.send(header + poruka_bytes)

    # connection closed
    c.close()


def Main():
    host = ""

    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 33334
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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


if __name__ == '__main__':
    Main()