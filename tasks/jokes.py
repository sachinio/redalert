from common import Bot
from common import ITask
from common import REPOSITORY_ROOT

import random


class Joker(ITask):
    def __init__(self):
        pass

    def __run__(self, time):
        if int(time['hour']) % 5 == 0 and time['min'] == '00':
            jokes = ['newword.mp3', 'policechief.mp3']
            Bot.play_sound(REPOSITORY_ROOT + '/assets/sounds/' + random.choice(jokes))