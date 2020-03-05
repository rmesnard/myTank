FROM resin/raspberrypi3-python:3.7-stretch

VOLUME /conf
ENV FLASK_APP run.py
EXPOSE 5005

RUN apt-get update
RUN apt-get install libbluetooth-dev
RUN apt-get install python-dev
RUN pip3 install --upgrade pip

COPY conf conf 
WORKDIR /conf

RUN pip install -r requirements.txt
RUN pip3 install PyBluez
RUN pip3 install daemonize

RUN python manage.py makemigrations
RUN python manage.py migrate

CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]

