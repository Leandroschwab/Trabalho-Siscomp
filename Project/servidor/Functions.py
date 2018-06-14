# -*- coding: utf-8 -*-
import sqlite3

def newMedicoDB(id):
    connSQL = sqlite3.connect('db/' + str(id) + '.db')
    cursor = connSQL.cursor()
    cursor.execute("CREATE TABLE medico (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,tipo TEXT NOT NULL,mensagem TEXT NOT NULL,info TEXT);")

def newPacienteDB(id):

    connSQL = sqlite3.connect('db/' + str(id) + '.db')
    cursor = connSQL.cursor()
    cursor.execute("CREATE TABLE id" + str(id) +" (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,tipo TEXT NOT NULL,mensagem TEXT NOT NULL);")
    cursor.execute("CREATE TABLE id" + str(id) + "data (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,tipo TEXT NOT NULL,mensagem TEXT NOT NULL);")