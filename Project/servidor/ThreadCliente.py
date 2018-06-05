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
        if msgRecA[0]== "CadastroPaciente":
            cadastroPaciente(msgRecA[1],msgRecA[2],msgRecA[3],msgRecA[4])
    conn.close()  # Fecha conexão
def cadastroMedico(nome,user,senha):
    conn = sqlite3.connect('db/server.db')
    cursor = conn.cursor()
    insert_stmt =("INSERT INTO Users (nome, usuario, senha, medico) VALUES ('"+nome+"','"+user+"','"+senha+"',1)")
    cursor.execute(insert_stmt)
    conn.commit()
    print "Servidou: Novo medico cadastrado com Sucesso "
    conn.close()

def cadastroPaciente(nome,user,senha,medicoid):
    conn = sqlite3.connect('db/server.db')
    cursor = conn.cursor()
    cursor.execute("SELECT medico FROM Users WHERE ID='"+medicoid+"';")
    data = cursor.fetchone()
    if data:
        if data[0]==1:
            insert_stmt =("INSERT INTO Users (nome, usuario, senha, medico,responsavel,autorizado) VALUES ('"+nome+"','"+user+"','"+senha+"',0,'"+medicoid+"',0)")
            cursor.execute(insert_stmt)
            conn.commit()
            print "Servidou: Novo Paciente cadastrado com Sucesso aguardando autorizaçao do medico"
            conn.close()
        else:
            print "usuario nao é medico"
    else:
        print "usuario nao existe"