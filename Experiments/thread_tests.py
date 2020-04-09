from threading import Thread
import os
import math
import time


def calc():
    for i in range(0, 40000000):
        math.sqrt(i)


threads = []

start = time.time()

for i in range(4):
    print('registering thread %d' % i)
    threads.append(Thread(target=calc))

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print(time.time() - start)