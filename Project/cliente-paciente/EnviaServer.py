# -*- coding: utf-8 -*-
import socket
import random
from datetime import datetime
from Functions import *
from threading import Thread, Lock, BoundedSemaphore, Semaphore
import time

def sendServer(connS, mensagem):
    connS.sendall(mensagem + "-+,+-")  # Envia dados


def backGroundTask(connS, myLock, varData):
    while 1:
        sensores(connS, myLock, varData)
        time.sleep(60)

def sensores(connS, myLock, varData):
    data = []
    data.append("ColetaSensores")
    data.append(str(datetime.now()))
    data.append(str(getBatimento()))
    valor = getPressao()
    data.append(str(valor[0]))
    data.append(str(valor[1]))
    data.append(str(getTemp()))
    data.append(str(getLocal()))
    data.append(str(datetime.now()))
    sendServer(connS, vetorToString(data))

def getBatimento():
    valor = 50
    if (random.randint(0, 100) <= 80):
        #print "batimento normal"
        valor += random.randint(0, 30)
    else:
        #print "batimento alto"
        valor += random.randint(30, 100)
    return valor

def getPressao():
    valor1 = 12
    aleatorio = random.randint(0, 100)
    if aleatorio <= 10:
        #print "pressao baixa"
        valor1 -= random.randint(2, 4)
        valor2 = valor1 - random.randint(2, 3)
    elif 10 < aleatorio <= 90:
        #print "pressao normal"
        valor1 += random.randint(-1, 1)
        valor2 = valor1 - random.randint(2, 4)
    else:
        #print "pressao alta"
        valor1 += random.randint(2, 4)
        valor2 = valor1 - random.randint(2, 4)
    return [valor1,valor2]

def getTemp():
    valor = 36.5
    aleatorio = random.randint(0, 100)
    if aleatorio <= 10:
        #print "temperatura baixa"
        valor += round(random.uniform(-2,-1.1), 1)#random.randrange(-2, -1.1,0.1)
    elif 10 < aleatorio <= 90:
        #print "temperatura normal"
        valor += round(random.uniform(-1,1), 1)#random.randrange(-1, 1,0.1)
    else:
        #print "temperatura alta"
        valor += round(random.uniform(1.1,4), 1)#random.randrange(1.1, 2,0.1)
    return valor

def getLocal():
    valor = random.randint(0, 100)
    return valor
