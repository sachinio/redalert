__author__ = 'sachinpatney'

import os, subprocess, random, csv, fcntl, smtplib, sys, datetime

from threading import Lock

REPOSITORY_ROOT = '/var/www/git/redalert'
TMP_FOLDER_PATH = '/var/www/tmp'
UPLOAD_FOLDER_PATH = '/var/www/upload'
OPTIONS_FILE_PATH = TMP_FOLDER_PATH + '/options.csv'

TALKING_PILLOW = Lock()
STATUS_FILE_LOCK = Lock()


class IMonaTask():
    def __run__(self, time):
        """Runs the job"""
        raise Exception('You must implement __run__ method on your service')


def switch_to_mona_path():
    os.chdir(REPOSITORY_ROOT + '/apis/mona')


def read_csv_as_dictionary(path):
    reader = csv.reader(open(path, 'rb'))
    return dict(x for x in reader)


def read_csv_as_list(path):
    list = []
    if os.path.isfile(path):
        reader = csv.DictReader(open(path, 'rb'))
        for l in reader:
            list.append(l)

    return list


def write_dictionary_to_csv(dict, path):
    writer = csv.writer(open(path, 'wb'))
    for key, value in dict.items():
        writer.writerow([key, value])

def write_list_to_csv_as(fieldnames, list, path):
    with open(path, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for l in list:
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


class Mona:
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
        switch_to_mona_path()
        subprocess.call(['sudo', 'python', 'mona.py', msg])
        TALKING_PILLOW.release()


class BuildNotifier:
    broadcast_address = '00 00 00 00 00 00 FF FF'

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
        return sync_read_status_file()['buildbroken'] == 'True'

    @classmethod
    def update_build_status(cls, status):
        sync_write_to_status_file('buildbroken', status)


    @classmethod
    def notify_build_break(cls, culprits):
        BuildNotifier.still_unit(cls.broadcast_address, '10', '20', '255, 0, 0', '0')
        for c in culprits:
            for u in cls.units:
                if c['uniqueName'] == u['email']:
                    cls.glow_unit(u['addr'], '500', '100', '255, 0, 0', '0')

        cls.announce_build_break()
        Mona.speak(culprits[0]['displayName'] + ', could you please fix it!')

    @classmethod
    def announce_build_break(cls):
        Mona.speak('Attention. This is an important message. There has been a build break!')

    @classmethod
    def notify_all_clear(cls):
        cls.still_unit(cls.broadcast_address, '10', '10', '0, 255, 0', '5')

    @classmethod
    def glow_unit(cls, addr, delay, bri, color, tout):
        cls.switch_to_lights_path()
        subprocess.call(['python', 'lights.py', addr, 'G', delay, bri, color, tout])

    @classmethod
    def still_unit(cls, addr, delay, bri, color, tout):
        cls.switch_to_lights_path()
        subprocess.call(['python', 'lights.py', addr, 'S', delay, bri, color, tout])

    @classmethod
    def switch_to_lights_path(cls):
        os.chdir(REPOSITORY_ROOT + '/apis/lights')

    @classmethod
    def off_all_lights(cls):
        subprocess.call(['python', 'lights.py', cls.broadcast_address, 'O', '500', '100', '0, 0, 0', '0'])


class EMail:
    def __init__(self, subject, msg):
        self.subject = subject
        self.msg = msg

    def send(self):
        from_address = 'monapbix@gmail.com'
        to_address = 'sachinpatney@gmail.com'

        header = 'To:' + to_address + '\n' + 'From: ' + from_address + '\n' + 'Subject:{0}\n'.format(self.subject)
        msg = header + self.msg

        # Credentials
        cred = sync_read_status_file()

        username = cred['gmail_username']
        password = cred['gmail_password']

        # The actual mail send
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)
        server.sendmail(from_address, to_address, msg)
        server.quit()


class Timeline:
    @classmethod
    def add_item(cls, name, title, content, img, icon, iconBack):
        if img is not None and img != '':
            img = '{0}/{1}/{2}'.format('../../../uploads',name,img)
        i = {
            "name": name,
            "title": title,
            "content": content,
            "img": img,
            'icon': icon,
            'iconBackground': iconBack,
            'timeStamp': datetime.datetime.now().strftime("%B %d, %Y @ %I:%M%p")
        }

        l = read_csv_as_list(TMP_FOLDER_PATH + '/timeline.csv')
        l.append(i)
        write_list_to_csv_as(
            ['name', 'title', 'content', 'img', 'icon', 'iconBackground', 'timeStamp']
            , l, TMP_FOLDER_PATH + '/timeline.csv')
