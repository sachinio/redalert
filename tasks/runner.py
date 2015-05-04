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
import threading

from datetime import datetime
from time import sleep

# tasks
from vso import VSO
from jokes import Joker
from stock import StockTicker
from days_to_ga import DaysToGA
from weather import WeatherTask

tasks = [VSO(), Joker(), StockTicker(), DaysToGA(), WeatherTask()]

time_info_list = datetime.now().strftime('%H,%M').split(',')

options = {'hour': time_info_list[0], 'min': time_info_list[1]}

if len(sys.argv) == 3:  # This is for testing the runner with a specific time
    options = {'hour': sys.argv[1], 'min': sys.argv[2]}

for task in tasks:
    threading.Thread(target=task.__run__,
                     args=(options,),
                     kwargs=None,
                     ).start()

    # start_new_thread(task.__run__, (options,))

sleep(45)  # give jobs 45 seconds to run
