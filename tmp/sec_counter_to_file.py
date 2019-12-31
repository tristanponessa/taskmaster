import multiprocessing
import subprocess
import time 
from threading import Thread
from queue import Queue, Empty

class NonBlockingStreamReader:

    def __init__(self, stream):
        '''
        stream: the stream to read from.
                Usually a process' stdout or stderr.
        '''

        self._s = stream
        self._q = Queue()

        def _populateQueue(stream, queue):
            '''
            Collect lines from 'stream' and put them in 'quque'.
            '''

            while True:
                line = stream.readline()
                if line:
                    queue.put(line)
                else:
                    raise UnexpectedEndOfStream

        self._t = Thread(target = _populateQueue,
                args = (self._s, self._q))
        self._t.daemon = True
        self._t.start() #start collecting lines from the stream

    def readline(self, timeout = None):
        try:
            return self._q.get(block = timeout is not None,
                    timeout = timeout)
        except Empty:
            return None

class UnexpectedEndOfStream(Exception): pass

try:
    stdout_file = open('sec_counter.txt', "w+")
    p = subprocess.Popen(["python3", "sec_counter.py"], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

    t = []
    nbsr = NonBlockingStreamReader(p.stdout)
    while True:
        x = nbsr.readline(0.1)
        print(x)
        if x is not None:
            x = x.decode('ascii')
            t.append(x)
            print(t)

finally:
    stdout_file.writelines(t)
    p.kill()
    stdout_file.close()
    print('process done')


#try:
    #p.communicate(timeout=3)
  
#except subprocess.TimeoutExpired:  
 
