from common import Mona
from common import IMonaTask
from common import REPOSITORY_ROOT

import random


class Joker(IMonaTask):
    def __run__(self, time):
        if int(time[0]) % 5 == 0 and time[1] == 0:
            jokes = ['newword.mp3', 'policechief.mp3']
            Mona.play_sound(REPOSITORY_ROOT+'/resources/sounds/'+random.choice(jokes))