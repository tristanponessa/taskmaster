
import cmd
import subprocess
import multiprocessing
import threading
import configparser

class cmd_process():

    def __init__(self):
        self.dir
        self.command
        self.autostart
        self.autorestart
        self.stoptime
        self.starttime
        self.retry
        self.nbretries
        self.stdout
        self.stderr
        self.env
        self.exitcodes
        self.succodes
        self.umask

      

class Taskmaster_shell(cmd.Cmd):
    
    prompt = 'taskmaster> '
    intro = "Welcome! Type ? to list commands"
    
    FRIENDS = [ 'Alice', 'Adam', 'Barbara', 'Bob' ]
    
    def __init__(self):
        super().__init__()
        self.data = dict()
        self.running_proc = []
        with open("config/.conf", "r") as f:
            lines = f.readlines()
        for line in lines:
            if '=' in line:
                key, value = line.split('=')
                self.data[key] = value
        
        #create file
        self.stdout_file = open(self.data['stdout'], "w+")
        self.stderr_file = open(self.data['stderr'], "w+")
        self.cmd_process = None
    
    def do_run(self, user_input):
        print('REP' + '<' + user_input + '>')
        print('REP clean',  self.clean_command(self.data['command']))
        try:
            cmd_process = subprocess.Popen(self.clean_command(self.data['command']), 
                                                            stdout=self.stdout_file,
                                                            stderr=self.stderr_file)
        except Exception:
            print("ERROR: popen > " + self.data['command'] + " can't run")
            return 

        self.running_proc.append(cmd_process)
    
    def do_status(self, user_input):
        for cmd_process in self.running_proc:
            print("{}   {} {} {} {}".format(cmd_process.args, 'RUNNING','PID:', cmd_process.pid, 'uptime: 00:00:00'))
       

    def do_stopall(self, user_input):
        for cmd_process in self.running_proc:
            print("{} {} {} {}".format("process :", cmd_process.args, 'PID:', cmd_process.pid))
            cmd_process.kill()
            cmd_process.wait()
            self.running_proc = []

    def clean_command(self, user_command):
        x = user_command
        x = x.replace('\n', '')
        x = x.split(' ')
        return x

    def emptyline(self):
        pass
    
    def default(self, inp):
        print("display help")
      
    def do_exit(self, inp):
        print("<Exiting Taskmaster>")
        self.stdout_file.close()
        self.stderr_file.close()
        return True


    def complete_greet(self, text, line, begidx, endidx):
        if not text:
            completions = self.FRIENDS[:]
        else:
            completions = [f for f in self.FRIENDS if f.startswith(text)]
        return completions
    
    def do_EOF(self, line):
        print("ctrl+D > exit Taskmaster")
        return True

if __name__ == '__main__':

    conf = configparser.ConfigParser()
    conf.read('./config/taskmaster_conf.ini')
    

    ts = Taskmaster_shell()
    try:
        ts.cmdloop()
    except KeyboardInterrupt:
        print('\n\n  Ctrl + c -> exiting shell')

