__author__ = 'sachinpatney'


class IMonaJob():

    def __run__(self, time, lock):
        """Runs the job"""
        raise Exception('You must implement __run__ method on your service')