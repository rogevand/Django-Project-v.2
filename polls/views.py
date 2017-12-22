
import json
from urllib.parse import urlparse
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response
from django.template import loader
import requests
from .models import Temp
from bs4 import BeautifulSoup
from lxml.html.soupparser import fromstring
from lxml import etree
from lxml.etree import tostring
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required(login_url="/login/")
def index(request):
    template = loader.get_template('polls/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

@login_required(login_url="/login/")
def main(request):
    template = loader.get_template('polls/main.html')
    context = {
        "template": template
    }
    return HttpResponse(template.render(context, request))

def login(request):
    template = loader.get_template('registration/login.html')
    context = {}
    return HttpResponse(template.render(context, request))


# to allow for logging into towers I need to make the IP input variable correct..
# 
@login_required(login_url="/login/")
def status(request):
    myKey = {}
    if request.method == 'GET':
        IP = request.GET.get('IP')
        myKey["dt"] = str(request.GET.get('dt'))
        if myKey["dt"] == "tower":
            tower()
            pass
    loginurl = "http://{0}/login.cgi".format(IP) #login page variable
    statusurl = "http://{0}/status.cgi".format(IP) #destination page variable
    auth = {'username': (None, 'ubnt'), 'password': (None, 'access')} #authenticate page... INSECURE
    get1 = requests.get(loginurl) #retrieve page
    post = requests.post(loginurl, files = auth, cookies = get1.cookies) #set cookies for password
    json2Dict = json.loads(requests.get(statusurl, cookies = get1.cookies).content.decode('utf-8')) #format the contents as a json object
    wireless = json2Dict["wireless"] #get specific elements from the json 
    host = json2Dict["host"] # create variable for easy access to specific dict element
    eth0 = json2Dict["interfaces"][0]["status"]["plugged"]
    myKey["eth"] = eth0

    #determine the uptime
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
    da = "days, "
    # no janky "1 minutes" will be found here
    if s == 1:
        sec = "second "
    if m == 1:
        mi = "minute, "
    if h == 1:
        ho = "hour, "
    elif h == 0:
        ho = ""
    if d == 1:
        da = "day, "
    elif d == 0:
        da = ""
    myKey["uptime"] = ("%d {0} %d {1} %2d {2} and like %2d {3}" % (d, h, m, s)).format(da, ho, mi, sec)
    if (seconds / 120) < 120:
        myKey["color"] = True
    elif (seconds / 120) >= 120:
            myKey["color"] = False

    #determine connected tower
    for key, value in wireless.items():
        if key == "essid":
            myKey["ssid"] = value

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

    # look for cpuload key and stick value into a dictionary (myKey)
    if "cpuload" in host:
        myKey["cpuload"] = int(host["cpuload"])
    else:
        myKey["cpuload"] = False

    for key, value in host.items():
        if key == "hostname":
            if "SL" in value:
                myKey["package"] = "Smart Link"
            elif "EL" in value:
                myKey["package"] = "Elite Link"
            elif "PL" in value:
                myKey["package"] = "Power Link"
            myKey["hostname"]  = value.split("[", 1)[0]
            # this is here for efficiency. by determining whether the device is a tower or a CPE I can skip something later I think
            if "-" in value:
                myKey["signalint"] = abs(int(wireless["sta"][0]["signal"]))

    #determine member distance from tower 
    
    for key, value in wireless.items(): # (same for distance)
        if key == "distance":
            dis = value /1609.34 #convert to miles from meters
            myKey[key] = "About " + str(round(dis, 2)) + " miles"
        if key == "signal":
            if abs(int(value)) > 70:
                myKey[key] = str(value) + " (Weak signal) "
                myKey["signalint"] = abs(int(value))
            elif 70 >= abs(int(value)) > 65:
                myKey[key] = str(value) + " (Decent signal) "
                myKey["signalint"] = abs(int(value))
            elif abs(int(value)) < 65:
                myKey[key] = str(value) + " (Strong signal) "
                myKey["signalint"] = abs(int(value))

    # if tower, determine the number of members connected to this tower
    members = wireless["count"]

    #determine if there is physically something wrong with the CPE
    if json2Dict["interfaces"][1]["status"]["duplex"] == 1:
        myKey["plex"] = True
    elif json2Dict["interfaces"][1]["status"]["duplex"] == 0:
        myKey["plex"] = False
    if json2Dict["interfaces"][1]["enabled"] == True:
        myKey["enabled"] = True #json2Dict["interfaces"][1]["enabled"]
    else:
        badkey = {}
        badkey["enabled"] = False
        return JsonResponse(badkey)
    return JsonResponse(myKey)

#beautifulsoup shit
def packagedeets(request):
    packagekey = {}
    if request.method == 'GET':
        global IP
        IP = request.GET.get('IP')
    loginurl = "http://{0}/login.cgi".format(IP) #login page variable
    statusurl = "http://{0}/network.cgi".format(IP) #destination page variable
    auth = {'username': (None, 'ubnt'), 'password': (None, 'access')} #authenticate page INSECURE
    page = requests.get(loginurl) #retrieve page
    post = requests.post(loginurl, files = auth, cookies = page.cookies) #set cookies for password
    #fullpage is the string html version of the entire page
    fullpage = requests.get(statusurl, cookies = page.cookies).content.decode('utf-8')

    #soup = BeautifulSoup(fullpage, 'html.parser')
    #print(fullpage)
    
    #get stuff and stick it into packagekey here
 
    return JsonResponse(packagekey) 

@login_required(login_url="/login/")
def rates(request):
    myKey = {}
    if request.method == 'GET':
        global IP
        IP = request.GET.get('IP')
    if IP == "":
        return HttpResponse("Go to '/main' and enter an IP address Einstein")
    else:
        loginurl = "http://{0}/login.cgi".format(IP)
        ratesurl =  "http://{0}/ifstats.cgi".format(IP)
        auth = {'username': (None, 'ubnt'), 'password': (None, 'access')} #authenticate page
        get1 = requests.get(loginurl)
        post = requests.post(loginurl, files = auth, cookies = get1.cookies) #post the login info into cookies
        
        #format the contents as a json object
        ratesDict = json.loads(requests.get(ratesurl, cookies = get1.cookies).content.decode('utf-8'))
        host = ratesDict["host"] # make a variable for a specific index in the json
        interfaces = ratesDict["interfaces"] #same as above, diff var
        

        # get and format the dl/ul speeds
        indy = len(interfaces) - 1
        txspeed = round(int(interfaces[indy]["stats"]["tx_bytes"]), 2)
        rxspeed = round(int(interfaces[indy]["stats"]["rx_bytes"]), 2)
        myKey["RX"] = rxspeed
        myKey["TX"] = txspeed
        
        return JsonResponse(myKey)
############################################################################################################################################################################
def tower(vars):
    print("there is nothing better than the moonlit apple tree on the north farm ")
    #determine the uptime
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
    da = "days, "
    # no janky "1 minutes" will be found here
    if s == 1:
        sec = "second "
    if m == 1:
        mi = "minute, "
    if h == 1:
        ho = "hour, "
    elif h == 0:
        ho = ""
    if d == 1:
        da = "day, "
    elif d == 0:
        da = ""
    myKey["uptime"] = ("%d {0} %d {1} %2d {2} and like %2d {3}" % (d, h, m, s)).format(da, ho, mi, sec)
    if (seconds / 120) < 120:
        myKey["color"] = True
    elif (seconds / 120) >= 120:
            myKey["color"] = False

    #determine connected tower
    for key, value in wireless.items():
        if key == "essid":
            myKey["ssid"] = value

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

    # look for cpuload key and stick value into a dictionary (myKey)
    if "cpuload" in host:
        myKey["cpuload"] = int(host["cpuload"])
    else:
        myKey["cpuload"] = False

    for key, value in host.items():
        if key == "hostname":
            if "SL" in value:
                myKey["package"] = "Smart Link"
            elif "EL" in value:
                myKey["package"] = "Elite Link"
            elif "PL" in value:
                myKey["package"] = "Power Link"
            myKey["hostname"]  = value.split("[", 1)[0]
            # this is here for efficiency. by determining whether the device is a tower or a CPE I can skip something later I think
            if "-" in value:
                myKey["signalint"] = abs(int(wireless["sta"][0]["signal"]))

    #determine member distance from tower 
    
    for key, value in wireless.items(): # (same for distance)
        if key == "distance":
            dis = value /1609.34 #convert to miles from meters
            myKey[key] = "About " + str(round(dis, 2)) + " miles"
        if key == "signal":
            if abs(int(value)) > 70:
                myKey[key] = str(value) + " (Weak signal) "
                myKey["signalint"] = abs(int(value))
            elif 70 >= abs(int(value)) > 65:
                myKey[key] = str(value) + " (Decent signal) "
                myKey["signalint"] = abs(int(value))
            elif abs(int(value)) < 65:
                myKey[key] = str(value) + " (Strong signal) "
                myKey["signalint"] = abs(int(value))

    # if tower, determine the number of members connected to this tower
    members = wireless["count"]
    return JsonResponse(myKey)

