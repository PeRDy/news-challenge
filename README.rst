==============
News Challenge
==============

:Version: 1.0.0
:Status: final
:Author: José Antonio Perdiguero López

This project contains the implementation of the News Challenge.

To install and run:

#. Install Docker following `official docs <https://docs.docker.com/engine/installation/linux/ubuntulinux/>`_.
#. Install docker-compose::

    curl -L https://github.com/docker/compose/releases/download/1.7.1/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

#. Install docker-machine::

    curl -L https://github.com/docker/machine/releases/download/v0.7.0/docker-machine-`uname -s`-`uname -m` > /usr/local/bin/docker-machine && \
    chmod +x /usr/local/bin/docker-machine

#. Create docker-machine::

    docker-machine create --driver virtualbox default

#. Build containers::

    docker-compose build

#. Run build configuration::

    docker-compose run news build

#. Run the application::

    docker-compose run --service-ports news runserver

#. Load data::

    docker-compose run news load audience audience.json
    docker-compose run news load segments segments.json

Once the application is running, you can connect to it under URL returned from::

    env | grep DOCKER_HOST | awk 'match($0, /tcp:\/\/([0-9.]+)/, a) { printf "http://%s:8000\n", a[1] }'

