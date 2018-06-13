from multiprocessing import Process, Value, Array
import time

def f(n, a):
    time.sleep(3)
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = -a[i]
    time.sleep(3)
    print "teste"