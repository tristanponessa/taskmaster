import cmd
import threading
import time
import sys
import re
import itertools
import os
import signal
import traceback
import subprocess
from datetime import datetime, timedelta

import Conf as confFILE
import Log as logFILE
import Global

#class FileGlobal:
pgs = dict()

def is_pg(pgTag):
    global pgs
    pg_catch = get_pgs(pgTag)
    return True if pg_catch else False

def get_pgs(pgTag):
    global pgs
    pgLst = list(pgs.keys())
    pg_net = []
    for pgName in pgLst:
        if pgName.startswith(f'{pgTag}'):
            pg_net.append(pgName)
    return pg_net


def init_pg(pgName, pgProps):
    global pgs
    
    nbpg = int(confFILE.get_pgProp(pgName, 'nbps'))
    for i in range(nbpg):
        inst_name = f'{pgName}__{i}'
        #if nbpg == 1:
        #    inst_name = pgName
        pgNew = Program(inst_name, pgProps)
        if confFILE.get_pgProp(pgName, 'autostart') == "yes": 
            pgNew.start_pg()
            Global.printx(f"{inst_name} : autostart")
        pgs[inst_name] = pgNew
        Global.printx(f"added {inst_name} to pgs {inst_name in list(pgs.keys())}")

def pgs_check_state():
    global pgs
    for pgName, pgClass in pgs.items():
        if pgClass.pgobj is not None:
            r = pgClass.get_returncode()
            if (r is not None) and r > 0 and pgClass.flag != 'STOPPED':
                pgClass.flag = 'DONE'
                #else is signaled

def signal_pg(pgName, isignal=signal.SIGINT, option=None):
    #signals and removes from lst
    global pgs
    if '__' not in pgName:
        nbpg = int(confFILE.get_pgProp(pgName, 'nbps'))
        for i in range(nbpg):
            inst_name = f'{pgName}__{i}'
            pgs[inst_name].signalJob_if_pgInit(isignal)
            if 'remove' in option:
                del pgs[inst_name]
    else:
        pgs[pgName].signalJob_if_pgInit(isignal)
        if 'remove' in option:
            del pgs[pgName]
        #Global.printx(f"destroying all insts {pgName}")

    #LOG
    #Global.printx(f"DESTROY all insts {pgName}")

def signal_job(pid, isignal=signal.SIGINT):
    #if pid exists, sig its chidren and it
    try:
        pgrp = os.getpgid(pid)
        os.killpg(pgrp, isignal)
    except OSError:
        print(f'signal_job : PID {pid} not existent')
        pass

def init_pgs():
    global pgs

    pgsk = [pgName.split('__')[0] for pgName in pgs.keys()]
    confk = confFILE.conf.keys()
    keys = set([*pgsk, *confk])

    #Global.printx(f"cur pgs : {pgsk}")
    #Global.printx(f"conf : {confk}")
    #Global.printx(f"fusion set : {keys}")
    
    for key in keys:
        if (key in confk):
            if (key not in pgsk):
                init_pg(key, confFILE.conf[key])
            elif (pgs[f'{key}__0'].props != confFILE.conf[key]):
                signal_pg(key, signal.SIGINT, 'remove')
                init_pg(key, confFILE.conf[key])
        elif (key not in confk):
            signal_pg(key, signal.SIGINT, 'remove')
    
        #else:
        #    Global.printx(f"protected {key}")

def tmExit_clean_pgs():
    for pgName in list(pgs.keys()):
        print(f'DESTROYING {pgName}')
        signal_pg(pgName, signal.SIGINT, 'remove')

def display_pgs():
    global pgs
    for pg in pgs.values():
        print(pg)
    print('\n')



def pgs_reboot_if_wrongExitcode():
    for pgObj in pgs.values():
        if confFILE.get_pgProp(pgObj.name, 'restart') == 'yes':
            pgObj.reboot_if_wrongExitcode()


def ft_thread(ft):
    p = threading.Thread(target=ft)
    p.deamon = True
    p.start()
    return p
        

####################################################################################################################

class Program:
    """
        __next__  , __cmp__ depending of pg priority another for pids
        
        pg class:
            -stocks all information about pg
            -methods to proform on Program start/stop/status
            -NO checking, log
            -executes a pg configuration on Program
    
    """
    
    def __init__(self, name, props):

        self.name = name
        self.gname = name.split('__')[0]
        self.props = props
        self.pgobj = None
        self.start_time = ''
        self.stop_call = False
        self.last_status = ''
        self.returncode = None
        self.nbrestart = 0
        self.flag = 'CREATED' #checkif manually stopped not signaled
    
    def pgInit(self):
        #return (self.pgobj is not None)
        return (self.flag == 'RUNNING')

    def setup_cmd(self):
        #umask 777 && cd .. && export v=1 && export v=2 && cmd'
        umask = f"umask {confFILE.get_pgProp(self.gname, 'umask')}"
        cd  = f"cd {confFILE.get_pgProp(self.gname, 'workdir')}"
        env_vars = [f'export {varname}={varval}' for varname,varval in confFILE.get_pgProp(self.gname, 'env').items()]

        setup_cmd = [umask, cd, *env_vars]
        setup_cmd = ' && '.join(setup_cmd)
        return setup_cmd

    def success_countdown(self):
        def ft():
            s = int(confFILE.get_pgProp(self.gname, 'timetillsuc'))
            time.sleep(s)
            if self.pgInit():
                Global.print_file(f'{Global.now_time()} : {self.gname} running for over {s}s, its working properly', Global.log_file, 'a')
            else:
                Global.print_file(f'{Global.now_time()} : {self.gname} running for over {s}s, FATAL finished too soon', Global.log_file, 'a')
                #supervisor reboots 3 times 
        t = ft_thread(ft)

    def signalJob_if_pgInit(self, isignal=signal.SIGINT):
        if self.pgInit():
            signal_job(self.pgobj.pid, isignal)
            self.flag = f'SIGNALED {signal.Signals(isignal).name}'
            #self.get_returncode()
            #self.last_status = f'LAST {self.status_pg()}'
            #self.pgobj = None

            return True
        return False

    def stop_pg(self):
        if self.pgInit() and self.stop_call == False:
            self.stop_call = True

            def ft():
                signame = confFILE.get_pgProp(self.gname, 'exitcode')
                signal_job(self.pgobj.pid, signal.Signals[signame].value)
                returncode = self.get_returncode('wait')
                if returncode is None:
                    self.flag = 'KILLED'
                    #self.last_status = f'LAST {self.status_pg()}'
                    signal_job(self.pgobj.pid, signal.SIGKILL)
                else:
                #print(f'{self.name} before:', self.returncode)
                    #print(f'{self.name}after:', self.returncode)
                    #self.last_status = f'LAST {self.status_pg()}'
                    #self.pgobj = None
                    self.stop_call = False
                    self.nbrestart = 0
                    self.flag = 'STOPPED'

            t = ft_thread(ft)
            return True
        return False
    
    def start_pg(self, option=None):
        
        if self.stop_call:
            Global.printx("can't start pg, its stopping")
        elif (not self.pgInit()):

            self.last_status = ''
            self.flag = 'RUNNING'
            self.start_time = int(time.time())
            #self.returncode = None

            #print('>>', self.gname)
            #print(confFILE.get_pgProp(self.gname, 'cmd'))

            cmd = f"{self.setup_cmd()} && {confFILE.get_pgProp(self.gname, 'cmd')}"
            if option != 'restart':
                self.nbrestart = 0
            #LOG
            Global.printx(cmd)

            with open(confFILE.get_pgProp(self.gname, 'stdout'),'a+') as out, \
                 open(confFILE.get_pgProp(self.gname, 'stderr'),'a+') as err:

                                #subprocess.Popen(cmd, shell=True, stdout=out, stderr=err, start_new_session=True)
                                #subprocess.Popen(cmd, shell=True, stdout=out, stderr=err, start_new_session=True)
                    self.pgobj = subprocess.Popen(cmd, shell=True, stdout=out, stderr=err, start_new_session=True)
                    #is pid of parent which is the shell
                    
                    #to get children pgrep -P 97520 
            
            self.success_countdown()
                    
            return True
        return False
    
    def reboot_if_wrongExitcode(self): 
        #returncode is an exitcode with - like -15 for sigterm
        ret = self.get_returncode()
        if self.flag not in ['STOPPED', 'FATAL', 'KILLED'] and self.returncode:
            wanted_exitcode = confFILE.get_pgProp(self.gname, 'exitcode')
            nbrestart = confFILE.get_pgProp(self.gname, 'nbrestart')

            if wanted_exitcode != str(self.returncode):
                if self.nbrestart > int(nbrestart):
                    self.flag = 'FATAL'
                    Global.print_file(f'pg {self.gname} has rebooted {self.nbrestart} the max {nbrestart} no more rebooting', Global.log_file, 'a')
                else:
                    self.nbrestart += 1
                    self.start_pg('restart')
                    Global.print_file(f'UNEXPECTED pg {self.gname} has {self.returncode} wrong exitcode should be {wanted_exitcode} REBOOTING', Global.log_file, 'a')
                    

    
    def get_returncode(self, option=None):

        if self.pgobj is None:
            return None

        #returncode = None
        
        """
        if not option:
            time.sleep(1)
            returncode = self.pgobj.poll()
            print('poll ret', returncode)
        
        """
        stoptime = 0.1
        if option == 'wait':
            stoptime = int(confFILE.get_pgProp(self.gname, 'stoptime'))
        try:
            returncode = self.pgobj.wait(timeout=stoptime)                  
            #print(f'ret : {returncode}')
            #print('wait ret', returncode)
            #logFILE.returncode_msg(self.gname, confFILE.get_pgProp(self.gname, 'returncode'), returncode)
        except subprocess.TimeoutExpired:
            #print(f'ret : TIME OUT ')
            returncode = None
        #        Global.printx(f"pg returncode waited {stoptime}> TIMEOUT ERROR killing pg")

        #self.returncode = returncode
        #if returncode:
        #    self.last_status = f'LAST {self.status_pg()}'
        #    self.pgobj = None
        return returncode

    def status_pg(self, option=''):
        
        #if not self.pgInit() and self.last_status != '':
        #    return (self.last_status)
        
        name = self.name
        cmd = confFILE.get_pgProp(self.gname, 'cmd')

        pid = self.pgobj.pid if self.pgobj else None
        run_time = self.get_runtime() if self.pgInit() else None
        returncode = self.get_returncode() #maybe tack if off
        #returncode = '-'
        state = self.flag
        lst = [name,cmd,state,pid,run_time, returncode]

        #DISPLAY
        pad = [30,30,20,7,10,3]
        for i in range(len(lst)):
            lst[i] = str(lst[i])
            lst[i] = lst[i].ljust(pad[i], ' ')
   
        status_msg = "name:{} | cmd:{} | state: {} | PID:{} | runtime:{} | returncode:{}".format(*lst)
        return status_msg

    def get_runtime(self):

        if not self.pgInit():
            return
        
        epoch_ct = int(self.start_time)
        epoch_now = int(time.time())
        
        datetime_ct = datetime.fromtimestamp(epoch_ct)
        datetime_now = datetime.fromtimestamp(epoch_now)
        
        run_time = str(datetime_now - datetime_ct)
        return run_time
    
    def __str__(self):
        x = f'pg : {self.gname} | obj : {self.pgobj} | props : {self.props}'
        return x
    
        
#####################################################################################################################

