import time
import sys
from cmd import Cmd
import keyword
import psutil

import multiprocessing as mp 


class X:
    
    p = psutil.Popen(cmd) #cmd
    
    #GENERAL INSTANCE OF 
    runtime = 
    coutndown = 
    
    
    
    STOP -> coutndowm + kill popen
    
    START ->
    
    EXIT -> wait for exitcode
    






def ft_sleep(self, q, nb):
                    
    for i in range(nb):
        self.pipe['msg'].put(f'sec {i}')
        q.put(f'sec {i}')
        time.sleep(1)
                        
def ft_popen(self, q, cmd):
    p = psutil.Popen(cmd)
    q.put(p)
                    
                    
                    
                    
class xProcess:
    
    def __init__(self):
        pss = []
    
    def t(self):
        p = psutil.Popen("sleep 50")
        self.q.put(p)
    
    def ft_sleep(self, q, nb):
        time.sleep(nb)
        
        
    
    def ft_popen(self, cmd):
        p = psutil.Popen(cmd)
    
    def launch_fts(self, *fts):
        for ft in fts:
            ft()
    
    def start_ps(self, *fts):
        ps = mp.Process(target=launch_fts )
            
    def create_ps(self, tag, ft, args):
        p = mp.Process(target=ft, args=args)
        self.pss[tag] = {'obj': p, 'queue': mp.Queue()}
        
        
        self.pss[tag] = Target(tag, ft, args)
        
        create_ps('stop1', ft_popen, )
        
        > info stop
        print self.pss['stop1'].pipe['msg']
        
        
        
        
        
        
        
        
        
        #display stop sleep
        self.pss[tag]
        
        class Target:
            
            def __init__(self, tag, ft, args):
                p = mp.Process(target=ft, args=args)
                self.obj = p 
                self.pipe = mp.Queue()
                self.
                
                self.pipe = {'obj':mp.Queue() , 'msg':mp.Queue()}
                
            def ft_pipe(self, option):
                """
                    displaying an empty q can break std
                """
                x = ''
                if not self.pipe[option].empty():
                    x = self.pipe[option].get()
                return x
                
                
                
            
        
    
    def ps_mng(self, action):
        if action == 'start':
            ps.start()
        if action == 'stop':
            ps.stop()
            
    """
    #class Process:
    def example_wait(self):
        for i in range(2):
            self.q.put(f'sec {i}')
            #print(f'sec {i}')
            time.sleep(1)
        self.q.put('green flag')
        
    def example_x(self):
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
    """

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
