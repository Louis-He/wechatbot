from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time

def clearlog():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

scheduler = BackgroundScheduler()
scheduler.add_job(clearlog, 'interval', seconds=3)#间隔3秒钟执行一次
scheduler.start()    #这里的调度任务是独立的一个线程

while True:
    time.sleep(2)
    print ('sleep')