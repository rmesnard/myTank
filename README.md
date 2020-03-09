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

sudo docker run -d --name="mytank" -p 5050:5050 -v mytank_config:/usr/share/conf lijah/mytank


#share config

..

#console

sudo docker exec -it mytank bash
