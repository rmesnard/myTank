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

def index(request):
    pagesettings = TankSettings.objects.get(id=1)
    #context = {'segment' : 'index', 'settings' : global_Settings }

    pagesettings.host_name = "raspberry_mytank"
    pagesettings.host_ip = "192.168.4.10"

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
        pagesettings.save()

    #context = {'segment' : 'settings', 'settings' : global_Settings }
    context = {'segment' : 'index' , 'step_time' : pagesettings.step_time , 'secure_enabled' : pagesettings.proximity_enabled , 'idle_time' : pagesettings.idle_time , 'anticollision_distance' : pagesettings.proximity_distance }
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
    data = { 'axe0=' + axe0 }
    response = requests.post('http://' + pagesettings.host_ip + ':8000/test',  data=[('axe0', axe0),('axe1', axe1),('axe2',axe2),('axe3',axe3)])
    json_response = response.json()

    return JsonResponse(json_response)

def aj_send_button(request):
    buttonid = request.GET.get('buttonclicked', None)
    data = { 'dgb_text': 'button =' + buttonid }
    return JsonResponse(data)

def api_set_status(request):
    #currentstatus = TankStatus.objects.get(id=1)

    if request.method == "POST":
        received_json_data = json.loads(request.body.decode("utf-8"))
        print(received_json_data)

    data = { 'status': 'ok' }
    return JsonResponse(data)

def api_get_settings(request):
    pagesettings = TankSettings.objects.get(id=1)

    data = {'step_time' : pagesettings.step_time , 'secure_enabled' : pagesettings.proximity_enabled , 'idle_time' : pagesettings.idle_time , 'anticollision_distance' : pagesettings.proximity_distance }
    return JsonResponse(data)
