import os
import time

def vetorToString(vetor):
    i=0
    mensagem = vetor[i]
    for i in range(1,len(vetor)):
        mensagem += "-,-"
        mensagem += vetor[i]
        i += 1
    return mensagem

def somAlarm():
    os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (0.3, 850))
    time.sleep(0.1)
    os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (0.3, 850))
def somChat():
    os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (0.2, 600))
    time.sleep(0.1)
    os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (0.2, 700))
