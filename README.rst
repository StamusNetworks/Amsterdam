=========
Amsterdam
=========

Introduction
============

Amsterdam is SELKS and Docker using Compose. The result of Amsterdam is a set of containers
providing a complete Suricata IDS/NSM ecosystem:

 - Suricata
 - Elasticsearch
 - Logstash
 - Kibana
 - Scirius
 - Evebox (https://github.com/jasonish/evebox)

The ELK stack is created using the official docker images. Communication between
logstash and suricata is done via a share directory (from the host). The same
applies to scirius and suricata where the `/etc/suricata/rules` directory is shared.

Installation
============

You can install amsterdam from the source directory by running ::

 sudo python setup.py install

Or you can use pip to install it ::

 sudo pip install amsterdam

Usage
=====

You need to install Docker compose. On Debian ::

 sudo apt-get install docker-compose

To sniff the `wlan0` interface and store data and config in the `ams` directory,
you can run ::
 
 amsterdam -d ams -i wlan0 setup
 amsterdam -d ams start

As of now the start command will take really long on first run as it will fetch from Docker hub
all the necessary images and build some custom container based on Debian.

Subsequent run should take less than 1 minute.

You can then connect to:

 - http://localhost:8000 on scirius with scirius/scirius as login/password 
 - http://localhost:5601 on kibana 4
 - http://localhost:5636/ on evebox

To stop the amsterdam instance, run ::

 amsterdam -d ams stop

To remove an amsterdam instance in directory hacklu, run ::

 amsterdam -d ~/builds/amsterdam/hacklu/ rm

and remove the data directory if you want to delete data.

Updating
========

When code is updated (new suricata package or new ELK versions), you can run ::

 amsterdam -d ams update

Then, you can restart the services ::

 amsterdam -d ams restart

Tuning and coding
=================

The configuration are stored in the config directory. For now only
scirius, logstash and suricata are configured that way.

Running Scirius from latest git
-------------------------------

To do so, simply edit docker-compose.yml in the data directory and uncomment and
set the path to the scirius source tree. You will also need to copy the local_settings.py
in config/scirius directory to in scirius subdirectory of your scirius source.

Once done, you can restart the services ::

 amsterdam -d ams restart

Run a migration inside the container ::

 docker exec ams_scirius_1 python /opt/selks/scirius/manage.py migrate
