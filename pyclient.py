#!/usr/bin/python

import time
import socket
import sys

# Direccion IP remota del servidor
HOST='127.0.0.1'
# Puerto de escucha del servidor.
PORT=60000

# Creamos el socket.
ClientSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
# Conectar con el servidor. Necesario definir tupla para la direccion del server.
ClientSocket.connect((HOST,PORT))
# Enviar datos.
while True:
    DATA=raw_input('>>')
    if not DATA:
        break
    ClientSocket.sendall(DATA)
    recData=ClientSocket.recv(1024)
    print("Datos enviados por el servidor ", recData)
ClientSocket.close()
