import threading

f = 0

print(f)

def d():
    global f
    f = 1

p = threading.Thread(target=d)
p.deamon = True
p.start()
p.join()

print(f)

print('multiprocess')

import multiprocessing

x = 0

print(x)

def l():
    global x
    x = 1

p = multiprocessing.Process(target=l)
p.start()
p.join()

print(x)