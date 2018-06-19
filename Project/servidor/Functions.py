# -*- coding: utf-8 -*-
import sqlite3
import time


def sendServer(connS, mensagem):
    connS.sendall(mensagem + "-+,+-")  # Envia dados


def newMedicoDB(idMedico):
    connSQL = sqlite3.connect('db/' + str(idMedico) + '.db')
    cursor = connSQL.cursor()
    cursor.execute(
        "CREATE TABLE medico (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,tipo TEXT NOT NULL,mensagem TEXT ,recebido TEXT);")


def authPacienteList(conn, idMedico):
    connSQL = sqlite3.connect('db/server.db')
    cursor = connSQL.cursor()
    cursor.execute("SELECT id, nome FROM Users WHERE responsavel = '" + str(idMedico) + "' and autorizado='0' ;")
    data = cursor.fetchall()
    if data:
        for linha in data:
            sendServer(conn, "MsgListaAutoriza-,-SucessoLista-,-" + str(linha[0]) + "        " + str(linha[1]) + ";")
    else:
        sendServer(conn, "MsgListaAutoriza-,-FalhaLista-,-Nao tem pacientes esperando aprovacao")


# fim das funçoes medico
# inicio funçoes Paciente

def newPacienteDB(conn, idMedico, idPaciente):
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

def saveSensorSQL(myLock, idPaciente, idMedico, dataehora, batimento, pressaoSTR, temperatura, local):
    connSQL = sqlite3.connect('db/' + str(idMedico) + '.db')
    cursor = connSQL.cursor()
    insert_stmt = (
            "INSERT INTO id" + str(
                    idPaciente) + "data (hora, batimentos, pressao, temperatura,local) VALUES ('" + dataehora + "','" + batimento + "','" + pressaoSTR+ "','" + temperatura + "','"+local+"')")
    cursor.execute(insert_stmt)
    connSQL.commit()
    print " Sensores Salvos BD"

def saveMensagemMedico(myLock,idMedico,tipo,mensagem):
    connSQL = sqlite3.connect('db/' + str(idMedico) + '.db')
    cursor = connSQL.cursor()
    insert_stmt = (
            "INSERT INTO medico (tipo, mensagem, recebido) VALUES ('" + tipo + "','" + mensagem + "','0')")
    cursor.execute(insert_stmt)
    connSQL.commit()