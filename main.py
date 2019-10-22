# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: trponess <trponess@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/10/22 00:21:18 by trponess          #+#    #+#              #
#    Updated: 2019/10/22 06:01:38 by trponess         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#!/usr/bin/python3.6

import time
import sys
from cmd import Cmd

class _Wrapper:

    def __init__(self, fd):
        self.fd = fd

    def readline(self, *args):
        try:
            return self.fd.readline(*args)
        except KeyboardInterrupt:#ctrl+C
            print("KeyboardInterrupt : ctrl+C")
            return ('\n')
            

class MyPrompt(Cmd):
    prompt = 'pb> '
    intro = "Welcome! Type ? to list commands"
    
    def __init__(self):
        super().__init__(stdin=_Wrapper(sys.stdin))
        self.use_rawinput = False
        self.prompt = '$ '

    FRIENDS = [ 'Alice', 'Adam', 'Barbara', 'Bob' ]
    
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
        if not text:
            completions = self.FRIENDS[:]
        else:
            completions = [ f
                            for f in self.FRIENDS
                            if f.startswith(text)
                            ]
        return completions

    
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
        

            

 
#    do_EOF = do_exit
 #   help_EOF = help_exit


if __name__ == '__main__':
    MyPrompt().cmdloop()
