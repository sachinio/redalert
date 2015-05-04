__author__ = 'sachinpatney'

import os
import subprocess
import csv
import fcntl
import smtplib
import datetime
import json

from urllib.request import urlopen
from urllib.request import Request
from threading import Lock

REPOSITORY_ROOT = '/var/www/git/redalert'
TMP_FOLDER_PATH = '/var/www/tmp'
UPLOAD_FOLDER_PATH = '/var/www/uploads'
ASSETS_FOLDER_PATH = REPOSITORY_ROOT + '/assets'

OPTIONS_FILE_PATH = TMP_FOLDER_PATH + '/options.csv'
TEXT_TO_SPEECH_PATH = REPOSITORY_ROOT + '/utilities/speech/text_to_speech.py'
LIGHTS_PATH = REPOSITORY_ROOT + '/hardware/lights/lights.py'

TALKING_PILLOW = Lock()
STATUS_FILE_LOCK = Lock()


class ITask():
    def __init__(self):
        pass
        # raise Exception('ITask is abstract. Are you calling __init__ from derived class?')

    def __run__(self, time):
        """Runs the job"""
        raise Exception('You must implement __run__ method on your service')


def safe_read_dictionary(d, key):
    try:
        val = d[key]
    except KeyError:
        return None
    return val


def read_csv_as_dictionary(path):
    reader = csv.reader(open(path, 'r'))
    return dict(x for x in reader)


def read_csv_as_list(path):
    li = []
    if os.path.isfile(path):
        reader = csv.DictReader(open(path, 'r'))
        for l in reader:
            li.append(l)

    return li


def write_dictionary_to_csv(dictionary, path):
    writer = csv.writer(open(path, 'w'))
    for key, value in dictionary.items():
        writer.writerow([key, value])


def sync_write_list_to_csv(fieldnames, li, path, operation):
    if not (operation == 'w' or operation == 'a'):
        raise Exception('Unsupported operation \'{0}\''.format(operation))
    write_header = not os.path.isfile(path)
    with open(path, operation) as csv_file:
        fcntl.flock(csv_file.fileno(), fcntl.LOCK_EX)
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        if write_header or operation == 'w':
            writer.writeheader()
        for l in li:
            writer.writerow(l)


def sync_write_to_file(name, operation, message):
    with open(name, operation) as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        f.write(message)


def sync_read_status_file():
    STATUS_FILE_LOCK.acquire()
    d = {}
    if os.path.isfile(OPTIONS_FILE_PATH):
        d = read_csv_as_dictionary(OPTIONS_FILE_PATH)
    STATUS_FILE_LOCK.release()
    return d


def sync_write_to_status_file(key, value):
    STATUS_FILE_LOCK.acquire()
    d = {}
    if os.path.isfile(OPTIONS_FILE_PATH):
        d = read_csv_as_dictionary(OPTIONS_FILE_PATH)
    d[key] = value
    write_dictionary_to_csv(d, OPTIONS_FILE_PATH)
    STATUS_FILE_LOCK.release()


class Bot:
    def __init__(self):
        pass

    rooms = ['3A', '3B', '3C']  # for future use
    room_ip = {  # for future use
        '3A': '',
        '3B': '',
        '3C': 'localhost'
    }

    @classmethod
    def play_sound(cls, name):
        TALKING_PILLOW.acquire()
        subprocess.call(['sudo','pkill','omxplayer'])
        subprocess.call(['sudo','omxplayer',name])
        TALKING_PILLOW.release()

    @classmethod
    def speak(cls, msg):
        TALKING_PILLOW.acquire()
        subprocess.call(['sudo', 'python3', TEXT_TO_SPEECH_PATH, msg])
        TALKING_PILLOW.release()


class NeoPixels:
    broadcast_address = '00 00 00 00 00 00 FF FF'
    full_brightness = '100'
    no_timeout = '0'

    @classmethod
    def glow(cls, address, delay, bri, color, tout=no_timeout):
        cls.execute_command(address, 'G', delay, bri, color, tout)

    @classmethod
    def running(cls, address, delay, bri, color, tout=no_timeout):
        cls.execute_command(address, 'R', delay, bri, color, tout)

    @classmethod
    def still(cls, address, delay, bri, color, tout=no_timeout):
        cls.execute_command(address, 'S', delay, bri, color, tout)

    @classmethod
    def police(cls, address, bri=full_brightness, tout=no_timeout):
        cls.execute_command(address, 'P', '50', bri, '0, 0, 0', tout)

    @classmethod
    def off(cls, address):
        cls.execute_command(address, 'O', '1', '1', '0, 0, 0', '0')

    @classmethod
    def execute_command(cls, address, command, delay, bri, color, tout):
        subprocess.call(['python3', LIGHTS_PATH, address, command, delay, bri, color, tout])


class BuildNotifier:
    def __init__(self):
        pass

    units = [
        {
            'id' : 0,
            'addr' : '00 00 00 00 00 00 FF FF',
            'email': 'spatney@microsoft.com',
            'room': '3C'
        }
    ]

    @classmethod
    def build_was_broken(cls):
        return safe_read_dictionary(sync_read_status_file(), 'buildbroken') == 'True'

    @classmethod
    def update_build_status(cls, status):
        sync_write_to_status_file('buildbroken', status)


    @classmethod
    def notify_build_break(cls, culprits):
        NeoPixels.still(NeoPixels.broadcast_address, '10', '20', '255, 0, 0', '0')
        for c in culprits:
            for u in cls.units:
                if c['uniqueName'] == u['email']:
                    NeoPixels.glow(u['addr'], '500', '100', '255, 0, 0', '0')

        cls.announce_build_break()
        Bot.speak(culprits[0]['displayName'] + ', could you please fix it!')

    @classmethod
    def announce_build_break(cls):
        Bot.speak('Attention. This is an important message. There has been a build break!')

    @classmethod
    def notify_all_clear(cls):
        NeoPixels.still(NeoPixels.broadcast_address, '10', '10', '0, 255, 0', '30')


class EMail:
    def __init__(self, subject, msg):
        self.subject = subject
        self.msg = msg

    def send(self):
        from_address = 'pbixbot@gmail.com'
        to_address = 'sachinpatney@gmail.com'

        header = 'To:' + to_address + '\n' + 'From: ' + from_address + '\n' + 'Subject:{0}\n'.format(self.subject)
        msg = header + self.msg

        # Credentials
        cred = sync_read_status_file()

        username = safe_read_dictionary(cred, 'gmail_username')
        password = safe_read_dictionary(cred, 'gmail_password')

        # The actual mail send
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)
        server.sendmail(from_address, to_address, msg)
        server.quit()


class SlackBot:

    def __init__(self):
        pass

    @classmethod
    def post_message_on_channel(cls, channel, msg):
        token = safe_read_dictionary(sync_read_status_file(), 'slack_token')
        subprocess.call(['curl',
                         '--data',
                         msg,
                         "https://pbiminerva.slack.com/services/hooks/"
                         "slackbot?token={0}&channel=%23{1}".format(token, channel)])


class Weather:
    def __init__(self):
        pass


    @classmethod
    def get_weather(cls, zipcode):
        key = safe_read_dictionary(sync_read_status_file(), 'weather_key')
        uri = 'http://api.openweathermap.org/data/2.5/weather?' \
              'zip={0},us&units=imperial&APPID={1}'\
            .format(zipcode, key)
        request = Request(uri)
        result = urlopen(request)
        response = result.read().decode('ascii')
        return json.loads(response)


class Timeline:
    def __init__(self):
        pass

    @classmethod
    def add_item_from_bot(cls, title, content, img, icon, icon_back):
        Timeline.add_item('Redbull', title, content, img, icon, icon_back)

    @classmethod
    def add_item(cls, name, title, content, img, icon, icon_back):
        if name == '':
            name = 'unknown'
        if img is not None and img != '':
            img = '{0}/{1}/{2}'.format('../../../uploads', name.lower(), img)
        list_item = {
            "name": name,
            "title": title,
            "content": content,
            "img": img,
            'icon': icon,
            'iconBackground': icon_back,
            'timeStamp': datetime.datetime.now().strftime("%B %d, %Y @ %I:%M%p")
        }

        sync_write_list_to_csv(
            ['name', 'title', 'content', 'img', 'icon', 'iconBackground', 'timeStamp'],
            [list_item],
            TMP_FOLDER_PATH + '/timeline.csv',
            'a')
