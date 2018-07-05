from playsound import playsound

def vetorToString(vetor):
    i=0
    mensagem = vetor[i]
    for i in range(1,len(vetor)):
        mensagem += "-,-"
        mensagem += vetor[i]
        i += 1
    return mensagem

def somAlarm():
    playsound('alarm.mp3')
def somChat():
    playsound('chat.mp3')
