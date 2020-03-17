
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


"""
NOTES:
    TASKMASTER WILL LAUNCH PROGRAMS FROM 1 OR MULTIPLE CONF FILES
    YOU CAN PRECISE EACH PROGRAM
    SUPERVISOR SEEMED TO DO THINGS BY CONFIG FILE

    #issues : bin/bash being spawed by popen must kill() them
    #a program is 1 process like ls or count_time

    bunch of functions use copy code , reduce to uniuversal functions
"""

#GENERAL FUNS for all classes
###################################################################################################################

class Global:
    
    log_file = 'taskmaster.log'
    
    """
    def printx(msg):
        print(msg, end='')
        if ifile is not None:
            with open(ifile, 'a+') as f:
                print(msg, file=f)
    """
    
    @staticmethod
    def printx(s):
        """ stdout and file """
        print(s)
        with open(Global.log_file, 'a+') as f:
            print(s, file=f)
    
    @staticmethod
    def print_file(s, ifile, mode):
        with open(ifile, mode) as f:
            print(s, file=f)
    

###################################################################################################################

class Program:

    """
        Program class:
            -stocks all information about program
            -methods to proform on process start/stop/status
            -NO checking, log
            -executes a program configuration on process
    """
    
    

    def __init__(self, program_name, iprogram, log_file_path):
        """
            cmdline 
            a ps contains the cmdline that launches it 
            i also stock it in self.program[cmd/cmdp]
        """
        
        ####################################################################################################################
        
        self.program = iprogram.copy()
        #change types
        self.program['stoptime'] = int(self.program['stoptime'])
        #add extra
        self.program['name'] = program_name
        self.program['cmdp'] = self.program['command'].replace('\n', '').split(' ')
        self.program['cmd'] = self.program['command'].replace('\n', '')
        #has to be updatable so lamdba
        #lamda when you do status before start it will be 0 after a new pid and after a stop a new pid
        self.program['create_time'] =  lambda : self.get_ps_info('create_time')#function
        self.program['pid'] =          lambda : self.get_ps_info('pid')
        self.program['status'] =       lambda : self.get_ps_info('status')#function
        #elf.program['isalive'] =      lambda : self.get_ps_info('isalive')#status has weird names and unexpected states
        
        self.program['stop_call'] = False
        self.program['start_time'] = None
        self.program['run_time'] = lambda : self.get_ps_info('run_time')
        
        #self.program['log'] = log_file_path
        
        #################################################################################################################### 
        
        if self.program['autostart']:
            self.auto_start()
    
     
        """          
        t0 = time.time()
        print (time.strftime("%H:%M:%S",time.localtime(t0)))
        t1 = t0 + 3600 * 2
        print (time.strftime("%H:%M:%S",time.localtime(t1)))
        datetime.now() - self.program['run_time']
        """
    
    def ps_exists(self):
        if self.program['pid']() == -1:
            return False
        return True
        
    def thread_fun(self, fun):
        p = multiprocessing.Process(target=fun)
        p.start()

    def stop_ps(self):
        #if self.get_ps_info('cmdline') != "":
        print (">>>>" , self.program['stop_call'])
        if self.ps_exists() and self.program['stop_call'] == False:
            self.program['stop_call'] = True
            def x():
                time.sleep(self.program['stoptime'])
                if self.program['pid']() > 0:#not necessary
                    os.kill(self.program['pid'](), signal.SIGKILL)
                self.program['start_time'] = None
                self.program['stop_call'] = False
            
            self.thread_fun(x)
            
            return True
        return False
    
    #launch one instance of a process
    def start_ps(self):
        """
            cmdline 
        """
        #if self.get_ps_info('cmdline') == "":
        
        if not self.ps_exists():
            self.program['start_time'] = time.time()
            with open(self.program['stdout'],'a+') as out, \
                 open(self.program['stderr'],'a+') as err:
                    psutil.Popen(self.program['cmdp'], stdout=out, stderr=err)
            return True
        return False
    
    def status_ps(self):

        lst = [
                self.program['name'],
                self.program['cmd'],
                self.program['status'](),
                self.program['pid'](),
                self.program['run_time']()
              ]
        
        status_msg = "{} : {}       state: {}      PID:{} runtime:{}".format(*lst)
        return status_msg
    
    def get_ps_info(self, info):
        """
            ps_iter contains all the info of a ps given by the os
        """
        
        ps_iter = psutil.process_iter(attrs=["cmdline", "pid", "create_time", "status"])
        #ps_iter goes threw all psesses in comp
        for cur_ps in ps_iter:
            cur_ps = cur_ps.as_dict(attrs=["cmdline", "pid", "create_time", "status"])

            #if this ps is ours
            if cur_ps['cmdline'] == self.program['cmdp']:
                if   info == 'create_time':
                    #return time.strftime("%H:%M:%S", time.localtime(cur_ps[info]))
                    return cur_ps[info]
                elif  info == 'run_time':
                    return self.get_runtime()
                elif info == 'pid':
                    return int(cur_ps[info])
                else:
                    return cur_ps[info]
                
        #if dont find default vals
        if info == 'pid':
            return -1
        else:
            return None
    
    def get_runtime(self):
        
        epoch_ct = int(self.program['create_time']())
        epoch_now = int(time.time())
        
        datetime_ct = datetime.fromtimestamp(epoch_ct)
        datetime_now = datetime.fromtimestamp(epoch_now)
        
        run_time = str(datetime_now - datetime_ct)
        return run_time
    
     #autostart
    def auto_start(self):
        #print(self.programs['random101'].program['autostart'])
        self.start_ps()
        Global.printx("AUTOSTART starting process |" + self.program['name'] + "| running")
            
    """
    def ps_time_elapsed(self):
        if not psutil.pid_exists(self.program['pid']()):
            p = multiprocessing.Process(target=self.msh)
            start_time = time.time()
            main()
            print("--- %s seconds ---" % (time.time() - start_time))
    """
        




#has auto complete but not for args for do commands
class Taskmaster_shell(cmd.Cmd):

    """
        Taskmaster class :
            -checks user input
            -stocks programs in list from file
            -stocks actions in log file
            -preform actions from program objects from program list
            -launch one process instance 
    """
    
    prompt = 'taskmaster> '
    #http://patorjk.com/software/taag/#p=display&f=Bloody&t=Taskmaster
    intro = taskmaster_ascii_art = \
    """

    ▄▄▄█████▓ ▄▄▄        ██████  ██ ▄█▀ ███▄ ▄███▓ ▄▄▄        ██████ ▄▄▄█████▓▓█████  ██▀███  
    ▓  ██▒ ▓▒▒████▄    ▒██    ▒  ██▄█▒ ▓██▒▀█▀ ██▒▒████▄    ▒██    ▒ ▓  ██▒ ▓▒▓█   ▀ ▓██ ▒ ██▒
    ▒ ▓██░ ▒░▒██  ▀█▄  ░ ▓██▄   ▓███▄░ ▓██    ▓██░▒██  ▀█▄  ░ ▓██▄   ▒ ▓██░ ▒░▒███   ▓██ ░▄█ ▒
    ░ ▓██▓ ░ ░██▄▄▄▄██   ▒   ██▒▓██ █▄ ▒██    ▒██ ░██▄▄▄▄██   ▒   ██▒░ ▓██▓ ░ ▒▓█  ▄ ▒██▀▀█▄  
    ▒██▒ ░  ▓█   ▓██▒▒██████▒▒▒██▒ █▄▒██▒   ░██▒ ▓█   ▓██▒▒██████▒▒  ▒██▒ ░ ░▒████▒░██▓ ▒██▒
    ▒ ░░    ▒▒   ▓▒█░▒ ▒▓▒ ▒ ░▒ ▒▒ ▓▒░ ▒░   ░  ░ ▒▒   ▓▒█░▒ ▒▓▒ ▒ ░  ▒ ░░   ░░ ▒░ ░░ ▒▓ ░▒▓░
        ░      ▒   ▒▒ ░░ ░▒  ░ ░░ ░▒ ▒░░  ░      ░  ▒   ▒▒ ░░ ░▒  ░ ░    ░     ░ ░  ░  ░▒ ░ ▒░
    ░        ░   ▒   ░  ░  ░  ░ ░░ ░ ░      ░     ░   ▒   ░  ░  ░    ░         ░     ░░   ░ 
                ░  ░      ░  ░  ░          ░         ░  ░      ░              ░  ░   ░     
                                                                                            
    """


    def __init__(self):
        
        super().__init__()
        self.conf = configparser.ConfigParser()
        self.conf.read('./config/taskmaster_conf.ini')
        self.log_file_path = './taskmaster.log'
        self.programs = dict()

        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        #dipslay help
        Global.printx('---taskmaster session : ' + now_time + '---')

        #load your running process on computer
        
        #auto to avoid taping everything everytime
        self.do_init("")
        self.do_start("random101")
        self.do_status("")
        #self.do_stop("random101")
        #self.do_status("")
        #self.do_stop("random101")
        #self.do_stop("random101")
        #self.do_status("")
        
        


    def precmd(self, user_input):
        
        Global.print_file(Taskmaster_shell.prompt + user_input, Global.log_file, 'a+')
        return cmd.Cmd.precmd(self, user_input)

    

    def do_init(self, user_input):
        Global.printx("loaded programs from conf file")
        for program_name,section in self.conf._sections.items():
            clean_program_name = program_name.replace("program:", "")
            p = Program(clean_program_name, section, self.log_file_path)
            self.programs[clean_program_name] = p
        Global.printx(' '.join(list(self.programs.keys())))

    #def do_run_all(self, user_input):
     #   for program in self.programs:
      #      program.run()
    
    def do_start(self, user_input):
        try:
            v = self.programs[user_input].start_ps()
            if not v:
                Global.printx("process |" + user_input + "| ALREADY running")
            else:    
                Global.printx("starting process |" + user_input + "| running")
        except KeyError:
            Global.printx("process |" + user_input + "| don't exist")

    def do_stop(self, user_input):
        try:
            v = self.programs[user_input].stop_ps()
            if not v:
                Global.printx("stop process ALREADY" + user_input)
            else:
                Global.printx("processes stopped " + user_input)
        except KeyError:
            Global.printx("process |" + user_input + "| don't exist")
    
    def do_status(self, user_input):
        if user_input == '':
            for program in self.programs.keys():
                status_msg = self.programs[program].status_ps()
                Global.printx(status_msg)
        else:
            try:
                status_msg = self.programs[user_input].status_ps()
                Global.printx(status_msg)
            except KeyError:
                Global.printx("process |" + user_input + "| don't exist")


    def emptyline(self):
        pass
    
    def default(self, inp):
        Global.printx("display help")
        self.do_help()
      
    def do_exit(self, inp):
        Global.printx("<Exiting Taskmaster>\n\n")
        return True
    
    def do_EOF(self, line):
        Global.printx('\n\n  Ctrl + d -> exit Taskmaster\n\n')
        return True

    def do_help(self, user_input=''):
        print('srcew you!')
    
    def do_reboot(self, i):
        os.execl(sys.executable, sys.executable, *sys.argv)
    
    
        
        
        

if __name__ == '__main__':
    
    
    ts = Taskmaster_shell()
    try:
        
        ts.cmdloop()
    except KeyboardInterrupt:#and ctrl d
        #Taskmaster_shell.print_stdout_log(ts, '\n\n  Ctrl + c -> exit Taskmaster\n\n')
        Global.printx('\n\n  Ctrl + c -> exit Taskmaster\n\n')
    """
    except Exception as e:
        print(traceback.print_exc())
        print('::::CRASH REBOOTING.....::::')
        os.execl(sys.executable, sys.executable, *sys.argv)
    """
        #relaunch new instance of taskmaster
