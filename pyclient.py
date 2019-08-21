#!/usr/bin/python

import time
import socket
import sys
import signal
import uuid

def readConfig(configFile):
  print("Read the configuration of the client.")
  dictConf={}
  try:
    configFile=open("client.conf","r")
    confString=configFile.read()
  except IOError as fileError:
    print("Couldn't open client config file.")
    print(fileError.strerror + ", error code: " + str(fileError.errno))
    sys.exit(fileError.errno)
  for confLine in confString.split("\n"):
    if len(confLine) != 0:
      tempLine=confLine.replace(" ","").split("=")
      dictConf[tempLine[0]]=tempLine[1]
  configFile.close()
  return(dictConf)

def control_signal(signal_control, signal_handler):
  print("Stopping pyclient. Please wait....")
  print("Signal received: " + str(signal_control))
  ## Es necesario disponer del objecto socket abierto para cerrarlo
  ## de manera correcta.
  sys.exit(1)

signal.signal(signal.SIGINT, control_signal)
signal.signal(signal.SIGTERM, control_signal)

clientConfig=readConfig("client.conf")

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
  ClientSocket.connect((clientConfig["HOST"],int(clientConfig["PORT"])))
except IOError as socketError:
  print("There was an error connecting to the server.")
  print(socketError.strerror + ", error code: " + str(socketError.errno))
  sys.exit(socketError.errno)
# Registro del cliente.
clientID=str(uuid.uuid4())
userName=raw_input("Please, input a username for the chat - ")
registerDATA="CONTROL" + "||" + clientID + "||" + userName
try:
  ClientSocket.sendall(registerDATA)
  recData=ClientSocket.recv(1024)
  print(recData)
except IOError as socketError:
  print("There was an error registering with the server.")
  print(socketError.strerror + ", error code: " + str(socketError.errno))
  ClientSocket.close()
  sys.exit(socketError.errno)
chatPROMPT=userName + " >> "
# Enviar datos.
while True:
    DATA=raw_input(chatPROMPT)
    if not DATA:
        closeMSG="CLOSE" + "||" + clientID + "||" + userName
        ClientSocket.sendall(closeMSG)
        recData=ClientSocket.recv(1024)
        break
    ClientSocket.sendall(DATA)
    recData=ClientSocket.recv(1024)
    print("Datos enviados por el servidor ", recData)
ClientSocket.close()
