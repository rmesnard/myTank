# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    #re_path(r'^.*\.html', views.pages, name='pages'),

    # The home page
    path('', views.index, name='home'),
    path('index', views.index, name='home'),
    # The Settings page
    path('settings', views.settings, name='settings'),
    # The Debug page
    path('debug', views.debug, name='debug'),

    # AJAX functions
    path('ajax/sendmove', views.aj_send_move, name='aj_send_move'),
    path('ajax/sendbutton', views.aj_send_button, name='aj_send_button'),

    # API functions
    path('api/setstatus', views.api_set_status, name='api_set_status'),
    path('api/getsettings', views.api_get_settings, name='api_get_settings'),
    
]
