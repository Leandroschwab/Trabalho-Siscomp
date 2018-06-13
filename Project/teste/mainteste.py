# -*- coding: cp1252 -*-
from multiprocessing import Process, Value, Array
import time
from teste2 import *


if __name__ == '__main__':
    num = Value('d', 0.0)
    arr = Array('i', range(10))
    print "Antes",num.value,arr[:]

    p = Process(target=f, args=(num, arr))
    p.start()
    r = Process(target=f, args=(num, arr))
    r.start()
    p.join() ##Bloqueia o pai até que o filho termine.
    r.join()
    print "Depois:"
    print num.value
    print arr[:]
