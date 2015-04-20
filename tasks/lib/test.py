__author__ = 'sachinpatney'

import fcntl, time
from thread import start_new_thread


def write_to_sync_to_file(name, operation):
    with open(name, operation) as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        f.write('Hello\n')
        print n + ' done with firt sleep'
    time.sleep(2)
    print n + ' done with second sleep'


start_new_thread(write_to_sync_to_file, ('0', ))
start_new_thread(write_to_sync_to_file, ('1', ))

time.sleep(12)