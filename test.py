import time
import sys
from cmd import Cmd
import keyword

from multiprocessing import Process, Pipe, Queue

class xProcess:
    
    
    
    def __init__(self):
        self.flag = '?'
        self.q = Queue()
    
    def wait(self):
        for i in range(2):
            self.q.put(f'sec {i}')
            #print(f'sec {i}')
            time.sleep(1)
        self.q.put('green flag')
        
    
        
        
    #class Process:
    def x(self):
        print('x go')
        _ = Queue()
        #p = Process(target=self.wait, args=(q,))
        p = Process(target=self.wait)
        p.start()
        #p.join()
        print('while go')
        i = 0
        for i in range(1000):
            
            x = ''
            if not self.q.empty():
                x = self.q.get()
            if x != '':
                print(x, end='')
            else:
                print('-', end='')
            
            
        print('end')


class MyPrompt(Cmd):
    prompt = '$> '
    intro = "Welcome! Type ? to list commands"

    def __init__(self):
        super().__init__()
        

    def emptyline(self):
        pass
      
    def do_exit(self, inp):
        print("Bye")
        return True
    
    def do_add(self, inp):
        print("adding '{}'".format(inp))

    def help_add(self):
        print("Add a new entry to the system.")

    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')

    
    def do_EOF(self, inp):
        print("EOF : ctrl+D")
        return self.do_exit(inp)
        
    def default(self, inp):
        print("command don't exist")
            


#if __name__ == '__main__':
#    main()

if __name__ == '__main__':
    p = xProcess()
    p.x()
    #MyPrompt().cmdloop()
