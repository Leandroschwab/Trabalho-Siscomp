# -*- coding: utf-8 -*-
import socket
from Functions import *


def sendServer(connS,mensagem):
    connS.sendall(mensagem)  # Envia dados

def recvServer(connS,printLock,varData):
    printLock.acquire()
    print "Cliente esta pronto para receber dados do servidor"
    printLock.release()
    while 1:
        data = connS.recv(1024)  # Recebe os dados
        if not data: break
        print "Recebeu debug: " + str(data)
        msgRec = str(data)
        msgRecA = msgRec.split("-,-")
        if msgRecA[0] == "MsgCadastro":
            print()

