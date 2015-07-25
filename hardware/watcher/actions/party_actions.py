__author__ = 'sachinpatney'

import time
from common import run_async
from common import Bot
from common import ASSETS_FOLDER_PATH
from common import NeoPixels
from actions_common import IAction


class LetsParty(IAction):
    def __init__(self):
        pass

    def __do__(self):
        run_async(Bot.play_sound, (ASSETS_FOLDER_PATH + '/sounds/gfdr.mp3',))
        NeoPixels.police(NeoPixels.broadcast_address, '50')
        time.sleep(10)
        NeoPixels.off(NeoPixels.broadcast_address)
        Bot.kill_sound()
        pass