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
    # The Settings page
    path('settings', views.settings, name='settings'),
    # AJAX functions
    path('ajax/sendmove', views.aj_send_move, name='aj_send_move'),
    path('ajax/sendbutton', views.aj_send_button, name='aj_send_button'),

    
]
