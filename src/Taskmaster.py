
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
import os
import signal
import traceback
import signal 
import readline
#files
import Process as psFILE
import Conf as confFILE
import Global


"""
NOTES:
"""



#has auto complete but not for args for do commands
class Taskmaster_shell(cmd.Cmd):

    """
        Taskmaster class :
            -checks user input
            -stocks pgs in list from file
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
    
    intro = 'welcome to TASKMASTER'


    def __init__(self):
        
        super().__init__()


        #dipslay help
        Global.print_log('---taskmaster session : ' + Global.now_time() + '---')
        
        Global.clean_historyFile()
        readline.read_history_file(Global.history_file)
        #Global.setup_files()

        #load your running process on computer
        
        #auto to avoid taping everything everytime
        self.do_init("./config/taskmaster_conf.json")
        #self.do_start("shg")
        #self.do_init("./config/taskmaster_conf2.json")
        #self.do_status("")
        #self.do_exit("")
        #self.do_stop("random101")
        #self.do_status("")
        #self.do_start("shg")
        #self.do_status("")
        #self.do_stop("shg")
        #self.do_status("")
        #self.do_stop("random101")
        #self.do_stop("random101")
        #self.do_status("")
        

    def precmd(self, user_input):
        #LOG
        Global.print_file(Taskmaster_shell.prompt + user_input, Global.log_file, 'a+')
        Global.print_file(f'{user_input}',Global.history_file,'a')
        
        psFILE.pgs_check_state()
        
        #psFILE.pgs_reboot_if_wrongExitcode()

        return cmd.Cmd.precmd(self, user_input)

    def do_history(self, user_input):
        l = Global.load_file(Global.history_file)
        if user_input == "":
            for i,s in enumerate(l):
                print(f'{i}.{s}', end='')
        else:
            i = int(user_input)
            self.onecmd(l[i])
    
    def do_init(self, user_input):
        #init conf file 
        err = confFILE.is_confFile(user_input)
        if err != []:
            Global.print_log(*err)
        else:
            #LOG
            Global.print_log(f"old conf file {confFILE.conf}")

            confFILE.confReload(user_input)
            psFILE.init_pgs()

            #LOG
            Global.print_log(f"updated conf file {confFILE.conf}")

    """
    def do_uninit(self, user_input):
        
        if user_input != '':
            Global.print_log("no args display help for uninit")
        else:
            Global.print_log("uninit conf file")
            confFILE.conf = dict()
            Global.print_log(f"{confFILE.conf}")
    """
    

    def do_print(self, user_input):
        if user_input == 'pgs':
            psFILE.display_pgs()
        if user_input == 'conf':
            print(confFILE.conf)
        if user_input == 'pwd':
            os.system('pwd')
        if user_input == 'conf':
            print(confFILE.conf_name)

        """
        if user_input == 'pgs_file':
            os.system(f'cat {Global.pgs_file}')
        if user_input == 'res_file':
            os.system(f'cat {Global.tk_res}')
        if user_input == 'log_file':
            os.system(f'cat {Global.taskmaster_log}')
        """
    
    def do_start(self, user_input):
        self.toggle_program(user_input, 'start')

    def do_stop(self, user_input):
        self.toggle_program(user_input, 'stop')
    
    """
    def do_reload(self, user_input):
        self.toggle_program(user_input, 'stop')
        self.toggle_program(user_input, 'start')
    """

    def get_userInput_arg(self, inp, index):
        inp_args = inp.split(' ')
        print(inp_args)
        if index < len(inp):
            return inp_args[index]

    def toggle_program(self, inp, action):

        pgLst = psFILE.get_pgs(inp) 
        if pgLst == []:
            Global.print_log(f"program <{inp}> don't exist") 
        else:

            d = {'start': lambda pgObj : pgObj.start_pg(),
                 'stop':  lambda pgObj : pgObj.stop_pg()}

            for pgName in pgLst: 
                pgObj = psFILE.pgs[pgName]
                res = d[action](pgObj)
                x = "already" if res == False else ''
                Global.print_log(f"{pgName} : action {action} {x} launched")

    
    def do_status(self, user_input):

        keys = psFILE.pgs.keys()
        if (user_input != ''):
            keys = psFILE.get_pgs(user_input) 
            if keys == []:
                Global.print_log("pgr |" + user_input + "| don't exist")
                return
            
        for k in keys:
            pgObj = psFILE.pgs[k]
            status_msg = pgObj.status_pg()
            #LOG
            Global.print_log(status_msg)
    
    def do_signal(self, inp):
        sigName = self.get_userInput_arg(inp, 0)
        pgTag = self.get_userInput_arg(inp, 1)

        pgLst = psFILE.get_pgs(pgTag)
        err = []
        values = [item.name for item in signal.Signals]
        if sigName not in values:
            err.append(f"signal <{sigName}> don't exist")
        if pgLst == []:
            err.append(f"program <{pgTag}> don't exist") 
        #for ierr in err:
        #    Global.print_log(err)
        if err != []:
            for ierr in err:
                Global.print_log(err)
            #map(lambda x : Global.print_log(x), err)
            return  
        
        for psName in pgLst:
            sigNb = signal.Signals[sigName].value
            r = psFILE.pgs[psName].signalJob_if_pgInit(sigNb)
            if r == False:
                Global.print_log(f'{psName} not running') 


    def do_result(self, user_input):
        l = Global.load_file(Global.tk_res)
        Global.print_log(*l)

    def emptyline(self):
        pass
    
    def default(self, inp):
        Global.print_log("display help")
        self.do_help()
      
    def do_exit(self, inp):
        Global.print_log("<Exiting Taskmaster>\n\n")
        return True
    
    def do_EOF(self, line):
        Global.print_log('\n\n  Ctrl + d -> exit Taskmaster\n\n')
        return True

    def do_help(self, user_input=''):
        print('srcew you!')
    
    def do_reboot(self, i):
        Global.print_log("REBOOT")
        Global.reboot = True
        self.do_exit()
        
