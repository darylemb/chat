import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 4000))
sock.listen(5)

while True:
    clientsocket, address = sock.accept()
    print("Connection is stablished", address)
    clientsocket.send(bytes("You are connected",encoding="utf-8"))
    r = clientsocket.recv(256)
    print(r.decode("utf-8"))
    clientsocket.close()
sock.close()