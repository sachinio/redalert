__author__ = 'sachinpatney'

import fcntl, time, csv, os
from common import STATUS_FILE_LOCK
from thread import start_new_thread

def sync_write_to_file(name, operation, message):
    with open(name, operation) as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        f.write(message)

def read_csv(path):
    reader = csv.reader(open(path, 'rb'))
    return dict(x for x in reader)


def write_to_csv(dict, path):
    writer = csv.writer(open(path, 'wb'))
    for key, value in dict.items():
        writer.writerow([key, value])




start_new_thread(sync_write_to_status_file, ('broken', True,))
start_new_thread(sync_write_to_status_file, ('key', 'somevalue',))

time.sleep(3)