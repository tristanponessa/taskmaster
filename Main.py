import sys

v = sys.version_info
if not (v.major == 3 and v.minor == 6):
   print(f'ERROR : wrong python version {v} please launch v3.6')
   sys.exit(0)

import os
import Taskmaster as tsFILE #psutil in 3.8 causes crash
import Global

if __name__ == '__main__':

    ts = tsFILE.Taskmaster_shell()
    try:
        ts.cmdloop()
    except (KeyboardInterrupt, EOFError) as e:#and ctrl d
        #Taskmaster_shell.print_stdout_log(ts, '\n\n  Ctrl + c -> exit Taskmaster\n\n')
        #STOP ALL PS
        if e.__class__.__name__ == 'KeyboardInterrupt':
            Global.printx('\n\n  Ctrl + c -> exit Taskmaster\n\n')
        else:
            Global.printx('\n\n  Ctrl + d -> graceful exit Taskmaster\n\n')
            
            
    finally:
        pids = Global.load_file(Global.pss_file)
        Global.printx('killing pids created by taskmaster : \n', *pids, '\n',end='')
        Global.kill_leftover()#control which
        
        
        if Global.reboot:
            os.execl(sys.executable, sys.executable, *sys.argv)
    """
    except Exception as e:
        print(traceback.print_exc())
        print('::::CRASH REBOOTING.....::::')
        os.execl(sys.executable, sys.executable, *sys.argv)
    """
    #relaunch new instance of taskmaster
