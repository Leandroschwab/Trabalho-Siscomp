# -*- coding: utf-8 -*-
import time
from SocketIO import *
from Functions import *

print "Iniciando Cliente Paciente"

def cadastro():
    print "---------------------------"
    print "Iniciando Cadastro"
    print "---------------------------"
    data = []
    data.append("CadastroPaciente")
    x = raw_input("digite seu nome: ")
    data.append(x)
    x = raw_input("digite o nome de usuario")
    data.append(x)
    x = raw_input(" digite sua senha")
    data.append(x)
    x = raw_input("digite o nome o id: digite 1 para listar os medicos")
    while x == "1":
        x = raw_input("digite o id do medico:")
    data.append(x)
    sendServer(vetorToString(data))


def Login():
    print "---------------------------"
    print "Iniciando Login"
    print "---------------------------"
    data = []
    data.append("Login")
    print "Login iniciado"
    x = raw_input("digite o nome de usuario")
    data.append(x)
    x = raw_input(" digite sua senha")

def Menu1():
    while 1:

        x = raw_input("digite 1-login 2-cadastro: ")
        while (x!="1" and x!="2"):
            if (x!="1" and x!="2"):
                x = raw_input("voce digitou errado digite 1 para login 2 para cadastro: ")
        if x== "1":
            Login()
        if x== "2":
            cadastro()
        time.sleep(3)

Menu1()
