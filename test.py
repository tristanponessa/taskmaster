from datetime import datetime, timedelta 
import time 

"""
#ini_time_for_now = time.strftime("%H:%M:%S", time.localtime(datetime.now()))
beg = datetime.now()
print(str(beg)) 
time.sleep(5)
# printing initial_date 
#print ("initial_date", str(ini_time_for_now)) 
now = datetime.now()
print(str(now))
# Calculating future dates 
# for two years 

#future_date_after_2yrs = ini_time_for_now + timedelta(hours = 2)   

diff = now - beg
print(str(diff))

x = time.strftime("%H:%M:%S", time.localtime(diff))
print(x)
"""

t0 = time.time()
print (time.strftime("%H:%M:%S",time.localtime(t0)))
t1 = t0 + 3600 * 2
print (time.strftime("%H:%M:%S",time.localtime(t1)))

#print('future_date_after_2yrs:', str(future_date_after_2yrs)) 