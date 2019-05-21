#!/usr/bin/python

import time
import socket
import sys
import signal

# Direccion IP remota del servidor
HOST='127.0.0.1'
# Puerto de escucha del servidor.
PORT=60000

def control_signal(signal_control, signal_handler):
  print("Stopping pyclient. Please wait....")
  print("Signal received: " + str(signal_control))
  ## Es necesario disponer del objecto socket abierto para cerrarlo
  ## de manera correcta.
  sys.exit(1)

signal.signal(signal.SIGINT, control_signal)
signal.signal(signal.SIGTERM, control_signal)

# Creamos el socket.
try:
  ClientSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
except socket.error:
  print("No se puede crear el socket.")
  sys.exit(111)
# Conectar con el servidor. Necesario definir tupla para la direccion del server.
try:
  ClientSocket.connect((HOST,PORT))
except socket.error:
  print("No se puede conectar con el servidor.")
  sys.exit(111)

# Enviar datos.
while True:
    DATA=raw_input('>>')
    if not DATA:
        break
    ClientSocket.sendall(DATA)
    recData=ClientSocket.recv(1024)
    print("Datos enviados por el servidor ", recData)
ClientSocket.close()
