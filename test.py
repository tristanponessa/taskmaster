import multiprocessing
import psutil
import time

"""
def prg_cmd(ch_conn):
    p = psutil.Popen(["sleep", "3"])
    fields = ["cmdline", "name",  "pid", "create_time", "status"]
    for cur_ps in psutil.process_iter():
        cur_ps = cur_ps.as_dict(attrs=fields)
        
        if cur_ps['pid'] == p.pid:
            print('this')
            ch_conn.send(cur_ps)
"""

"""
pr = dict()
pr['nbpr'] = 8
pr['cmdp'] = ["sleep", "10"]


class Process:
    
    def __init__(self):
        
        self.
        
        #multiple popen
        
        

def start_ps(pr, ps):
    
    if not ps_exists(ps):
        with open(pr['stdout'],'a+') as out, \
             open(pr['stderr'],'a+') as err:
            #if self.program['umask'] != -1:
                ps = psutil.Popen(pr['cmdp'], stdout=out, stderr=err)
    return ps
    
def stop_ps(self):
    #if self.get_ps_info('cmdline') != "":
    if self.ps_exists() and self.program['stop_call'] == False:
        self.program['stop_call'] = True
        def x():
            time.sleep(self.program['stoptime'])
            if self.program['pid']() > 0:#not necessary if -1 kills session
                os.kill(self.program['pid'](), signal.SIGKILL)
            self.program['stop_call'] = False
        
        self.thread_fun(x)
        
        return True
    return False

def prg_ps():
    par_conn, ch_conn = multiprocessing.Pipe()
    p = psutil.Popen(pr['cmdp'], stdout=out, stderr=err)


pss_lst = gen_ps_lst(pr)

def gen_pss_lst(pr):
    par_conn, ch_conn = multiprocessing.Pipe()
    p = lambda : psutil.Popen(pr['cmdp'], stdout=pr['stdout'], stderr=pr['stderr'])
    x = multiprocessing.Process(target=p, args=(ch_conn,)) 
    return [x] * pr['nbpr']

def get_infos(ps):
    
    
def stop_ps(pr, ps):
    
    
    
pss = 
"""



#print("popen pid >  ", p)
par_conn, ch_conn = multiprocessing.Pipe()

x = multiprocessing.Process(target=fun, args=(ch_conn,))

#par_conn.close()
x.start()
print(">>", par_conn.recv())
x.join()

print("multips pid >", x.pid)

while x.is_alive():
    print("alive ", x.pid)
    time.sleep(1)
    
    #print("alive ", x.status())
print('finish')