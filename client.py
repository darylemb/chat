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
    send()

root = Tk()
root.title("Proyecto chat Redes")
messages_frame = Frame(root)
my_msg = StringVar()  # Variable que guarda los mensajes a enviar.
my_msg.set("Escribe tu mensaje.")
scrollbar = Scrollbar(messages_frame)  # Scrollbar para visualizar mensajes pasados
#Ventana que contiene los mensajes:
msg_list = Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
msg_list.pack(side=LEFT, fill=BOTH)
msg_list.pack()
messages_frame.pack()
#Campo de entrada para guardar en la variable my_msg los strings a enviar
entry_field = Entry(root, textvariable=my_msg)
entry_field.bind('<FocusIn>', on_entry_click)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = Button(root, text="Send", command=send)
send_button.pack()
root.protocol("WM_DELETE_WINDOW", on_closing)
#Conexión al servidor
HOST = os.popen('hostname -I').read().strip() #Función que indica la IP desde la que se está conectando el cliente
PORT = 33002 #Puerto por el que se establece la conexión
BUFSIZ = 1024 #Tamaño del buffer a enviar/recibir
ADDR = (HOST, PORT) #Tupla de dirección para clase socket
client_socket = socket.socket(AF_INET, SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.connect(ADDR)
receive_thread = Thread(target=receive) #Hilo generado cada vez que se recibe un mensaje
receive_thread.start()
root.mainloop()