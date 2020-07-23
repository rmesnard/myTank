# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2020
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.primary_key=True

class TankSettings(models.Model):
    id = models.IntegerField(default=1,primary_key=True)
    host_name = models.CharField(default="",max_length=50)
    host_ip = models.CharField(default="",max_length=50)
    proximity_enabled = models.IntegerField(default=0)
    proximity_distance = models.IntegerField(default=0)
    step_time = models.IntegerField(default=1500)
    idle_time = models.IntegerField(default=10000)
    log_level = models.IntegerField(default=0)

    def is_proximityenable(self):
        if ( proximity_enabled == 0 ):
            return True
        else:
            return False

class TankStatus(models.Model):
    id = models.IntegerField(default=1,primary_key=True)

#{"isRunning": false, "gear": "off", "hum": 50.5, "temp": 29.5, "pitch": 0.09, "roll": 180.0, "yaw": -0.9, "power": "off", "speed": 0, "sonar_mode": "F", "sonar_A": 0, "sonar_B": 0, "sonar_C": 0, "sonar_D": 0, "sonar_E": 0, "sonar_F": 0, "sonar_G": 0, "sonar_H": 0, "stopA": 0, "stopB": 0, "SONAR_Id": 0, "CORE_Id": 1}

    isRunning = models.IntegerField(default=0)
    gear = models.IntegerField(default=0)
    hum = models.IntegerField(default=0)
    temp = models.IntegerField(default=0)
    pitch = models.IntegerField(default=0)
    roll = models.IntegerField(default=0)
    yaw = models.IntegerField(default=0)
    power = models.IntegerField(default=0)
    speed = models.IntegerField(default=0)
    stopA = models.IntegerField(default=0)
    stopB = models.IntegerField(default=0)


class TankSonar(models.Model):
    id = models.IntegerField(default=1,primary_key=True)

    sonar_mode = models.CharField(default="",max_length=10)
    sonar_A = models.IntegerField(default=0)
    sonar_B = models.IntegerField(default=0)
    sonar_C = models.IntegerField(default=0)
    sonar_D = models.IntegerField(default=0)
    sonar_E = models.IntegerField(default=0)
    sonar_F = models.IntegerField(default=0)
    sonar_G = models.IntegerField(default=0)
    sonar_H = models.IntegerField(default=0)
          