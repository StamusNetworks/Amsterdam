import os

USE_ELASTICSEARCH = True
ELASTICSEARCH_ADDRESS = "elasticsearch:9200"
ELASTICSEARCH_2X = True
KIBANA_VERSION=4
KIBANA_INDEX = ".kibana"
KIBANA_URL = "http://kibana:5601"

SURICATA_UNIX_SOCKET = "/var/run/suricata/suricata-command.socket"

USE_KIBANA = True
KIBANA_PROXY = True

USE_EVEBOX = True
EVEBOX_ADDRESS = "evebox:5636"

USE_SURICATA_STATS = True
USE_LOGSTASH_STATS = True

DATA_DIR = "/sciriusdata/"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DATA_DIR, 'scirius.sqlite3'),
    }
}

GIT_SOURCES_BASE_DIRECTORY = os.path.join(DATA_DIR, 'git-sources/')
