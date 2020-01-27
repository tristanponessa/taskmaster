
import cmd
import subprocess
import multiprocessing
import threading
import configparser
import time
import datetime
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

"""
class Print():

    docstring
        Print class:
            -static methods for any class to proform special prints
    
    @staticmethod
    give print funs and launch them with this
    def printX(**print_funs):
        for every print fun print 

    @staticmethod
    def write_file(file, mode, s):
        with open(file, mode) as f:
            f.write(s)   
"""

class Program():

    """
        Program class:
            -stocks all information about program
            -methods to proform on process start/stop/status
            -NO checking, log
            -executes a program configuration on process
    """
    
    

    def __init__(self, program_name, iprogram, log_file_path):
        self.program = iprogram.copy()
        #add extra
        self.program['name'] = program_name
        self.program['cmdp'] = self.program['command'].replace('\n', '').split(' ')
        self.program['cmd'] = self.program['command'].replace('\n', '')
        #has to be updatable so lamdba
        self.program['create_time'] =  lambda : self.get_ps_info('create_time')#function
        self.program['pid'] =          lambda : self.get_ps_info('pid')
        self.program['status'] =       lambda : self.get_ps_info('status')#function
        
        self.program['log'] = log_file_path 

    def msh(self):
        print(self.program['stoptime'])
        time.sleep(5)
        os.kill(self.program['pid'](), signal.SIGKILL)

    def stop_ps(self):
        if self.get_ps_info('cmdline') != "":
            #if self.program['stoptime'] != '':
                #thread clocck n sec 
            p = multiprocessing.Process(target=self.msh)
            p.start()

            #os.kill(self.program['pid'](), signal.SIGKILL)
            return True
        return False
        #cmd =  "kill -9 {pid}".format(pid=self.get_ps_info(self.program['cmd'], 'pid'))#SIGKILL
        #subprocess.Popen(cmd)
    
    #launch one instance of a process
    def start_ps(self):
        if self.get_ps_info('cmdline') == "":
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
                self.program['create_time']()
              ]
        
        status_msg = "{} : {}       state: {}      PID:{} runtime:{}".format(*lst)
        return status_msg
    
    def get_ps_info(self, info):   
        val = ""
        proc_iter = psutil.process_iter(attrs=["cmdline", "pid", "create_time", "status"])
        for proc in proc_iter:
            p = proc.as_dict(attrs=["cmdline", "pid", "create_time", "status"])
            #print(p)
            if p['cmdline'] == self.program['cmdp']:
                if info == 'create_time':
                    val = time.strftime("%H:%M:%S", time.localtime(p[info]))
                elif info == 'pid':
                    val = int(p[info])
                else:
                    val = p[info]
                break
        return val
        
    def print_stdout_log(self, s):
        print(s)
        self.write_file(self.program['log'], s) 

    def write_file(self, file, s):
        with open(file, 'a+') as f:
            f.write(s + '\n')    
    

       # def run_cmd(self)


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
        self.print_stdout_log('---taskmaster session : ' + now_time + '---')

        #load your running process on computer


    def precmd(self, user_input):
        self.write_file(self.log_file_path, Taskmaster_shell.prompt + user_input)
        return cmd.Cmd.precmd(self, user_input)

    def do_init(self, user_input):
        self.print_stdout_log("loaded programs from conf file")
        for program_name,section in self.conf._sections.items():
            clean_program_name = program_name.replace("program:", "")
            p = Program(clean_program_name, section, self.log_file_path)
            self.programs[clean_program_name] = p
        self.print_stdout_log(' '.join(list(self.programs.keys())))

        print(self.programs['random69'].program['autostart'])
        if self.programs['random69'].program['autostart']:
            self.programs['random69'].start_ps()
            self.print_stdout_log("starting process |" + "" + "| running")
            
            
         
        
        #if self.programs[user_input]['autostart'] == True:
        #    #self.do_start(self.programs[user_input]['name'])
        #    print(self.programs[user_input]['name'])


    #def do_run_all(self, user_input):
     #   for program in self.programs:
      #      program.run()
    
    def do_start(self, user_input):
        try:
            v = self.programs[user_input].start_ps()
            if not v:
                self.print_stdout_log("process |" + user_input + "| ALREADY running")
            else:    
                self.print_stdout_log("starting process |" + user_input + "| running")
        except KeyError:
            self.print_stdout_log("process |" + user_input + "| don't exist")

    def do_stop(self, user_input):
        try:
            v = self.programs[user_input].stop_ps()
            if not v:
                self.print_stdout_log("stop process ALREADY" + user_input)
            else:
                self.print_stdout_log("processes stopped " + user_input)
        except KeyError:
            self.print_stdout_log("process |" + user_input + "| don't exist")
    
    def do_status(self, user_input):
        if user_input == '':
            for program in self.programs.keys():
                status_msg = self.programs[program].status_ps()
                self.print_stdout_log(status_msg)
        else:
            try:
                status_msg = self.programs[user_input].status_ps()
                self.print_stdout_log(status_msg)
            except KeyError:
                self.print_stdout_log("process |" + user_input + "| don't exist")
    
    def print_stdout_log(self, s):
        print(s)
        self.write_file(self.log_file_path, s) 
    
    def write_file(self, file, s):
        with open(file, 'a+') as f:
            f.write(s + '\n')

    def emptyline(self):
        pass
    
    def default(self, inp):
        self.print_stdout_log("display help")
        self.do_help()
      
    def do_exit(self, inp):
        self.print_stdout_log("<Exiting Taskmaster>\n\n")
        return True
    
    def do_EOF(self, line):
        self.print_stdout_log('\n\n  Ctrl + d -> exit Taskmaster\n\n')
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
        Taskmaster_shell.print_stdout_log(ts, '\n\n  Ctrl + c -> exit Taskmaster\n\n')
    """
    except Exception as e:
        print(traceback.print_exc())
        print('::::CRASH REBOOTING.....::::')
        os.execl(sys.executable, sys.executable, *sys.argv)
    """
        #relaunch new instance of taskmaster
