__author__ = 'sachinpatney'

import time

from common import Bot
from common import ASSETS_FOLDER_PATH
from common import NeoPixels


class IAction:
    def __init__(self):
        pass;

    def __do__(self):
        raise Exception('This should be overridden')


class LetsParty(IAction):
    def __init__(self):
        pass

    def __do__(self):
        Bot.play_sound(ASSETS_FOLDER_PATH + '/sounds/gfdr.mp3')
        NeoPixels.police(NeoPixels.broadcast_address, 99)
        time.sleep(10)
        NeoPixels.off(NeoPixels.broadcast_address)
        Bot.kill_sound()
        pass


LetsParty().__do__()