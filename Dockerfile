FROM resin/raspberrypi3-python:3.7-stretch

EXPOSE 5005
EXPOSE 8000

RUN apt-get update
RUN apt-get install libbluetooth-dev
RUN apt-get install python-dev
RUN pip3 install --upgrade pip

COPY requirements.txt requirements.txt 

RUN pip install -r requirements.txt
RUN pip3 install PyBluez

COPY config config 
WORKDIR /config

CMD ["bash","start-daemon.sh"]