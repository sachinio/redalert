__author__ = 'sachinpatney'

import json
import urllib2
import base64

from common import IMonaTask
from common import BuildNotifier


class VSO_API_Templates:
    getBuilds = "https://{0}.visualstudio.com/defaultcollection/{1}/_apis/build/builds?api-version={2}"


class VSO(IMonaTask):

    mona = None

    def getAuth(self):
        with open('/var/www/tmp/vsoauth.txt','r') as auth:
            return auth.read().replace('\n', '').split(':')
        return None

    def isBroken(self, build):
        if build['status'] == 'succeeded':
            return False
        return True

    def getBrokenBuilds(self, data):
        brokenBuilds = []

        for build in data['value']:
            if self.isBroken(build):
                brokenBuilds.append(build)
            #else:  # We only want broken builds after last success
                #break
        return brokenBuilds

    def getBuildInfo(self):
        request = urllib2.Request(VSO_API_Templates.getBuilds.format('pbix','powerbiclients','1.0'))
        auth = self.getAuth()
        base64string = base64.encodestring('%s:%s' % (auth[0], auth[1])).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        result = urllib2.urlopen(request)

        return json.loads(result.read())

    def __run__(self, time):
        broken = self.getBrokenBuilds(self.getBuildInfo())

        if len(broken) == 0:
            if BuildNotifier.wasBroken():
                BuildNotifier.writeStatus(False)
                BuildNotifier.notifyAllClear()
            else:
                print 'Was not broken previously too, so do nothing new'
        else:
            if not BuildNotifier.wasBroken():
                culprits = []
                for b in broken:
                    culprits.append(b['requests'][0]['requestedFor'])
                BuildNotifier.notifyOfBreak(culprits)
                BuildNotifier.writeStatus(True)
            else:
                print 'Was broken previously too, so do nothing'