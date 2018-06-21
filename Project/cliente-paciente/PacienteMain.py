# -*- coding: utf-8 -*-
import time
from RecebeServer import *
from EnviaServer import *
from Functions import *

from threading import Thread, Lock, BoundedSemaphore, Semaphore


def cadastro(connS):
    myLock.acquire()
    print "---------------------------"
    print "Iniciando Cadastro"
    print "---------------------------"
    myLock.release()
    data = []
    data.append("CadastroPaciente")
    x = raw_input("digite seu nome: ")
    data.append(x)
    x = raw_input("digite o nome de usuario: ")
    data.append(x)
    x = raw_input("digite sua senha: ")
    data.append(x)
    x = raw_input("digite o nome o id: digite 1 para listar os medicos: ")
    while x == "1":
        x = raw_input("digite o id do medico: ")
    data.append(x)
    sendServer(connS, vetorToString(data))
    time.sleep(0.3)


def login(connS):
    myLock.acquire()
    print "---------------------------"
    print "Iniciando Login"
    print "---------------------------"
    print "Login iniciado"
    myLock.release()
    data = []
    data.append("LoginPaciente")
    x = raw_input("digite o nome de usuario: ")
    data.append(x)
    x = raw_input("digite sua senha: ")
    data.append(x)
    sendServer(connS, vetorToString(data))
    time.sleep(0.3)

def menu1(connS):
    #myLock.acquire()
    x = raw_input("digite 1-login 2-cadastro: ")
    #myLock.release()
    while (x != "1" and x != "2"):
        if (x != "1" and x != "2"):
            #myLock.acquire()
            x = raw_input("voce digitou errado digite 1 para login 2 para cadastro: ")
            #myLock.release()
    if x == "1":
        login(connS)
    if x == "2":
        cadastro(connS)
    time.sleep(0.3)

def menu2(connS):
    time.sleep(0.3)

if __name__ == "__main__":

    global varData
    varData = {}
    global myLock
    myLock = Semaphore()
    HOST = '127.0.0.1'  # The remote host
    PORT = 50007  # The same port as used by the server
    connS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # qw12IPv4,tipo de socket
    connS.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connS.connect((HOST, PORT))  # Abre uma conexão com IP e porta especificados
    myLock.acquire()
    print "Iniciando Cliente Paciente"
    print "Conectado"
    myLock.release()
    varData['logado'] = False


    t = Thread(target=recvServer, args=(connS,myLock,varData))
    t.start()
    time.sleep(0.3)
    while 1:
        if varData['logado'] == False :
            menu1(connS)
        if varData['logado']:
            menu2(connS)
