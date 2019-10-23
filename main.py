# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: user <user@student.42.fr>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/10/22 00:21:18 by trponess          #+#    #+#              #
#    Updated: 2019/10/23 02:10:33 by user             ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#!/usr/bin/python3.6

import time
import sys
from cmd import Cmd
import keyword


class _Wrapper:

    linex = None
    
    def __init__(self, fd):
        self.fd = fd
        

    def readline(self, *args):
        try:
            line = self.fd.readline(*args)
            print("<", line.split(" "), ">")
            self.linex = line
            return line
        except KeyboardInterrupt:#ctrl+C
            print("KeyboardInterrupt : ctrl+C")
            return ('\n')
         

class MyPrompt(Cmd):
    prompt = 'pb> '
    intro = "Welcome! Type ? to list commands"
    FRIENDS = [ 'Alice', 'Adam', 'Barbara', 'Bob' ]

    def __init__(self):
        self.use_rawinput = False
        super().__init__(stdin=_Wrapper(sys.stdin))
        
        #if self.stdin == 'ls\n':
         #   print("tab")
        #dir(self.stdin)
        
        #self.prompt = '$ '
        #self.FRIENDS = [ 'Alice', 'Adam', 'Barbara', 'Bob' ]
    
    def do_greet(self, person):
        "Greet the person"
        if person and person in self.FRIENDS:
            greeting = 'hi, %s!' % person
        elif person:
            greeting = "hello, " + person
        else:
            greeting = 'hello'
        print (greeting)
    
    def complete_greet(self, text, line, begidx, endidx):
        print("xxx")
        if not text:
            completions = self.FRIENDS[:]
        else:
            completions = [ f
                            for f in self.FRIENDS
                            if f.startswith(text)
                            ]
        return completions
    
    #def defaultcomplete(self, text, line, begidx, endidx):


    def precmd(self, line):
        print("precmd line:", line)
        if line == '\t':
            print("tab")
        
        return super().precmd(line)
        
    def do_exit(self, inp):
        print("Bye")
        return True
    
    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')
 
    def do_add(self, inp):
        print("adding '{}'".format(inp))
    
    def complete_add(self, inp):
        return ["AAA"]
 
    def help_add(self):
        print("Add a new entry to the system.")
    
    def emptyline(self):
        pass
    
    def do_EOF(self, inp):
        print("EOF : ctrl+D")
        return self.do_exit(inp)
        
    def default(self, inp):
        print("command don't exist")
    
    def do_tab(self, inp):
        print("x")
        

            

 
#    do_EOF = do_exit
 #   help_EOF = help_exit



if __name__ == '__main__':
    MyPrompt().cmdloop()

