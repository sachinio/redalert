__author__ = 'sachinpatney'

import json, urllib2, base64, buildNotifier
from common import IMonaJob


class VSO_API_Templates:
    getBuilds = "https://{0}.visualstudio.com/defaultcollection/{1}/_apis/build/builds?api-version={2}"


class VSO(IMonaJob):

    def isBroken(self, build):
        if build['status'] == 'succeeded':
            return False
        return True

    def getBrokenBuilds(self, data):
        brokenBuilds = []

        for build in data['value']:
            if self.isBroken(build):
                brokenBuilds.append(build)
            else: # We only want broken builds after last success
                break
        return brokenBuilds

    def getBuildInfo(self):
        request = urllib2.Request(VSO_API_Templates.getBuilds.format('pbix','powerbiclients','1.0'))
        base64string = base64.encodestring('%s:%s' % ('spy', 'Ilovedogs2')).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        result = urllib2.urlopen(request)

        return json.loads(result.read())

    def __run__(self, time, lock):
        broken = self.getBrokenBuilds(self.getBuildInfo())

        buildNotifier.notifyOfBreak(['spatney@microsoft.com'])
        if len(broken) == 0:
            print 'No broken builds'

        for b in broken:
            print b['requests'][0]['requestedFor']['displayName']