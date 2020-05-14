
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
import Json as jsonFILE
import Global
from jinja2.filters import do_default

"""
NOTES:
    TASKMASTER WILL LAUNCH pss FROM 1 OR MULTIPLE CONF FILES
    YOU CAN PRECISE EACH PROGRAM
    SUPERVISOR SEEMED TO DO THINGS BY CONFIG FILE

    #issues : bin/bash being spawed by popen must kill() them
    #a program is 1 process like ls or count_time

    bunch of functions use copy code , reduce to uniuversal functions
    
    check aname of pss regex no <>...
    add colors to make it clear for already launched and errors in red 
    launch everythoin gas multiprocess so umask can ably all the time for a process
    dont launch program without config file good
    universal vaklue system umasl not set ? how to check?
    
    
    psutil process contains much more infos than subprocess 
    i could make a simpler version with popen alone and use p.pid / p.status and two more others
    psutil offers so much more and to make it flexible i created this complicated system where
    you have to simply call self.program[info]() 
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
        
        self.pss = dict()

        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        #dipslay help
        Global.printx('---taskmaster session : ' + now_time + '---')
        
        readline.read_history_file(Global.history_file)
        

        #load your running process on computer
        
        #auto to avoid taping everything everytime
        self.do_init("./config/taskmaster_conf.json")
        #self.do_start("random101")
        self.do_status("")
        #self.do_stop("random101")
        #self.do_status("")
        #self.do_stop("random101")
        #self.do_stop("random101")
        #self.do_status("")
        
    

    def precmd(self, user_input):
        
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
        
        err = Global.is_conf_file(user_input)
        if err != []:
            Global.printx(*err)
        else:
            Global.printx("updated conf file")
            jsonFILE.load_json(user_input)
            Global.printx(f"{jsonFILE.conf}")
            
            self.pss.clear()
            #only stop those who are active
            
            for ps,props in jsonFILE.conf.items():
                self.pss[ps] = psFILE.Process(ps, props)
            
            
    
    def do_uninit(self, user_input):
        
        if user_input != '':
            Global.printx("no args display help for uninit")
        else:
            Global.printx("uninit conf file")
            jsonFILE.conf = dict()
            Global.printx(f"{jsonFILE.conf}")
    
    

    def do_echo(self, user_input):
        if user_input == 'config':
            print(jsonFILE.conf)
        if user_input == 'ps':
            print(self.pss)

    #def do_run_all(self, user_input):
     #   for program in self.pss:
      #      program.run()
    
    def do_pwd(self, user_input):
        os.system('pwd')
    
    def do_start(self, user_input):
        self.toggle_program(user_input, 'start')

    def do_stop(self, user_input):
        self.toggle_program(user_input, 'stop')
    
    def do_reload(self, suer_input):
        self.toggle_program(user_input, 'stop')
        self.toggle_program(user_input, 'start')
    
    def toggle_program(self, ps, action):
        if ps not in self.pss.keys():
            Global.printx("program <" + ps + "> don't exist")
            return
        if action == 'stop':  
            res = self.pss[ps].stop_ps()
        if action == 'start':
            res = self.pss[ps].start_ps()
        
        if res == False: 
            Global.printx("action " + action + " already launched")
        else:            
            Global.printx("action " + action + " launched")
    
    def do_status(self, user_input):
        if user_input == '':
            for program in self.pss.keys():
                status_msg = self.pss[program].status_ps()
                Global.printx(status_msg)
        else:
            if not user_input in self.pss:
                Global.printx("process |" + user_input + "| don't exist")
                return
            status_msg = self.pss[user_input].status_ps()
            Global.printx(status_msg)
            
                


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
    
    
        
        
        
