__author__ = 'sachinpatney'

from common import ITask
from common import Timeline


class WeatherTask(ITask):
    def __init__(self):
        pass

    def __run__(self, time):
        if time['hour'] == '8' and time['min'] == '15':
            #w = Weather.get_weather('98043')
            w = eval("{'weather': [{'main': 'Clear', 'description': 'Sky is Clear', 'id': 800, 'icon': '01n'}], "
                     "'main': {'sea_level': 1024.89, 'temp_min': 281.239, 'grnd_level': 1015.26, 'pressure': 1015.26, "
                     "'temp_max': 281.239, 'temp': 281.239, 'humidity': 85}, 'sys': {'country': 'US', "
                     "'sunset': 1430796375, 'message': 0.0159, 'sunrise': 1430743540}, 'coord': "
                     "{'lat': 47.79, 'lon': -122.31}, 'cod': 200, 'wind': {'speed': 0.85, 'deg': 334.503}, "
                     "'base': 'stations', 'id': 0, 'dt': 1430725317, 'name': 'Mountlake Terrace', "
                     "'clouds': {'all': 0}}")

            message = 'The weather right now at {0} is {1}, and the temperature is around {2}.' \
                .format(w['name'], w['weather'][0]['main'], w['main']['temp'])

            Timeline.add_item_from_bot('Weather Report', message, '', 'fa-cloud', 'info')