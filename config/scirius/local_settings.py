import os

USE_ELASTICSEARCH = True
ELASTICSEARCH_ADDRESS = "elasticsearch:9200"
KIBANA_VERSION=4
KIBANA_INDEX = ".kibana"
KIBANA_URL = "http://localhost:5601"

USE_KIBANA = True

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
