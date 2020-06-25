import os
import signal 
import psutil
import threading
import time

import Json as jsonFILE

log_file = 'taskmaster.log' #echo terminal
history_file = 'history.txt' #last cmds
pss_file = 'pss.txt' #all the pids of this session
#pss_res = #what was cleaned up
pss_json = 'pss.json'
tk_res = 'taskmaster_res.txt' #launch res of ps
conf_file = 'config/taskmaster_conf.json'


reboot = False

def now_time():
    epoch_now = time.time()
    structtime_now = time.localtime(epoch_now)
    format_now = time.strftime("%Y-%m-%d %H:%M:%S", structtime_now)
    return format_now

def print_res_msg(msg, res, expect):
    if str(res) in expect:
        msg += 'success'
    else:
        msg += 'fail'
    
    Global.print_file(msg, Global.tk_res, 'a')

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

def check_exit():
    #get par id tk
    
    
    
