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
import copy



#with open("random101.stdout",'a+') as out:
p = psutil.Popen("sleep 1", shell=True)


#while psutil.pid_exists(p.pid):
while p.is_running():
    print(p.pid, 'exists')
    print('p', p)
    print('status', p.status())
    x = p.poll()
    print("->", x)
    
    p.terminate()
    p.wait()
    
    
    

print('finish')
#try:
print('isrunning', p.is_running())
p.start()
print('isrunning', p.is_running())
#print(p.pid, 'exists')
#print('p', p)
#print('status', p.status())
#except:
print('fire')
    
#x = p.poll()
#print("->", x)
    
"""
print(p.status())
print(p.status())
print(p.status())
print(p.poll())
#p.kill()
#print(p.poll())
print(p.status())
"""







