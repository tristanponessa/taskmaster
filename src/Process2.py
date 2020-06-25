import cmd
import threading
import time
from datetime import datetime, timedelta 
import sys
import re
import itertools
import psutil
import os
import signal
import traceback
import subprocess

import Conf as confFILE
import Global


pss = dict()

def init_pss(protected=None):
    global pss

    if protected is not None:
        for ps in pss:
            if ps.name not in protected:
                if ps.psInit():
                    ps.psobj.kill()
                    del pss[ps.name]
            else:
                ###add rest
    else:
        pss.clear()
    #only stop those who are active
    for psName,psProps in confFILE.conf.items():
        pss[ps] = []
        
        nbps = int(confFILE.get_psProp(psName, 'nbps'))
        for i in range(nbps):
            psNew = Process(psName)
            if confFILE.get_psProp(psName, 'autostart') == "yes": 
                psNew.start_ps()
                Global.printx(f"{psName} : autostart")
                
            pss[psName].append(psNew)


class Process:
    """
        __next__  , __cmp__ depending of ps priority another for pids
        
        ps class:
            -stocks all information about ps
            -methods to proform on process start/stop/status
            -NO checking, log
            -executes a ps configuration on process
    
    """
    
    def __init__(self, name):

        self.name = name
        self.psobj = None
        self.start_time = ''
        self.stop_call = False
    
    def setup_cmd(self):
        #umask 777 && cd .. && export v=1 && export v=2 && cmd'
        umask = self.get_prop('umask')
        cd  = f"cd {self.get_prop('work_dir')}"
        env_vars = [f'export {varname}={varval}' for varname,varval in self.get_prop('env').items()]

        setup_cmd = [umask, cd, *env_vars]
        setup_cmd = ' && '.join(setup_cmd)
        return setup_cmd


  

    def psInit(self):
        return (self.psobj is not None)


    def success_countdown(self):
        def ft():
            s = int(self.ps['timetillsuc'])
            name = self.ps['name']
            time.sleep(s)
            if self.exitcode is None:
                Global.print_file(f'{Global.now_time()} : {name} running for over {s}s, its working properly', Global.tk_res, 'a')

        t = Global.ft_thread(ft)

    def stop_ps(self):
        if self.psInit() and self.stop_call == False:
            self.stop_call = True

            def ft():
                stoptime = int(self.get_prop('stoptime'))
                time.sleep(stoptime)
                self.psobj.kill()
                self.stop_call = False

            t = Global.ft_thread(ft)
            return True

        return False
    
    def start_ps(self):
        
        if not self.psInit():

            self.start_time = int(time.time())
            self.success_countdown()
            cmd = f"{self.setup_cmd()} && {self.get_prop('cmd')}"

            with open(self.get_prop('stdout'),'a+') as out, \
                 open(self.get_prop('stderr'),'a+') as err:
                    
                    self.psobj = subprocess.Popen(self.get_prop('cmd'), shell=True, stdout=out, stderr=err)
                    #Global.print_file(f"{self.ps['popen'].pid}", Global.pss_file, 'a')
                    
            return True
        return False

    
    def status_ps(self):
        
        cmd = self.psobj.args
        pid = self.psobj.pid
        run_time = self.get_runtime(),
        returncode = self.psobj.poll()
        lst = [cmd,pid,run_time,returncode]
        
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
   
        status_msg = "name:{} | cmd:{} | state: {} | PID:{} | runtime:{} | exitcode:{} ".format(*lst)
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
    
    def auto_start(self):
        self.start_ps()
        Global.printx(f"AUTOSTART <{self.ps['name']}>")
  
    def __repr__(self):
        
        lst = []
        lst.append('\n')
        lst.append(f"PS {self.ps['name']}".center(50, '*'))
        for k,v in self.ps.items():
            lst.append(f'{k} : {v}')
        lst.append("".center(50, '*'))
        x = '\n'.join(lst)
        return x
        
        
#####################################################################################################################

