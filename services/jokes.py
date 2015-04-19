from common import Mona
from common import IMonaTask


class Joker(IMonaTask):
    def __run__(self, time):
        if time[1] == '15' or time[1] == '30' or time[1] == '45':
            Mona.tellARandomJoke()