import requests
import json


auth = {'username': (None, 'ubnt'), 'password': (None, 'access')}
get1 = requests.get('http://10.1.85.29/login.cgi')
post = requests.post('http://10.1.85.29/login.cgi', files=auth, cookies = get1.cookies)
post1 = requests.get('http://10.1.85.29/161111.1236/status.cgi', cookies = get1.cookies)
cont = post1.content
co = post.cookies

json2Dict = json.loads(cont)

myKey = json2Dict["host"]["uptime"]

#c = json2Dict.json()

stringkey = str(myKey)

print(stringkey)
