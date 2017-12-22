
import requests
from urllib.parse import urlparse
import json

IP = '10.1.85.5'

myKey = {}

loginurl = "http://{0}/login.cgi".format(IP)
ratesurl =  "http://{0}/status.cgi".format(IP)
auth = {'username': (None, 'wearethebest'), 'password': (None, 'extra123')} #authenticate page
get1 = requests.get(loginurl)
post = requests.post(loginurl, files = auth, cookies = get1.cookies) #post the login info into cookies

#format the contents as a json object
ratesDict = json.loads(requests.get(ratesurl, cookies = get1.cookies).content.decode('utf-8'))
host = ratesDict["host"] # make a variable for a specific index in the json
interfaces = ratesDict["interfaces"] #same as above, diff var
myKey["uptime"] = str(round(float(host["uptime"]) /120, 2)) 
myKey["upsec"] = str(round(float(host["uptime"]), 2))

# get and format the CPE uptime
seconds = int(host["uptime"])
m, s = divmod(seconds, 60)
h, m = divmod(m, 60)
d, h = divmod(h, 24)
sec = "seconds"
mi = "minutes"
ho = "hours"
da = "days"

# no janky "1 minutes" will be found here
if s == 1:
    sec = "second"
if m == 1:
    mi = "minute"
if h == 1:
    ho = "hour"
if d == 1:
    da = "day"
myKey["uptime"] = ("%d {0}, %d {1}, %2d {2}, and like %2d {3}" % (d, h, m, s)).format(da, ho, mi, sec)
if (seconds / 120) < 120:
    myKey["color"] = True
elif (seconds / 120) >= 120:
        myKey["color"] = False

print(myKey["upsec"])
print(myKey["uptime"])