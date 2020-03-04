#!/bin/bash

echo "Start Django."
cd /django
nohup python3 manage.py runserver 0:7000 &

echo "Start Daemon."
cd /python

nohup python3 mytank.py

