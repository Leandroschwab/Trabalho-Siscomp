# -*- coding: utf-8 -*-

import sqlite3
import time


def sendServer(connS, mensagem):
    connS.sendall(mensagem + "-+,+-")  # Envia dados


def newMedicoDB(idMedico): #ja esta protegido do lock
    connSQL = sqlite3.connect('db/' + str(idMedico) + '.db')
    cursor = connSQL.cursor()
    cursor.execute(
        "CREATE TABLE medico (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,tipo TEXT NOT NULL,mensagem TEXT ,recebido TEXT,paciente TEXT);")
    connSQL.close()

def authPacienteList(conn, myLock, idMedico):
    acquireReadLock(myLock)
    connSQL = sqlite3.connect('db/server.db')
    cursor = connSQL.cursor()
    cursor.execute("SELECT id, nome FROM Users WHERE responsavel = '" + str(idMedico) + "' and autorizado='0' ;")
    data = cursor.fetchall()
    connSQL.close()
    releaseReadLock(myLock)
    if data:
        for linha in data:
            sendServer(conn, "MsgListaAutoriza-,-SucessoLista-,-" + str(linha[0]) + "        " + str(linha[1]) + ";")
    else:
        sendServer(conn, "MsgListaAutoriza-,-FalhaLista-,-Nao tem pacientes esperando aprovacao")


def listPacienteDB(conn, myLock, idMedico):
    acquireReadLock(myLock)
    connSQL = sqlite3.connect('db/server.db')
    cursor = connSQL.cursor()
    cursor.execute("SELECT id, nome FROM Users WHERE responsavel = '" + str(idMedico) + "' and autorizado='1' ;")
    data = cursor.fetchall()
    connSQL.close()
    releaseReadLock(myLock)
    if data:
        for linha in data:
            sendServer(conn,
                       "MsgListaAprovados-,-SucessoLista-,-" + str(linha[0]) + "        " + str(linha[1]) + "-,-" + str(
                           linha[0]))
    else:
        sendServer(conn, "MsgListaAutoriza-,-FalhaLista-,-Nao tem pacientes esperando aprovacao")


def listPacienteHistorico(conn, myLock, idMedico, idPaciente):
    acquireReadLock(myLock)
    connSQL = sqlite3.connect('db/' + str(idMedico) + '.db')
    cursor = connSQL.cursor()
    cursor.execute("SELECT * FROM id" + str(idPaciente) + "data WHERE 1 ;")
    data = cursor.fetchall()
    connSQL.close()
    releaseReadLock(myLock)
    if data:
        for linha in data:
            sendServer(conn, "MsgListaHistorico-,-SucessoLista-,-" + str(linha[2]) + "        " + str(
                linha[3]) + "        " + str(linha[4]) + "        " + str(linha[5]) + ";")
    else:
        sendServer(conn, "MsgListaAutoriza-,-FalhaLista-,-Nao foi encontrado historico")


def saveChatToPaciente(myLock, idMedico, idPaciente, mensagem):
    acquireWriteLock(myLock)
    connSQL = sqlite3.connect('db/' + str(idMedico) + '.db')
    cursor = connSQL.cursor()
    insert_stmt = ("INSERT INTO id" + str(
        idPaciente) + "chat (destinatario, mensagem, recebido) VALUES ('" + idPaciente + "','" + mensagem + "','0')")
    cursor.execute(insert_stmt)
    connSQL.commit()
    connSQL.close()
    releaseWriteLock(myLock)


# fim das funçoes medico
# inicio funçoes Paciente
def listMedicoDB(conn, myLock):
    acquireReadLock(myLock)
    connSQL = sqlite3.connect('db/server.db')
    cursor = connSQL.cursor()
    cursor.execute("SELECT id, nome FROM Users WHERE medico='1' ;")
    data = cursor.fetchall()
    connSQL.close()
    releaseReadLock(myLock)
    if data:
        for linha in data:
            sendServer(conn,
                       "MsgListaMedicos-,-SucessoLista-,-" + str(linha[0]) + "        " + str(linha[1]))
    else:
        sendServer(conn, "MsgListaMedicos-,-FalhaLista-,-nao existem medicos")

def newPacienteDB(conn, myLock, idMedico, idPaciente):
    acquireWriteLock(myLock)
    connSQL = sqlite3.connect('db/server.db')
    cursor = connSQL.cursor()
    cursor.execute("SELECT * FROM Users WHERE id='" + idPaciente + "';")
    data = cursor.fetchone()
    if data:  # verifica se ja existe este usuario
        if data[5] == str(idMedico):  # verifica se o medico é o responsavel
            if data[6] == 0:  # verifica se o usuario ja foi autorizado
                # atualiza a tabela geral do servidor
                cursor.execute("UPDATE Users SET autorizado = '1' WHERE id = '" + str(idPaciente) + "';")
                connSQL.commit()
                # cria tabelas no bando de dados do medico
                connSQL2 = sqlite3.connect('db/' + str(idMedico) + '.db')
                cursor = connSQL2.cursor()
                cursor.execute("CREATE TABLE id" + str(
                    idPaciente) + " (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,tipo TEXT NOT NULL,mensagem TEXT NOT NULL);")
                cursor.execute("CREATE TABLE id" + str(
                    idPaciente) + "data (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,hora TEXT NOT NULL,batimentos TEXT NOT NULL,pressao TEXT NOT NULL,temperatura TEXT NOT NULL,local TEXT NOT NULL);")
                cursor.execute("CREATE TABLE id" + str(
                    idPaciente) + "chat (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,destinatario TEXT NOT NULL,mensagem TEXT NOT NULL,recebido TEXT NOT NULL);")
                connSQL2.commit()
                connSQL2.close()
                ############################
                sendServer(conn,
                           "MsgAutoriza-,-SucessoAutoriza-,-Paciente " + str(data[1]) + " Autorizado com sucesso")
            else:
                print "Servidou: medico tentou autorizar o paciente novamente"
                sendServer(conn, "MsgAutoriza-,-FalhaAutoriza-,-Este paciente ja foi autorizado")
        else:
            print "Servidou: Medico Tentou autorizar paciente errado"
            sendServer(conn, "MsgAutoriza-,-FalhaAutoriza-,-Id usuario incorreto")
    else:
        print "Servidou: Usuario nao existe"
        sendServer(conn, "MsgAutoriza-,-FalhaAutoriza-,-Id usuario incorreto")
    connSQL.close()
    releaseWriteLock(myLock)

def saveSensorSQL(myLock, idPaciente, idMedico, dataehora, batimento, pressaoSTR, temperatura, local):
    acquireWriteLock(myLock)
    connSQL = sqlite3.connect('db/' + str(idMedico) + '.db')
    cursor = connSQL.cursor()
    insert_stmt = (
            "INSERT INTO id" + str(
        idPaciente) + "data (hora, batimentos, pressao, temperatura,local) VALUES ('" + dataehora + "','" + batimento + "','" + pressaoSTR + "','" + temperatura + "','" + local + "')")
    cursor.execute(insert_stmt)
    connSQL.commit()
    connSQL.close()
    releaseWriteLock(myLock)
    print " Sensores Salvos BD"


def saveMensagemMedico(idMedico, tipo, mensagem, idPaciente):# ja esta protegido  de lock
    connSQL = sqlite3.connect('db/' + str(idMedico) + '.db')
    cursor = connSQL.cursor()
    insert_stmt = (
            "INSERT INTO medico (tipo, mensagem, recebido, paciente) VALUES ('" + tipo + "','" + mensagem + "','0','" + str(
        idPaciente) + "')")
    cursor.execute(insert_stmt)
    connSQL.commit()
    connSQL.close()

def saveChatToMedic(myLock, idMedico, idPaciente, mensagem):
    acquireWriteLock(myLock)
    connSQL = sqlite3.connect('db/' + str(idMedico) + '.db')
    cursor = connSQL.cursor()
    insert_stmt = ("INSERT INTO id" + str(
        idPaciente) + "chat (destinatario, mensagem, recebido) VALUES ('" + idMedico + "','" + mensagem + "','0')")
    cursor.execute(insert_stmt)
    connSQL.commit()
    connSQL.close()
    releaseWriteLock(myLock)


# LeitorEscritor

def acquireReadLock(myLock):
    #print 'pegando read lock'
    while 1:# verifica se existe algum escritor e se o atingiu o numero maximo de leitores
        myLock['mutex'].acquire()
        if (myLock['escritor'] == 0 and myLock['leitores'] < 5):
            myLock['leitores'] += 1
            myLock['mutex'].release()
            break
        else:
            myLock['mutex'].release()
            time.sleep(0.01)
    #print 'pegou read lock'

def releaseReadLock(myLock):
    #print "liberou read lock"
    myLock['mutex'].acquire()
    myLock['leitores'] -= 1
    myLock['mutex'].release()

def acquireWriteLock(myLock):

    print 'pegando write lock'
    while 1:#verifica se ja existe algum escritor
        myLock['mutex'].acquire()
        if (myLock['escritor'] == 0):
            myLock['escritor'] = 1
            myLock['mutex'].release()
            break
        else:
            myLock['mutex'].release()
            time.sleep(0.01)
    while 1:#espera todos leitores acabarem
        myLock['mutex'].acquire()
        if (myLock['leitores'] == 0):
            myLock['mutex'].release()
            break
        else:
            myLock['mutex'].release()
            time.sleep(0.01)
    print 'pegou write lock'


def releaseWriteLock(myLock):
    print "liberou write lock"
    myLock['mutex'].acquire()
    myLock['escritor'] = 0
    myLock['mutex'].release()
