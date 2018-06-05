# -*- coding: utf-8 -*-
import socket

HOST = '127.0.0.1'  # The remote host
PORT = 50007  # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # qw12IPv4,tipo de socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect((HOST, PORT))  # Abre uma conexão com IP e porta especificados
print "Conectou"

def sendServer(mensagem):
    s.sendall(mensagem)  # Envia dados