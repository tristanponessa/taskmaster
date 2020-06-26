import cmd
import threading
import time
import sys
import re
import itertools
import psutil
import os
import signal
import traceback
import subprocess
from datetime import datetime, timedelta

import Conf as confFILE
import Global


pss = dict()

def init_ps(psName, psProps):
    global pss
    pss[psName] = []
    
    nbps = int(confFILE.get_psProp(psName, 'nbps'))
    for i in range(nbps):
        psNew = Process(psName, psProps)
        if confFILE.get_psProp(psName, 'autostart') == "yes": 
            psNew.start_ps()
            #Global.printx(f"{psName} : autostart")
            
        pss[psName].append(psNew)

        Global.printx(f"INIT {psNew}")

def destroy_ps(psName):
    #kills and removes from lst
    global pss
    inst_lst = pss[psName]
    for inst_elem in inst_lst:
        inst_elem.kill_if_psInit()
        del pss[psName]

        #LOG
        Global.printx(f"DESTROY {psName}")


def init_pss():
    global pss

    pssk = pss.keys()
    confk = confFILE.conf.keys()
    keys = set([*pssk, *confk])

    Global.printx(f"cur pss : {pssk}")
    Global.printx(f"conf : {confk}")
    Global.printx(f"fusion set : {keys}")

    for key in keys:
        if (key in confk):
            if (key not in pssk):
                init_ps(key, confFILE.conf[key])
            elif (pss[key][0].props != confFILE.conf[key]):
                destroy_ps(key)
                init_ps(key, confFILE.conf[key])
        elif (key not in confk):
            destroy_ps(key)
        else:
            Global.printx(f"protected {key}")
    
def display_pss():
    global pss
    for ps in pss.values():
        print('\n')
        for inst in ps:
            print(inst)
    print('\n')

  
def ft_thread(ft):
    p = threading.Thread(target=ft)
    p.deamon = True
    p.start()
    return p
        

####################################################################################################################

class Process:
    """
        __next__  , __cmp__ depending of ps priority another for pids
        
        ps class:
            -stocks all information about ps
            -methods to proform on process start/stop/status
            -NO checking, log
            -executes a ps configuration on process
    
    """
    
    def __init__(self, name, props):

        self.name = name
        self.props = props
        self.psobj = None
        self.start_time = ''
        self.stop_call = False
    
    def setup_cmd(self):
        #umask 777 && cd .. && export v=1 && export v=2 && cmd'
        umask = f"umask {confFILE.get_psProp(self.name, 'umask')}"
        cd  = f"cd {confFILE.get_psProp(self.name, 'workdir')}"
        env_vars = [f'export {varname}={varval}' for varname,varval in confFILE.get_psProp(self.name, 'env').items()]

        setup_cmd = [umask, cd, *env_vars]
        setup_cmd = ' && '.join(setup_cmd)
        return setup_cmd

    def kill_if_psInit(self):
        if self.psInit():
            self.psobj.kill()

    def psInit(self):
        return (self.psobj is not None)

    def success_countdown(self):
        def ft():
            s = int(self.ps['timetillsuc'])
            name = self.ps['name']
            time.sleep(s)
            if self.exitcode is None:
                Global.print_file(f'{Global.now_time()} : {name} running for over {s}s, its working properly', Global.tk_res, 'a')

        t = ft_thread(ft)

    def stop_ps(self):
        if self.psInit() and self.stop_call == False:
            self.stop_call = True

            def ft():
                stoptime = int(confFILE.get_psProp(self.name, 'stoptime'))
                time.sleep(stoptime)
                self.psobj.kill()
                self.stop_call = False

            t = ft_thread(ft)
            return True

        return False
    
    def start_ps(self):
        
        if not self.psInit():

            self.start_time = int(time.time())
            #self.success_countdown()
            cmd = f"{self.setup_cmd()} && {confFILE.get_psProp(self.name, 'cmd')}"
            #LOG
            Global.printx(cmd)

            with open(confFILE.get_psProp(self.name, 'stdout'),'a+') as out, \
                 open(confFILE.get_psProp(self.name, 'stderr'),'a+') as err:
                    
                    self.psobj = subprocess.Popen(cmd, shell=True, stdout=out, stderr=err)
                    #Global.print_file(f"{self.ps['popen'].pid}", Global.pss_file, 'a')
                    
            return True
        return False
        

    
    def status_ps(self):
        
        name = self.name
        cmd = confFILE.get_psProp(self.name, 'cmd')
        state = '?'
        pid = self.psobj.pid if self.psInit() else None
        run_time = self.get_runtime(),
        returncode = self.psobj.poll() if self.psInit() else None
        lst = [name,cmd,state,pid,run_time,returncode]
        
        #LOG
        """
        msg = f"ps {cmd} ended  returncode:{returncode} expecting {self.ps['exitcode']}  "
        msg += 'fail'
        if str(returncode) == self.ps['exitcode']:
            msg += 'success'
        Global.print_file(msg, Global.tk_res, 'a')
        """

        #DISPLAY
        pad = [30,30,10,7,10,3]
        for i in range(len(lst)):
            lst[i] = str(lst[i])
            lst[i] = lst[i].ljust(pad[i], ' ')
   
        status_msg = "name:{} | cmd:{} | state: {} | PID:{} | runtime:{} | returncode:{} ".format(*lst)
        return status_msg

    def get_runtime(self):

        if not self.psInit():
            return

        epoch_ct = int(self.start_time)
        epoch_now = int(time.time())
        
        datetime_ct = datetime.fromtimestamp(epoch_ct)
        datetime_now = datetime.fromtimestamp(epoch_now)
        
        run_time = str(datetime_now - datetime_ct)
        return run_time
    
    """
    def auto_start(self):
        self.start_ps()
        Global.printx(f"AUTOSTART <{self.ps['name']}>")
    """

    
    def __str__(self):
        x = f'PS : {self.name} | obj : {self.psobj} | props : {self.props}'
        return x
    
        
#####################################################################################################################

