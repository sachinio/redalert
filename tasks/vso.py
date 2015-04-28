__author__ = 'sachinpatney'

import json
import base64

from urllib.request import urlopen
from urllib.request import Request
from common import ITask
from common import BuildNotifier
from common import sync_read_status_file
from common import Timeline
from common import safe_read_dictionary


class VSO_API_Templates:
    getBuilds = "https://{0}.visualstudio.com/defaultcollection/{1}/_apis/build/builds?api-version={2}"


class VSO(ITask):

    def get_auth(self):
        d = sync_read_status_file()
        return [
            safe_read_dictionary(d, 'vso_username'),
            safe_read_dictionary(d, 'vso_password')
        ]

    def is_broken(self, build):
        if build['status'] == 'failed':
            return True
        return False

    def get_broken_builds(self, data):
        broken_builds = []

        for build in data['value']:
            if self.is_broken(build):
                if build['definition']['name'] == 'CI':
                    broken_builds.append(build)
            else:  # We only want broken builds after last success
                break
        return broken_builds

    def get_build_info(self):
        request = Request(VSO_API_Templates.getBuilds.format('pbix', 'powerbiclients', '1.0'))
        auth = self.get_auth()
        username_password = base64.b64encode(("%s:%s" % (auth[0], auth[1])).encode('utf-8')).decode("ascii")
        request.add_header("Authorization", "Basic %s" % username_password)
        result = urlopen(request)
        response = result.read().decode('ascii')
        return json.loads(response)

    def __run__(self, time):
        broken = self.get_broken_builds(self.get_build_info())

        if len(broken) == 0:
            if BuildNotifier.build_was_broken():
                BuildNotifier.update_build_status(False)
                BuildNotifier.notify_all_clear()
                Timeline.add_item_from_bot('BUILD BREAK FIXED',
                                           'Thank you for taking care of it',
                                           '',
                                           'fa-wrench',
                                           'success')
                print('Sent all clear notification')
            else:
                print('Was not broken previously too, so do nothing new')
        else:
            if not BuildNotifier.build_was_broken():
                culprits = []
                for b in broken:
                    culprits.append(b['requests'][0]['requestedFor'])
                BuildNotifier.notify_build_break(culprits)
                BuildNotifier.update_build_status(True)
                Timeline.add_item_from_bot('BUILD BREAK',
                                           '{0} broke the build. Change was requested by {1}'.format(
                                               broken[len(broken) - 1]['buildNumber'],
                                               broken[len(broken) - 1]['requests'][0]['requestedFor']['displayName']),
                                           '',
                                           'fa-ambulance',
                                           'danger')
                print('Sent build break notification')
            else:
                print('Was broken previously too, so do nothing')