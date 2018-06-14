# -*- coding: utf-8 -*-
import socket
from Functions import *


def sendServer(connS,mensagem):
    connS.sendall(mensagem)  # Envia dados

def recvServer(connS,myLock,varData):
    myLock.acquire()
    print "Cliente esta pronto para receber dados do servidor"
    myLock.release()
    while 1:
        data = connS.recv(1024)  # Recebe os dados
        if not data: break
        print "debug Recebeu: " + str(data)
        msgRec = str(data)
        msgRecA = msgRec.split("-,-")

        if msgRecA[0] == "MsgCadastro":
            if msgRecA[1]=="ErroCadastro":
                myLock.acquire()
                print "Ocorreu um erro no cadastro: "+ msgRecA[2]
                myLock.release()
            if msgRecA[1]=="SucessoCadastro":
                myLock.acquire()
                print msgRecA[2]
                myLock.release()
        if msgRecA[0] == "MsgLogin":
            if msgRecA[1]=="FalhaLogin":
                myLock.acquire()
                print "Ocorreu um erro no cadastro: "+ msgRecA[2]
                myLock.release()
            if msgRecA[1]=="SucessoLogin":
                myLock.acquire()
                varData['logado'] = True
                print msgRecA[2]
                myLock.release()

