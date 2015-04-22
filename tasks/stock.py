__author__ = 'sachinpatney'

from common import IMonaTask
from common import Mona
from common import Timeline
import urllib2, random

template = "Microsoft stock closed at {0}, {1}, {2}."
motivate = ['come on people we can do better!', 'OK. Clearly you guys need to work harder.']
praise = ['Great job guys!', 'Well done! Go treat yourself to some coffee.']

class StockTicker(IMonaTask):
    def __run__(self, time):
        if  True or (time[0] == '1' and time[1] == '15'):
            result = urllib2.urlopen("http://finance.yahoo.com/d/quotes.csv?s=MSFT&f=spc1").read()
            result = result.strip().split(',')

            dir = 'down'

            if float(result[2]) > 0:
                dir = 'up'

            msg = template.format(result[1].replace('.',' point '), dir, result[2].replace('.',' point ').replace('-', ''))
            Mona.speak(msg);
            Timeline.add_item('Mona', 'Stock update', msg + ' ' + random.choice(motivate), '', 'fa-bar-chart', 'success')

            if dir == 'up':
                Mona.speak(random.choice(praise))
            else:
                Mona.speak(random.choice(motivate))