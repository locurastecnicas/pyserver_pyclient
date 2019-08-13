#!/usr/bin/python

import time
import socket
import sys
import signal

# Direccion IP remota del servidor
HOST='127.0.0.1'
# Puerto de escucha del servidor.
PORT=60000

def readConfig(configFile):
  print("Read the configuration of the client.")
  dictConf={}
  try:
    configFile=open("client.conf","r")
    confString.replace(" ","")=configFile.read()
  except IOError as fileError:
    print("Couldn't open client config file.")
    print(fileError.strerror + ", error code: " + str(fileError.errno))
    sys.exit(fileError.errno)
  print(confString)
  for confLine in confString.split("\n"):
    if len(confLine) != 0:
      tempLine=confLine.split(" = ")
      dictConf[confLine(0)]=confLine(1)
  print("The configuration is:")
  print(dictConf)

def control_signal(signal_control, signal_handler):
  print("Stopping pyclient. Please wait....")
  print("Signal received: " + str(signal_control))
  ## Es necesario disponer del objecto socket abierto para cerrarlo
  ## de manera correcta.
  sys.exit(1)

signal.signal(signal.SIGINT, control_signal)
signal.signal(signal.SIGTERM, control_signal)

readConfig("client.conf")

# Creamos el socket.
try:
  ClientSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
except IOError as socketError:
  print("There was an error creating the socket.")
  print(socketError.strerror + ", error code: " + str(socketError.errno))
  sys.exit(socketError.errno)
# Stablishing connection with the remote server. A tuple is needed to define the
# address and port of the server.
try:
  ClientSocket.connect((HOST,PORT))
except IOError as socketError:
  print("There was an error connecting to the server.")
  print(socketError.strerror + ", error code: " + str(socketError.errno))
  sys.exit(socketError.errno)

# Enviar datos.
while True:
    DATA=raw_input('>>')
    if not DATA:
        break
    ClientSocket.sendall(DATA)
    recData=ClientSocket.recv(1024)
    print("Datos enviados por el servidor ", recData)
ClientSocket.close()
