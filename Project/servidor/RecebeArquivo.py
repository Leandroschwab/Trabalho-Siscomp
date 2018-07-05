#https://stackoverflow.com/questions/9382045/send-a-file-through-sockets-in-python
import socket
import sys
def receberArquivo(conn,nomeArquivo):
    f = open('file_'+ nomeArquivo,'wb') #open in binary
    # recibimos y escribimos en el fichero
    l = conn.recv(1024)
    while (l):
            f.write(l)
            l = sc.recv(1024)
    f.close()




