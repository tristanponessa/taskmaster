
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
        
        self.program['etime'] = lambda : self.get_ps_info(self.program['cmd'], 'etime')#function
        self.program['pid'] = lambda : self.get_ps_info(self.program['cmd'], 'pid')
        self.program['status'] = lambda : self.get_ps_info(self.program['cmd'], 'status')#function
        
        self.program['log'] = log_file_path 
        self.program['popen'] = None
        self.program['stdout'] = open(self.program['stdout'], "a+")
        self.program['stderr'] = open(self.program['stderr'], "a+")

    def stop_ps(self):
        cmd =  "kill -9 {pid}".format(pid=self.get_ps_info(self.program['cmd'], 'pid'))#SIGKILL
        subprocess.Popen(cmd)
        
    def start_ps(self):
        subprocess.Popen(self.program['cmdp'], stdout=self.program['stdout'], stderr=self.program['stderr'])
    
    def status_ps(self):
        stuff = [
                    self.program['name'],
                    self.program['cmd'], 
                    self.get_ps_info(self.program['cmd'], 'pid'),
                    self.get_ps_info(self.program['cmd'], 'etime'),
                    self.get_ps_info(self.program['cmd'], 'state')
                ]
        print('test:' + self.get_ps_info(self.program['cmd'], 'etime'))

        status_msg = "{} : {}       state: {}      PID:{} runtime:{}".format(*stuff)
        return status_msg
 
    def get_ps_info(self, ps_name, info):
        """
        cmd = 'ps -o {info} | grep "{ps_name}"'.format(info=info, ps_name=ps_name)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        val = p.stdout.read().decode('ascii').replace('\n', '')
        return val
        #p.wait()
        """
        

        cmd_ps = 'ps -o {info} --no-headers'.format(info=info)
        cmd_grep = 'grep "{ps_name}"'.format(ps_name=ps_name)
        p1 = subprocess.Popen(cmd_ps, stdout=subprocess.PIPE, shell=True)
        p2 = subprocess.Popen(cmd_grep, stdin=p1.stdout, stdout=subprocess.PIPE, shell=True)
        val = p2.stdout.read().decode('ascii').replace('\n', '')
        p1.wait()
        p2.wait()


        #p kill perhaps
        return val
        
    
    def print_stdout_log(self, s):
        print(s)
        self.write_file(self.program['log'], s) 

    def write_file(self, file, s):
        with open(file, 'a+') as f:
            f.write(s + '\n')    
    

       # def run_cmd(self)



class Taskmaster_shell(cmd.Cmd):

    """
        Taskmaster class :
            -checks user input
            -stocks programs in list from file
            -stocks actions in log file
            -preform actions from program objects from program list
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


    #def do_run_all(self, user_input):
     #   for program in self.programs:
      #      program.run()
    
    def do_start(self, user_input):
        try:
            self.programs[user_input].start_ps()
            self.print_stdout_log("starting process |" + user_input + "| running")
        except KeyError:
            self.print_stdout_log("process |" + user_input + "| don't exist")

    def do_stop(self, user_input):
        try:
            self.programs[user_input].stop_ps()
            self.print_stdout_log("stopping process |" + user_input + "| can't run")
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

    def do_help(self, user_input):
        print('srcew you!')
    
    def get_os_ps_lst(self):
        cmd_ps = 'ps -o cmd --no-headers'
        p1 = subprocess.Popen(cmd_ps, stdout=subprocess.PIPE)
        val = p1.stdout.read().decode('ascii').split('\n')
        return val
    
    def do_psx(self, i):
        
        proc_iter = psutil.process_iter(attrs=["pid", "name", "cmdline"])
        for proc in proc_iter:
            if proc.info['pid'] == 18408:
                print(proc.info['pid'], ' ', proc.info['name'], ' ', proc.info['cmdline'])

        for proc in psutil.process_iter():
            try:
                # Get process name & pid from process object.
                processName = proc.name()
                processID = proc.pid
                
                #print(processName , ' ::: ', proc.exe() , ':', processID)
                #if  '.sh' in proc.exe():
                print(proc.exe(), '>>', processName , ' :::', processID)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    
    def do_reboot(self, i):
        os.execl(sys.executable, sys.executable, *sys.argv)

if __name__ == '__main__':

    ts = Taskmaster_shell()
    try:
        ts.cmdloop()
    except KeyboardInterrupt:#and ctrl d
        Taskmaster_shell.print_stdout_log(ts, '\n\n  Ctrl + c -> exit Taskmaster\n\n')
        #relaunch new instance of taskmaster
