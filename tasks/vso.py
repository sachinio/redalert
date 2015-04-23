__author__ = 'sachinpatney'

import json
import urllib2
import base64

from common import IMonaTask
from common import BuildNotifier
from common import sync_read_status_file
from common import Timeline

class VSO_API_Templates:
    getBuilds = "https://{0}.visualstudio.com/defaultcollection/{1}/_apis/build/builds?api-version={2}"


class VSO(IMonaTask):

    mona = None

    def get_auth(self):
        d = sync_read_status_file()
        return [d['vso_username'], d['vso_password']]

    def is_broken(self, build):
        if build['status'] == 'failed':
            return True
        return False

    def get_broken_builds(self, data):
        brokenBuilds = []

        for build in data['value']:
            if self.is_broken(build):
                if build['definition']['name'] == 'CI':
                    brokenBuilds.append(build)
            else:  # We only want broken builds after last success
                break
        return brokenBuilds

    def get_build_info(self):
        request = urllib2.Request(VSO_API_Templates.getBuilds.format('pbix','powerbiclients','1.0'))
        auth = self.get_auth()
        base64string = base64.encodestring('%s:%s' % (auth[0], auth[1])).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        result = urllib2.urlopen(request)

        return json.loads(result.read())

    def __run__(self, time):
        broken = self.get_broken_builds(self.get_build_info())

        if len(broken) == 0:
            if BuildNotifier.build_was_broken():
                BuildNotifier.update_build_status(False)
                BuildNotifier.notify_all_clear()
                Timeline.add_item('Mona', 'BUILD BREAK FIXED','Thank you for taking care of it', '', 'fa-bar-chart', 'success')
                print 'Sent all clear notification'
            else:
                print 'Was not broken previously too, so do nothing new'
        else:
            if not BuildNotifier.build_was_broken():
                culprits = []
                for b in broken:
                    culprits.append(b['requests'][0]['requestedFor'])
                BuildNotifier.notify_build_break(culprits)
                BuildNotifier.update_build_status(True)
                Timeline.add_item('Mona', 'BUILD BREAK',
                                  '{0} broke the build. Change was requested by {1}'.format(
                                      broken[0]['buildNumber'],
                                      broken[0]['requests'][0]['requestedFor']['displayName']), '', 'fa-ambulance', 'danger')
                print 'Sent build break notification'
            else:
                print 'Was broken previously too, so do nothing'