# -*- coding: utf-8 -*-
import socket
from EnviaServer import *
from Functions import *
from threading import Thread, Lock, BoundedSemaphore, Semaphore

def recvServer(connS,myLock,varData):
    myLock['print'].acquire()
    print "Cliente esta pronto para receber dados do servidor"
    myLock['print'].release()
    while 1:
        if varData['ativo'] == False:
            break
        try:
            data = connS.recv(1024)  # Recebe os dados
            if not data: break
            print "Servidou recebeu data: " + str(data)
            msgRec = str(data).split("-+,+-")
            for linha in msgRec:
                msgRecA = linha.split("-,-")
                print "Servidou recebeu linha: " + str(linha)
                if msgRecA[0] == "MsgCadastro":
                    if msgRecA[1]=="ErroCadastro":
                        myLock['print'].acquire()
                        print "Ocorreu um erro no cadastro: "+ msgRecA[2]
                        myLock['print'].release()
                    if msgRecA[1]=="SucessoCadastro":
                        myLock['print'].acquire()
                        print msgRecA[2]
                        myLock['print'].release()
                elif msgRecA[0] == "MsgLogin":
                    if msgRecA[1]=="FalhaLogin":
                        myLock['print'].acquire()
                        print "Ocorreu um erro no login: "+ msgRecA[2]
                        myLock['print'].release()
                    if msgRecA[1]=="SucessoLogin":
                        myLock['print'].acquire()
                        varData['logado'] = True
                        print msgRecA[2]
                        myLock['print'].release()
                        t = Thread(target=backGroundTask, args=(connS, myLock, varData))
                        t.start()
                elif msgRecA[0] == "MsgListaMedicos":
                    if msgRecA[1]=="FalhaLista":
                        myLock['print'].acquire()
                        print msgRecA[2]
                        myLock['print'].release()
                    if msgRecA[1]=="SucessoLista":
                        myLock['print'].acquire()
                        print msgRecA[2]
                        myLock['print'].release()
                elif msgRecA[0] == "alertaSensorPaciente":
                    myLock['print'].acquire()
                    print msgRecA[1]
                    myLock['print'].release()
                    somAlarm()
                elif msgRecA[0] == "MensagemChat":
                    myLock['print'].acquire()
                    print msgRecA[1]
                    myLock['print'].release()
                    somChat()
                elif msgRecA[0] == "Stop":
                    print 'finalizando recServer'
                    break
                elif msgRecA[0] == "ErroServidor":
                    print msgRecA[1]
                    connS.close()
                    break
        except Exception as e:
            print('Um erro ocorreu!')
            print e
            break

