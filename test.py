import time
import sys
from cmd import Cmd
import keyword


class _Wrapper:

    def __init__(self, fd):
        self.fd = fd
    
    #is called on enter
    def readline(self, *args):
        try:
            line = self.fd.readline(*args)
            print("<", line.split(" "), ">")
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
        
        
    
    def preloop(self):
        print(sys.stdin.readline())
        Cmd.preloop(self)

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
from curtsies import Input

def main():
    with Input(keynames='curses') as input_generator:
        for e in input_generator:
            print(repr(e))

#if __name__ == '__main__':
#    main()


if __name__ == '__main__':
    
    
    MyPrompt().cmdloop()
