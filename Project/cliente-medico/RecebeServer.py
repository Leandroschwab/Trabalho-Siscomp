# -*- coding: utf-8 -*-
import socket
from Functions import *
import time

def sendServer(connS, mensagem):
    connS.sendall(mensagem + "-+,+-")  # Envia dados


def recvServer(connS, myLock, varData):
    myLock.acquire()
    print "Cliente esta pronto para receber dados do servidor"
    myLock.release()
    while 1:
        data = connS.recv(1024)  # Recebe os dados
        if not data: break
        #print "Debug recebeu data: " + str(data)
        msgRec = str(data).split("-+,+-")
        for linha in msgRec:
            msgRecA = linha.split("-,-")
            print "Debug recebeu linha: " + str(linha)
            if msgRecA[0] == "MsgCadastro":
                if msgRecA[1] == "ErroCadastro":
                    myLock.acquire()
                    print "Ocorreu um erro no cadastro: " + msgRecA[2]
                    myLock.release()
                if msgRecA[1] == "SucessoCadastro":
                    myLock.acquire()
                    print msgRecA[2]
                    myLock.release()
            if msgRecA[0] == "MsgLogin":
                if msgRecA[1] == "FalhaLogin":
                    myLock.acquire()
                    print "Ocorreu um erro no cadastro: " + msgRecA[2]
                    myLock.release()
                if msgRecA[1] == "SucessoLogin":
                    myLock.acquire()
                    varData['logado'] = True
                    print msgRecA[2]
                    myLock.release()
            if msgRecA[0] == "MsgListaAutoriza":
                if msgRecA[1] == "FalhaLista":
                    myLock.acquire()
                    print msgRecA[2]
                    myLock.release()
                if msgRecA[1] == "SucessoLista":
                    myLock.acquire()
                    print msgRecA[2]
                    myLock.release()
            if msgRecA[0] == "MsgAutoriza":
                if msgRecA[1] == "FalhaAutoriza":
                    myLock.acquire()
                    print msgRecA[2]
                    myLock.release()
                if msgRecA[1] == "SucessoAutoriza":
                    myLock.acquire()
                    print msgRecA[2]
                    myLock.release()
            if msgRecA[0] == "alertaSensorPaciente":
                myLock.acquire()
                print msgRecA[1]
                myLock.release()
            if msgRecA[0] == "AlertaNovoPaciente":
                myLock.acquire()
                print msgRecA[1]
                myLock.release()
            if msgRecA[0] == "MsgListaAprovados":
                if msgRecA[1] == "FalhaLista":
                    myLock.acquire()
                    print msgRecA[2]
                    myLock.release()
                if msgRecA[1] == "SucessoLista":
                    myLock.acquire()
                    print msgRecA[2]
                    myLock.release()
            if msgRecA[0] == "MsgListaHistorico":
                if msgRecA[1] == "FalhaLista":
                    myLock.acquire()
                    print msgRecA[2]
                    myLock.release()
                if msgRecA[1] == "SucessoLista":
                    myLock.acquire()
                    print msgRecA[2]
                    myLock.release()


