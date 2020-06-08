import socket
from socket import AF_INET, SOCK_STREAM
from threading import Thread
import sys
import re

def accept_incoming_connections():
    """Revisa las conexiones entrantes"""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s Se ha conectado." % client_address)
        client.send(bytes("Bienvenido al chat, ingresa tu nickname y presiona ENTER!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()#Crea un hilo cada vez que se recibe un mensaje de un usuario

def handle_client(client):
    """Gestiona un envío de un cliente"""
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Bienvenido %s! Si deseas salir escribe {salir} para dejar la sala.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s se ha unido al chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name #Diccionario que asigna a una llave de tipo client (objeto socket) el valor nickname, que se empleará para distingur a los usuarios destinos 

    while True:
        msg = client.recv(BUFSIZ)
        if bool(re.search(r'.*::.*', bytes(msg).decode("utf8"))):#Mediante expresiones regulares se identifica si el mmensajes para una persona (unicast) o muchas personas(multicast)
            multicast(msg,name)
        elif msg != bytes("{salir}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{salir}", "utf8"))
            client.close()
            del clients[client]
            if len(clients) == 0: #Si no hay clientes, el servidor se cierra
                SERVER.close()
                sys.exit(0)
                break
            broadcast(bytes("%s ha dejado el chat." % name, "utf8"))
            break

def broadcast(msg, name=""):  #Name es el identificador de cada usuario. Envía un broadcast, este es el texto por defecto, es un chat global.
    for client in clients:
        client.send(bytes(name, "utf8")+msg)

def multicast(msg,name): #Al validar que es para uno o varios usuarios, se extrae del mensaje los nicknames destinos con regex, enviando a cada uno con un ciclo for el mensaje de origen.
    nameunicast = re.findall(r'((?<=\/)\w*)(?!=::)',bytes(msg).decode("utf8"))
    msgunicast = re.findall(r'(?<=::).*',bytes(msg).decode("utf8"))
    for i in range(len(nameunicast)):
        for client, nombre in clients.items():
            if nombre == nameunicast[i]:
                client.send(bytes(name+": "+msgunicast[0],"utf8"))
        
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
    SERVER.listen(10)
    print("Esperando conexión...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()