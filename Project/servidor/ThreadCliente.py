# -*- coding: utf-8 -*-
import sqlite3



def novaConn(conn):
    while 1:
        data = conn.recv(1024)  # Recebe os dados
        if not data: break
        print "Servidou recebeu: " + str(data)
        msgRec = str(data)
        msgRecA = msgRec.split("-,-")
        print "Servidou msgRecA: " + msgRecA[0]
        if msgRecA[0]== "CadastroMedico":
            cadastroMedico(msgRecA[1],msgRecA[2],msgRecA[3])
    conn.close()  # Fecha conexão
def cadastroMedico(nome,user,senha):
    conn = sqlite3.connect('db/server.db')
    cursor = conn.cursor()
    insert_stmt =("INSERT INTO Users (nome, user, senha, medico) VALUES ('"+nome+"','"+user+"','"+senha+"','true')")
    cursor.execute(insert_stmt)
    conn.commit()
    print "Servidou: Novo medico cadastrado com Sucesso "
    conn.close()