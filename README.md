# Custom docker image for rPi python django daemonize

Docker image for rPi with [Django](https://www.djangoproject.com/) 

This image is based on the [resin/raspberrypi3-python:3.7](https://hub.docker.com/r/resin/raspberrypi3-python/)
image. 

Django is installed from pip, not github, to make sure we get a stable
version. 

#build

install git :

sudo apt-get install git

Build with docker :

sudo docker build -t lijah/mytank github.com/rmesnard/mytank 


#install

create volume :

sudo docker volume create mytank_config

#run

sudo docker run -d --name="mytank" -p 80:5005 -p 8000:8000 --device /dev/ttyUSB0:/dev/ttyUSB0 --device /dev/ttyUSB1:/dev/ttyUSB1 -v mytank_config:/usr/share/config --restart always lijah/mytank


#share config

sudo docker run -d -p 445:445 -v mytank_config:/share/conf --name samba_tank trnape/rpi-samba -u "admin:paswword" --restart always -s "config:/share/conf:rw:admin"

#console

sudo docker exec -it mytank bash

#logs

sudo docker logs mytank


