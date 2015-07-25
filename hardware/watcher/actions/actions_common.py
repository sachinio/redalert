__author__ = 'sachinpatney'


class IAction:
    def __init__(self):
        pass

    def __do__(self):
        raise Exception('This should be overridden')

