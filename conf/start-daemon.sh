#!/bin/bash

echo "Starting."

echo "Install config."
if [ ! -e "/usr/share/config/mytank.py" ]; then
  echo "Install default config."
  cp -R -f /conf /usr/share/config
fi
chmod -R 777 /usr/share/config

cd /usr/share/config

python manage.py makemigrations
python manage.py migrate

nohup gunicorn --config gunicorn-cfg.py core.wsgi

