__author__ = 'sachinpatney'

'''
    This runner will be launched very frequently,
    typically once per minute via an OS Cron Job.

    It will run all registered tasks each time,
    it is up to each task to use the time info
    and only run when required.

    For example the stock closing is only run at
    1:15 PM PST.

'''

import sys

from datetime import datetime
from common import IMonaTask
from thread import start_new_thread
from time import sleep
from common import TALKING_PILLOW

# tasks
from vso import VSO
from jokes import Joker
from stock import StockTicker
from days_to_ga import DaysToGA


class SampleTask(IMonaTask):
    def __init__(self):
        pass

    def __run__(self, t):
        TALKING_PILLOW.acquire()
        print 'yawn, i have the talking pillow even though i am not talking :) Do not do this :P'
        sleep(10)
        TALKING_PILLOW.release()


tasks = [VSO(), Joker(), StockTicker(), DaysToGA()]

hourAndMin = datetime.now().strftime('%H,%M').split(',')

if len(sys.argv) == 3:  # This is for testing the runner with a specific time
    hourAndMin = [sys.argv[1], sys.argv[2]]

for task in tasks:
    start_new_thread(task.__run__, (hourAndMin,))

sleep(45)  # give jobs 45 seconds to run
