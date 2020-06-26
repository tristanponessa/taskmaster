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

def str_padding(lst, pad):

    for i in range(len(lst)):
        lst[i] = str(lst[i])
        lst[i] = lst[i].ljust(pad[i], ' ')
    return lst
"""
def setup_files():
    #create files if dont exist
    with open(log_file, 'a+') as f:pass
    with open(history_file, 'a+') as f:pass
    with open(pss_file, 'w+') as f:pass
    with open(pss_json, 'w+') as f:pass
    with open(tk_res, 'w+') as f:pass
"""
    
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
        

