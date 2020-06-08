#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
import socket
from socket import AF_INET, SOCK_STREAM
from threading import Thread
import sys
import re

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from the cave! Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        #Aqui se tiene que diferenciar el unicast de multicast y broadcast \/\w.*
        if bool(re.search(r'\S*::.*', bytes(msg).decode("utf8"))):
            unicast(msg,name)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            if len(clients) == 0:
                SERVER.close()
                sys.exit(0)
                break
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break
        print(clients)


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    #if msg = "/unicast":

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

def multicast()
def unicast(msg,name):
    nameunicast = re.findall(r'\w*(?=::)',bytes(msg).decode("utf8"))
    msgunicast = re.findall(r'(?<=::).*',bytes(msg).decode("utf8"))
    clientunicast = list(clients.keys())[list(clients.values()).index(nameunicast[0])]
    clientunicast.send(bytes(name+":"+msgunicast[0],"utf8"))

        
clients = {}
addresses = {}

HOST = ''
PORT = 33002
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket.socket(AF_INET, SOCK_STREAM)
SERVER.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
