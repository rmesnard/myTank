FROM resin/raspberrypi3-python:3.7-stretch

ENV FLASK_APP run.py
EXPOSE 5005

RUN apt-get update
RUN apt-get install libbluetooth-dev
RUN apt-get install python-dev
RUN pip3 install --upgrade pip

COPY requirements.txt requirements.txt 

RUN pip install -r requirements.txt
RUN pip3 install PyBluez
RUN pip3 install daemonize

COPY conf conf 
WORKDIR /conf

CMD ["bash","start-daemon.sh"]