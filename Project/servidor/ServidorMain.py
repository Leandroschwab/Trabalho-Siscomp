# -*- coding: utf-8 -*-
import socket
from ThreadCliente import *
from threading import Thread, Lock, BoundedSemaphore, Semaphore

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPv4,tipo de socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT)) #liga o socket com IP e porta

myLock = Semaphore()
print "Servidor Rodando"
while 1:
    s.listen(1)  # espera chegar pacotes na porta especificada
    conn, addr = s.accept()  # Aceita uma conexão
    print "Aceitou mais um cliente"
    print 'Connected by', addr
    t = Thread(target=novaConn, args=(conn,myLock))
    t.start()

