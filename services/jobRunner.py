from datetime import datetime
from common import IMonaJob
from thread import start_new_thread
from threading import Lock
from time import sleep

# jobs
from vsoNotification import VSO


class SampleJob(IMonaJob):
    def __run__(self, t, l):
        l.acquire()
        print 'yawn'
        sleep(10)
        l.release()

lock = Lock()
jobs = [SampleJob(), VSO()]

hourAndMin = datetime.now().strftime('%H,%M').split(',')
for job in jobs:
    start_new_thread(job.__run__, (hourAndMin, lock))

sleep(30) # give jobs 30 seconds to run