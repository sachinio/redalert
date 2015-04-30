from common import Bot
from common import ITask
from common import ASSETS_FOLDER_PATH

import random


class Joker(ITask):
    def __init__(self):
        pass

    def __run__(self, time):
        if int(time['hour']) % 5 == 0 and time['min'] == '00':
            jokes = ['newword.mp3', 'policechief.mp3']
            Bot.play_sound(ASSETS_FOLDER_PATH + '/sounds/' + random.choice(jokes))