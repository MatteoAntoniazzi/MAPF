from multiprocessing import Process
import os
import math
import time


def calc():
    for i in range(0, 400000000):
        math.sqrt(i)


if __name__ == '__main__':

    threads = []

    start = time.time()

    for i in range(7):
        print('registering process %d' % i)
        threads.append(Process(target=calc))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print(time.time() - start)