__author__ = 'sachinpatney'

'''
    This task will be launched very frequently,
    typically once per minute via an OS Cron Job.

    It will run all registered tasks each time,
    it is up to each task to use the time info
    and only run when required.

    For example the stock closing is only run at
    415 PM PST.

'''

from datetime import datetime
from common import IMonaTask
from thread import start_new_thread
from time import sleep
from common import TALKING_PILLOW

# tasks
from vso import VSO
from jokes import Joker
from stock import StockInfo


class SampleTask(IMonaTask):
    def __run__(self, t):
        TALKING_PILLOW.acquire()
        print 'yawn, acquring sound card lock for fun :) Do not do this :P'
        sleep(10)
        TALKING_PILLOW.release()

jobs = [VSO(), Joker(), StockInfo()]

hourAndMin = datetime.now().strftime('%H,%M').split(',')
# hourAndMin = ['1','15'] #test with specific time

for job in jobs:
    start_new_thread(job.__run__, (hourAndMin,))

sleep(45)  # give jobs 45 seconds to run