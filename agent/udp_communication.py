import socket


UDP_IP = "192.168.0.18"
UDP_PORT = 5555
MESSAGE = 'Hello, world'
print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)
print("message:", MESSAGE)


def send_log_line(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.sendto(bytes(message, "utf-8"), (UDP_IP, UDP_PORT))
    sock.close()
