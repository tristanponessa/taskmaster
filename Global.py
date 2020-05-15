import os
import signal 
import psutil

log_file = 'taskmaster.log' #echo terminal
history_file = 'history.txt' #last cmds
pss_file = 'pss.txt' #all the pids of this session
tk_res = 'taskmaster_res.txt' #launch res of ps

reboot = False

def setup_files():
    #create files if dont exist
    with open(log_file, 'a+') as f:pass
    with open(history_file, 'a+') as f:pass
    with open(pss_file, 'w+') as f:pass
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
    pids = load_file(pss_file)
    for pid in pids:
        pid = int(pid)
        if psutil.pid_exists(pid):
            printx(f'{pid} state > {psutil.Process(pid).status()}')
            os.kill(int(pid), signal.SIGKILL)
        else:
            printx(f'{pid} state > already dead')

    