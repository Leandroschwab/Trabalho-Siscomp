# -*- coding: utf-8 -*-
import sqlite3


def newMedicoDB(id):
    connSQL = sqlite3.connect('db/' + str(id) + '.db')
    cursor = connSQL.cursor()
    cursor.execute(
        "CREATE TABLE medico (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,tipo TEXT NOT NULL,mensagem TEXT NOT NULL,info TEXT);")


def authPacienteList(conn, idMedico):
    connSQL = sqlite3.connect('db/server.db')
    cursor = connSQL.cursor()
    cursor.execute("SELECT id, nome FROM Users WHERE responsavel = '" + str(idMedico) + "' and autorizado='0' ;")
    data = cursor.fetchall()
    if data:
        for linha in data:
            print(linha[0])
            print(linha[1])
            conn.sendall("MsgListaAutoriza-,-SucessoLista-,-" + str(linha[0]) + "        " + str(linha[1]) + ";")
    else:
        conn.sendall("MsgListaAutoriza-,-FalhaLista-,-Nao tem pacientes esperando aprovacao")


# fim das funçoes medico
# inicio funçoes Paciente

def newPacienteDB(id):
    connSQL = sqlite3.connect('db/' + str(id) + '.db')
    cursor = connSQL.cursor()
    cursor.execute("CREATE TABLE id" + str(
        id) + " (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,tipo TEXT NOT NULL,mensagem TEXT NOT NULL);")
    cursor.execute("CREATE TABLE id" + str(
        id) + "data (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,tipo TEXT NOT NULL,mensagem TEXT NOT NULL);")
