import  time
import datetime

b_time = datetime.datetime.now()
time.sleep(5)
e_time = datetime.datetime.now()
now_time =( e_time - b_time)
print('B',b_time.strftime('%Y-%m-%d %H:%M:%S'))
print('N',now_time)