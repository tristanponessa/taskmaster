import os
import signal 
import psutil
import threading

import Json as jsonFILE

log_file = 'taskmaster.log' #echo terminal
history_file = 'history.txt' #last cmds
pss_file = 'pss.txt' #all the pids of this session
#pss_res = #what was cleaned up
pss_json = 'pss.json'
tk_res = 'taskmaster_res.txt' #launch res of ps


reboot = False

def ft_thread(ft):
    p = threading.Thread(target=ft)
    p.deamon = True
    p.start()
    return p

def str_padding(lst, pad):

    for i in range(len(lst)):
        lst[i] = str(lst[i])
        lst[i] = lst[i].ljust(pad[i], ' ')
    return lst

def setup_files():
    #create files if dont exist
    with open(log_file, 'a+') as f:pass
    with open(history_file, 'a+') as f:pass
    with open(pss_file, 'w+') as f:pass
    with open(pss_json, 'w+') as f:pass
    with open(tk_res, 'w+') as f:pass
    
def printx(*args, end=None):
    """ stdout and file """
    for arg in args:
        print(arg, end=end)
        with open(log_file, 'a+') as f:
            print(arg, file=f, end=end)

def print_file(s, ifile, mode):
    with open(ifile, mode) as f:
        print(s, file=f)

def load_file(file):
    l = []
    with open(file, 'r') as f:
        l = f.readlines()
    return l

def save_file(lines, file, mode):
    lines = list(map(str, lines))
    with open(file, mode) as f:
        f.writelines(lines)
        
def is_conf_file(conf):
    err = []
    
    msg = f'error : config file <{conf}>'
    if not os.path.exists(conf):
        err.append(f"{msg} don't exist")
    if not conf.endswith('.json'):
        err.append(f"{msg} don't end with json")
    return err

def kill_leftover():
    """
        keep all dead ps as zombies 
        so the os dont give the pid to another
        or youll be killing outside ps
    """
    d = jsonFILE.load_json(pss_json)
    for pid,info in d.items():
        pid = int(pid)
        state = 'already dead'
        if psutil.pid_exists(pid):
            pp = psutil.Process(pid)
            state = pp.status()
            os.kill(pid, signal.SIGKILL)    
        printx(f"PID {pid} NAME {info['name']} CMD {info['cmd']} state > {state}")

