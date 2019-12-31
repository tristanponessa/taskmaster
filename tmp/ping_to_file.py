import multiprocessing
import subprocess
import time 

stdout_file = open('ping.txt', "w+")
#p = subprocess.Popen(["ping", "127.0.0.1"], stdout=stdout_file)
p = subprocess.Popen(["sh", "sec_counter.bash"], stdout=stdout_file)
try:
    p.communicate(timeout=3)
except subprocess.TimeoutExpired:
    p.kill()
    print('process done')
    
