__author__ = 'sachinpatney'

from common import IMonaTask
from common import Mona
from common import Timeline
import urllib2, random

template = "Microsoft stock closed at {0}, {1}, {2}.{3}"
motivate = [' Come on people we can do better!', ' OK. Clearly you guys need to work harder.']
praise = [' Great job guys!', ' Well done! Go treat yourself to some coffee.']


class StockTicker(IMonaTask):
    def __run__(self, time):
        if time[0] == '13' and time[1] == '15':
            result = urllib2.urlopen("http://finance.yahoo.com/d/quotes.csv?s=MSFT&f=spc1").read()
            result = result.strip().split(',')

            dir = 'down'

            if float(result[2]) > 0:
                dir = 'up'

            msg = template.format(result[1].replace('.',' point '), dir, result[2].replace('.',' point ').replace('-', ''),'')
            Mona.speak(msg)

            speak = ''
            iconBack = ''
            if dir == 'up':
                iconBack = 'success'
                speak = random.choice(praise)
                Mona.speak(speak)
            else:
                iconBack = 'danger'
                speak = random.choice(motivate)
                Mona.speak(speak)

            Timeline.add_item('Mona', 'Stock update',
                              template.format(result[1],
                                              dir,
                                              result[2].replace('-', ''), speak),
                              '',
                              'fa-bar-chart',
                              iconBack)
