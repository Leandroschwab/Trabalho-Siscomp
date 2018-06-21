# -*- coding: utf-8 -*-
import time
from RecebeServer import *
from Functions import *
from threading import Thread, Lock, BoundedSemaphore, Semaphore


def cadastro(connS):
    myLock.acquire()
    print "---------------------------"
    print "Iniciando Cadastro"
    print "---------------------------"
    myLock.release()
    data = []
    data.append("CadastroMedico")
    x = raw_input("digite seu nome: ")
    data.append(x)
    x = raw_input("digite o nome de usuario: ")
    data.append(x)
    x = raw_input("digite sua senha: ")
    data.append(x)
    sendServer(connS, vetorToString(data))
    time.sleep(0.3)


def login(connS):
    myLock.acquire()
    print "---------------------------"
    print "Iniciando Login"
    print "---------------------------"
    myLock.release()
    data = []
    data.append("LoginMedico")
    x = raw_input("digite o nome de usuario: ")
    data.append(x)
    x = raw_input("digite sua senha: ")
    data.append(x)
    sendServer(connS, vetorToString(data))
    time.sleep(0.3)

def authPacientes(connS):
    myLock.acquire()
    print "---------------------------"
    print "Iniciando authPaciente"
    print "---------------------------"
    print "Listando Pacientes Aguardando aprovacao"
    myLock.release()
    x="AuthPacienteList"
    sendServer(connS, x)
    time.sleep(0.3)
    myLock.acquire()
    data = []
    data.append("AuthPacienteID")
    x = raw_input("digite o id do usuario: ")
    data.append(x)
    myLock.release()
    sendServer(connS, vetorToString(data))
    time.sleep(0.3)

def listPacientes(connS):
    myLock.acquire()
    print "---------------------------"
    print "Iniciando Lista de pacientes"
    print "---------------------------"
    print "Listando Pacientes Aprovados"
    myLock.release()
    x="PacienteList"
    sendServer(connS, x)
    time.sleep(0.3)

def histPacientes(connS):
    myLock.acquire()
    print "---------------------------"
    print "Iniciando histPaciente"
    print "---------------------------"
    print "Listando Seus Pacientes"
    myLock.release()
    x="PacienteList"
    sendServer(connS, x)
    time.sleep(0.3)
    myLock.acquire()
    data = []
    data.append("PacienteHistorico")
    x = raw_input("digite o id do usuario que deseja ver o historico: ")
    data.append(x)
    myLock.release()
    sendServer(connS, vetorToString(data))
    time.sleep(0.3)


def menu1(connS):
    myLock.acquire()
    x = raw_input("digite 1-login 2-cadastro: ")
    myLock.release()
    while (x != "1" and x != "2"):
        if (x != "1" and x != "2"):
            time.sleep(0.5)
            #myLock.acquire()
            x = raw_input("voce digitou errado digite 1 para login 2 para cadastro: ")
            #myLock.release()
    if x == "1":
        login(connS)
    if x == "2":
        cadastro(connS)
    time.sleep(0.3)

def menu2(connS):
    #myLock.acquire()
    x = raw_input("digite 1-Autorizar Pacientes 2-listar pacientes: ")
    #myLock.release()
    while (x != "1" and x != "2" and x != "3"):
        if (x != "1" and x != "2" and x != "3"):
            time.sleep(0.5)
            #myLock.acquire()
            x = raw_input("voce digitou errado: ")
            #yLock.release()
    if x == "1":
        authPacientes(connS)
    if x == "2":
        listPacientes(connS)
    if x == "3":
        histPacientes(connS)
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
    print "Iniciando Cliente Medico"
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
