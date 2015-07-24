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
from common import Icons
from common import IconBackgrounds


class VSO_API_Templates:
    getBuilds = "https://{0}.visualstudio.com/defaultcollection/{1}/_apis/build/builds?definitions={2}&$top={3}&api-version={4}"


class VSO(ITask):

    def get_user_info_from_build(self, build):
        return build['requestedFor']

    def get_auth(self):
        d = sync_read_status_file()
        return [
            safe_read_dictionary(d, 'vso_username'),
            safe_read_dictionary(d, 'vso_password')
        ]

    def is_broken(self, build):
        if build['status'] == 'failed':
            return True
        if build['status'] == 'partiallySucceeded':
            return True
        return False

    def get_broken_pr_builds(self, data):
        broken_builds = []

        for build in data['value']:
            print(build['definition']['name'])
            print(self.get_user_info_from_build(build)['displayName'])
            if self.is_broken(build):
                broken_builds.append(build)

        return broken_builds

    def get_broken_master_builds(self, data):
        broken_builds = []
        
        for build in data['value']:
            if self.is_broken(build):
                broken_builds.append(build)
            else:  # We only want broken builds after last success
                break
        return broken_builds

    def get_build_info(self, definitionId):
        request = Request(VSO_API_Templates.getBuilds.format('pbix', 'powerbiclients', definitionId, '10', '2.0'))
        auth = self.get_auth()
        username_password = base64.b64encode(("%s:%s" % (auth[0], auth[1])).encode('utf-8')).decode("ascii")
        request.add_header("Authorization", "Basic %s" % username_password)
        result = urlopen(request)
        response = result.read().decode('ascii')
        return json.loads(response)

    def __run__(self, time):
        self.get_broken_pr_builds(self.get_build_info('7'))
        broken = self.get_broken_master_builds(self.get_build_info('1'))

        if len(broken) == 0:
            if BuildNotifier.build_was_broken():
                BuildNotifier.update_build_status(False)
                BuildNotifier.notify_all_clear()
                Timeline.add_item_from_bot('BUILD BREAK FIXED',
                                           'Thank you for taking care of it',
                                           '',
                                           Icons.Wrench,
                                           IconBackgrounds.Green)
                print('Sent all clear notification')
            else:
                print('Was not broken previously too, so do nothing new')
        else:
            if not BuildNotifier.build_was_broken():
                culprits = []
                for b in broken:
                    culprits.append(self.get_user_info_from_build(b))
                BuildNotifier.notify_build_break(culprits)
                BuildNotifier.update_build_status(True)
                Timeline.add_item_from_bot('BUILD BREAK',
                                           '{0} broke the build. Change was requested by {1}'.format(
                                               broken[len(broken) - 1]['buildNumber'],
                                               broken[len(broken) - 1]['requestedFor']['displayName']),
                                           '',
                                           Icons.Ambulance,
                                           IconBackgrounds.Red)
                print('Sent build break notification')
            else:
                print('Was broken previously too, so do nothing')
