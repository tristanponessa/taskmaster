
import cmd
import subprocess
import multiprocessing
import threading

"""
an infinite process increases a number and prints it 
taskmaster redirects this process output to a file
its taskmasters job to deal how its printed in the file
we must flush immediatley at every print
cuase by default it waits for the process to be
temrinated before printing
we use multiprocess so we can temrinate it at free will
threading we cant
"""

from threading import Thread
from queue import Queue, Empty
from time import sleep

import asyncio


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


class Taskmaster_shell(cmd.Cmd):
    
    prompt = '$> '
    intro = "Welcome! Type ? to list commands"
    
    FRIENDS = [ 'Alice', 'Adam', 'Barbara', 'Bob' ]
    
    def __init__(self):
        super().__init__()
        self.data = dict()
        self.stdout_file = None
        
        self.running_proc = []
        with open("config/.conf", "r") as f:
            lines = f.readlines()
        for line in lines:
            key, value = line.split('=')
            self.data[key] = value
        
        #create file
        open(self.data['stdout'], "a+").close()
        open(self.data['stderr'], "a+").close()

    def emptyline(self):
        pass
    
    def default(self, inp):
        print("command don't exist")
      
    def do_exit(self, inp):
        print("Bye")

        #for processn in self.running_proc:
        #   print(processn)
        #  processn.terminate()
        # processn.join()
            #processn.shutdown()
            #processn.kill()
        #self.stdout_file.close()
        
        return True#exit shell
    
    def do_run(self, person):
        #with open(self.data['stdout'], "w") as stdout_file, \
         #    open(self.data['stderr'], "w") as stderr_file:
        #self.run_process()
        self.stdout_file = open(self.data['stdout'], "w")
        
        #stderr_file = open(self.data['stderr'], "w")

        #other option get output in list than write list in file after closing file and temrinating 
        #l = lambda : subprocess.Popen("ping 127.0.0.1", shell=True, stdout=self.stdout_file)
        #self.running_proc.append(multiprocessing.Process(target=l))
        #self.running_proc[-1].start()

        self.ll = []
        
        self.run_process()
        """
        p = multiprocessing.Process(target=self.run_process)
        
        p.start()
        print(p)
        import time 
        time.sleep(4)
        p.terminate()
        p.join()
        print(p)
        """
        print(self.ll)
        
        #import time
        

        #self.running_proc.append(threading.Thread(target=l, name='x', daemon=True))
        #self.running_proc.append(threading.Thread(target=l, name='x'))
        
        print("running time")
        
    
    #pain in the ass 
    #dont block readline , stocks every line from program stdout 
    #but blocks temrinal
    def run_process(self):
        
        #self.pp = subprocess.Popen(["ls"],shell=True, stdout=subprocess.PIPE)
        self.pp = subprocess.Popen(["python3", "time_program.py"],stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE) #BLOCKING 


        #self.pp = subprocess.Popen(["ping 127.0.0.1"],shell=True, stdout=subprocess.PIPE)
        #self.pp = subprocess.Popen("ping 127.0.0.1",shell=True, stdout=subprocess.PIPE) #NON BLOCKING
        #print(self.pp.stdout.read())

        nbsr = NonBlockingStreamReader(self.pp.stdout)
        #print('after')
        #self.pp.wait()
        #t = self.pp.communicate()
        
        #you gotta put this as a separate process
        while self.pp.poll() is None:
            t = nbsr.readline(0.1)
            self.ll.append(t)
            print('+ :', t)
            print(self.pp.poll())
            #print(*self.ll, sep=' ')
            


        #print(self.pp.poll())
        #self.pp.kill()
        #self.pp.wait()
        print(self.pp.poll())
        
        
        #self.stdout_file = open(self.data['stdout'], "w")
        #process1 = subprocess.Popen("locate a", shell=True, stdout=subprocess.PIPE)
        #print(process1.stdout.read())
        #process1 = subprocess.Popen("python3 time_program.py", shell=True, stdout=subprocess.PIPE)
        #process1 = subprocess.Popen("locate a", shell=True, stdout=subprocess.PIPE)
        #process1 = subprocess.Popen(["python3", "time_program.py"], stdout=stdout_file)
        #l = lambda x: subprocess.Popen(["python3", "time_program.py"], stdout=stdout_file)
        #self.running_proc.append(multiprocessing.Process(target=l))
        #self.running_proc[-1].start()
        #shell=True seemed ot block
        #print('after')
        #process1.communicate()
        #print(process1.stdout.read())
        #p = psutil.Process(process1.pid)
        #p.suspend()
        #p.resume()
        

        """
        print(process1.stdout.read())
        output = process1.stdout.readline()
        process1.stdout.close()
        process1.kill()
        with open(self.data['stdout'], "w") as f:
            f.write(str(output))
        """
        #    stdout_file = open(self.data['stdout'], "w")
        #   stderr_file = open(self.data['stderr'], "w")
        #  process1 = subprocess.Popen("python3 time_program.py", shell=True, stdout=stdout_file ,stderr=stderr_file)
        #x = process1.communicate()
        #print(x)



    def complete_greet(self, text, line, begidx, endidx):
        if not text:
            completions = self.FRIENDS[:]
        else:
            completions = [f for f in self.FRIENDS if f.startswith(text)]
        return completions
    
    def do_EOF(self, line):
        return True

if __name__ == '__main__':

    ts = Taskmaster_shell()
    try:
        ts.cmdloop()
    except KeyboardInterrupt:
        print('\n\n  Ctrl + c -> exiting shell')



"""
from subprocess import Popen, PIPE
from time import sleep
from nbstreamreader import NonBlockingStreamReader as NBSR

# run the shell as a subprocess:
p = Popen(['python', 'shell.py'],
        stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = False)
# wrap p.stdout with a NonBlockingStreamReader object:
nbsr = NBSR(p.stdout)
# issue command:
p.stdin.write('command\n')
# get the output
while True:
    output = nbsr.readline(0.1)
    # 0.1 secs to let the shell output the result
    if not output:
        print '[No more data]'
        break
    print output
"""