import socket

HOST = '127.0.0.1'
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, 4000))
while True:
    sock.send(bytes(input(),encoding="utf-8"))
sock.close()