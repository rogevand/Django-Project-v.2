
import requests
from urllib.parse import urlparse
import json

IP = '10.1.85.5'

myKey = {}

loginurl = "http://{0}/login.cgi".format(IP)
statusurl =  "http://{0}/status.cgi".format(IP)
auth = {'username': (None, 'wearethebest'), 'password': (None, 'extra123')} #authenticate page
get1 = requests.get(loginurl)
post = requests.post(loginurl, files = auth, cookies = get1.cookies) #post the login info into cookies
json2Dict = json.loads(requests.get(statusurl, cookies = get1.cookies).content.decode('utf-8')) #format the contents as a json object
wireless = json2Dict["wireless"] #get specific elements from the json



members = len(wireless["sta"])
print(members)