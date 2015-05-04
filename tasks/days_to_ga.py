__author__ = 'sachinpatney'

import datetime
import os

from common import ITask
from common import Timeline
from common import UPLOAD_FOLDER_PATH

class DaysToGA(ITask):
    def __init__(self):
        pass

    def __run__(self, time):
        if time['hour'] == '8' and time['min'] == '15':
            pictures = os.listdir(UPLOAD_FOLDER_PATH + '/redbull')
            d0 = datetime.datetime.now().date()
            d1 = datetime.date(2015, 7, 24)
            delta = d1 - d0
            Timeline.add_item_from_bot('{0} days to GA :)'.format(delta.days),
                                       '',
                                       pictures[delta.days % len(pictures)],
                                       'fa-bullhorn',
                                       'info')
