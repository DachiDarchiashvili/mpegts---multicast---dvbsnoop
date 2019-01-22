import socket
import struct
import subprocess

# Multicast address
MCAST_GRP = '239.1.6.2'
# Multicast port
MCAST_PORT = 5004

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((MCAST_GRP, MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Run dvbsnoop so it's waiting input on stdin
process = subprocess.Popen("dvbsnoop -s ts -if -", shell=True, stdin=subprocess.PIPE)

while True:
    process.stdin.write(sock.recv(10240))
    process.stdin.flush()
