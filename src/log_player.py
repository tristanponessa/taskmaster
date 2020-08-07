import time
import os

#no with , it will close while main will operate on the file
os.chdir('.')

f = open('../logs/taskmaster.log', 'r')
#with open('../logs/taskmaster.log', 'r') as f:
l = f.readlines()
print(*l, end='\n')


cur = []
while True:
    l = []
    #with open('../logs/taskmaster.log', 'r') as f:
    l = f.readlines()
    if cur != l:
        print('diff')
        cur = l.copy()
        print(*l, end='\n')
    
    time.sleep(1)


