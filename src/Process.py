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

def init_pg(pgName, pgProps):
    global pgs
    
    nbpg = int(confFILE.get_pgProp(pgName, 'nbpg'))
    for i in range(nbpg):
        inst_name = f'{pgName}___{i}'
        if nbpg == 1:
            inst_name = pgName
        pgNew = Program(inst_name, pgProps)
        if confFILE.get_pgProp(pgName, 'autostart') == "yes": 
            pgNew.start_pg()
            Global.printx(f"{inst_name} : autostart")
        FileGlobal.pgs[inst_name] = pgNew
        Global.printx(f"added {inst_name} to pgs")

def map_pgs(ft):
    global pgs
    for pg in pgs.values():
        ft()

def signal_pg(pgTag, isignal=signal.SIGINT, option=None):
    #signals and removes from lst
    global pgs
    pgLst = [pgTag]
    if pgTag.endswith('*'):
        pgLst = list(pgs.keys())
    for pgName in pgLst:
        pgs[pgName].killJob_if_pgInit(isignal)
        if 'remove' in option:
            del pgs[pgName]

    #LOG
    #Global.printx(f"DESTROY all insts {pgName}")


def init_pgs():
    global pgs

    pgsk = pgs.keys()
    confk = confFILE.conf.keys()
    keys = set([*pgsk, *confk])

    #Global.printx(f"cur pgs : {pgsk}")
    #Global.printx(f"conf : {confk}")
    #Global.printx(f"fusion set : {keys}")

    for key in keys:
        if (key in confk):
            if (key not in pgsk):
                init_pg(key, confFILE.conf[key])
            elif (pgs[key][0].propg != confFILE.conf[key]):
                signal_pg(key, signal.SIGINT, 'remove')
                init_pg(key, confFILE.conf[key])
        elif (key not in confk):
            signal_pg(key, signal.SIGINT, 'remove')
        else:
            Global.printx(f"protected {key}")

def tmexit_clean_pgs():
    keys = list(pgs.keys())
    for pgName in keys:
        destroy_pg(pgName)


def display_pgs():
    global pgs
    for pg in pgs.values():
        print('\n')
        for inst in pg:
            print(inst)
    print('\n')

def kill_job(pid, isignal=signal.SIGINT):
    #if pid exists
    try:
        pgrp = os.getpgid(pid)
        os.killpg(pgrp, isignal)
    except OSError:
        pass

def pgs_reboot_if_wrongExitcode():
    for pg in pgs.values():
        for inst in pg:
            print(inst)
            if confFILE.get_pgProp(inst.name, 'restart') == 'yes':
                print('in')
                inst.reboot_if_wrongExitcode()


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
    
    def __init__(self, name, propg):

        self.name = name
        self.propg = propg
        self.pgobj = None
        self.start_time = ''
        self.stop_call = False
        self.last_status = ''
        self.returncode = None
        self.nbrestart = 0
    
    def setup_cmd(self):
        #umask 777 && cd .. && export v=1 && export v=2 && cmd'
        umask = f"umask {confFILE.get_pgProp(self.name, 'umask')}"
        cd  = f"cd {confFILE.get_pgProp(self.name, 'workdir')}"
        env_vars = [f'export {varname}={varval}' for varname,varval in confFILE.get_pgProp(self.name, 'env').items()]

        setup_cmd = [umask, cd, *env_vars]
        setup_cmd = ' && '.join(setup_cmd)
        return setup_cmd

    def killJob_if_pgInit(self, isignal=signal.SIGINT):
        if self.pgInit():
            kill_job(self.pgobj.pid, isignal)

    def pgInit(self):
        return (self.pgobj is not None)

    def success_countdown(self):
        def ft():
            s = int(confFILE.get_pgProp(self.name, 'timetillsuc'))
            time.sleep(s)
            if self.pgInit():
                Global.print_file(f'{Global.now_time()} : {self.name} running for over {s}s, its working properly', Global.log_file, 'a')
            else:
                Global.print_file(f'{Global.now_time()} : {self.name} running for over {s}s, FATAL finished too soon', Global.log_file, 'a')
        t = ft_thread(ft)

    def stop_pg(self):
        if self.pgInit() and self.stop_call == False:
            self.stop_call = True

            def ft():
                stoptime = int(confFILE.get_pgProp(self.name, 'stoptime'))
                signame = confFILE.get_pgProp(self.name, 'exitcode')
                kill_job(self.pgobj.pid, signal.Signals[signame].value)
                self.last_status = f'LAST {self.status_pg()}'
                self.pgobj = None
                self.stop_call = False

            t = ft_thread(ft)
            return True
        return False
    
    def start_pg(self):
        
        if self.stop_call:
            Global.printx("can't start pg, its in a stop Program")
        elif (not self.pgInit()):

            self.last_status = ''
            self.start_time = int(time.time())
            cmd = f"{self.setup_cmd()} && {confFILE.get_pgProp(self.name, 'cmd')}"
            #LOG
            Global.printx(cmd)

            with open(confFILE.get_pgProp(self.name, 'stdout'),'a+') as out, \
                 open(confFILE.get_pgProp(self.name, 'stderr'),'a+') as err:
                    
                    self.pgobj = subProgram.Popen(cmd, shell=True, stdout=out, stderr=err, start_new_session=True)
            
            self.success_countdown()
                    
            return True
        return False
        
    def reboot_if_wrongExitcode(self): 
        #returncode is an exitcode with - like -15 for sigterm
        x = self.status_pg()
        if self.last_status != '' and self.returncode is not None and self.returncode < 0:
            wanted_exitcode = confFILE.get_pgProp(self.name, 'exitcode')
            if wanted_exitcode != str(self.returncode):
                nbrestart = confFILE.get_pgProp(self.name, 'nbrestart')
                if self.nbrestart > int(nbrestart):
                    #print(f'pg {self.name} has rebooted {self.nbrestart} the max {nbrestart} no more rebooting')
                    pass
                else:
                    self.nbrestart += 1
                    Global.print_file(f'UNEXPECTED pg {self.name} has {self.returncode} wrong exitcode should be {wanted_exitcode} REBOOTING', Global.log_file, 'a')
                    self.start_pg()
    
    def get_returncode(self, option=None):

        returncode = None
        """
        if self.pgInit():
            returncode = self.pgobj.poll()

        if returncode:
            #Global.print_file(f'pg DONE ret {returncode}', Global.log_file, 'a')
            #logFILE.returncode_msg(self.name, confFILE.get_pgProp(self.name, 'returncode'), returncode)
        """    
        
        stoptime = confFILE.get_pgProp(self.name, 'stoptime')
        try:
            returncode = self.pgobj.wait(timeout=stoptime)               
            self.pgobj = None
#                logFILE.returncode_msg(self.name, confFILE.get_pgProp(self.name, 'returncode'), returncode)
        except subProgram.TimeoutExpired:
            Global.print_file("pg returncode waited {} TIMEOUT ERROR its still running", Global.log_file, 'a')

        self.returncode = returncode
        return returncode

    def status_pg(self, option=''):
        
        if not self.pgInit() and self.last_status != '':
            print (f'LAST {self.last_status}', end=' ')
            return
        
        name = self.name
        cmd = confFILE.get_pgProp(self.name, 'cmd')
        state = 'STOPPED' if self.returncode else 'RUNNING'
        pid = self.pgobj.pid if self.pgInit() else None
        run_time = self.get_runtime()
        lst = [name,cmd,state,pid,run_time]
        
        #LOG
        """
        msg = f"pg {cmd} ended  returncode:{returncode} expecting {self.pg['exitcode']}  "
        msg += 'fail'
        if str(returncode) == self.pg['exitcode']:
            msg += 'success'
        Global.print_file(msg, Global.tk_res, 'a')
        """

        #DISPLAY
        pad = [30,30,10,7,10]
        for i in range(len(lst)):
            lst[i] = str(lst[i])
            lst[i] = lst[i].ljust(pad[i], ' ')
   
        status_msg = "name:{} | cmd:{} | state: {} | PID:{} | runtime:{}".format(*lst)

        if self.returncode:
            self.last_status = status_msg
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
    
    """
    def auto_start(self):
        self.start_pg()
        Global.printx(f"AUTOSTART <{self.pg['name']}>")
    """

    
    def __str__(self):
        x = f'pg : {self.name} | obj : {self.pgobj} | propg : {self.propg}'
        return x
    
        
#####################################################################################################################

