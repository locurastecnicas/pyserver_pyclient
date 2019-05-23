#!/usr/bin/python

import errno
import time
import socket
import sys
import signal
import threading

# Direccion IP del servidor
HOST='127.0.0.1'
# Puerto de escucha del servidor.
PORT=60000

class echo_server(threading.Thread):
  def __init__(self, connected_socket, client_addr):
    threading.Thread.__init__(self)
    self.chat_socket=connected_socket
    self.remote_addr=client_addr
    print("Iniciado thread de conversacion.")

  def run(self):
    # Recibir datos del cliente.
    while True:
        recData=self.chat_socket.recv(1024)
        print("La direccion remota es ", self.remote_addr )
        print("Los datos recibidos son ", recData)
        # Enviar datos al cliente.
        self.chat_socket.send(b'Hola cliente, yo soy el servidor.')
        if not recData:
            break
    self.chat_socket.close()

def control_signal(signal_control, signal_handler):
  print("Stopping pyerver. Please wait....")
  print("Signal received: " + str(signal_control))
  ## Es necesario disponer de la lista de sockets abiertos en
  ## este punto para cerrarlos de forma correcta.
  sys.exit(1)

signal.signal(signal.SIGINT, control_signal)
signal.signal(signal.SIGTERM, control_signal)

# Creamos el socket.
try:
  ServerSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
except socket.error as CreateSocket:
  print("No se puede crear el socket.")
  print(CreateSocket)
  sys.exit(100)

# Enlazar el servidor con la direccion local y el puerto. Necesario definir una tupla.
try:
  ServerSocket.bind((HOST,PORT))
except socket.error as BindError:
  exctype, value = sys.exc_info()[:2]
  print("En exctype tengo ")
  print(exctype)
  print("En value tengo ")
  print(value)
  print("No se puede enlazar con la direccion especificada.")
  print(BindError)
  sys.exit(111)

# Pasar el socket a estado LISTEN. En versiones inferiores a la 3.5 de Python, el valor
# de backlog es obligatorio.
ServerSocket.listen(10)
# Lanzamos el metodo accept sobre el socket. Esto bloquea el codigo hasta que se establezca
# una conexion. Este metodo devuelve una pareja conn, addr; siendo conn un nuevo objecto socket
# para la nueva conexion y addr la direccion remota que se ha conectado.
while True:
    connSocket,remoteAddr=ServerSocket.accept()  
    chat=echo_server(connSocket,remoteAddr) 
    chat.start()
# Recibir datos del cliente.
#while True:
#    recData=connSocket.recv(1024)
#    print("La direccion remota es ", remoteAddr )
#    print("Los datos recibidos son ", recData)
#    # Enviar datos al cliente.
#    connSocket.send(b'Hola cliente, yo soy el servidor.')
#    if not recData:
#        break

ServerSocket.close()

