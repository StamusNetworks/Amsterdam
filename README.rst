=========
Amsterdam
=========

Introduction
============

SELKS and Docker using Compose. The result of Amsterdam is a set of containers providing
a complete Suricata installation:

 - Suricata
 - Elasticsearch
 - Logstash
 - Kibana
 - Scirius

The ELK stack is created using the official docker images. Communication between
logstash and suricata is done via a share directory (from the host). The same
applies to scirius and suricata where the `/etc/suricata/rules` directory is shared.

Usage
=====

You need to install Docker compose. On Debian ::

 apt-get install docker-compose

Then got to the root directory of Amsterdam.

Select the interface Suricata will listen to by editing `docker-compose.yml`. To do
that update the `environment:` line at the beginning of the file

You may need to create the `data` directory that will contain the persistent data.

Then you can run ::
 
 ./amsterdam -d data -i wlan0 setup
 ./amsterdam -d data start

As of now the start command will take really long on first run as it will fetch from Docker hub
all the necessary images and build some custom container based on Debian.

Subsequent run should take less than 1 minute.

You can then connect to:

 - http://localhost:8000 on scirius with scirius/scirius as login/password 
 - http://localhost:5601 on kibana 4

To stop the amsterdam instance, run ::

 ./amsterdam -d data stop

Updating
========

When code is updated (new suricata package or new ELK versions), you can run ::

 ./amsterdam -d data update

Then, you can restart the services ::

 ./amsterdam -d data restart

Tuning and coding
=================

The configuration are stored in the config directory. For now only
scirius, logstash and suricata are configured that way.

Running latest git
------------------

To do so, simply edit docker-compose.yml by uncommenting and setting the path
to the scirius source tree. Then restart the services ::

 docker-compose restart

Run a migration inside the container ::

 docker exec amsterdam_scirius_1 python /opt/selks/scirius/manage.py migrate
