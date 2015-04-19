from datetime import datetime
from common import IMonaJob
from thread import start_new_thread
from time import sleep
from common import COMMON_LOCK

# jobs
from vsoNotification import VSO
from jokes import Joker
from stock import StockInfo

class SampleJob(IMonaJob):
    def __run__(self, t):
        COMMON_LOCK.acquire()
        print 'yawn'
        sleep(10)
        COMMON_LOCK.release()

jobs = [VSO(), Joker(), StockInfo()]

hourAndMin = datetime.now().strftime('%H,%M').split(',')
for job in jobs:
    start_new_thread(job.__run__, (hourAndMin,))

sleep(45) # give jobs 45 seconds to run