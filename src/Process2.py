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

import Json as jsonFILE
import Global

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
        
        self.ps = props.copy()
        self.default_vals(name, props)
        self.psobj = None
        
        ####################################################################        
        
        #self.pss = [None] * self.ps['nbps']
        #if self.ps['umask'] != -1:        self.set_umask()
        
        
        #self.success_countdown()
    umask 'umask {umask}'
    cd 'cd {working_dir}'
    env = 'export {VARNAME}={}'

    join '&& '.cmds



    def success_countdown(self):
        def ft():
            s = int(self.ps['timetillsuc'])
            name = self.ps['name']
            time.sleep(s)
            if self.exitcode is None:
                Global.print_file(f'{Global.now_time()} : {name} running for over {s}s, its working properly', Global.tk_res, 'a')

        t = Global.ft_thread(ft)

            

    def default_vals(self, ps_name, conf):
    
        dft =   {
                    'cmd':          'sh sec_counter.bash',
                    'nbps':         '1',
                    'timetillsuc':  '0',
                    'autostart':    'no',
                    'autorestart':  'no',
                    'stoptime':     '0',
                    'dir':          './',
                    'env':          "",
                    'stdout':       f'./{ps_name}.stdout',
                    'stderr':       f'./{ps_name}.stderr',
                    'nbretries':    '0',#if crashes, restarts
                    'exitsignal':   '15',#SIGTERM
                    'exitcode':     '0',
                    'umask':        '022'
                }
        
        for k,v in dft.items():
            if k not in self.ps:
                self.ps[k] = v 
    
    """
    def convert_types(self, ps):
        for key,val in ps.items():
            if val.isnumeric():
                ps[key] = int(ps[key])
    """
           
    
    def stop_ps(self):
        if self.ps_exists() and self.ps['stop_call'] == False:
            self.ps['stop_call'] = True 
            
            def ft():
                stopt = int(self.ps['stoptime'])
                time.sleep(stopt)
                if self.ps['pid']() > 0:#not necessary if -1 kills session
                    p = self.ps['popen']
                    p.kill()
                    self.exitcode = p.wait(timeout=1)
                    
                 
                self.ps['stop_call'] = False
                #self.ps['popen'] = None
                
            t = Global.ft_thread(ft)
            
            return True
        return False
    
    def is_psobj(self):
        return (self.psobj is None)
            
        

    #launch one instance of a process
    def start_ps(self):
        """
            cmdline 
        """
        #if self.get_ps_info('cmdline') == "":
        self.success_countdown()
        
        if not self.ps_exists():
            with open(self.ps['stdout'],'a+') as out, \
                 open(self.ps['stderr'],'a+') as err:
                #if self.ps['umask'] != -1:
                    
                    self.ps['popen'] = psutil.Popen(self.ps['cmdp'], stdout=out, stderr=err)
                    Global.print_file(f"{self.ps['popen'].pid}", Global.pss_file, 'a')
                    
            return True
        return False

    
    def status_ps(self):
        
        cmd = self.psobj.args
        pid = self.psobj.pid
        run_time = self.get_runtime(),
        returncode = self.psobj.poll()
        lst = [cmd,pid,run_time,returncode]
        
        #LOG
        msg = f"ps {cmd} ended  returncode:{returncode} expecting {self.ps['exitcode']}  "
        msg += 'fail'
        if str(returncode) == self.ps['exitcode']:
            msg += 'success'
        Global.print_file(msg, Global.tk_res, 'a')
        
        #DISPLAY
        pad = [30,30,10,7,10,3]
        for i in range(len(lst)):
            lst[i] = str(lst[i])
            lst[i] = lst[i].ljust(pad[i], ' ')
   
        status_msg = "name:{} | cmd:{} | state: {} | PID:{} | runtime:{} | exitcode:{} ".format(*lst)
        return status_msg

    def get_runtime(self):
        
        epoch_ct = int(self.ps['create_time']())
        epoch_now = int(time.time())
        
        datetime_ct = datetime.fromtimestamp(epoch_ct)
        datetime_now = datetime.fromtimestamp(epoch_now)
        
        run_time = str(datetime_now - datetime_ct)
        return run_time
    
    def auto_start(self):
        self.start_ps()
        Global.printx(f"AUTOSTART <{self.ps['name']}>")
    
    def set_umask(self):
        os.umask(self.ps['umask'])
        Global.printx(f"umask set to :{self.ps['umask']}")
    
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

pss = dict()