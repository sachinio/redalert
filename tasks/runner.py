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
from thread import start_new_thread
from time import sleep

# tasks
from vso import VSO
from jokes import Joker
from stock import StockTicker
from days_to_ga import DaysToGA

tasks = [VSO(), Joker(), StockTicker(), DaysToGA()]

time_info_list = datetime.now().strftime('%H,%M').split(',')

options = {'hour': time_info_list[0], 'min': time_info_list[1]}

print options

if len(sys.argv) == 3:  # This is for testing the runner with a specific time
    options = {'hour': sys.argv[1], 'min': sys.argv[2]}

for task in tasks:
    start_new_thread(task.__run__, (options,))

sleep(45)  # give jobs 45 seconds to run
