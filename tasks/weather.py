__author__ = 'sachinpatney'

from common import ITask
from common import Timeline
from common import Weather

class WeatherTask(ITask):
    def __init__(self):
        pass

    def __run__(self, time):
        if time['hour'] == '12' and time['min'] == '00':
            w = Weather.get_weather('98052')

            message = 'The weather right now at {0} is {1}, and the temperature is around {2} degrees fahrenheit.' \
                .format(w['name'], w['weather'][0]['main'], w['main']['temp'])

            Timeline.add_item_from_bot('Weather Report', message, '', 'fa-cloud', 'info')