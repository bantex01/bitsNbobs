import sys
import urllib2
import urllib
import base64
import json
baseurl="https://api.thousandeyes.com/v6/tests.json"
base64string = base64.b64encode('%s:%s' % ("1ke_user", "1ke_token"))
request = urllib2.Request(baseurl)
request.add_header("Content-Type",'application/json')
request.add_header("Accept",'application/json')
request.add_header("Authorization", "Basic %s" % base64string)
response = urllib2.urlopen(request)
tests=json.loads(response.read())
for test in tests["test"]:
    testid = test["testId"]
    type = test["type"]
    deleteurl="https://api.thousandeyes.com/v6/tests/"+str(type)+"/"+str(testid)+"/delete.json"
    body="{}"
    # build a request
    print deleteurl
    request = urllib2.Request(deleteurl, data=json.dumps(body))
    request.add_header("Content-Type",'application/json')
    request.add_header("Accept",'application/json')
    request.add_header("Authorization", "Basic %s" % base64string)
    response = urllib2.urlopen(request)
