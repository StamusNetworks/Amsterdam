=========
Amsterdam
=========

Introduction
============

SELKS and docker using docker compose.

Usage
=====

You need to have installed Docker compose. On Debian ::

 apt-get install docker-compose

Then got to the root directory of amsterdam.

Select the interface Suricata will listen to by editing docker-compose.yml. To do
that update the `command:` line at the beginning.

Then you can run ::
 
 docker-compose up

As of now this will take really long.

You can then connect to:

 - http://localhost:8000 on scirius with scirius/scirius
 - http://localhost:5601 on kibana 4
