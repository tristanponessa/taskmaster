# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: trponess <trponess@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/10/22 00:21:18 by trponess          #+#    #+#              #
#    Updated: 2019/10/24 14:11:22 by trponess         ###   ########.fr        #
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
            #print("<", line.split(" "), ">")
            #self.linex = line
            return line
        except KeyboardInterrupt:#ctrl+C
            print("\nKeyboardInterrupt : ctrl+C")
            return ('\n')
         

class MyPrompt(Cmd):
    prompt = '$> '
    intro = "Welcome! Type ? to list commands"

    def __init__(self):
        self.use_rawinput = False
        super().__init__(stdin=_Wrapper(sys.stdin))

    def emptyline(self):
        pass
      
    def do_exit(self, inp):
        print("Bye")
        return True
    
    def do_add(self, inp):
        print("adding '{}'".format(inp))

    def help_add(self):
        print("Add a new entry to the system.")

    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')

    
    def do_EOF(self, inp):
        print("EOF : ctrl+D")
        return self.do_exit(inp)
        
    def default(self, inp):
        print("command don't exist")
            

 
#    do_EOF = do_exit
 #   help_EOF = help_exit



if __name__ == '__main__':
    MyPrompt().cmdloop()

