FROM resin/raspberrypi3-python:3.7-stretch

ENV FLASK_APP run.py

EXPOSE 5005

RUN apt-get update
RUN apt-get install libbluetooth-dev
RUN apt-get install python-dev

COPY python python 
COPY manage.py gunicorn-cfg.py requirements.txt .env ./
COPY app app
COPY authentication authentication
COPY core core

RUN pip3 install --upgrade pip

RUN pip install -r requirements.txt
RUN pip3 install PyBluez
RUN pip3 install daemonize


RUN python manage.py makemigrations
RUN python manage.py migrate

EXPOSE 5005
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]

