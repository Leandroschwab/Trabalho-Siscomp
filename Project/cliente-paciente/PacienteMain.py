# -*- coding: utf-8 -*-
import time
from RecebeServer import *
from EnviaServer import *
from EnviaArquivo import *

from Functions import *

from threading import Thread, Lock, BoundedSemaphore, Semaphore


def cadastro(connS,myLock):
    myLock['print'].acquire()
    print "---------------------------"
    print "Iniciando Cadastro"
    print "---------------------------"
    myLock['socket'].acquire()
    sendServer(connS,"MedicoList")
    myLock['socket'].release()
    print "listando medicos"
    myLock['print'].release()
    time.sleep(0.6)
    data = []
    data.append("CadastroPaciente")
    x = raw_input("digite seu nome: ")
    data.append(x)
    x = raw_input("digite o nome de usuario: ")
    data.append(x)
    x = raw_input("digite sua senha: ")
    data.append(x)
    x = raw_input("digite o nome o id do medico: ")
    data.append(x)
    myLock['socket'].acquire()
    sendServer(connS, vetorToString(data))
    myLock['socket'].release()
    time.sleep(0.3)


def login(connS,myLock):
    myLock['print'].acquire()
    print "--------------------------"
    print "Iniciando Login"
    print "---------------------------"
    myLock['print'].release()
    data = []
    data.append("LoginPaciente")
    x = raw_input("digite o nome de usuario: ")
    data.append(x)
    x = raw_input("digite sua senha: ")
    data.append(x)
    myLock['socket'].acquire()
    sendServer(connS, vetorToString(data))
    myLock['socket'].release()
    time.sleep(0.3)

def chat(connS,myLock):
    myLock['socket'].acquire()
    sendServer(connS, "ChatStart")
    myLock['socket'].release()
    time.sleep(0.5)
    myLock['print'].acquire()
    print "---------------------------"
    print "Iniciando Chat"
    print "---------------------------"
    myLock['print'].release()
    #myLock['print'].acquire()
    x = raw_input("digite sua mensagem ou digite 'exit' para sair: ")
    #myLock['print'].release()
    while (x != "exit"):
        time.sleep(0.3)
        men = "ChatCliente-,-"+x
        myLock['socket'].acquire()
        sendServer(connS, men)
        myLock['socket'].release()

        x = raw_input("")
    myLock['socket'].acquire()
    sendServer(connS, "ChatEnd")
    myLock['socket'].release()

    time.sleep(0.3)

def  enviaarq(connS, myLock):
    myLock['print'].acquire()
    print "---------------------------"
    print "Iniciando envio de arquio"
    print "---------------------------"
    myLock['print'].release()
    nomeArquivo = raw_input("digite o nome do arquivo ")
    myLock['socket'].acquire()
    men = "EnvioArquivo-,-"+nomeArquivo
    sendServer(connS, men)
    time.sleep(0.5)
    enviarArquivo(connS, nomeArquivo)
    time.sleep(0.1)
    myLock['socket'].release()

def menu1(connS,myLock ,varData):
    #myLock['print'].acquire()
    x = raw_input("digite 1-login 2-cadastro 0-sair: ")
    #myLock['print'].release()
    while (x != "1" and x != "2"):
        #myLock['print'].acquire()
        x = raw_input("voce digitou errado digite 1 para login 2 para cadastro 0 para sair: ")
        #myLock['print'].release()
    if x == "1":
        login(connS,myLock)
    if x == "2":
        cadastro(connS,myLock)
    if x == "0":
        varData['ativo'] = False
        myLock['socket'].acquire()
        sendServer(connS, "Stop")
        myLock['socket'].release()
    time.sleep(0.3)

def menu2(connS,myLock,varData):
    #myLock['print'].acquire()
    x = raw_input("digite 1-iniciar chat com medico 2-enviar arquivo 0-sair: ")
    #myLock['print'].release()
    while (x != "1"  and x != "2" and x != "0"):
            #myLock['print'].acquire()
            x = raw_input("voce digitou errado digite 1 para iniciar chat 2-enviar arquivo 0-sair: ")
            #myLock['print'].release()
    if x == "1":
        chat(connS,myLock)
    if x == "2":
        enviaarq(connS, myLock)
    if x == "0":
        varData['ativo'] = False
        myLock['socket'].acquire()
        sendServer(connS, "Stop")
        myLock['socket'].release()
    time.sleep(0.3)

if __name__ == "__main__":

    global varData
    varData = {}
    varData['ativo'] = True
    global myLock
    myLock = {}
    myLock['print'] = Semaphore()
    myLock['socket'] = Semaphore()

    HOST = '127.0.0.1'  # The remote host
    PORT = 50999  # The same port as used by the server
    connS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # qw12IPv4,tipo de socket
    connS.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connS.connect((HOST, PORT))  # Abre uma conexão com IP e porta especificados
    myLock['print'].acquire()
    print "Iniciando Cliente Paciente"
    print "Conectado"
    myLock['print'].release()
    varData['logado'] = False
    t = Thread(target=recvServer, args=(connS,myLock,varData)) # inicia o thread que recebe informacoes do servidor
    t.start()
    time.sleep(0.3)
    while 1:
        if varData['ativo'] == False:
            break
        try:
            if varData['logado'] == False :
                menu1(connS,myLock,varData)
            if varData['logado']:
                menu2(connS,myLock,varData)
        except Exception as e:
            print('Um erro ocorreu!')
            print e
            break
    x = raw_input("finalizando o programa")
    connS.close()