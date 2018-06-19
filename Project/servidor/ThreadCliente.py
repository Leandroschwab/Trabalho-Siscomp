# -*- coding: utf-8 -*-
import sqlite3
from Functions import *
from threading import Thread, Lock, BoundedSemaphore, Semaphore
import time


def novaConn(conn, myLock):
    while 1:
        data = conn.recv(1024)  # Recebe os dados
        if not data: break
        print "Servidou recebeu data: " + str(data)
        msgRec = str(data).split("-+,+-")
        for linha in msgRec:
            msgRecA = linha.split("-,-")
            print "Servidou recebeu linha: " + str(linha)
            if msgRecA[0] == "CadastroMedico":
                cadastroMedico(conn, msgRecA[1], msgRecA[2], msgRecA[3])
            if msgRecA[0] == "CadastroPaciente":
                cadastroPaciente(conn, msgRecA[1], msgRecA[2], msgRecA[3], msgRecA[4])
            if msgRecA[0] == "LoginPaciente":
                loginPaciente(conn, myLock, msgRecA[1], msgRecA[2])
            if msgRecA[0] == "LoginMedico":
                loginMedico(conn, myLock, msgRecA[1], msgRecA[2])
            if msgRecA[0] == "ColetaSensores":
                recSensors(conn, msgRecA[1], msgRecA[2], msgRecA[3], msgRecA[4], msgRecA[5], msgRecA[6])

    conn.close()  # Fecha conexão


def medicoLogado(conn, myLock, idMedico):
    while 1:
        data = conn.recv(1024)  # Recebe os dados
        if not data: break
        print "Servidou recebeu data: " + str(data)
        msgRec = str(data).split("-+,+-")
        for linha in msgRec:
            msgRecA = linha.split("-,-")
            print "Servidou recebeu linha: " + str(linha)
            print "Servidou msgRecA: " + msgRecA[0]
            if msgRecA[0] == "AuthPacienteList":
                authPacienteList(conn, idMedico)
            if msgRecA[0] == "AuthPacienteID":
                newPacienteDB(conn, idMedico, msgRecA[1])


def pacienteLogado(conn, myLock, idPaciente, idMedico, nomeP):
    while 1:
        data = conn.recv(1024)  # Recebe os dados
        if not data: break
        print "Servidou recebeu data: " + str(data)
        msgRec = str(data).split("-+,+-")
        for linha in msgRec:
            msgRecA = linha.split("-,-")
            print "Servidou recebeu linha: " + str(linha)
            print "Servidou msgRecA: " + msgRecA[0]
            if msgRecA[0] == "ColetaSensores":
                recSensors(conn, myLock, idPaciente, idMedico, nomeP, msgRecA[1], msgRecA[2], msgRecA[3], msgRecA[4],
                           msgRecA[5], msgRecA[6])


def cadastroMedico(conn, nome, user, senha):
    connSQL = sqlite3.connect('db/server.db')
    cursor = connSQL.cursor()
    cursor.execute("SELECT usuario FROM Users WHERE usuario='" + user + "';")
    data = cursor.fetchone()
    if data:  # verifica se ja existe usuario cadastrado com mesmo nome
        sendServer(conn, "MsgCadastro-,-ErroCadastro-,-Este usuario ja existe")
    else:
        insert_stmt = (
                "INSERT INTO Users (nome, usuario, senha, medico) VALUES ('" + nome + "','" + user + "','" + senha + "',1)")
        cursor.execute(insert_stmt)
        connSQL.commit()
        cursor.execute("SELECT id FROM Users WHERE usuario='" + user + "';")
        data2 = cursor.fetchone()
        newMedicoDB(data2[0])
        print "Servidou: Novo Medico id: " + str(data2[0])
        sendServer(conn, "MsgCadastro-,-SucessoCadastro-,-Novo Medico cadastrado com Sucesso voce pode fazer o login")


def loginMedico(conn, myLock, user, senha):
    connSQL = sqlite3.connect('db/server.db')
    cursor = connSQL.cursor()
    cursor.execute("SELECT * FROM Users WHERE usuario='" + user + "';")
    data = cursor.fetchone()
    if data:  # verifica se ja existe este usuario
        if data[3] == senha:  # verifica se a senha esta correta
            if data[4] == 1:  # verifica se o usuario é medico
                print "Servidou: Usuario logou com sucesso"
                sendServer(conn, "MsgLogin-,-SucessoLogin-,-Paciente logado com sucesso")
                medicoLogado(conn, myLock, data[0])
            else:
                print "Servidou: paciente tentou fazer login no programa medico"
                sendServer(conn, "MsgLogin-,-FalhaLogin-,-Utilize o programa do Paciente")
        else:
            print "Servidou: Usuario errou a senha"
            sendServer(conn, "MsgLogin-,-FalhaLogin-,-Senha Incorreta")
    else:
        print "Servidou: Usuario nao existe"
        sendServer(conn, "MsgLogin-,-FalhaLogin-,-Usuario incorreto")


def cadastroPaciente(conn, nome, user, senha, medicoid):
    connSQL = sqlite3.connect('db/server.db')
    cursor = connSQL.cursor()
    cursor.execute("SELECT usuario FROM Users WHERE usuario='" + user + "';")
    data = cursor.fetchone()
    if data:  # verifica se ja existe usuario cadastrado com mesmo nome
        sendServer(conn, "MsgCadastro-,-ErroCadastro-,-Este usuario ja existe")
    else:
        cursor.execute("SELECT medico FROM Users WHERE ID='" + medicoid + "';")
        data = cursor.fetchone()
        if data:  # verifica se o numero do medico é valido
            if data[0] == 1:
                insert_stmt = (
                        "INSERT INTO Users (nome, usuario, senha, medico,responsavel,autorizado) VALUES ('" + nome + "','" + user + "','" + senha + "',0,'" + medicoid + "',0)")
                cursor.execute(insert_stmt)
                connSQL.commit()
                print "Servidou: Novo Paciente cadastrado com Sucesso aguardando autorizaçao do medico"
                sendServer(conn,
                           "MsgCadastro-,-SucessoCadastro-,-Novo Paciente cadastrado com Sucesso aguardando autorizaçao do medico")
            else:
                print "usuario nao é medico"
                sendServer(conn, "MsgCadastro-,-ErroCadastro-,-Medico nao encontrado")
        else:
            print "medico nao existe"
            sendServer(conn, "MsgCadastro-,-ErroCadastro-,-Medico nao encontrado")


def loginPaciente(conn, myLock, user, senha):
    connSQL = sqlite3.connect('db/server.db')
    cursor = connSQL.cursor()
    cursor.execute("SELECT * FROM Users WHERE usuario='" + user + "';")
    data = cursor.fetchone()
    if data:  # verifica se ja existe este usuario
        if data[3] == senha:  # verifica se a senha esta correta
            if data[4] == 0:  # verifica se o usuario nao é medico
                if data[6] == 1:  # verifica se o medico ja autorizou o paciente
                    print "Servidou: Usuario logou com sucesso"
                    sendServer(conn, "MsgLogin-,-SucessoLogin-,-Paciente logado com sucesso")
                    pacienteLogado(conn, myLock, data[0], data[5],data[1])
                else:
                    print "Servidou: Usuario nao autorizado"
                    sendServer(conn, "MsgLogin-,-FalhaLogin-,-Paciente Nao foi autorizado")
            else:
                print "Servidou: medico tentou fazer login no programa paciente"
                sendServer(conn, "MsgLogin-,-FalhaLogin-,-Utilize o programa do medico")
        else:
            print "Servidou: Usuario errou a senha"
            sendServer(conn, "MsgLogin-,-FalhaLogin-,-Senha Incorreta")
    else:
        print "Servidou: Usuario nao existe"
        sendServer(conn, "MsgLogin-,-FalhaLogin-,-Usuario incorreto")


def recSensors(conn, myLock, idPaciente, idMedico, nomeP, dataehora, batimento, pressao1, pressao2, temperatura, local):
    pressaoSTR = pressao1 + " - " + pressao2
    saveSensorSQL(myLock, idPaciente, idMedico, dataehora, batimento, pressaoSTR, temperatura, local)
    if int(batimento) > 80:
        mensagem = "Paciente " + nomeP + " esteve com batimento Cardiaco alto valor: " + batimento + " Horario: " + dataehora
        saveMensagemMedico(myLock, idMedico, "alertaSensorPaciente", mensagem)
        sendServer(conn, "alertaSensorPaciente-,- Seu batimento cardiaco esta acelerado, pls dont die")
    if int(pressao1)<10:
        mensagem = "Paciente " + nomeP + " esteve com pressao baixa valor: " + pressaoSTR  + " Horario: " + dataehora
        saveMensagemMedico(myLock, idMedico, "alertaSensorPaciente", mensagem)
        sendServer(conn, "alertaSensorPaciente-,- Sua pressao esta baixa, pls dont die")
    elif int(pressao1)>14:
        mensagem = "Paciente " + nomeP + " esteve com pressao alta valor: " + pressaoSTR  + " Horario: " + dataehora
        saveMensagemMedico(myLock, idMedico, "alertaSensorPaciente", mensagem)
        sendServer(conn, "alertaSensorPaciente-,- Sua pressao esta alta, pls dont die")
    if float(temperatura)<35.5:
        mensagem = "Paciente " + nomeP + " esteve com temperatura baixa valor: " + temperatura  + " Horario: " + dataehora
        saveMensagemMedico(myLock, idMedico, "alertaSensorPaciente", mensagem)
        sendServer(conn, "alertaSensorPaciente-,- Sua temperatura esta baixa, pls dont die")
    elif float(temperatura)>37.5:
        mensagem = "Paciente " + nomeP + " esteve com temperatura alta valor: " + temperatura + " Horario: " + dataehora
        saveMensagemMedico(myLock, idMedico, "alertaSensorPaciente", mensagem)
        sendServer(conn, "alertaSensorPaciente-,- Sua temperatura esta alta, pls dont die")