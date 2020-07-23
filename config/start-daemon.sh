#!/bin/bash

echo "Starting."

echo "Install config."
if [ ! -e "/usr/share/config/mytank.py" ]; then
  echo "Install default config."
  cp -R -f /config /usr/share
fi
chmod -R 777 /usr/share/config

cd /usr/share/config

python manage.py makemigrations app
python manage.py migrate

nohup python3 -u mytank.py 2> mytank_error.log &
echo "my tank service Started."

nohup gunicorn --config gunicorn-cfg.py core.wsgi
