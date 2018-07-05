# -*- coding: utf-8 -*-
import socket
from Functions import *
import time

def sendServer(connS, mensagem):
    connS.sendall(mensagem + "-+,+-")  # Envia dados


def recvServer(connS, myLock, varData, pacienteList):

    myLock.acquire()
    print "Cliente esta pronto para receber dados do servidor"
    myLock.release()
    while 1:
        if varData['ativo'] == False:
            break
        print pacienteList
        try:
            data = connS.recv(1024)  # Recebe os dados
            if not data: break
            #print "Debug recebeu data: " + str(data)
            msgRec = str(data).split("-+,+-")
            for linha in msgRec:
                msgRecA = linha.split("-,-")
                print "Debug recebeu linha: " + str(msgRecA[0])
                if msgRecA[0] == "MsgCadastro":
                    if msgRecA[1] == "ErroCadastro":
                        myLock.acquire()
                        print "Ocorreu um erro no cadastro: " + msgRecA[2]
                        myLock.release()
                    if msgRecA[1] == "SucessoCadastro":
                        myLock.acquire()
                        print msgRecA[2]
                        myLock.release()
                elif msgRecA[0] == "MsgLogin":
                    if msgRecA[1] == "FalhaLogin":
                        myLock.acquire()
                        print "Ocorreu um erro no cadastro: " + msgRecA[2]
                        myLock.release()
                    if msgRecA[1] == "SucessoLogin":
                        myLock.acquire()
                        varData['logado'] = True
                        print msgRecA[2]
                        myLock.release()
                elif msgRecA[0] == "MsgListaAutoriza":
                    if msgRecA[1] == "FalhaLista":
                        myLock.acquire()
                        print msgRecA[2]
                        myLock.release()
                    if msgRecA[1] == "SucessoLista":
                        myLock.acquire()
                        print msgRecA[2]
                        myLock.release()
                elif msgRecA[0] == "MsgAutoriza":
                    if msgRecA[1] == "FalhaAutoriza":
                        myLock.acquire()
                        print msgRecA[2]
                        myLock.release()
                    if msgRecA[1] == "SucessoAutoriza":
                        myLock.acquire()
                        print msgRecA[2]
                        myLock.release()
                elif msgRecA[0] == "alertaSensorPaciente":
                    myLock.acquire()
                    print msgRecA[1]
                    myLock.release()
                    somAlarm()
                elif msgRecA[0] == "AlertaNovoPaciente":
                    myLock.acquire()
                    print msgRecA[1]
                    myLock.release()
                    somAlarm()
                elif msgRecA[0] == "MsgListaAprovados":
                    if msgRecA[1] == "FalhaLista":
                        myLock.acquire()
                        print msgRecA[2]
                        myLock.release()
                    if msgRecA[1] == "SucessoLista":
                        myLock.acquire()
                        print msgRecA[2]
                        pacienteList[msgRecA[3]] = True
                        myLock.release()
                elif msgRecA[0] == "MsgListaHistorico":
                    if msgRecA[1] == "FalhaLista":
                        myLock.acquire()
                        print msgRecA[2]
                        myLock.release()
                    if msgRecA[1] == "SucessoLista":
                        myLock.acquire()
                        print msgRecA[2]
                        myLock.release()
                elif msgRecA[0] == "MensagemChat":
                    myLock.acquire()
                    print msgRecA[1]
                    myLock.release()
                    somChat()
                elif msgRecA[0] == "Stop":
                    print 'finalizando recServer'
                    break
                elif msgRecA[0] == "ErroServidor":
                    print msgRecA[1]
                    varData['ativo'] = False
                    break
        except Exception as e:
            print('Um erro ocorreu!')
            print e
            break
