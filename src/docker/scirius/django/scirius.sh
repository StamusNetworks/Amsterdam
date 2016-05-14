#!/bin/bash

cd /opt/selks/scirius/

migrate_db() {
	python manage.py migrate
	python manage.py collectstatic  --noinput
}

create_db() {
	echo "no" | python manage.py syncdb
	#echo "no" | python manage.py syncdb --settings=scirius.local_settings
	python manage.py migrate
	python manage.py loaddata /tmp/scirius.json
	python manage.py createcachetable my_cache_table
	python manage.py addsource "ETOpen Ruleset" https://rules.emergingthreats.net/open/suricata-3.0/emerging.rules.tar.gz http sigs
	python manage.py addsource "SSLBL abuse.ch" https://sslbl.abuse.ch/blacklist/sslblacklist.rules http sig
	python manage.py defaultruleset "Default SELKS ruleset"
	python manage.py disablecategory "Default SELKS ruleset" stream-events
	python manage.py addsuricata suricata "Suricata on SELKS" /etc/suricata/rules "Default SELKS ruleset"
	python manage.py updatesuricata
	python manage.py collectstatic --noinput
}

start() {
	python manage.py collectstatic --noinput
	gunicorn -b 0.0.0.0:8000 scirius.wsgi
}

# update requirements if needed
pip install -r requirements.txt

if [ ! -e "/sciriusdata/scirius.sqlite3" ]; then
	create_db
else
	migrate_db
fi

start
