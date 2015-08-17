#!/bin/bash

cd /opt/selks/scirius/

create_db() {
	echo "no" | python manage.py syncdb
	python manage.py migrate
	python manage.py loaddata /opt/selks/scirius/scirius.json
	python manage.py createcachetable my_cache_table
	python manage.py addsource "ETOpen Ruleset" https://rules.emergingthreats.net/open/suricata-2.0.7/emerging.rules.tar.gz http sigs
	python manage.py addsource "SSLBL abuse.ch" https://sslbl.abuse.ch/blacklist/sslblacklist.rules http sig
	python manage.py defaultruleset "Default SELKS ruleset"
	python manage.py disablecategory "Default SELKS ruleset" stream-events
	python manage.py addsuricata SELKS "Suricata on SELKS" /etc/suricata/rules "Default SELKS ruleset"
	python manage.py updatesuricata
}

start() {
	python manage.py runserver 0.0.0.0:8000
}

if [ ! -e "/opt/selks/sciriusdata/db.sqlite3" ]; then
	create_db
fi

start
