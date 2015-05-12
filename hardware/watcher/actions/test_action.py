__author__ = 'sachinpatney'

import sys
sys.path.append('/var/www/git/redalert/tasks')
import time
import threading
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

    def run_async(self, target, args):
        threading.Thread(target=target,
                         args=args,
                         kwargs=None,
                         ).start()

    def __do__(self):
        self.run_async(Bot.play_sound, (ASSETS_FOLDER_PATH + '/sounds/gfdr.mp3',))
        NeoPixels.police(NeoPixels.broadcast_address, '50')
        time.sleep(10)
        NeoPixels.off(NeoPixels.broadcast_address)
        Bot.kill_sound()
        pass


LetsParty().__do__()