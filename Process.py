import cmd
import subprocess
import multiprocessing
import threading
import configparser
import time
from datetime import datetime, timedelta 
import sys
import re
import itertools
import psutil
import os
import signal
import traceback



def ps_exists(self):
        if self.program['pid']() == -1:
            return False
        return True
        
def thread_fun(self, fun):
    p = multiprocessing.Process(target=fun)
    p.start()

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


def ps_exists(ps):
    
    if (ps is None) or 
       (not ps.is_running()):
        return False
    return True

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


def status_ps(self, ps):

    lst = [
            self.program['name'],
            self.program['cmd'],
            self.program['status'](),
            self.program['pid'](),
            self.program['run_time']()
          ]
    
    status_msg = "{} : {}       state: {}      PID:{} runtime:{}".format(*lst)
    return status_msg

def get_ps_infos(self, ps):
    """
        ps_iter contains all the info of a ps given by the os
    """
    fields = ["cmdline", "pid", "create_time", "status"]
    for cur_ps in psutil.process_iter(attrs=fields):
        cur_ps = cur_ps.as_dict(attrs=fields)
        if cur_ps['cmdline'] == self.program['cmdp']:
            return cur_ps
    return None

def get_ps_info(self, info):
    """
        ps_iter contains all the info of a ps given by the os
    """
    cur_ps = self.get_ps_infos()
    
    if cur_ps is None:
        if info == 'pid': return -1
        else:             return None
    
    if  info == 'run_time':    return self.get_runtime()
    elif info == 'pid':        return int(cur_ps[info])
    else:                      return cur_ps[info]

def get_runtime(self):
    
    epoch_ct = int(self.program['create_time']())
    epoch_now = int(time.time())
    
    datetime_ct = datetime.fromtimestamp(epoch_ct)
    datetime_now = datetime.fromtimestamp(epoch_now)
    
    run_time = str(datetime_now - datetime_ct)
    return run_time

def auto_start(self):
    self.start_ps()
    Global.printx(f"AUTOSTART <{self.program['name']}>")

def set_umask(self):
    os.umask(self.program['umask'])
    Global.printx(f"umask set to :{self.program['umask']}")
    
