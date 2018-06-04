import time

print "Iniciando Cliente Paciente"
def cadastro():
    data = []
    data.append("aaa")
    print "cadastro iniciado"
    x = raw_input("digite seu nome: ")
    data.append(x)
    x = raw_input("digite o nome de usuario")
    data.append(x)
    x = raw_input(" digite sua senha")

while 1:
    x = raw_input("digite 1-login 2-cadastro: ")
    while (x!="1" and x!="2"):
        if (x!="1" and x!="2"):
            x = raw_input("voce digitou errado digite 1 para login 2 para cadastro: ")
    if (x=="1"):
        print "vc digitou 1"
    if (x=="2"):
        print "vc digitou 2"
        cadastro()
    time.sleep(3)
