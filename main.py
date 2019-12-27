
import cmd
import subprocess
import multiprocessing
import threading
import configparser
import time
import datetime
import sys
#log file ./taskmaster.log

"""
    TASKMASTER WILL LAUNCH PROGRAMS FROM 1 OR MULTIPLE CONF FILES
    YOU CAN PRECISE EACH PROGRAM
    SUPERVISOR SEEMED TO DO THINGS BY CONFIG FILE

    timer is calc by epoch time differences from start  - end
"""

#issues : bin/bash being spawed by popen must kill() them
#reload processes after closing taskmaster, stock pids in log than kill the pid
#a program is 1 process like ls or count_time
#only launch bash commands to control processes like ps kill dont pass by popen

class Program():

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

    def start(self):#prevent starting two times
        names = self.program['name'] + ' : ' + self.program['cmd']
        x = self.launch_cmd()
        if x == 'reloaded':
            log_msg = "reloaded {} : {}".format(self.program['name'], self.program['cmd'])
        elif x == True:
            log_msg = "start {} : {}".format(self.program['name'], self.program['cmd'])
        else:
            log_msg = "ERROR {} : {} can't run".format(self.program['name'], self.program['cmd'])
            #self.program['status'] = 'FAILED'
        self.print_stdout_log(log_msg)
            
    
    def stop(self):
        log_msg = 'stop ' + self.program['name']
        self.print_stdout_log(log_msg)
        self.stop_cmd()
        #self.program['status'] = 'STOPPED'
         
    #if already launched no popen object
    def status(self):
        #if self.program['cmd_process'] is not None and \
         #  self.program['cmd_process'].poll() is None:
        try:
            stuff = [
                        self.program['name'],
                        self.program['cmd'], 
                        self.program['status'],
                        self.program['pid'], #catch by info 
                        self.program['etime']
                        #self.get_time_diff(self.get_now_time(), self.program['start_time'])
                    ]

            status_msg = "{} : {}       {}      PID:{} runtime:{}".format(*stuff)
                                               
                                              
        except Exception as e:
            print(e)
            status_msg = self.program['name'] + ' not running'
        self.print_stdout_log(status_msg)

    def stop_cmd(self):
        cmd =  "kill -9 {pid}".format(pid=self.program['pid'])#SIGKILL
        self.run_cmd(cmd)
        

    def launch_cmd(self):
        cmd = ''.join(self.program['cmd'])
        os_ps = self.get_ps_info('', 'list')
        if any(cmd in ps for ps in os_ps):
            return 'reloaded'
        try:
            self.program['cmd_process'] = self.run_cmd(self.program['cmdp'], self.program['stdout'], self.program['stderr'])
        except Exception as e:
            return False
        return True 

    """
    def get_time_elapsed(self):
        time_elapsed = '?'
        cmd_ref = ' '.join(self.program['command'])
        cmd = 'ps -o cmd,etime | grep "{}"'.format(cmd_ref)

        p = subprocess.Popen(cmd,
                                        shell=True,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
        p.wait()
        #time.sleep(1)
        time_elapsed = p.stdout.read().decode('ascii').replace('\n', '').split(' ')[-1]
        p.kill()
        p.wait()
        return time_elapsed
    
    def get_os_pros(self):
        cmd = 'ps -o cmd'
        p = subprocess.Popen(cmd,
                                        shell=True,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
        p.wait()
        #time.sleep(1)
        os_proc = p.stdout.read().decode('ascii').split('\n')
        p.kill()
        p.wait()
        return os_proc
    """
    
    #search for nothing '' get all 
    def get_ps_info(self, cmd, info):
        cmd = 'ps -o cmd,pid,state,etime | grep "{cmd}"'.format(cmd=cmd)
        p = self.run_cmd(cmd, subprocess.PIPE, subprocess.PIPE, True)
        p.wait()

        cmd_output = p.stdout.read()
        ps_info = cmd_output.decode('ascii').split('\n')
        if info == 'list':
            return ps_info
        if cmd_output == '':
            return None
        ps_info = cmd_output.decode('ascii').replace('\n', '').split(' ')
        if info == 'pid':
            return ps_info[1]
        if info == 'status':
            return ps_info[2]
        if info == 'etime':
            return ps_info[3]

        p.kill()
        p.wait()

    def run_cmd(self, cmd, istdout=sys.stdout, istderr=sys.stderr, ishell=False):
        p = subprocess.Popen(cmd,
                            shell=ishell,
                            stdout=istdout,
                            stderr=istderr)
        return p

    def print_stdout_log(self, s):
        print(s)
        self.write_file(self.program['log'], s) 

    def write_file(self, file, s):
        with open(file, 'a+') as f:
            f.write(s + '\n')    
    

       # def run_cmd(self)


class Taskmaster_shell(cmd.Cmd):
    
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
        if self.check_program(user_input):
            self.programs[user_input].start()
    
    def do_stop(self, user_input):
        if self.check_program(user_input):
            self.programs[user_input].stop()
    
    def do_status(self, user_input):
        if user_input == '':
            for program in self.programs.keys():
                self.programs[program].status()
        else:
            if self.check_program(user_input):
                self.programs[user_input].status()

    #def complete_
   # def completedefault(self, a, b, c, d):
    #    return self.programs.keys()

    def check_program(self, program):
        if program not in self.programs.keys():
            self.print_stdout_log("program |" +  program + "| don't exist")
            return False
        return True
    
    
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
      
    def do_exit(self, inp):
        self.print_stdout_log("<Exiting Taskmaster>\n\n")
        return True
    
    def do_EOF(self, line):
        self.print_stdout_log('\n\n  Ctrl + d -> exit Taskmaster\n\n')
        return True

    def do_help(self, user_input):
        print('srcew you!')
    
    def do_ps(self, inp):
        p = subprocess.Popen(["ps", "-o", "cmd,pid,start,etime"])
        time.sleep(1)
        p.kill()
        p.wait()
    
    def do_psx(self, inp):
        time_elapsed = None
        p = subprocess.Popen(["ps", "-o", "cmd,etime"],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
        time.sleep(1)
        #print(p.stdout.read())
        output = p.stdout.readlines()
        """
        for ps in output:
            ps = ps.decode('ascii')
            s = ps.split(' ')
            if self.program['random69']['command'] == s[0].split(' '):
                time_elapsed = s[1]
        """
        print(*output, sep='\n')
        p.kill()
        p.wait()
        print(time_elapsed)

if __name__ == '__main__':

    ts = Taskmaster_shell()
    try:
        ts.cmdloop()
    except KeyboardInterrupt:#and ctrl d
        Taskmaster_shell.print_stdout_log(ts, '\n\n  Ctrl + c -> exit Taskmaster\n\n')
        #relaunch new instance of taskmaster
