#!/usr/bin/python

import time
import socket

# Direccion IP del servidor
HOST='127.0.0.1'
# Puerto de escucha del servidor.
PORT=60000

# Creamos el socket.
ServerSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
# Enlazar el servidor con la dirección local y el puerto. Necesario definir una tupla.
ServerSocket.bind((HOST,PORT))
# Pasar el socket a estado LISTEN. En versiones inferiores a la 3.5 de Python, el valor
# de backlog es obligatorio.
ServerSocket.listen(10)
# Lanzamos el metodo accept sobre el socket. Esto bloquea el código hasta que se establezca
# una conexión. Este método devuelve una pareja conn, addr; siendo conn un nuevo objecto socket
# para la nueva conexión y addr la dirección remota que se ha conectado.
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
