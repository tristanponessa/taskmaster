
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

popen for commands
multiprocess for python processes defs
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
        self.ll = []
        
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
    
    """
    
    
    def do_run(self, person):
        #with open(self.data['stdout'], "w") as stdout_file, \
         #    open(self.data['stderr'], "w") as stderr_file:
        #self.run_process()
      
        
            #stderr_file = open(self.data['stderr'], "w")

        #other option get output in list than write list in file after closing file and temrinating 
        #l = lambda : subprocess.Popen("ping 127.0.0.1", shell=True, stdout=self.stdout_file)
        #self.running_proc.append(multiprocessing.Process(target=l))
        #self.running_proc[-1].start()

        self.ll = []
        
        self.run_process()
    
        print(self.ll)    
        print("running time")
        
    """
    
    #pain in the ass 
    #dont block readline , stocks every line from program stdout 
    #but blocks temrinal
    def do_run(self, run_processes) :
        self.run_processes()

    def run_processes(self):

        self.stdout_file = open(self.data['stdout'], "w")
        self.extra_file = open("extra.txt", "w")
        
        #self.px = Popen()
        self.p0 = multiprocessing.Process(name="PING_process", target=self.ping_process)

        self.read_ping_process()
        #p1 = multiprocessing.Process(name="PYTHONFOREVER_process", target=self.read_process)
        #p2 = multiprocessing.Process(name="LS_process", target=self.read_process)
        
        #self.px = subprocess.Popen(["ping", "127.0.0.1"])

        #out, err = px.communicate()
        
        #self.p0.start()
        #p1.run()
        #p2.run()

        """
        self.running_proc.append(multiprocessing.Process(name="ping_process", target=self.read_process))
        self.running_proc[-1].start()

        while True:        
            if self.running_proc[-1].is_alive() == False:
                break
        """
        

        #print("process over")
        #self.pp.kill()
        
    def read_ping_process(self):
        pass
        #if self.px.poll() is None:
        #    out, err = self.px.communicate()
        #    print(out)
        #else:
        #    print('no process')
    
    def ping_process(self):
        self.px = subprocess.Popen(["ping", "127.0.0.1"])
        print(self.px)
      
        """
        i = 0
        while self.pp.poll() is None and i < 3:
            t = self.pp.stdout.readline(1)
            self.ll.append(t)
            print('+ :', t, stdout=self.x_file, flush=True)
            #print(self.pp.poll())
            self.stdout_file.writeline('>>' + t)
            i += 1
        self.pp.kill()
        """
    
    def do_show(self, ll):
        print(self.ll)

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

