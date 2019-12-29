import os
pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]

for pid in pids:
    try:
        #print open(os.path.join('/proc', pid, 'cmdline'), 'rb').read().split('\0')
        
         print pid
    except IOError: # proc has already terminated
        continue

  cmd_ps_name = 'ps -o cmd --no-headers'
        cmd_ps_pid_= 'ps -o pid --no-headers'
        cmd_ps_state = 'ps -o state --no-headers'
        cmd_ps_etime = 'ps -o etime --no-headers'

        cmd_ps = 'ps -o {info} --no-headers'.format(info=info)
        cmd_grep = 'grep "{ps_name}"'.format(ps_name=ps_name)
 
        p1 = subprocess.Popen(cmd_ps, stdout=subprocess.PIPE)
        p2 = subprocess.Popen(cmd_grep, stdin=p1, stdout=subprocess.PIPE)
        val = p2.stdout.read().decode('ascii').replace('\n', '')
        return val
        

        #cmd = 'ps -o cmd,pid,state,etime | grep "{cmd}"'.format(cmd=cmd)
        #p = self.run_cmd(cmd, subprocess.PIPE, subprocess.PIPE, True)
        #put shell to false t oavoid bin/bash process to be launched
        #may have to devide the popen into two
        #p.wait()
        
        os_ps = dict()
        p = subprocess.Popen(cmd_ps_name, stdout=subprocess.PIPE)
        lst = p.stdout.read().decode('ascii').split('\n')
        for l in lst:
            os_ps[l] = dict()
        
        p = subprocess.Popen(cmd_ps_pid, stdout=subprocess.PIPE)
        pid_lst = p.stdout.read().decode('ascii').split('\n')
        for pc,pid in itertools.izip(os_ps.keys(), pid_lst):
            os_ps[k]['pid'] = 

        cmd_output = p.stdout.read()
        os_pc = dict()
        pc_str_lst = cmd_output.decode('ascii').split('\n')
        #pc_str_lst = [pc_bstr.decode('ascii') for pc_bstr in pc_bstr_lst]
        for pc_str in pc_str_lst:
            pc_str_div = pc_str.split( )
            #have to fetch manually 'cmdsh x pidNNNNN is a command
            pc_name = pc_str[]

            pc_name = pc_str_div[0]
            os_pc[pc_name] = dict()
            os_pc[pc_name]['pid'] = pc_str_div[1]
            os_pc[pc_name]['state'] = pc_str_div[2]
            os_pc[pc_name]['etime'] = pc_str_div[3]
            

        
        ps_info = cmd_output.decode('ascii').split('\n')
        if info == 'list':
            return ps_info
        if cmd_output == '':
            return None
        #i consider theres only one string when here
        ps_info = cmd_output.decode('ascii').replace('\n', ' ').split(' ')
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
