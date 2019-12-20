
import cmd
import subprocess

class Taskmaster_shell(cmd.Cmd):
    
    prompt = '$> '
    intro = "Welcome! Type ? to list commands"
    
    FRIENDS = [ 'Alice', 'Adam', 'Barbara', 'Bob' ]
    
    def __init__(self):
        super().__init__()
        self.data = dict()
        with open("config/.conf", "r") as f:
            lines = f.readlines()
        for line in lines:
            key, value = line.split('=')
            self.data[key] = value
        
        #create file
        open(self.data['stdout'], "a+").close()
        open(self.data['stderr'], "a+").close()

    def emptyline(self):
        pass
    
    def default(self, inp):
        print("command don't exist")
      
    def do_exit(self, inp):
        print("Bye")
        return True
    
    def do_run(self, person):
        with open(self.data['stdout'], "w") as stdout_file, \
             open(self.data['stderr'], "w") as stderr_file:
            subprocess.run(["python3", "time_program.py"], stdout=stdout_file ,stderr=stderr_file)
        print("runnung time")
    
    def complete_greet(self, text, line, begidx, endidx):
        if not text:
            completions = self.FRIENDS[:]
        else:
            completions = [f for f in self.FRIENDS if f.startswith(text)]
        return completions
    
    def do_EOF(self, line):
        return True

if __name__ == '__main__':
    ts = Taskmaster_shell()
    ts.cmdloop()