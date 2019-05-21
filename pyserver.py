#!/usr/bin/python

import errno
import time
import socket
import sys
import signal

# Direccion IP del servidor
HOST='127.0.0.1'
# Puerto de escucha del servidor.
PORT=22

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
  print("No se puede enlazar con la direccion especificada.")
  print(BindError)
  sys.exit(111)

# Pasar el socket a estado LISTEN. En versiones inferiores a la 3.5 de Python, el valor
# de backlog es obligatorio.
ServerSocket.listen(10)
# Lanzamos el metodo accept sobre el socket. Esto bloquea el codigo hasta que se establezca
# una conexion. Este metodo devuelve una pareja conn, addr; siendo conn un nuevo objecto socket
# para la nueva conexion y addr la direccion remota que se ha conectado.
connSocket,remoteAddr=ServerSocket.accept()  
# Recibir datos del cliente.
while True:
    recData=connSocket.recv(1024)
    print("La direccion remota es ", remoteAddr )
    print("Los datos recibidos son ", recData)
    # Enviar datos al cliente.
    connSocket.send(b'Hola cliente, yo soy el servidor.')
    if not recData:
        break

connSocket.close()
ServerSocket.close()
