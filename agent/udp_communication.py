import socket


UDP_IP = "localhost"
UDP_PORT = 5555
# MESSAGE = 'Hello, world'
# print("UDP target IP:", UDP_IP)
# print("UDP target port:", UDP_PORT)
# print("message:", MESSAGE)

#from OpenSSL import SSL

def send_log_line(message):
    print("Salje se: %s" % message)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.sendto(bytes(message, "utf-8"), (UDP_IP, UDP_PORT))
    sock.close()


# def send_log_line(message):
#     try:
#         print("Salje se: %s" % message)
#         ctx = SSL.Context(SSL.SSLv23_METHOD)
#         # ctx.set_verify(SSL.VERIFY_PEER, verify_cb) # Demand a certificate
#         ctx.use_privatekey_file("/home/vi3/Faks/Bezbednost/siem/mini_parser/certs/sysqo-parser.key")
#         ctx.use_certificate_file("/home/vi3/Faks/Bezbednost/siem/mini_parser/certs/sysqo_parser.crt")
#         ctx.load_verify_locations("/home/vi3/Faks/Bezbednost/siem/mini_parser/certs/ca.crt")
#
#         # Set up client
#         sock = SSL.Connection(ctx, socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
#         addr = (UDP_IP, UDP_PORT)
#         sock.setblocking(0)
#         sock.connect(addr)
#         sock.send(bytes(message, 'utf-8'))
#     except:
#         print("Dolazis li ovde?")
