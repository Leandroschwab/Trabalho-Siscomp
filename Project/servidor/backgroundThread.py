import time
import sqlite3
from Functions import *

def backGrondMedico(conn, myLock, idMedico,varData):
    print "Rodando backGround Thread"
    while 1:
        if varData['ativo'] == False:
            print "finalizando background"
            break
        try:
            acquireReadLock(myLock)
            connSQL = sqlite3.connect('db/' + str(idMedico) + '.db')
            cursor = connSQL.cursor()
            cursor.execute("SELECT * FROM medico WHERE recebido = '0' ;")
            data = cursor.fetchall()
            releaseReadLock(myLock)
            if data:
                for linha in data:
                    print linha
                    sendServer(conn,str(linha[1])+"-,-"+str(linha[2])+"-,-"+str(linha[3]))
                    acquireWriteLock(myLock)
                    cursor.execute("UPDATE medico SET recebido = '1' WHERE id = '" + str(linha[0]) + "';")
                    connSQL.commit()
                    releaseWriteLock(myLock)
            if varData['chat'] != False:
                acquireReadLock(myLock)
                cursor.execute("SELECT * FROM id"+str(varData['chat'])+"chat WHERE destinatario = '"+str(idMedico)+"' and recebido = '0' ;")
                data = cursor.fetchall()
                releaseReadLock(myLock)
                if data:
                    for linha in data:
                        print linha
                        sendServer(conn,"MensagemChat-,-"+str(varData['chat'])+": "+str(linha[2]))
                        acquireWriteLock(myLock)
                        cursor.execute("UPDATE id"+str(varData['chat'])+"chat SET recebido = '1' WHERE id = '" + str(linha[0]) + "';")
                        connSQL.commit()
                        releaseWriteLock(myLock)
            connSQL.close()
        except Exception as e:
            print('Um erro ocorreu!')
            print e
            break

def backGrondPaciente(conn, myLock, idPaciente, idMedico,varData):
    print "Rodando backGround Thread"
    while 1:
        if varData['ativo'] == False:
            print "finalizando background"
            break
        try:
            if varData['chat'] != False:
                acquireReadLock(myLock)
                connSQL = sqlite3.connect('db/' + str(idMedico) + '.db')
                cursor = connSQL.cursor()
                cursor.execute("SELECT * FROM id"+str(idPaciente)+"chat WHERE destinatario = '"+str(idPaciente)+"' and recebido = '0' ;")
                data = cursor.fetchall()
                releaseReadLock(myLock)
                if data:
                    for linha in data:
                        print linha
                        acquireWriteLock(myLock)
                        sendServer(conn,"MensagemChat-,-"+str(idMedico)+": "+str(linha[2]))
                        cursor.execute("UPDATE id"+str(idPaciente)+"chat SET recebido = '1' WHERE id = '" + str(linha[0]) + "';")
                        connSQL.commit()
                        releaseWriteLock(myLock)
                connSQL.close()

        except Exception as e:
            print('Um erro ocorreu!')
            print e
            break