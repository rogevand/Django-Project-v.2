import requests
from urllib.parse import urlparse
import json

myKey = {}

IP = '10.1.85.56'

loginurl = "http://{0}/login.cgi".format(IP) #login page variable
statusurl = "http://{0}/status.cgi".format(IP) #destination page variable
auth = {'username': (None, 'ubnt'), 'password': (None, 'access')} #authenticate page INSECURE
get1 = requests.get(loginurl) #retrieve page
post = requests.post(loginurl, files = auth, cookies = get1.cookies) #set cookies for password
json2Dict = json.loads(requests.get(statusurl, cookies = get1.cookies).content.decode('utf-8')) #format the contents as a json object
wireless = json2Dict["wireless"] #get specific elements from the json 
host = json2Dict["host"] # create variable for easy access to specific dict element
eth0 = json2Dict["interfaces"][0]["status"]["plugged"]
myKey["eth"] = eth0

#determine member package (need to find a better way of doing this)
for key, value in host.items():
    if key == "hostname":
        if "SL" in value:
            myKey["package"] = "Smart Link"
        elif "EL" in value:
            myKey["package"] = "Elite Link"
        elif "PL" in value:
            myKey["package"] = "Power Link"
        myKey["hostname"]  = value.split("[", 1)[0]

print(myKey["package"])
 