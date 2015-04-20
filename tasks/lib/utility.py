__author__ = 'sachinpatney'

import fcntl, time


def sync_write_to_file(name, operation, message):
    with open(name, operation) as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        f.write(message)