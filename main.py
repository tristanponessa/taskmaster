
import cmd
import subprocess
import multiprocessing
import threading
import configparser
import time
#log file ./taskmaster.log

"""
    TASKMASTER WILL LAUNCH PROGRAMS FROM 1 OR MULTIPLE CONF FILES
    YOU CAN PRECISE EACH PROGRAM
    SUPERVISOR SEEMED TO DO THINGS BY CONFIG FILE
"""
class Program():

    def __init__(self, program_name, iprogram, log_file_path):
        self.program = iprogram.copy()
        #add extra
        self.program['name'] = program_name
        self.program['run_time'] = None
        self.program['status'] = None
        self.program['log'] = log_file_path 
        self.program['cmd_process'] = None
        #replace str by obj
        self.program['command'] = self.program['command'].replace('\n', '').split(' ')
        self.program['stdout'] = open(self.program['stdout'], "a+")
        self.program['stderr'] = open(self.program['stderr'], "a+")

    def start(self):#prevent starting two times
        log_msg = 'start ' + self.program['name']
        self.write_file(self.program['log'], log_msg)
        self.launch_cmd()
    
    def stop(self):
        log_msg = 'stop ' + self.program['name']
        self.write_file(self.program['log'], log_msg)
        self.stop_cmd()
         

    def status(self):
        #if self.program['cmd_process'] is not None and \
         #  self.program['cmd_process'].poll() is None:
        try:
            status_msg = "{}   {} {} {} {}".format(
                                                self.program['cmd_process'].args, 
                                                self.program['status'],
                                                'PID:', 
                                                self.program['cmd_process'].pid, 
                                                'uptime: 00:00:00'
                                              )
        except Exception:
            status_msg = self.program['name'] + ' standby'
        print(status_msg)

    def stop_cmd(self):
        self.program['cmd_process'].kill()
        self.program['cmd_process'].wait()
        self.program['status'] = 'STOPPED'

    def launch_cmd(self):
        try:
            self.program['cmd_process'] = subprocess.Popen( self.program['command'],
                                            stdout=self.program['stdout'],
                                            stderr=self.program['stderr'])
            self.program['status'] = 'RUNNING'
        except Exception:
            err_msg = "ERROR: popen > " + self.data['command'] + " can't run"
            self.write_file(self.program['log'], err_msg)
            print(err_msg)
            self.program['status'] = 'FAILED'
            return False

        return True 


    def write_file(self, file, s):
        with open(file, 'a+') as f:
            f.write(s)    
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
        #intro
        self.print_stdout_log('---taskmaster session : ' + now_time + '---')

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
    
    def do_run(self, user_input):
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

if __name__ == '__main__':

    ts = Taskmaster_shell()
    try:
        ts.cmdloop()
    except KeyboardInterrupt:#and ctrl d
        Taskmaster_shell.print_stdout_log(ts, '\n\n  Ctrl + c -> exit Taskmaster\n\n')
        #relaunch new instance of taskmaster
    

    