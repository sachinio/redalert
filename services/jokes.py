from common import Mona
from common import IMonaJob

class Joker(IMonaJob):

    def __run__(self, time):
        Mona.joke()