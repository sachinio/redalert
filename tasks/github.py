from common import ITask
import json
import base64
from common import safe_read_dictionary
from common import sync_read_status_file

from urllib.request import urlopen
from urllib.request import Request

class Github(ITask):
    def __run__(self, time):
        info = self.get_build_info()
        for i in info:
            print(i['id'])
            print(i['title'])
            print(i['user']['login'])


    def get_auth(self):
        d = sync_read_status_file()
        return [
            safe_read_dictionary(d, 'github_username'),
            safe_read_dictionary(d, 'github_password')
        ]

    def get_build_info(self):
        request = Request('https://api.github.com/repos/Microsoft/PowerBI-visuals/issues')
        auth = self.get_auth()
        username_password = base64.b64encode(("%s:%s" % (auth[0], auth[1])).encode('utf-8')).decode("ascii")
        request.add_header("Authorization", "Basic %s" % username_password)
        result = urlopen(request)
        response = result.read().decode('ascii')
        return json.loads(response)

Github().__run__(None)
