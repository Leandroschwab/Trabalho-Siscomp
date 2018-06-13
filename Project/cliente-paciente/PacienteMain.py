# -*- coding: utf-8 -*-
import time
from SocketIO import *
from Functions import *
from threading import Thread, Lock, BoundedSemaphore, Semaphore


def cadastro(connS):
    printLock.acquire()
    print "---------------------------"
    print "Iniciando Cadastro"
    print "---------------------------"
    printLock.release()
    data = []
    data.append("CadastroPaciente")
    x = raw_input("digite seu nome: ")
    data.append(x)
    x = raw_input("digite o nome de usuario: ")
    data.append(x)
    x = raw_input("digite sua senha: ")
    data.append(x)
    x = raw_input("digite o nome o id: digite 1 para listar os medicos")
    while x == "1":
        x = raw_input("digite o id do medico: ")
    data.append(x)
    sendServer(connS, vetorToString(data))
    time.sleep(3)


def Login(connS):
    printLock.acquire()
    print "---------------------------"
    print "Iniciando Login"
    print "---------------------------"
    print "Login iniciado"
    printLock.release()
    data = []
    data.append("Login")
    x = raw_input("digite o nome de usuario")
    data.append(x)
    x = raw_input(" digite sua senha")


def Menu1(connS):
    x = raw_input("digite 1-login 2-cadastro: ")
    while (x != "1" and x != "2"):
        if (x != "1" and x != "2"):
            printLock.acquire()
            x = raw_input("voce digitou errado digite 1 para login 2 para cadastro: ")
            printLock.release()
    if x == "1":
        Login(connS)
    if x == "2":
        cadastro(connS)
    time.sleep(3)


if __name__ == "__main__":

    global varData
    varData = {}
    global PrintLock
    printLock = Semaphore()
    HOST = '127.0.0.1'  # The remote host
    PORT = 50007  # The same port as used by the server
    connS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # qw12IPv4,tipo de socket
    connS.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connS.connect((HOST, PORT))  # Abre uma conexão com IP e porta especificados
    printLock.acquire()
    print "Iniciando Cliente Paciente"
    print "Conectado"
    printLock.release()
    varData['login'] = False


    t = Thread(target=recvServer, args=(connS,printLock,varData))
    t.start()
    while 1:
        if varData['login']==False :
            Menu1(connS)
