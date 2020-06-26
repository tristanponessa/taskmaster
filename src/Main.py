import sys

"""
v = sys.version_info
if not (v.major == 3 and v.minor == 6):
   print(f'ERROR : wrong python version {v} please launch v3.6')
   sys.exit(0)
"""

import os
import Taskmaster as tsFILE #psutil in 3.8 causes crash
import Global

if __name__ == '__main__':
    
    #exitid = None

    try:
        ts = tsFILE.Taskmaster_shell()
        ts.cmdloop()
        #exitid = 0
    except (KeyboardInterrupt, EOFError) as e:#and ctrl d
        #Taskmaster_shell.print_stdout_log(ts, '\n\n  Ctrl + c -> exit Taskmaster\n\n')
        #STOP ALL PS
        if e.__class__.__name__ == 'KeyboardInterrupt':
            Global.printx('\n\n  Ctrl + c -> exit Taskmaster\n\n')
            #exitid = signal.SIGINT.value
        else:#suppose to be SIGHUP
            Global.printx('\n\n  Ctrl + d -> graceful exit Taskmaster\n\n')
            
            
            #exitid = 77
            
            
    finally:
        pass
        #Global.printx('killing pids created by taskmaster : \n')
        #Global.kill_leftover()#control which
        
        #Global.print_file(f'{Global.now_time()} TASKMASTER EXIT : {exitid} expected {Json.conf['']} > ')
        
        #if Global.reboot:
        #    os.execl(sys.executable, sys.executable, *sys.argv)
    """
    except Exception as e:
        print(traceback.print_exc())
        print('::::CRASH REBOOTING.....::::')
        os.execl(sys.executable, sys.executable, *sys.argv)
    """
    #relaunch new instance of taskmaster
