#!/usr/bin/python

import errno
import time
import socket
import sys
import signal
import threading

class echo_server(threading.Thread):
  def __init__(self, connected_socket, client_addr):
    threading.Thread.__init__(self)
    self.close_flag=threading.Event()
    self.chat_socket=connected_socket
    self.remote_addr=client_addr
    print("Iniciado thread de conversacion.")

  def run(self):
    # Recibir datos del cliente.
    while True:
        if not self.close_flag.is_set():
           recData=self.chat_socket.recv(1024)
        else:
           print("SERVER - Enviando cierre al cliente.")
           self.chat_socket.send(b'CIERRE')
           print("Pues se ha activado el flag.")
           break
        if recData.find("CONTROL") != -1:
           controlMSG=recData.split('||')
           clientID=controlMSG[1] + "-" + self.remote_addr[0]
           userName=controlMSG[2]
           self.chat_socket.send(b'Hola ' + userName + ', yo soy el servidor.')
           self.chat_socket.send(b' Conexion registrada como ' + clientID + '.')
        elif recData.find("CLOSE") != -1:
           print("Recibido cierre de " + userName + "@" + clientID + ".")
           self.chat_socket.send(b'Cerrando chat, adios ' + userName + '@' + clientID + '.')
           break
        else:
           self.chat_socket.send(b'Hola ' + userName + '@' + clientID + ', yo soy el servidor.')
        
        print("La direccion remota es ", self.remote_addr )
        print("Los datos recibidos son ", recData)
        # Enviar datos al cliente.
        
    self.chat_socket.close()

def readConfig(configFile):
  print("Read the configuration of the server.")
  dictConf={}
  try:
    configFile=open("server.conf","r")
    confString=configFile.read()
  except IOError as fileError:
    print("Couldn't open server config file.")
    print(fileError.strerror + ", error code: " + str(fileError.errno))
    sys.exit(fileError.errno)
  for confLine in confString.split("\n"):
    if len(confLine) != 0:
      tempLine=confLine.replace(" ","").split("=")
      dictConf[tempLine[0]]=tempLine[1]
  configFile.close()
  return(dictConf)

def control_signal(signal_control, signal_handler):
  print("Stopping pyerver. Please wait....")
  print("Signal received: " + str(signal_control))
  ## Es necesario disponer de la lista de sockets abiertos en
  ## este punto para cerrarlos de forma correcta.
  for chatThread in threading.enumerate():
    print("Cerrando threads y conversaciones.")
    print("Procesando thread" + chatThread.getName())
    if chatThread.getName() == "MainThread":
      continue
    chatThread.close_flag.set()
  raise CloseAll

class CloseAll(Exception):
  pass

signal.signal(signal.SIGINT, control_signal)
signal.signal(signal.SIGTERM, control_signal)

serverConfig=readConfig("server.conf")

# Creamos el socket.
try:
  ServerSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
except IOError as socketError:
  print("Could not create the socket.")
  print(socketError.strerror + ", error code: " + str(socketError.errno))
  sys.exit(socketError.errno)

# Enlazar el servidor con la direccion local y el puerto. Necesario definir una tupla.
try:
  ServerSocket.bind((serverConfig["HOST"],int(serverConfig["PORT"])))
except IOError as socketError:
  print("Could not bind with the specified address.")
  print(socketError.strerror + ", error code: " + str(socketError.errno))
  sys.exit(socketError.errno)

# Pasar el socket a estado LISTEN. En versiones inferiores a la 3.5 de Python, el valor
# de backlog es obligatorio.
ServerSocket.listen(10)
# Lanzamos el metodo accept sobre el socket. Esto bloquea el codigo hasta que se establezca
# una conexion. Este metodo devuelve una pareja conn, addr; siendo conn un nuevo objecto socket
# para la nueva conexion y addr la direccion remota que se ha conectado.
try:
  while True:
    connSocket,remoteAddr=ServerSocket.accept()  
    chat=echo_server(connSocket,remoteAddr) 
    chat.start()
except IOError as commsError:
  print("There was an unexpected error.")
  print(socketError.strerror + ", error code: " + str(socketError.errno))
  sys.exit(socketError.errno)
except CloseAll:
  ServerSocket.close()
  sys.exit(1)

