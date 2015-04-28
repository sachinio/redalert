__author__ = 'sachinpatney'

from urllib.request import urlopen
import random

from common import ITask
from common import Bot
from common import Timeline


template = "Microsoft stock closed at {0}, {1}, {2}.{3}"
motivate = [' Come on people we can do better!', ' OK. Clearly you guys need to work harder.']
praise = [' Great job guys!', ' Well done! Go treat yourself to some coffee.']


class StockTicker(ITask):
    def __init__(self):
        pass

    def __run__(self, time):
        if time['hour'] == '13' and time['min'] == '15':
            result = urlopen("http://finance.yahoo.com/d/quotes.csv?s=MSFT&f=spc1").read()
            result = result.strip().split(',')

            direction = 'down'

            if float(result[2]) > 0:
                direction = 'up'

            msg = template.format(result[1].replace('.', ' point '), direction,
                                  result[2].replace('.', ' point ').replace('-', ''), '')
            Bot.speak(msg)

            if direction == 'up':
                icon_back = 'success'
                speak = random.choice(praise)
                Bot.speak(speak)
            else:
                icon_back = 'danger'
                speak = random.choice(motivate)
                Bot.speak(speak)

            Timeline.add_item_from_bot('Stock update',
                                       template.format(result[1],
                                                       direction,
                                                       result[2].replace('-', ''), speak),
                                       '',
                                       'fa-line-chart',
                                       icon_back)
