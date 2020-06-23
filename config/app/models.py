# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2020
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.primary_key=True

class TankSettings(models.Model):
    id = models.IntegerField(default=0,primary_key=True)
    test_text = models.CharField(max_length=200)
    proximity_enabled = models.IntegerField(default=0)
    proximity_distance = models.IntegerField(default=0)
    step_time = models.IntegerField(default=1500)

    def is_proximityenable(self):
        if ( proximity_enabled == 0 ):
            return True
        else:
            return False