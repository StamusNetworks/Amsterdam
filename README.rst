=========
Amsterdam
=========

Introduction
============

SELKS and docker using compose. The result of Amsterdam is a set of containers providing
a complete Suricata installation:

 - Suricata
 - Elasticsearch
 - Logstash
 - Kibana
 - Scirius

The ELK stack is created using the official docker images. Communication between
logstash and suricata is done via a share repository (from the host). The same
apply to scirius and suricata were `/etc/suricata/rules` is shared.

Usage
=====

You need to have installed Docker compose. On Debian ::

 apt-get install docker-compose

Then got to the root directory of amsterdam.

Select the interface Suricata will listen to by editing docker-compose.yml. To do
that update the `command:` line at the beginning.

You may need to create the `data` directory that will contain the persistent data.

Then you can run ::
 
 docker-compose up

As of now this will take really long.

You can then connect to:

 - http://localhost:8000 on scirius with scirius/scirius
 - http://localhost:5601 on kibana 4

Tuning and coding
=================

The configuration are stored in the config directory. For now only
scirius, logstash and suricata are configured that way.
