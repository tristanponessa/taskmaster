
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
            -stocks pss in list from file
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
        Global.printx('---taskmaster session : ' + Global.now_time() + '---')
        
        readline.read_history_file(Global.history_file)
        #Global.setup_files()

        #load your running process on computer
        
        #auto to avoid taping everything everytime
        self.do_init("./config/taskmaster_conf.json")
        #self.do_start("shg")
        self.do_status("")
        #self.do_exit("")
        #self.do_stop("random101")
        #self.do_status("")
        #self.do_start("random101")
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
            Global.printx(*err)
        else:
            #LOG
            Global.printx(f"old conf file {confFILE.conf}")

            confFILE.confReload(user_input)
            psFILE.init_pss()

            #LOG
            Global.printx(f"updated conf file {confFILE.conf}")

    """
    def do_uninit(self, user_input):
        
        if user_input != '':
            Global.printx("no args display help for uninit")
        else:
            Global.printx("uninit conf file")
            confFILE.conf = dict()
            Global.printx(f"{confFILE.conf}")
    """
    

    def do_print(self, user_input):
        if user_input == 'pss':
            psFILE.display_pss()
        if user_input == 'conf':
            print(confFILE.conf)
        if user_input == 'pwd':
            os.system('pwd')
        """
        if user_input == 'pss_file':
            os.system(f'cat {Global.pss_file}')
        if user_input == 'res_file':
            os.system(f'cat {Global.tk_res}')
        if user_input == 'log_file':
            os.system(f'cat {Global.taskmaster_log}')
        """
    
    def do_start(self, user_input):
        self.toggle_program(user_input, 'start')

    def do_stop(self, user_input):
        self.toggle_program(user_input, 'stop')
    
    def do_reload(self, user_input):
        self.toggle_program(user_input, 'stop')
        self.toggle_program(user_input, 'start')
    
    def toggle_program(self, ps, action):
        if ps not in psFILE.pss.keys():
            Global.printx("program <" + ps + "> don't exist")
        else:
            inst_lst = psFILE.pss[ps]
            res = None
            for i in range(len(inst_lst)):
                if action == 'start':
                    res = inst_lst[i].start_ps()
                if action == 'stop':
                    res = inst_lst[i].stop_ps()    
                #LOG
                if res == False: 
                    Global.printx("action " + action + " already launched")
                else:            
                    Global.printx("action " + action + " launched")
    
    def do_status(self, user_input):

        keys = psFILE.pss.keys()
        if (user_input != ''):
            if (user_input in psFILE.pss):
                keys = [user_input]
                #LOG
            else:
                Global.printx("process |" + user_input + "| don't exist")
                return
            
        for k in keys:
            lst = psFILE.pss[k]
            for elem in lst:
                status_msg = elem.status_ps()
                #LOG
                Global.printx(status_msg)

    def do_result(self, user_input):
        l = Global.load_file(Global.tk_res)
        Global.printx(*l)

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
        Global.printx("REBOOT")
        Global.reboot = True
        self.do_exit()
        
