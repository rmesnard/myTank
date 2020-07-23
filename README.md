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

sudo docker run -d --name="mytank" --log-opt mode=non-blocking --log-opt max-buffer-size=4m --log-opt max-size=10m --log-opt max-file=2 -p 80:5005 -p 8000:8000 --device /dev/ttyUSB0:/dev/ttyUSB0 --device /dev/ttyUSB1:/dev/ttyUSB1 -v mytank_config:/usr/share/config --restart always lijah/mytank


#share config

sudo docker run -d -p 445:445 -v mytank_config:/share/conf --restart always --name samba trnape/rpi-samba -u "admin:password" -s "config:/share/conf:rw:admin"


#manage docker

sudo docker volume create portainer_data

sudo docker run -d -p 9000:9000 -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data --restart always --name portainer portainer/portainer

#console

sudo docker exec -it mytank bash

#show logs

sudo docker logs mytank


#Port used

80	Mytank Web interface
8000	Mytank API
9000	Portainer Docker management
445	Samba share
22	SSH




