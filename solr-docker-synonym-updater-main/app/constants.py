import os

SOLR_HOST = os.getenv("SOLR_HOST", "host.docker.internal")
CONF_PATH = os.getenv("CONF_PATH", "/mycore_config/conf/")
SYNONYMS_PATH = os.getenv("SYNONYMS_PATH", "/mycore_config/conf/synonyms.txt")
#CONF_PATH = os.getenv("CONF_PATH", "./conf/")
#SYNONYMS_PATH = os.getenv("SYNONYMS_PATH", "./conf/synonyms.txt")
UPDATER_RUN_INTERVAL = .5 #seconds
