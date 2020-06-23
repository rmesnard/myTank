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
from .models import TankSettings

def index(request):
    #global_Settings = TankSettings.objects.get(id=1)
    #context = {'segment' : 'index', 'settings' : global_Settings }
    context = {'segment' : 'index'}
    return render(request, "index.html", context)

def settings(request):
    #global_Settings = TankSettings.objects.get(id=1)
    #context = {'segment' : 'settings', 'settings' : global_Settings }
    context = {'segment' : 'index' , 'step_time' : 1500 }
    return render(request, "settings.html", context)

def aj_send_move(request):
    axe0 = request.GET.get('axe0', 0)
    axe1 = request.GET.get('axe1', 0)
    axe2 = request.GET.get('axe2', 0)
    axe3 = request.GET.get('axe3', 0)
    data = { 'axe0=' + axe0 }
    response = requests.post('http://127.0.0.1:8000/test',  data=[('axe0', axe0),('axe1', axe1),('axe2',axe2),('axe3',axe3)])
    #json_response = response.json()

    return JsonResponse(data)

def aj_send_button(request):
    buttonid = request.GET.get('buttonclicked', None)
    data = { 'dgb_text': 'button =' + buttonid }
    return JsonResponse(data)