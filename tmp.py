#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/10/22 00:21:18 by trponess          #+#    #+#              #
#    Updated: 2019/12/15 20:04:11 by user             ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#!/usr/bin/python3.6



import time
import sys
from cmd import Cmd
import keyword

         
class MyPrompt(Cmd):
    prompt = '$> '
    intro = "Welcome! Type ? to list commands"

    def __init__(self):
        pass

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

