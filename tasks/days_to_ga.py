__author__ = 'sachinpatney'

import datetime

from common import ITask
from common import Timeline


class DaysToGA(ITask):
    def __init__(self):
        pass

    def __run__(self, time):
        if time['hour'] == '8' and time['min'] == '15':
            d0 = datetime.datetime.now().date()
            d1 = datetime.date(2015, 7, 24)
            delta = d1 - d0
            Timeline.add_item_from_bot('{0} days to GA :)'.format(delta.days),
                                       '',
                                       ['owl.gif', 'owl2.gif'][delta.days % 2],
                                       'fa-bullhorn',
                                       'info')
