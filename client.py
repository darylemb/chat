import socket
from socket import AF_INET, SOCK_STREAM
from threading import Thread
from tkinter import *
import os

firstclick = True

def on_entry_click(event):
    """Funcion que limpia el texto a enviar en la interfaz al presionar Enter/Send"""        
    global firstclick

    if firstclick: 
        firstclick = False
        entry_field.delete(0, "end") # Limpia el texto que se escribió en el mensaje anterior


def receive():
    """Funcion que recibe mensaje, está escuchando permanentemente"""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(END, msg)
        except OSError:  # Si el cliente abandona el chat con esta excepción finaliza el ciclo de escucha.
            break


def send(event=None):  # event is passed by binders.
    """Funcion que captura y envía el mensaje."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{salir}":
        client_socket.close()
        root.quit()


def on_closing(event=None):
    """Se llama cuando se cierra la ventana de la interfaz, se envía {salir} al servidor para finalizar conexión con cliente """
    my_msg.set("{salir}")
    send(my_msg)
#-------------------------INTERFAZ DE USUARIO-----------------------------#
root = Tk()
root.title("Proyecto chat Redes")
messages_frame = Frame(root)
my_msg = StringVar()  # Variable que guarda los mensajes a enviar.
my_msg.set("Escribe tu mensaje.")
scrollbar = Scrollbar(messages_frame)  # Scrollbar para visualizar mensajes pasados
#Ventana que contiene los mensajes:
msg_list = Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)#Genera una Listbox (una caja de mensajes donde se apilaran los mensajes enviados)
scrollbar.pack(side=RIGHT, fill=Y)#Barra lateral derecha para subir y bajar sobre los mensajes escritos
msg_list.pack(side=LEFT, fill=BOTH)#Manera en que se acomodan los mensajes, a la izquierda y completa la  caja de mensajes
msg_list.pack()#Declaracion de la caja de mensajes
messages_frame.pack()#declaracion del espacio donde se encuentra la caja de mensajes
#Campo de entrada para guardar en la variable my_msg los strings a enviar
entry_field = Entry(root, textvariable=my_msg)#Espacio en blanco que permite escribir el mensaje a enviar, lo guardará en la variable my_msg
entry_field.bind('<FocusIn>', on_entry_click)#
entry_field.bind("<Return>", send)
entry_field.pack()#Declaracion del espacio para escribir el mensaje a enviar
send_button = Button(root, text="Send", command=send)#Creacion del boton que llamará a la funcion send
send_button.pack()#Declaracion del boton
root.protocol("WM_DELETE_WINDOW", on_closing)#Método que llama a la funcion on_closing al cerrar la ventana de la interfaz, es decir, manda el mensaje "{salir}" al servidor.
#--------------FIN DE INTERFAZ DE USUARIO----------------------------------#
#Conexión al servidor
HOST = '192.168.0.100'#Dirección del servidor al cual se va a conectar
PORT = 33002 #Puerto por el que se establece la conexión
BUFSIZ = 1024 #Tamaño del buffer a enviar/recibir
ADDR = (HOST, PORT) #Tupla de dirección para clase socket
client_socket = socket.socket(AF_INET, SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.connect(ADDR)
receive_thread = Thread(target=receive) #Hilo generado cada vez que se recibe un mensaje
receive_thread.start()
root.mainloop()

