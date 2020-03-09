#!/bin/bash

echo "Starting."


python manage.py makemigrations
python manage.py migrate

nohup gunicorn --config gunicorn-cfg.py core.wsgi

