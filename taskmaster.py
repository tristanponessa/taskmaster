
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

#files
import Process

"""
NOTES:
    TASKMASTER WILL LAUNCH PROGRAMS FROM 1 OR MULTIPLE CONF FILES
    YOU CAN PRECISE EACH PROGRAM
    SUPERVISOR SEEMED TO DO THINGS BY CONFIG FILE

    #issues : bin/bash being spawed by popen must kill() them
    #a program is 1 process like ls or count_time

    bunch of functions use copy code , reduce to uniuversal functions
    
    check aname of programs regex no <>...
    add colors to make it clear for already launched and errors in red 
    launch everythoin gas multiprocess so umask can ably all the time for a process
    dont launch program without config file good
    universal vaklue system umasl not set ? how to check?
    
    
    psutil process contains much more infos than subprocess 
    i could make a simpler version with popen alone and use p.pid / p.status and two more others
    psutil offers so much more and to make it flexible i created this complicated system where
    you have to simply call self.program[info]() 
"""

#GENERAL FUNS for all classes
###################################################################################################################

class Global:
    
    log_file = 'taskmaster.log'
    conf_file = './config/taskmaster_conf.ini'
    
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

class Txt:
    
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    #msg_autorun = "{FAIL}autorun{ENDC}"
    #msg_x =       "{var}x"

class Process:
    """
        __next__  , __cmp__ depending of ps priority another for pids
    """
    def __init__(self):
        
        self.program['name'] = program_name
        self.program['cmdp'] = self.program['command'].replace('\n', '').split(' ')
        self.program['cmd'] = self.program['command'].replace('\n', '')
        #has to be updatable so lamdba
        #lamda when you do status before start it will be 0 after a new pid and after a stop a new pid
        self.program['create_time'] =  lambda : self.get_ps_info('create_time')#function
        self.program['run_time'] =     lambda : self.get_ps_info('run_time')
        self.program['pid'] =          lambda : self.get_ps_info('pid')
        self.program['status'] =       lambda : self.get_ps_info('status')#function
        
        self.program['stop_call'] = False
    
   
    
    

class Program:

    """
        Program class:
            -stocks all information about program
            -methods to proform on process start/stop/status
            -NO checking, log
            -executes a program configuration on process
    """
    
    

    def __init__(self, program_name, aprogram):
        """
            cmdline 
            a ps contains the cmdline that launches it 
            i also stock it in self.program[cmd/cmdp]
        """
        
        ####################################################################################################################
        self.program = aprogram
        self.default_vals(program_name, self.program)
        self.convert_types(self.program)
        
        self.pss = [None] * self.program['nbps']
        #################################################################################################################### 
        #if self.program['umask'] != -1:        self.set_umask()
        
        if self.program['autostart'] == "yes": self.pss_start()
        
    
    def default_vals(self, program_name, program):
        
        dft = dict()
        dft['command'] =      'sh sec_counter.bash'
        dft['nbps'] =         '1'
        dft['timetillsuc'] =  '0' 
        dft['autostart'] =    'no'
        dft['autorestart'] =  'no'
        dft['stoptime'] =     '0' 
        dft['dir'] =          './'
        dft['env'] =          ""
        dft['stdout'] =       f'./{program_name}.stdout'
        dft['stderr'] =       f'./{program_name}.stderr'
        dft['nbretries'] =    '0'#if crashes, restarts
        dft['exitsignal'] =   '15'#SIGTERM
        dft['suc_signal'] =   '15'#SIGTERM
        dft['umask'] =        '022'
        
        for key,val in program.items():
            if val == "":
                program[key] = dft[key]
        
        #check types and false entries
    
    def convert_types(self, program):
        for key,val in program.items():
            if val.isnumeric():
                program[key] = int(program[key])
    
    def pss_start(self):
       self.pss = map(Process.start_ps, self.program, self.pss) #[Process.start_ps(self.program, ps) for ps in pss]
    
    def pss_stop(self):
        self.pss = map(Process.stop_ps, self.program, self.pss) #[Process.start_ps(self.program, ps) for ps in pss]



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
        self.conf.read(Global.conf_file)
        self.log_file_path = Global.log_file
        self.programs = dict()

        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        #dipslay help
        Global.printx('---taskmaster session : ' + now_time + '---')

        #load your running process on computer
        
        #auto to avoid taping everything everytime
        self.do_init("")
        #self.do_start("random101")
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
            self.programs[program_name] = Program(program_name, section)
        Global.printx(' '.join(list(self.programs.keys())))

    #def do_run_all(self, user_input):
     #   for program in self.programs:
      #      program.run()
    
    def do_start(self, user_input):
        self.toggle_program(user_input, 'start')

    def do_stop(self, user_input):
        self.toggle_program(user_input, 'stop')
    
    def do_reload(self, suer_input):
        self.toggle_program(user_input, 'stop')
        self.toggle_program(user_input, 'start')
    
    def toggle_program(self, ps, action):
        if ps not in self.programs.keys():
            Global.printx("program <" + ps + "> don't exist")
            return
        if action == 'stop':  res = self.programs[ps].stop_program()
        if action == 'start': res = self.programs[ps].start_program()
        
        if res == False: Global.printx("action " + action + " already launched")
        else:            Global.printx("action " + action + " launched")
    
    
        
                
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
    
    
    #print(f"{Txt.FAIL}autorun{Txt.ENDC}")
    
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
