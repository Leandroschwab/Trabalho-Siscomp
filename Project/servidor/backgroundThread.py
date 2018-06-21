import time
import sqlite3
from Functions import *

def backGrondMedico(conn, myLock, idMedico):
    print "Rodando backGround Thread"
    while 1:
        connSQL = sqlite3.connect('db/' + str(idMedico) + '.db')
        cursor = connSQL.cursor()
        cursor.execute("SELECT * FROM medico WHERE recebido = '0' ;")
        data = cursor.fetchall()
        if data:
            for linha in data:
                print linha
                sendServer(conn,str(linha[1])+"-,-"+str(linha[2])+"-,-"+str(linha[3]))
                cursor.execute("UPDATE medico SET recebido = '1' WHERE id = '" + str(linha[0]) + "';")
                connSQL.commit()


