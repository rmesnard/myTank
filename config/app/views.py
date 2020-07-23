# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django.http import JsonResponse
from .models import TankSettings, TankStatus
import json
import requests

def index(request):
    pagesettings = TankSettings.objects.get(id=1)
    #context = {'segment' : 'index', 'settings' : global_Settings }

    pagesettings.host_name = "raspberry_mytank"
    pagesettings.host_ip = "192.168.4.10"

    pagesettings.save()

    context = {'segment' : 'index'}
    return render(request, "index.html", context)

def settings(request):

    #pagesettings = TankSettings()
    #pagesettings.save()
    pagesettings = TankSettings.objects.get(id=1)

    if request.method == "POST":
        #print(request.POST)
        pagesettings.proximity_enabled = int(request.POST['secureenabled'])
        pagesettings.proximity_distance = int(request.POST['anticollisiondistance'])
        pagesettings.step_time = int(request.POST['steptime'])
        pagesettings.idle_time = int(request.POST['idletime'])
        pagesettings.log_level = int(request.POST['loglevel'])
        pagesettings.save()
        payload = {'step_time' : pagesettings.step_time , 'proximity_enabled' : pagesettings.proximity_enabled, 'log_level' : pagesettings.log_level , 'idle_time' : pagesettings.idle_time , 'proximity_distance' : pagesettings.proximity_distance }
        send_update(pagesettings.host_ip,payload)

    #context = {'segment' : 'settings', 'settings' : global_Settings }
    context = {'segment' : 'index' , 'step_time' : pagesettings.step_time , 'proximity_enabled' : pagesettings.proximity_enabled , 'log_level' : pagesettings.log_level ,'idle_time' : pagesettings.idle_time , 'anticollision_distance' : pagesettings.proximity_distance }
    return render(request, "settings.html", context)


def debug(request):

    #currentstatus = TankStatus()
    #currentstatus.save()
    currentstatus = TankStatus.objects.get(id=1)

    context = {'segment' : 'debug' , 'isRunning' : currentstatus.isRunning , 'gear' : currentstatus.gear , 'hum' : currentstatus.hum , 'temp' : currentstatus.temp, 'pitch' : currentstatus.pitch , 'roll' : currentstatus.roll , 'yaw' : currentstatus.yaw , 'power' : currentstatus.power , 'speed' : currentstatus.speed, 'stopA' : currentstatus.stopA , 'stopB' : currentstatus.stopB   }
    return render(request, "debug.html", context)

def aj_send_move(request):
    pagesettings = TankSettings.objects.get(id=1)

    axe0 = request.GET.get('axe0', 0)
    axe1 = request.GET.get('axe1', 0)
    axe2 = request.GET.get('axe2', 0)
    axe3 = request.GET.get('axe3', 0)
    
    payload = {'axe0': axe0,'axe1': axe1,'axe2': axe2,'axe3': axe3}
    response = requests.get('http://' + pagesettings.host_ip + ':8000/command/move', params=payload)

    data = { 'status': 'ok' }
    return JsonResponse(data)

def aj_send_button(request):
    pagesettings = TankSettings.objects.get(id=1)
    buttonid = request.GET.get('buttonclicked', None)

    payload = {'buttonid': buttonid}
    response = requests.get('http://' + pagesettings.host_ip + ':8000/command/button', params=payload)

    data = { 'status': 'ok' }
    return JsonResponse(data)

def api_set_status(request):
    currentstatus = TankStatus.objects.get(id=1)

    if request.method == "POST":
        received_body = request.body.decode("utf-8")
        
        python_obj = json.loads(received_body)
        sub_python_obj = json.loads(python_obj)

        #print(json.dumps(sub_python_obj, sort_keys=True, indent=4))
        if sub_python_obj['isRunning'] == False:
            currentstatus.isRunning = 0
        else:
            currentstatus.isRunning = 1

        #currentstatus.gear = int(sub_python_obj['gear'])
        currentstatus.hum = sub_python_obj['hum']
        currentstatus.temp = sub_python_obj['temp']
        currentstatus.pitch = sub_python_obj['pitch']
        currentstatus.roll = sub_python_obj['roll']
        currentstatus.yaw = sub_python_obj['yaw']
        #currentstatus.power = int(sub_python_obj['power'])
        currentstatus.speed = int(sub_python_obj['speed'])
        currentstatus.stopA = int(sub_python_obj['stopA'])
        currentstatus.stopB = int(sub_python_obj['stopB'])
        currentstatus.save()

    data = { 'status': 'ok' }
    return JsonResponse(data)

def api_get_settings(request):
    #pagesettings = TankSettings.objects.get(id=1)
    pagesettings = TankSettings()
    pagesettings.save()

    data = {'step_time' : pagesettings.step_time , 'proximity_enabled' : pagesettings.proximity_enabled , 'log_level' : pagesettings.log_level, 'idle_time' : pagesettings.idle_time , 'anticollision_distance' : pagesettings.proximity_distance }
    return JsonResponse(data)

def send_update(host,payload):
    response = requests.get('http://' + host + ':8000/settings/update', params=payload)
    return