
import cmd
import subprocess
import multiprocessing
import threading
import configparser
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
        self.program['stdout'] = open(self.program['stdout'], "w+")
        self.program['stderr'] = open(self.program['stderr'], "w+")

    def start(self):#prevent starting two times
        log_msg = 'start ' + self.program['name']
        self.write_file(self.program['log'], log_msg)
        self.launch_cmd()
    
    def stop(self):
        log_msg = 'stop ' + self.program['name']
        self.write_file(self.program['log'], log_msg)
        self.stop_cmd()
         

    def status(self):
        status_msg = "{}   {} {} {} {}".format(
                                                self.program['cmd_process'].args, 
                                                self.program['status'],
                                                'PID:', 
                                                self.program['cmd_process'].pid, 
                                                'uptime: 00:00:00'
                                              )
        print(status)

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
        with open(file, 'w+') as f:
            f.write(s)    
       # def run_cmd(self)


 

      

class Taskmaster_shell(cmd.Cmd):
    
    prompt = 'taskmaster> '
    intro = "Welcome! Type ? to list commands"
    
    def __init__(self):
        super().__init__()
        self.conf = configparser.ConfigParser()
        self.conf.read('./config/taskmaster_conf.ini')
        self.log_file_path = './taskmaster.log'
        self.programs = dict()

        
    def do_init(self, user_input):
        print("running programs in conf file...")
        for program_name,section in self.conf._sections.items():
            clean_program_name = program_name.replace("program:", "")
            p = Program(clean_program_name, section, self.log_file_path)
            self.programs[clean_program_name] = p
        pass

    #def do_run_all(self, user_input):
     #   for program in self.programs:
      #      program.run()
    
    def do_run(self, user_input):
        if user_input == '':
           print('zzz')
        elif user_input not in self.programs.keys():
            print("program don't exist")
        else:
            self.programs[user_input].start()
    
    def do_stop(self, user_input):
            self.programs[user_input].stop()
    #def do_status(self, user_input):
     #    for program in self.programs:
      #      program.status()
       
    """
    docstring
    
    def do_stopall(self, user_input):
        for cmd_process in self.running_proc:
            print("{} {} {} {}".format("process :", cmd_process.args, 'PID:', cmd_process.pid))
            cmd_process.kill()
            cmd_process.wait()
            self.running_proc = []
    """

    def emptyline(self):
        pass
    
    def default(self, inp):
        print("display help")
      
    def do_exit(self, inp):
        print("<Exiting Taskmaster>")
        return True
    
    def do_EOF(self, line):
        print("ctrl+D > shell catch")
        return True

if __name__ == '__main__':

    ts = Taskmaster_shell()
    try:
        ts.cmdloop()
    except KeyboardInterrupt:#and ctrl d
        print('\n\n  Ctrl + c -> exit Taskmaster')
    except EOFError:#and ctrl d
        print("n\n\  ctrl + d > exit Taskmaster")
