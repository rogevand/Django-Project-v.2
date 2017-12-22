myKey = {}
if request.method == 'GET':
    IP = request.GET.get('IP')
    myKey["device_type"] = str(request.GET.get('device_type'))
