##https://stackoverflow.com/questions/9382045/send-a-file-through-sockets-in-python
import socket
import sys


def enviarArquivo(conn,nomeArquivo):
    try:
        f = open("doc.pdf", "rb")
        l = f.read(1024)
        while (l):
            conn.send(l)
            l = f.read(1024)
        f.close()
    except Exception as e:
        print('Um erro ocorreu ao enviar o arquivo!')
        print e

